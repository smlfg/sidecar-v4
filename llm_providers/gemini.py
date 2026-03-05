"""Gemini Flash provider — direct HTTP call, no SDK dependency."""

import json
import urllib.request

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.0-flash:generateContent"
)


def call_gemini(
    system_prompt: str,
    user_prompt: str,
    api_key: str,
    timeout: float = 1.5,
) -> str | None:
    """Call Gemini Flash with strict timeout. Returns text or None."""
    body = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 150,
            "temperature": 0.3,
        },
    }
    url = f"{GEMINI_ENDPOINT}?key={api_key}"
    req = urllib.request.Request(
        url,
        json.dumps(body).encode(),
        {"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read())
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return None
