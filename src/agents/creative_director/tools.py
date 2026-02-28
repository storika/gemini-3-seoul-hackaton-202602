"""Creative Director tools — actual media generation via Veo 3.1 & Imagen 4."""

from __future__ import annotations

import asyncio
import os
import time
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types
from google.adk.tools import FunctionTool

from src.config import GOOGLE_API_KEY, VEO_MODEL, IMAGEN_MODEL, PROJECT_ROOT
from src.media.imagen_client import build_product_image_prompt, build_lifestyle_image_prompt
from src.media.veo_client import build_product_video_prompt, build_brand_story_prompt

OUTPUT_DIR = PROJECT_ROOT / "demo"


def _get_client() -> genai.Client:
    api_key = GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY", "")
    return genai.Client(api_key=api_key)


async def generate_image(
    brand_name: str,
    product_name: str,
    style: str = "editorial product photography",
    context: str = "",
    aspect_ratio: str = "1:1",
) -> dict:
    """Generate a product image using Imagen 4 and save to demo/generated_images/.

    Args:
        brand_name: The brand name (TIRTIR, ANUA, COSRX).
        product_name: The product to feature.
        style: Photography style (editorial, lifestyle, flat lay, etc.).
        context: Additional visual context for the image.
        aspect_ratio: Image aspect ratio (1:1, 9:16, 16:9, 3:4, 4:3).

    Returns:
        Dict with generation status, prompt used, and saved file path.
    """
    prompt = build_product_image_prompt(brand_name, product_name, style, context)
    client = _get_client()

    try:
        response = await client.aio.models.generate_images(
            model=IMAGEN_MODEL,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
            ),
        )

        if response.generated_images:
            out_dir = OUTPUT_DIR / "generated_images"
            out_dir.mkdir(parents=True, exist_ok=True)

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = product_name.replace(" ", "_")[:30]
            filename = f"{brand_name.lower()}_{safe_name}_{ts}.png"
            out_path = out_dir / filename

            image_bytes = response.generated_images[0].image.image_bytes
            out_path.write_bytes(image_bytes)

            return {
                "status": "success",
                "prompt": prompt,
                "model": IMAGEN_MODEL,
                "file_path": str(out_path),
                "file_size_kb": round(len(image_bytes) / 1024, 1),
            }
        else:
            return {"status": "error", "prompt": prompt, "error": "No images generated"}

    except Exception as e:
        return {"status": "error", "prompt": prompt, "error": str(e)}


async def generate_video(
    brand_name: str,
    product_name: str,
    style: str = "smooth cinematic reveal",
    hero_ingredient: str = "",
    aspect_ratio: str = "9:16",
    duration_seconds: int = 8,
) -> dict:
    """Generate a product video using Veo 3.1 and save to demo/generated_videos/.

    This calls the real Veo 3.1 API. Video generation takes 2-5 minutes.

    Args:
        brand_name: The brand name (TIRTIR, ANUA, COSRX).
        product_name: The product to feature.
        style: Video style (cinematic reveal, ASMR application, brand story, etc.).
        hero_ingredient: Optional hero ingredient to highlight visually.
        aspect_ratio: Video aspect ratio (9:16 vertical or 16:9 horizontal).
        duration_seconds: Video duration (5 or 8 seconds).

    Returns:
        Dict with generation status, prompt used, and saved file path.
    """
    prompt = build_product_video_prompt(brand_name, product_name, style, hero_ingredient)
    client = _get_client()

    try:
        operation = await client.aio.models.generate_videos(
            model=VEO_MODEL,
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                duration_seconds=duration_seconds,
            ),
        )

        # Poll for completion (Veo takes 2-5 min)
        poll_count = 0
        while not operation.done:
            await asyncio.sleep(10)
            operation = await client.aio.operations.get(operation)
            poll_count += 1
            if poll_count > 60:  # 10min timeout
                return {"status": "timeout", "prompt": prompt, "error": "Generation timed out after 10 minutes"}

        if not operation.response or not operation.response.generated_videos:
            return {"status": "error", "prompt": prompt, "error": "No videos generated"}

        video = operation.response.generated_videos[0]
        video_bytes = video.video.video_bytes

        out_dir = OUTPUT_DIR / "generated_videos"
        out_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = product_name.replace(" ", "_")[:30]
        filename = f"{brand_name.lower()}_{safe_name}_{ts}.mp4"
        out_path = out_dir / filename

        out_path.write_bytes(video_bytes)

        return {
            "status": "success",
            "prompt": prompt,
            "model": VEO_MODEL,
            "file_path": str(out_path),
            "file_size_mb": round(len(video_bytes) / (1024 * 1024), 2),
            "duration_seconds": duration_seconds,
            "aspect_ratio": aspect_ratio,
        }

    except Exception as e:
        return {"status": "error", "prompt": prompt, "error": str(e)}


def build_creative_brief(
    brand_name: str,
    campaign_goal: str,
    target_platform: str = "TikTok",
    content_type: str = "product_launch",
) -> dict:
    """Build a creative brief for a K-beauty brand campaign.

    Args:
        brand_name: The brand name (TIRTIR, ANUA, COSRX).
        campaign_goal: What the campaign should achieve.
        target_platform: Primary distribution platform.
        content_type: Type of content (product_launch, seasonal, brand_story, trend_response).

    Returns:
        Dict with the creative brief template.
    """
    platform_specs = {
        "TikTok": {"format": "9:16 vertical", "duration": "8s video or carousel", "style": "authentic, trend-aware"},
        "Instagram": {"format": "1:1 or 9:16", "duration": "15-30s reels", "style": "polished, aesthetic"},
        "YouTube": {"format": "16:9", "duration": "15-60s", "style": "editorial, storytelling"},
    }

    specs = platform_specs.get(target_platform, platform_specs["TikTok"])

    brand_guidelines = {
        "TIRTIR": {
            "visual_tone": "Bold, radiant, inclusive",
            "colors": "Red accents, warm tones",
            "must_include": "Shade diversity, cushion compact",
        },
        "ANUA": {
            "visual_tone": "Gentle, minimal, natural",
            "colors": "Soft greens, earth tones",
            "must_include": "Heartleaf motif, ingredient transparency",
        },
        "COSRX": {
            "visual_tone": "Clinical, honest, transformative",
            "colors": "White, clean, medical-inspired",
            "must_include": "Before/after results, ingredient callouts",
        },
    }

    guidelines = brand_guidelines.get(brand_name.upper(), {})

    return {
        "brand": brand_name,
        "campaign_goal": campaign_goal,
        "platform": target_platform,
        "content_type": content_type,
        "platform_specs": specs,
        "brand_guidelines": guidelines,
        "deliverables": [
            f"1x Hero image ({specs['format']})",
            f"1x Product video ({specs['duration']})",
            "3x Supporting images for carousel",
        ],
    }


generate_image_tool = FunctionTool(generate_image)
generate_video_tool = FunctionTool(generate_video)
build_creative_brief_tool = FunctionTool(build_creative_brief)
