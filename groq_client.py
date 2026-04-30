"""
Groq API client wrapper.
Exposes temperature and top_p as configurable params (required for INT428 evaluation).
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Add it to your .env file.")
    return Groq(api_key=api_key)


def chat(
    messages: list[dict],
    system_prompt: str,
    temperature: float = 0.4,
    top_p: float = 0.9,
    max_tokens: int = 1024,
) -> str:
    """
    Send a conversation to Groq and return the assistant's reply.

    Args:
        messages: List of {"role": "user"/"assistant", "content": "..."} dicts
        system_prompt: Domain-specific system instruction
        temperature: 0.0 = deterministic, 1.0 = creative. Default 0.4 for factual eco advice.
        top_p: Nucleus sampling. Default 0.9 for balanced responses.
        max_tokens: Max response length.

    Returns:
        Assistant reply string
    """
    client = get_client()

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model=MODEL,
        messages=full_messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content
