"""Veo 3.1 video generation wrapper."""

from __future__ import annotations

import asyncio
import time
from pathlib import Path

from google import genai
from google.genai import types

from src.config import GOOGLE_API_KEY, VEO_MODEL


def _generate_video_sync(
    prompt: str,
    output_path: str | Path | None,
    aspect_ratio: str,
    duration_seconds: int,
) -> bytes | None:
    """Synchronous Veo generation (runs in thread to avoid async httpx bug)."""
    client = genai.Client(api_key=GOOGLE_API_KEY)

    operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=prompt,
        config=types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            duration_seconds=duration_seconds,
        ),
    )

    # Poll for completion
    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation)

    if not operation.response or not operation.response.generated_videos:
        return None

    video = operation.response.generated_videos[0]
    video_bytes = video.video.video_bytes

    if output_path and video_bytes:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(video_bytes)

    return video_bytes


async def generate_video(
    prompt: str,
    output_path: str | Path | None = None,
    aspect_ratio: str = "9:16",
    duration_seconds: int = 8,
) -> bytes | None:
    """Generate a video with Veo 3.1.

    Uses sync client in a thread to work around google-genai async httpx bug.

    Args:
        prompt: Video generation prompt.
        output_path: Optional path to save the video file.
        aspect_ratio: "9:16" (vertical), "16:9" (horizontal).
        duration_seconds: 5 or 8 seconds.

    Returns:
        Video bytes (MP4) or None if generation fails.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, _generate_video_sync, prompt, output_path, aspect_ratio, duration_seconds
    )


def build_product_video_prompt(
    brand_name: str,
    product_name: str,
    style: str = "smooth cinematic reveal",
    hero_ingredient: str = "",
) -> str:
    """Build a Veo prompt for Korean soju product video."""
    prompt = (
        f"{style} of {brand_name} {product_name}. "
        "Elegant Korean soju commercial style. "
        "Close-up product shots with soft lighting transitions. "
        "Clean, minimal aesthetic."
    )
    if hero_ingredient:
        prompt += f" Feature {hero_ingredient} ingredient elements."
    return prompt


def build_brand_story_prompt(
    brand_name: str,
    narrative: str,
    mood: str = "warm and aspirational",
) -> str:
    """Build a Veo prompt for brand storytelling video."""
    return (
        f"Brand story video for {brand_name}: {narrative}. "
        f"Mood: {mood}. "
        "Cinematic Korean soju style, natural lighting, "
        "product close-ups, 9:16 vertical format for social media."
    )
