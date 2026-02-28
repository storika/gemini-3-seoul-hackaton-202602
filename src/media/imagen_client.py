"""Imagen 4 image generation wrapper."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional

from google import genai
from google.genai import types

from src.config import GOOGLE_API_KEY, IMAGEN_MODEL


async def generate_image(
    prompt: str,
    output_path: str | Path | None = None,
    aspect_ratio: str = "1:1",
    number_of_images: int = 1,
) -> list[bytes]:
    """Generate images with Imagen 4.

    Args:
        prompt: Image generation prompt.
        output_path: Optional directory to save images.
        aspect_ratio: "1:1", "9:16", "16:9", "3:4", "4:3".
        number_of_images: How many images to generate (1-4).

    Returns:
        List of image bytes (PNG).
    """
    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = await client.aio.models.generate_images(
        model=IMAGEN_MODEL,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=number_of_images,
            aspect_ratio=aspect_ratio,
        ),
    )

    images: list[bytes] = []
    if response.generated_images:
        for i, img in enumerate(response.generated_images):
            image_bytes = img.image.image_bytes
            images.append(image_bytes)

            if output_path:
                out_dir = Path(output_path)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / f"imagen_{i}.png"
                out_file.write_bytes(image_bytes)

    return images


def build_product_image_prompt(
    brand_name: str,
    product_name: str,
    style: str = "editorial product photography",
    context: str = "",
) -> str:
    """Build an optimized Imagen prompt for Korean soju product imagery."""
    base = (
        f"{style} of {brand_name} {product_name}, "
        "Korean soju aesthetic, clean minimalist background, "
        "soft diffused lighting, high-end beverage photography"
    )
    if context:
        base += f", {context}"
    return base


def build_lifestyle_image_prompt(
    brand_name: str,
    concept: str,
    demographic: str = "young Korean woman",
) -> str:
    """Build a lifestyle/campaign image prompt."""
    return (
        f"Lifestyle campaign photo for {brand_name}: {concept}. "
        f"Model: {demographic}. "
        "Natural lighting, Korean soju culture aesthetic, "
        "social gathering ambiance, editorial quality"
    )
