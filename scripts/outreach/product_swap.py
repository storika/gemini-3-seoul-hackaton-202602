"""
Product swap demo: same creator aesthetic, different products.
Generates Boksoondoga content → swaps product noun → regenerates.
Demonstrates prompt engineering for consistent scene/mood with different products.
Output: output/swap/
"""

import os
import pathlib
import io
from google import genai
from PIL import Image

from creators import all_creators, Creator
from brand import BRAND, brand_visual_prompt
from text_overlay import overlay_text_on_image
from product_reference import get_product_description

OUTPUT_DIR = pathlib.Path(__file__).parent / "output" / "swap"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Base scene template — {product} gets swapped
SCENE_TEMPLATE = (
    "Premium product photography: {product_description} on a dark volcanic stone surface "
    "with soft natural backlighting. The bottle/glass is centered, with subtle moisture droplets. "
    "A few {garnish} placed artfully nearby. "
    "Clean minimalist composition, lots of negative space. "
    "Warm white and soft gold color palette. Jeju-inspired natural backdrop. "
    "1:1 aspect ratio, editorial quality, shot on medium format camera."
)

def _build_products() -> list[dict]:
    """Build product list with Gemini-analyzed descriptions from actual bottle images."""
    return [
        {
            "name": "복순도가 손막걸리",
            "name_en": "Boksoondoga Makgeolli",
            "description": get_product_description("boksoondoga"),
            "garnish": "rice grains and a small ceramic cup",
            "label_color": "#F5F0E8",
        },
        {
            "name": "프리미엄 위스키",
            "name_en": "Premium Whiskey",
            "description": get_product_description("johnnie_walker"),
            "garnish": "orange peel and cinnamon sticks",
            "label_color": "#C4A86B",
        },
        {
            "name": "프리미엄 소주",
            "name_en": "Premium Soju",
            "description": get_product_description("soju"),
            "garnish": "fresh green chili and cucumber slices",
            "label_color": "#90B77D",
        },
    ]


def generate_image(prompt: str, output_path: pathlib.Path) -> pathlib.Path | None:
    """Generate an image using Imagen."""
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
        img = Image.new("RGB", (1080, 1080), "#1A1A1A")
        img.save(output_path)
        return output_path
    return None


def generate_swap_set():
    """Generate the same scene with 3 different products."""
    print("Generating product swap comparison...\n")
    print("  [Gemini 3] Analyzing actual bottle images for accurate prompts...")
    products = _build_products()

    for product in products:
        prompt = SCENE_TEMPLATE.format(
            product_description=product["description"],
            garnish=product["garnish"],
        )

        safe_name = product["name_en"].lower().replace(" ", "_")
        raw_path = OUTPUT_DIR / f"{safe_name}_raw.png"
        final_path = OUTPUT_DIR / f"{safe_name}.png"

        print(f"  {product['name']} ({product['name_en']})...", end=" ", flush=True)
        result = generate_image(prompt, raw_path)

        if result:
            overlay_text_on_image(
                raw_path,
                product["name"],
                position=(60, 940),
                font_size=48,
                color=product["label_color"],
                output_path=final_path,
            )
            print("✓")
        else:
            print("FAILED")

    # Also save the prompt template for demo explanation
    template_path = OUTPUT_DIR / "prompt_template.txt"
    template_path.write_text(
        "=== PRODUCT SWAP PROMPT TEMPLATE ===\n\n"
        f"{SCENE_TEMPLATE}\n\n"
        "=== PRODUCTS (Gemini-analyzed from actual bottle images) ===\n" +
        "\n".join(f"  {p['name']}: {p['description']}" for p in products) +
        "\n\n=== KEY INSIGHT ===\n"
        "Same scene structure, same lighting, same composition.\n"
        "Only the product description and garnish change.\n"
        "This demonstrates prompt engineering for consistent brand aesthetics\n"
        "while swapping the featured product — a key capability for\n"
        "scaling influencer content across multiple brand partnerships.\n",
        encoding="utf-8",
    )

    print(f"\nDone! Swap images saved to {OUTPUT_DIR}/")


def main():
    generate_swap_set()


if __name__ == "__main__":
    main()
