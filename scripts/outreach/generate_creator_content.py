"""
Generate influencer-specific content using real Instagram data as reference.

Two-step AI pipeline:
  1. Gemini 3 Flash analyzes the creator's real photos (profile + posts) from ClickHouse
  2. Imagen 4 generates new content based on that analysis + Boksoondoga brand guide

Usage:
    python3 generate_creator_content.py              # all creators
    python3 generate_creator_content.py jungha.0     # single creator
"""

import os
import sys
import pathlib
import io
import json
import requests
from google import genai
from google.genai import types
from PIL import Image

from creators import all_creators, get_creator, Creator
from brand import BRAND, brand_visual_prompt
from text_overlay import overlay_text_on_image
from product_reference import get_product_description

BASE_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output" / "creator_content"
REFERENCE_DIR = BASE_DIR / "output" / "reference"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# ClickHouse Cloud config
CH_HOST = os.environ.get("CLICKHOUSE_HOST", "")
CH_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD", "")
CH_USER = "default"
CH_DB = "default"

STORIKA_CDN = "https://cdn.storika.ai"

GEMINI_MODEL = "gemini-3-flash-preview"
IMAGEN_MODEL = "imagen-4.0-generate-001"


# ---------------------------------------------------------------------------
# ClickHouse helpers
# ---------------------------------------------------------------------------

def query_clickhouse(sql: str) -> list[dict]:
    """Execute a SELECT against ClickHouse HTTP API."""
    if not CH_HOST or not CH_PASSWORD:
        return []
    try:
        r = requests.post(
            f"https://{CH_HOST}:8443/",
            params={"query": sql, "default_format": "JSON", "database": CH_DB},
            auth=(CH_USER, CH_PASSWORD),
            timeout=30,
        )
        if r.status_code == 200:
            return r.json().get("data", [])
    except Exception as e:
        print(f"    ClickHouse error: {e}")
    return []


def fetch_profile_id(handle: str) -> str | None:
    rows = query_clickhouse(
        f"SELECT profile_id FROM apify_instagram_profiles "
        f"WHERE username = '{handle}' LIMIT 1"
    )
    return rows[0]["profile_id"] if rows else None


def fetch_top_posts(handle: str, limit: int = 6) -> list[dict]:
    return query_clickhouse(
        f"SELECT DISTINCT post_id, short_code, display_url, type, likes_count "
        f"FROM apify_instagram_posts "
        f"WHERE owner_username = '{handle}' AND type IN ('Image', 'Sidecar') "
        f"ORDER BY likes_count DESC LIMIT {limit}"
    )


# ---------------------------------------------------------------------------
# Image download + cache
# ---------------------------------------------------------------------------

def download_image(url: str, output_path: pathlib.Path) -> bool:
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and len(r.content) > 500:
            output_path.write_bytes(r.content)
            return True
    except Exception:
        pass
    return False


def ensure_reference_images(creator: Creator) -> list[pathlib.Path]:
    """Get cached reference images, downloading from ClickHouse/CDN if needed."""
    ref_dir = REFERENCE_DIR / creator.handle
    ref_dir.mkdir(parents=True, exist_ok=True)

    # Profile pic — Storika CDN is permanent
    profile_path = ref_dir / "profile.jpg"
    if not profile_path.exists() or profile_path.stat().st_size < 500:
        profile_id = fetch_profile_id(creator.handle)
        if profile_id:
            download_image(f"{STORIKA_CDN}/profile/{profile_id}.jpeg", profile_path)

    # Post images — Instagram CDN URLs expire, but try anyway
    cached_posts = [f for f in sorted(ref_dir.glob("post_*.jpg")) if f.stat().st_size > 500]
    if len(cached_posts) < 2:
        posts = fetch_top_posts(creator.handle, limit=6)
        for i, post in enumerate(posts):
            post_path = ref_dir / f"post_{i}.jpg"
            if not post_path.exists() and post.get("display_url"):
                download_image(post["display_url"], post_path)

    # Collect all valid images
    images = []
    if profile_path.exists() and profile_path.stat().st_size > 500:
        images.append(profile_path)
    for f in sorted(ref_dir.glob("post_*.jpg")):
        if f.stat().st_size > 500:
            images.append(f)
    for f in sorted(ref_dir.glob("*.png")) + sorted(ref_dir.glob("*.jpeg")):
        if f not in images and f.stat().st_size > 500:
            images.append(f)
    return images


# ---------------------------------------------------------------------------
# Step 1: Gemini analyzes reference images
# ---------------------------------------------------------------------------

ANALYSIS_PROMPT = """\
You are a creative director preparing to generate AI lifestyle content \
featuring this influencer for a premium Korean makgeolli brand (복순도가 Boksoondoga).

Analyze this person's photos and provide a JSON response with these fields:
{
  "appearance": "Detailed physical description (age range, face shape, hair color/style/length, skin tone, build)",
  "fashion_style": "Their typical clothing/accessory style based on these photos",
  "aesthetic": "Their visual aesthetic and mood (lighting, color palette, composition style)",
  "best_setting": "The type of setting/background that would look most natural for them",
  "photography_notes": "Camera angle, lighting style, and mood that matches their content"
}

Return ONLY valid JSON, no markdown fences."""


def analyze_creator(reference_images: list[pathlib.Path]) -> dict:
    """Use Gemini 3 Flash to analyze creator's appearance and style."""
    contents = []

    # Include up to 4 reference images
    for img_path in reference_images[:4]:
        img_bytes = img_path.read_bytes()
        mime = "image/jpeg" if img_path.suffix in (".jpg", ".jpeg") else "image/png"
        contents.append(types.Part(inline_data=types.Blob(
            mime_type=mime, data=img_bytes,
        )))

    contents.append(ANALYSIS_PROMPT)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        ),
    )

    try:
        return json.loads(response.text)
    except (json.JSONDecodeError, AttributeError):
        # Fallback: try to extract JSON from response
        text = response.text or ""
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        return {}


# ---------------------------------------------------------------------------
# Step 2: Imagen generates content based on analysis
# ---------------------------------------------------------------------------

def build_personalized_prompts(creator: Creator, analysis: dict) -> list[dict]:
    """Build Imagen prompts incorporating the Gemini analysis + actual product reference."""
    visual = BRAND["visual_identity"]
    appearance = analysis.get("appearance", "a stylish Korean woman in her late 20s")
    fashion = analysis.get("fashion_style", "modern minimalist fashion")
    aesthetic = analysis.get("aesthetic", "clean, premium, editorial")
    setting = analysis.get("best_setting", "modern Seoul interior")
    photo_notes = analysis.get("photography_notes", "soft natural lighting, medium shot")

    # Get actual product description from Gemini analysis of the real bottle image
    product_desc = get_product_description("boksoondoga")

    base_style = (
        f"Color palette: warm white, volcanic black, soft gold. "
        f"Natural lighting, high-end editorial quality. {photo_notes}."
    )

    person = (
        f"A Korean woman matching this exact description: {appearance}. "
        f"Wearing {fashion}."
    )

    return [
        {
            "name": "hero",
            "prompt": (
                f"{person} Elegantly holding {product_desc} in both hands. "
                f"Upper body portrait, confident natural expression, slight smile. "
                f"Background: blurred {setting}. {aesthetic} mood. "
                f"{base_style} Square 1:1 aspect ratio. "
                f"Premium brand ambassador photography."
            ),
            "text_overlay": f"@{creator.handle} × 복순도가",
            "text_position": "bottom",
        },
        {
            "name": "lifestyle",
            "prompt": (
                f"{person} Enjoying Boksoondoga sparkling makgeolli at a modern Seoul rooftop "
                f"during golden hour. She pours golden-white sparkling liquid from {product_desc} "
                f"into a crystal glass, natural candid moment with warm smile. "
                f"Table has the bottle and minimal styling (one tangerine, linen napkin). "
                f"{aesthetic} mood. {base_style} Square 1:1 aspect ratio."
            ),
            "text_overlay": "제주 프리미엄 스파클링 막걸리\nJeju Premium Sparkling",
            "text_position": "bottom",
        },
        {
            "name": "intimate",
            "prompt": (
                f"{person} In a cozy minimalist interior, sitting at a clean table with "
                f"{product_desc} and a small white ceramic cup of milky makgeolli. "
                f"She holds the cup near her lips, eyes closed in appreciation. "
                f"Intimate, personal moment. Soft window light, volcanic stone coaster, "
                f"warm amber evening glow. {aesthetic} mood. "
                f"{base_style} Square 1:1 aspect ratio."
            ),
            "text_overlay": None,
        },
    ]


def generate_imagen(prompt: str, output_path: pathlib.Path) -> pathlib.Path | None:
    """Generate with Imagen 4."""
    response = client.models.generate_images(
        model=IMAGEN_MODEL,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            numberOfImages=1,
            aspectRatio="1:1",
            personGeneration="ALLOW_ADULT",
        ),
    )
    if response.generated_images:
        img_bytes = response.generated_images[0].image.image_bytes
        img = Image.open(io.BytesIO(img_bytes))
        img.save(output_path)
        return output_path
    return None


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def generate_creator_content(creator: Creator) -> list[pathlib.Path]:
    """Full pipeline for a single creator."""
    creator_dir = OUTPUT_DIR / creator.handle
    creator_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  @{creator.handle} ({creator.name_kr}):")

    # Step 1: Get reference images from DB
    print(f"    [DB] Fetching reference images...", end=" ", flush=True)
    ref_images = ensure_reference_images(creator)
    if ref_images:
        print(f"✓ ({len(ref_images)} found)")
    else:
        print("none cached")

    # Step 2: Gemini analyzes the creator
    print(f"    [Gemini 3] Analyzing appearance & style...", end=" ", flush=True)
    if ref_images:
        analysis = analyze_creator(ref_images)
        # Cache analysis for reference
        analysis_path = creator_dir / "analysis.json"
        analysis_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
        appearance = analysis.get("appearance", "")[:80]
        print(f"✓ ({appearance}...)")
    else:
        analysis = {
            "appearance": f"A {creator.content_style.split(',')[0].lower()} Korean woman in her late 20s",
            "fashion_style": "modern Korean fashion",
            "aesthetic": "clean, editorial, premium",
            "best_setting": "modern minimalist interior",
            "photography_notes": "soft natural lighting, medium shot",
        }
        print(f"✓ (using profile data)")

    # Step 3: Build personalized prompts and generate
    contents = build_personalized_prompts(creator, analysis)
    generated = []

    for i, content in enumerate(contents, 1):
        print(f"    [Imagen 4] {content['name']} ({i}/{len(contents)})...", end=" ", flush=True)

        raw_path = creator_dir / f"{content['name']}_raw.png"
        final_path = creator_dir / f"{content['name']}.png"

        try:
            result = generate_imagen(content["prompt"], raw_path)
        except Exception as e:
            print(f"FAILED ({e})")
            continue

        if not result:
            print("FAILED (no image)")
            continue

        # Apply text overlay
        if content.get("text_overlay"):
            pos_map = {"bottom": (60, 900), "center": (60, 460), "top": (60, 60)}
            pos = pos_map.get(content.get("text_position", "bottom"), (60, 900))
            overlay_text_on_image(
                raw_path, content["text_overlay"],
                position=pos, font_size=42, max_width=960,
                output_path=final_path,
            )
            print(f"✓ (with overlay)")
        else:
            raw_path.rename(final_path)
            print("✓")

        generated.append(final_path)

    # Save prompts for reference
    prompts_path = creator_dir / "prompts.json"
    prompts_path.write_text(
        json.dumps([c["prompt"] for c in contents], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return generated


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  GREENBOTTLE — Influencer Content Generation")
    print("  Step 1: Gemini 3 Flash (analyze creator)")
    print("  Step 2: Imagen 4 (generate personalized content)")
    print("=" * 60)

    if len(sys.argv) > 1:
        handle = sys.argv[1].lstrip("@")
        creator = get_creator(handle)
        results = generate_creator_content(creator)
        print(f"\n  → {len(results)} content pieces generated")
    else:
        for creator in all_creators():
            results = generate_creator_content(creator)
            print(f"    → {len(results)} content pieces\n")

    print(f"\nDone! Content saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
