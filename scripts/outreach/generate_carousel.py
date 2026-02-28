"""
Generate carousel images using Imagen 4 (via Gemini API) with Korean text overlays.
3-5 slides per creator: hook, product showcase, lifestyle, CTA.
Output: output/carousel/{handle}/slide_N.png
"""

import os
import pathlib
import base64
from google import genai
from PIL import Image
import io

from creators import all_creators, Creator
from brand import BRAND, brand_summary, brand_visual_prompt
from text_overlay import overlay_text_on_image, create_title_card
from product_reference import get_product_description

OUTPUT_DIR = pathlib.Path(__file__).parent / "output" / "carousel"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def build_slide_prompts(creator: Creator) -> list[dict]:
    """Build image generation prompts for each carousel slide."""
    visual = BRAND["visual_identity"]
    base_style = (
        f"Premium product photography style. {visual['mood']} "
        f"Color palette: warm white, volcanic black, soft gold. "
        f"Natural lighting, high-end editorial quality. Aspect ratio 1:1."
    )

    # Get actual product description from Gemini analysis of the real bottle image
    product_desc = get_product_description("boksoondoga")

    slides = [
        {
            "name": "hook",
            "prompt": (
                f"Aesthetic flat-lay of {product_desc} on a dark volcanic stone surface, "
                f"surrounded by fresh rice grains and Jeju tangerines. "
                f"{base_style} Hero product shot with dramatic lighting."
            ),
            "text_overlay": f"@{creator.handle} × 복순도가",
            "text_position": "bottom",
        },
        {
            "name": "product",
            "prompt": (
                f"Close-up of Boksoondoga sparkling makgeolli being poured from {product_desc} "
                f"into an elegant glass, golden-white liquid with fine bubbles, condensation on the glass. "
                f"Background: blurred Jeju landscape (volcanic rock, green fields). "
                f"{base_style} Focus on the pour and bubbles."
            ),
            "text_overlay": "제주 프리미엄 쌀 막걸리\nJeju Premium Rice Wine",
            "text_position": "bottom",
        },
        {
            "name": "lifestyle",
            "prompt": (
                f"A stylish Korean woman in her late 20s enjoying Boksoondoga makgeolli "
                f"at a modern rooftop bar in Seoul during golden hour. "
                f"She's holding {product_desc}, laughing naturally with friends. "
                f"{'Fashion editorial mood, high-end lifestyle.' if 'fashion' in creator.categories else 'Warm, authentic, candid moment.'} "
                f"{base_style}"
            ),
            "text_overlay": None,
        },
        {
            "name": "heritage",
            "prompt": (
                f"Traditional Korean brewing process — hands carefully mixing rice and nuruk (yeast) "
                f"in a ceramic onggi pot. Warm, intimate lighting. Steam rising. "
                f"Showing the craft behind Boksoondoga. {base_style} "
                f"Documentary-style, authentic, not staged."
            ),
            "text_overlay": "전통의 맛, 현대의 감각\nTraditional Taste, Modern Sensibility",
            "text_position": "bottom",
        },
        {
            "name": "cta",
            "prompt": (
                f"{product_desc} displayed alongside the sparkling variant, "
                f"side by side on a marble surface with soft natural light. "
                f"Minimal composition, lots of negative space for text. "
                f"{base_style} Clean and inviting."
            ),
            "text_overlay": f"어떤 복순도가를 선택하시겠어요?\nWhich Boksoondoga is yours?",
            "text_position": "center",
        },
    ]
    return slides


def generate_image(prompt: str, output_path: pathlib.Path) -> pathlib.Path | None:
    """Generate an image using Imagen via Gemini API."""
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
            ),
        )

        if response.generated_images:
            img_bytes = response.generated_images[0].image.image_bytes
            img = Image.open(io.BytesIO(img_bytes))
            img.save(output_path)
            return output_path
    except Exception as e:
        print(f"\n    Image generation error: {e}")
        # Fallback: create a placeholder
        img = Image.new("RGB", (1080, 1080), "#1A1A1A")
        img.save(output_path)
        return output_path
    return None


def generate_carousel(creator: Creator):
    """Generate all carousel slides for a creator."""
    creator_dir = OUTPUT_DIR / creator.handle
    creator_dir.mkdir(parents=True, exist_ok=True)

    slides = build_slide_prompts(creator)
    generated = []

    for i, slide in enumerate(slides, 1):
        print(f"    Slide {i}/{len(slides)} ({slide['name']})...", end=" ", flush=True)

        raw_path = creator_dir / f"slide_{i}_{slide['name']}_raw.png"
        final_path = creator_dir / f"slide_{i}_{slide['name']}.png"

        # Generate base image
        result = generate_image(slide["prompt"], raw_path)
        if not result:
            print("FAILED")
            continue

        # Add text overlay if specified
        if slide.get("text_overlay"):
            pos_map = {
                "bottom": (60, 900),
                "center": (60, 460),
                "top": (60, 60),
            }
            pos = pos_map.get(slide.get("text_position", "bottom"), (60, 900))
            overlay_text_on_image(
                raw_path,
                slide["text_overlay"],
                position=pos,
                font_size=42,
                max_width=960,
                output_path=final_path,
            )
            print(f"✓ (with text)")
        else:
            raw_path.rename(final_path)
            print("✓")

        generated.append(final_path)

    return generated


def main():
    print("Generating carousel images...\n")
    for creator in all_creators():
        print(f"  @{creator.handle} ({creator.name_kr}):")
        slides = generate_carousel(creator)
        print(f"    → {len(slides)} slides generated\n")

    print(f"Done! Carousels saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
