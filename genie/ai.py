from __future__ import annotations

import json

from openai import APIError, OpenAI

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
    # prepare prompt
    os_target = "Linux" if linux else "macOS"
    user_message = f"OS: {os_target}\nTask: {prompt}"

    client = OpenAI(api_key=config.api_key, base_url=config.base_url)

    try:
        response = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
    except APIError as e:
        msg = str(e)
        if "429" in msg:
            raise RuntimeError(
                "Rate limit reached. Please wait a moment and try again."
            ) from e
        if "401" in msg or "403" in msg:
            raise RuntimeError("Invalid API key. Please check your API_KEY.") from e
        if "404" in msg:
            raise RuntimeError(
                f"Model not found. Check your AI_MODEL setting (currently: {config.model})."
            ) from e
        raise RuntimeError(f"API error: {e}") from e

    return json.loads(response.choices[0].message.content)
