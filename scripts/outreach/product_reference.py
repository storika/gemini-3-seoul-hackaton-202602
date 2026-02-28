"""
Product image reference analysis using Gemini 3 Flash.

Analyzes actual product bottle images to generate detailed visual descriptions
that can be injected into Imagen 4 and Veo 3.1 prompts for accurate product depiction.
"""

import os
import pathlib
import json
from google import genai
from google.genai import types

BASE_DIR = pathlib.Path(__file__).parent
PRODUCTS_DIR = BASE_DIR / "assets" / "products"
CACHE_PATH = PRODUCTS_DIR / "_analysis_cache.json"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
GEMINI_MODEL = "gemini-3-flash-preview"

PRODUCT_ANALYSIS_PROMPT = """\
You are a product photography expert. Analyze this bottle/product image in detail.
Provide a JSON response with these fields:
{
  "bottle_shape": "Exact shape, proportions, and silhouette of the bottle",
  "color": "Exact colors of the bottle, liquid, and label",
  "label_design": "Detailed description of the label — text, logo, typography, layout",
  "material": "Bottle material (glass, ceramic, etc.) and finish (matte, glossy, frosted)",
  "distinctive_features": "Any unique visual elements that make this product recognizable",
  "prompt_description": "A single detailed sentence describing this exact product for use in AI image generation prompts — include bottle shape, color, label details, and material"
}

Return ONLY valid JSON, no markdown fences."""

# In-memory cache for the session
_cache: dict[str, dict] = {}


def _load_cache() -> dict[str, dict]:
    """Load cached analysis from disk."""
    global _cache
    if _cache:
        return _cache
    if CACHE_PATH.exists():
        try:
            _cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            _cache = {}
    return _cache


def _save_cache():
    """Persist cache to disk."""
    CACHE_PATH.write_text(
        json.dumps(_cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def analyze_product_image(image_path: pathlib.Path) -> dict:
    """Use Gemini 3 Flash to analyze a product bottle image and return structured description."""
    cache = _load_cache()
    cache_key = image_path.name

    if cache_key in cache:
        return cache[cache_key]

    img_bytes = image_path.read_bytes()
    mime = "image/jpeg" if image_path.suffix in (".jpg", ".jpeg") else "image/png"

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Part(inline_data=types.Blob(mime_type=mime, data=img_bytes)),
            PRODUCT_ANALYSIS_PROMPT,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )

    try:
        result = json.loads(response.text)
    except (json.JSONDecodeError, AttributeError):
        text = response.text or ""
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(text[start:end])
        else:
            result = {"prompt_description": "a premium Korean alcohol bottle"}

    # Cache the result
    _cache[cache_key] = result
    _save_cache()
    return result


def get_product_description(product_key: str) -> str:
    """Get the prompt-ready description for a product.

    Args:
        product_key: One of 'boksoondoga', 'soju', 'johnnie_walker'

    Returns:
        Detailed product description string for use in image/video generation prompts.
    """
    file_map = {
        "boksoondoga": PRODUCTS_DIR / "boksoondoga.png",
        "soju": PRODUCTS_DIR / "soju.jpeg",
        "johnnie_walker": PRODUCTS_DIR / "johnnie_walker.jpeg",
    }

    image_path = file_map.get(product_key)
    if not image_path or not image_path.exists():
        # Fallback to generic description
        fallback = {
            "boksoondoga": "a Boksoondoga premium makgeolli bottle with minimalist Korean label",
            "soju": "a premium Korean soju bottle with clean modern label",
            "johnnie_walker": "a Johnnie Walker Black Label whisky bottle with iconic angled label",
        }
        return fallback.get(product_key, "a premium alcohol bottle")

    analysis = analyze_product_image(image_path)
    return analysis.get("prompt_description", analysis.get("bottle_shape", "a premium bottle"))


def get_all_product_descriptions() -> dict[str, str]:
    """Analyze all product images and return descriptions keyed by product name."""
    return {
        key: get_product_description(key)
        for key in ("boksoondoga", "soju", "johnnie_walker")
    }


if __name__ == "__main__":
    print("Analyzing product images with Gemini 3 Flash...\n")
    for key in ("boksoondoga", "soju", "johnnie_walker"):
        path = PRODUCTS_DIR / ("boksoondoga.png" if key == "boksoondoga"
                               else f"{key}.jpeg")
        if path.exists():
            print(f"  {key}:")
            analysis = analyze_product_image(path)
            for k, v in analysis.items():
                print(f"    {k}: {v}")
            print()
        else:
            print(f"  {key}: image not found at {path}")
