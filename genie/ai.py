from __future__ import annotations

import json

from google import genai
from google.genai import errors, types

from genie.config import Config

SYSTEM_PROMPT = """You are a shell command expert. Given a plain English description, return a shell command for the specified OS.

Always respond with valid JSON in exactly this format:
{
  "command": "<the full command>",
  "breakdown": [
    {"part": "<part of the command>", "explanation": "<what it does>"},
    ...
  ]
}

Rules:
- Return only the JSON, no extra text or markdown
- Split the command into meaningful parts for the breakdown
- Keep explanations short and clear
"""


def get_command(prompt: str, config: Config, linux: bool = False) -> dict:
    os_target = "Linux" if linux else "macOS"
    user_message = f"OS: {os_target}\nTask: {prompt}"
    return _call_gemini(user_message, config)


def _call_gemini(user_message: str, config: Config) -> dict:
    client = genai.Client(api_key=config.api_key)

    try:
        response = client.models.generate_content(
            model=config.model,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0,
            ),
        )
    except errors.ClientError as e:
        msg = str(e)
        if "429" in msg:
            raise RuntimeError(
                "Rate limit reached. Please wait a moment and try again."
            ) from e
        if "401" in msg or "403" in msg:
            raise RuntimeError(
                "Invalid API key. Please check your GEMINI_API_KEY."
            ) from e
        if "404" in msg:
            raise RuntimeError(
                f"Model not found. Check your GENIE_MODEL setting (currently: {config.model})."
            ) from e
        raise RuntimeError(f"Gemini API error: {e}") from e

    return json.loads(response.text)
