#!/usr/bin/env python3
"""Batch-generate Imagen 4 portrait images for all soju models.

Generates a portrait image for each model in MODEL_GALLERY.

Usage:
    python scripts/generate_model_images.py [--dry-run] [--model MODEL_ID]
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.timeline.model_gallery import MODEL_GALLERY
from src.media.imagen_client import generate_image

OUTPUT_DIR = Path(__file__).parent.parent / "generated_images" / "models"


async def generate_for_model(model_id: str, prompt: str, dry_run: bool) -> bool:
    out_file = OUTPUT_DIR / f"{model_id}.png"

    if out_file.exists():
        print(f"  [SKIP] {model_id} — already exists")
        return True

    print(f"  [GEN]  {model_id}")
    print(f"         {prompt[:80]}...")

    if dry_run:
        print(f"         (dry run)")
        return True

    try:
        images = await generate_image(
            prompt=prompt,
            output_path=None,
            aspect_ratio="1:1",  # Square portrait for thumbnails
            number_of_images=1,
        )
        if images:
            out_file.write_bytes(images[0])
            print(f"         Saved ({len(images[0])} bytes)")
            return True
        else:
            print(f"         [FAIL] No image returned")
            return False
    except Exception as e:
        print(f"         [ERROR] {e}")
        return False


async def main():
    parser = argparse.ArgumentParser(description="Generate model portrait images")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", type=str, help="Generate for specific model ID only")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    models = MODEL_GALLERY
    if args.model:
        models = [m for m in models if m.id == args.model]
        if not models:
            print(f"Model '{args.model}' not found.")
            sys.exit(1)

    print(f"Soju Model Gallery Image Generator (Imagen 4)")
    print(f"{'=' * 50}")
    print(f"Models: {len(models)}  |  Output: {OUTPUT_DIR}")
    if args.dry_run:
        print(f"Mode: DRY RUN")
    print()

    success = 0
    failed = 0

    for model in models:
        print(f"--- {model.id}: {model.name_ko} ({model.brand}, {model.start_year}-{model.end_year}) ---")
        ok = await generate_for_model(model.id, model.image_prompt, args.dry_run)
        success += ok
        failed += (not ok)
        print()

    print(f"Done: {success} success, {failed} failed")


if __name__ == "__main__":
    asyncio.run(main())
