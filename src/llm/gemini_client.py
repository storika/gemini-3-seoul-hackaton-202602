"""Gemini 3 client wrapper using google-genai SDK."""

from __future__ import annotations

import os
from typing import Any

from google import genai
from google.genai import types

from src.config import GOOGLE_API_KEY, GEMINI_MODEL


_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY", "")
        _client = genai.Client(api_key=api_key)
    return _client


async def generate_text(
    prompt: str,
    system_instruction: str = "",
    model: str = GEMINI_MODEL,
    temperature: float = 0.7,
    max_output_tokens: int = 1024,
) -> str:
    """Generate text with Gemini 3."""
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    if system_instruction:
        config.system_instruction = system_instruction

    response = await client.aio.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text or ""


async def extract_keywords(content: str) -> list[str]:
    """Use Gemini to extract keywords from content."""
    prompt = (
        "Extract 5-10 keywords from the following text. "
        "Return only a comma-separated list of keywords, nothing else.\n\n"
        f"Text: {content}"
    )
    result = await generate_text(prompt, temperature=0.2, max_output_tokens=200)
    return [kw.strip() for kw in result.split(",") if kw.strip()]


async def generate_context(content: str, existing_keywords: list[str] | None = None) -> str:
    """Generate a contextual summary for a memory note."""
    kw_hint = f"\nExisting keywords: {', '.join(existing_keywords)}" if existing_keywords else ""
    prompt = (
        "Generate a brief contextual summary (1-2 sentences) for the following Korean liquor brand information. "
        "Focus on why this information matters for brand strategy and marketing.\n\n"
        f"Content: {content}{kw_hint}"
    )
    return await generate_text(prompt, temperature=0.3, max_output_tokens=200)


async def find_connections(
    note_content: str,
    candidate_notes: list[dict[str, str]],
) -> list[str]:
    """Use Gemini to identify semantically related notes.

    Returns IDs of notes that should be connected.
    """
    if not candidate_notes:
        return []

    candidates_text = "\n".join(
        f"- ID={n['id']}: {n['content'][:100]}" for n in candidate_notes[:20]
    )
    prompt = (
        "Given the following new Korean liquor note and a list of existing notes, "
        "identify which existing notes are strongly related. "
        "Return only the IDs of related notes as a comma-separated list. "
        "If none are related, return 'NONE'.\n\n"
        f"New note: {note_content}\n\n"
        f"Existing notes:\n{candidates_text}"
    )
    result = await generate_text(prompt, temperature=0.1, max_output_tokens=200)
    if "NONE" in result.upper():
        return []
    return [id_.strip() for id_ in result.split(",") if id_.strip()]


async def summarize_memories(brand_namespace: str, category: str, note_texts: list[str]) -> str:
    """Consolidate multiple notes into a single high-quality summary."""
    notes_blob = "\n".join([f"- {text}" for text in note_texts])
    prompt = (
        f"The following are multiple memory notes regarding the Korean liquor brand '{brand_namespace}' "
        f"in the category '{category}'. Consolidate these into a single, comprehensive, and "
        "strategically useful summary that retains all critical facts (ingredients, claims, "
        "achievements) while removing redundancy. Keep the tone professional and brand-aligned.\n\n"
        f"Notes:\n{notes_blob}"
    )
    return await generate_text(prompt, temperature=0.3, max_output_tokens=500)
