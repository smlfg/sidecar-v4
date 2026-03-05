"""Ollama provider — local LLM call. For async/background evaluations only."""

import json
import urllib.request

OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"


def call_ollama(
    system_prompt: str,
    user_prompt: str,
    model: str = "phi4",
    timeout: float = 10.0,
) -> str | None:
    """Call local Ollama model. Too slow for sync path (~5-15s)."""
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {"num_predict": 150, "temperature": 0.3},
    }
    req = urllib.request.Request(
        OLLAMA_ENDPOINT,
        json.dumps(body).encode(),
        {"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read())
        return data["message"]["content"].strip()
    except Exception:
        return None
