"""MiniMax M2.5 provider — direct HTTP call, no SDK dependency.

Default LLM for Sidecar Judge. Fast enough for sync path (<2s).
"""

import json
import urllib.request

MINIMAX_ENDPOINT = "https://api.minimaxi.chat/v1/text/chatcompletion_v2"
MINIMAX_MODEL = "MiniMax-M2.5"


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
