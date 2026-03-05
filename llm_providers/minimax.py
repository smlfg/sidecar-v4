"""MiniMax M2.5 provider — direct HTTP call, no SDK dependency.

Default LLM for Sidecar Judge. Fast enough for sync path (<2s).
"""

import json
import time
import urllib.request

MINIMAX_ENDPOINT = "https://api.minimaxi.chat/v1/text/chatcompletion_v2"
MINIMAX_MODEL = "MiniMax-M2.5"

KNOWLEDGE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a markdown file from Samuel's knowledge base. Use to get detailed information about a specific topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Filename in the knowledge/ directory (e.g. 'chatgpt_PORTRAIT_SAMUEL.md')"},
                    "section": {"type": "string", "description": "Optional: extract only the section starting with this ## heading"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the knowledge index for files relevant to a query. Returns matching topics with file lists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query (German or English keywords)"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_topics",
            "description": "List all available knowledge topics with descriptions. Use for orientation.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


def call_minimax(
    system_prompt: str,
    user_prompt: str,
    api_key: str,
    timeout: float = 8.0,
) -> str | None:
    """Call MiniMax M2.5 (reasoning model). Returns text or None.

    M2.5 uses reasoning_content + content. We need enough tokens
    for both the chain-of-thought and the final answer.
    """
    body = {
        "model": MINIMAX_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
    }
    req = urllib.request.Request(
        MINIMAX_ENDPOINT,
        json.dumps(body).encode(),
        {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read())
        msg = data["choices"][0]["message"]
        # M2.5 reasoning model: answer is in content, reasoning in reasoning_content
        content = (msg.get("content") or "").strip()
        if content:
            return content
        # Fallback: if content is empty, extract from reasoning_content
        reasoning = (msg.get("reasoning_content") or "").strip()
        if reasoning:
            # Take the last paragraph as the actual answer
            paragraphs = [p.strip() for p in reasoning.split("\n\n") if p.strip()]
            return paragraphs[-1] if paragraphs else None
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Agent loop (function calling)
# ---------------------------------------------------------------------------

def _log_agent(msg: str) -> None:
    """Append a log line with [minimax-agent] prefix to the sidecar log."""
    line = f"[minimax-agent] {msg}\n"
    try:
        with open("/tmp/claude-sidecar.log", "a") as fh:
            fh.write(line)
    except Exception:
        pass  # Never crash the caller over logging


def call_minimax_agent(
    system_prompt: str,
    user_prompt: str,
    api_key: str,
    tools: list[dict],
    tool_handler: callable,
    max_rounds: int = 3,
    timeout: float = 15.0,
) -> str | None:
    """Call MiniMax M2.5 with function calling (agent loop).

    Keeps calling the API until the model responds with text (no tool_calls)
    or max_rounds is exhausted. Each tool call is dispatched to tool_handler.

    Args:
        system_prompt: System prompt for the agent.
        user_prompt: Initial user message.
        api_key: MiniMax API key.
        tools: Tool definitions in MiniMax/OpenAI function calling format.
        tool_handler: Callback (tool_name, arguments) -> str. Exceptions are
            caught and returned as error strings so the loop keeps running.
        max_rounds: Maximum agent loop iterations (budget protection).
        timeout: Total wall-clock budget for ALL rounds combined.

    Returns:
        Final text response from the model, or None if no text was produced.
    """
    start = time.monotonic()

    messages: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    last_text: str | None = None

    for round_num in range(1, max_rounds + 1):
        elapsed = time.monotonic() - start
        if elapsed >= timeout:
            _log_agent(f"timeout before round {round_num} (elapsed={elapsed:.1f}s)")
            break

        per_round_timeout = max(2.0, timeout - elapsed)

        body = {
            "model": MINIMAX_MODEL,
            "messages": messages,
            "tools": tools,
            "max_tokens": 1024,
            "temperature": 0.3,
        }
        req = urllib.request.Request(
            MINIMAX_ENDPOINT,
            json.dumps(body).encode(),
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )

        try:
            resp = urllib.request.urlopen(req, timeout=per_round_timeout)
            data = json.loads(resp.read())
        except Exception as exc:
            _log_agent(f"round {round_num} HTTP error: {exc}")
            break

        choice = data["choices"][0]
        finish_reason = choice.get("finish_reason", "")
        msg = choice["message"]

        # Accumulate the assistant turn in the message history
        messages.append(msg)

        # Check for tool calls
        tool_calls = msg.get("tool_calls") or []
        tool_names = [tc["function"]["name"] for tc in tool_calls]
        elapsed_now = time.monotonic() - start
        _log_agent(
            f"round {round_num} finish_reason={finish_reason!r} "
            f"tool_calls={tool_names} elapsed={elapsed_now:.1f}s"
        )

        if finish_reason != "tool_calls" or not tool_calls:
            # Model is done — extract the text answer
            content = (msg.get("content") or "").strip()
            if content:
                last_text = content
            else:
                # Reasoning-model fallback: last paragraph of reasoning_content
                reasoning = (msg.get("reasoning_content") or "").strip()
                if reasoning:
                    paragraphs = [p.strip() for p in reasoning.split("\n\n") if p.strip()]
                    last_text = paragraphs[-1] if paragraphs else None
            break

        # Dispatch each tool call and collect results
        for tc in tool_calls:
            call_id = tc.get("id", "")
            fn_name = tc["function"]["name"]
            raw_args = tc["function"].get("arguments", "{}")

            try:
                arguments = json.loads(raw_args)
            except json.JSONDecodeError:
                arguments = {}

            try:
                result = tool_handler(fn_name, arguments)
            except Exception as exc:
                result = f"[tool error] {exc}"

            messages.append(
                {
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": call_id,
                }
            )

    total_elapsed = time.monotonic() - start
    _log_agent(f"agent loop done rounds_used={round_num} total_elapsed={total_elapsed:.1f}s result={'ok' if last_text else 'None'}")
    return last_text
