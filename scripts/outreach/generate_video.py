"""
Generate short-form video using Veo 3.1 image-to-video pipeline.

Two-step process:
  1. Imagen 4 generates a hero image of the creator holding 참이슬 (Chamisul soju)
  2. Veo 3.1 animates that image into a 5-8 second vertical video (9:16, 1080p)

Output: output/video/{handle}/
"""

import os
import io
import pathlib
import json
import time
from google import genai
from google.genai import types
from PIL import Image

from creators import all_creators, Creator
from brand import BRAND, brand_visual_prompt
from product_reference import get_product_description

BASE_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output" / "video"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CREATOR_CONTENT_DIR = BASE_DIR / "output" / "creator_content"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

IMAGEN_MODEL = "imagen-4.0-generate-001"


# ---------------------------------------------------------------------------
# Step 1: Generate hero image — creator holding 참이슬
# ---------------------------------------------------------------------------

def load_creator_analysis(creator: Creator) -> dict:
    """Load cached Gemini analysis of the creator's appearance and style."""
    analysis_path = CREATOR_CONTENT_DIR / creator.handle / "analysis.json"
    if analysis_path.exists():
        try:
            return json.loads(analysis_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    # Fallback when no analysis exists
    return {
        "appearance": f"A stylish Korean woman in her late 20s",
        "fashion_style": "modern Korean fashion",
        "aesthetic": "clean, editorial, premium",
        "best_setting": "modern Seoul bar interior",
        "photography_notes": "soft natural lighting, medium shot",
    }


def build_chamisul_image_prompt(creator: Creator, analysis: dict) -> str:
    """Build an Imagen 4 prompt for the creator holding 참이슬."""
    appearance = analysis.get("appearance", "a stylish Korean woman in her late 20s")
    fashion = analysis.get("fashion_style", "modern minimalist fashion")
    aesthetic = analysis.get("aesthetic", "clean, premium, editorial")
    setting = analysis.get("best_setting", "modern Seoul bar interior")
    photo_notes = analysis.get("photography_notes", "soft natural lighting, medium shot")

    chamisul_desc = get_product_description("soju")

    # Creator-specific scene direction based on content category
    style_map = {
        "fashion": (
            f"A Korean woman matching this description: {appearance}. "
            f"Wearing {fashion}. "
            f"Standing confidently in a dimly lit premium bar, holding {chamisul_desc} "
            f"elegantly in one hand at chest height. "
            f"Fashion editorial lighting with warm amber tones and soft bokeh. "
            f"Upper body portrait, slight smile, eye contact with camera."
        ),
        "lifestyle": (
            f"A Korean woman matching this description: {appearance}. "
            f"Wearing {fashion}. "
            f"Sitting at a cozy Seoul rooftop bar during golden hour, "
            f"holding {chamisul_desc} casually while laughing naturally. "
            f"Table has soju glasses and light Korean bar snacks. "
            f"Warm, authentic, candid energy. Natural sunlight."
        ),
        "music": (
            f"A Korean woman matching this description: {appearance}. "
            f"Wearing {fashion}. "
            f"In a moody, atmospheric bar with neon accents, "
            f"holding {chamisul_desc} while resting her chin on her other hand. "
            f"Cinematic close-up, artistic mood, music-video quality lighting. "
            f"Cool blue and warm amber tones."
        ),
        "product review": (
            f"A Korean woman matching this description: {appearance}. "
            f"Wearing {fashion}. "
            f"Sitting at a clean table, holding {chamisul_desc} and examining it "
            f"with an approving expression. Soft overhead lighting, "
            f"minimalist background. Close-up, product-focused composition."
        ),
    }

    # Pick the best matching style
    scene = style_map.get("lifestyle")  # default
    for cat in creator.categories:
        if cat in style_map:
            scene = style_map[cat]
            break

    return (
        f"{scene} "
        f"{aesthetic} mood. {photo_notes}. "
        f"Vertical composition (9:16 aspect ratio), 1080p quality. "
        f"Premium Korean soju advertisement photography. "
        f"Photorealistic, high-end commercial quality."
    )


def generate_chamisul_image(creator: Creator) -> pathlib.Path | None:
    """Generate an image of the creator holding 참이슬 using Imagen 4."""
    creator_dir = OUTPUT_DIR / creator.handle
    creator_dir.mkdir(parents=True, exist_ok=True)

    image_path = creator_dir / "chamisul_hero.png"

    # Use cached image if it exists
    if image_path.exists() and image_path.stat().st_size > 1000:
        print("✓ (cached)", end=" ", flush=True)
        return image_path

    analysis = load_creator_analysis(creator)
    prompt = build_chamisul_image_prompt(creator, analysis)

    # Save prompt for reference
    prompt_path = creator_dir / "chamisul_image_prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")

    try:
        response = client.models.generate_images(
            model=IMAGEN_MODEL,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                numberOfImages=1,
                aspectRatio="9:16",
                personGeneration="ALLOW_ADULT",
            ),
        )
        if response.generated_images:
            img_bytes = response.generated_images[0].image.image_bytes
            img = Image.open(io.BytesIO(img_bytes))
            img.save(image_path)
            print("✓", end=" ", flush=True)
            return image_path
    except Exception as e:
        print(f"FAILED ({e})", end=" ", flush=True)

    return None


# ---------------------------------------------------------------------------
# Step 2: Veo 3.1 image-to-video
# ---------------------------------------------------------------------------

def build_video_prompt(creator: Creator) -> str:
    """Build a short video motion prompt to animate the hero image."""
    style_map = {
        "fashion": (
            "She slowly raises the soju bottle, tilts it to pour into a small glass. "
            "Soft bokeh lights shimmer in the background. Slow motion, cinematic."
        ),
        "lifestyle": (
            "She smiles naturally, lifts the soju glass and takes a small sip. "
            "Golden hour light shifts gently. Wind subtly moves her hair. "
            "Warm, authentic candid moment."
        ),
        "music": (
            "She slowly turns toward the camera with a mysterious smile, "
            "lifts the soju bottle slightly. Neon lights pulse gently in the background. "
            "Cinematic, moody, music-video energy."
        ),
        "product review": (
            "She holds up the soju bottle, rotates it slowly to show the label, "
            "then sets it down and gives a satisfied nod. "
            "Clean, well-lit product showcase moment."
        ),
    }

    motion = style_map.get("lifestyle")  # default
    for cat in creator.categories:
        if cat in style_map:
            motion = style_map[cat]
            break

    return (
        f"{motion} "
        f"Vertical video (9:16 aspect ratio), 1080p quality. "
        f"5-8 seconds duration. Smooth, cinematic camera motion. "
        f"Premium Korean soju commercial quality."
    )


def generate_video(prompt: str, image_path: pathlib.Path, output_path: pathlib.Path) -> pathlib.Path | None:
    """Generate video from image using Veo 3.1 image-to-video."""
    try:
        # Load the hero image for Veo input
        image = types.Image.from_file(location=str(image_path))

        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio="9:16",
                number_of_videos=1,
            ),
        )

        # Poll for completion
        print("(generating", end="", flush=True)
        while not operation.done:
            time.sleep(5)
            print(".", end="", flush=True)
            operation = client.operations.get(operation)
        print(")", end=" ", flush=True)

        if operation.response and operation.response.generated_videos:
            video = operation.response.generated_videos[0]
            video_data = client.files.download(file=video.video)
            output_path.write_bytes(video_data)
            return output_path

    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
            print(f"\n    Veo API not available: {e}")
            print("    Creating placeholder description instead...")
            _create_placeholder(prompt, image_path, output_path)
            return output_path
        print(f"\n    Video generation error: {e}")
    return None


def _create_placeholder(prompt: str, image_path: pathlib.Path, output_path: pathlib.Path):
    """Create a text placeholder when video API is unavailable."""
    desc_path = output_path.with_suffix(".txt")
    desc_path.write_text(
        f"VIDEO PROMPT (image-to-video):\n\n"
        f"Source image: {image_path.name}\n"
        f"Motion prompt: {prompt}\n\n"
        f"Specs: 9:16 vertical, 1080p, 5-8 seconds\n"
        f"Model: Veo 3.1 (image-to-video mode)\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def generate_creator_video(creator: Creator):
    """Two-step video pipeline: Imagen → Veo for a single creator."""
    creator_dir = OUTPUT_DIR / creator.handle
    creator_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Generate hero image with 참이슬
    print(f"    [Imagen 4] Generating 참이슬 hero image...", end=" ", flush=True)
    hero_image = generate_chamisul_image(creator)

    if not hero_image:
        print("    ✗ Cannot generate video without hero image.")
        return None

    # Step 2: Animate with Veo 3.1
    video_prompt = build_video_prompt(creator)
    output_path = creator_dir / f"{creator.handle}_chamisul.mp4"

    # Save video prompt for reference
    video_prompt_path = creator_dir / "video_prompt.txt"
    video_prompt_path.write_text(video_prompt, encoding="utf-8")

    print(f"\n    [Veo 3.1] Animating image-to-video...", end=" ", flush=True)
    result = generate_video(video_prompt, hero_image, output_path)

    if result and result.suffix == ".mp4":
        size_mb = result.stat().st_size / (1024 * 1024)
        print(f"✓ ({size_mb:.1f}MB)")
    elif result:
        print("✓ (placeholder created)")
    else:
        print("FAILED")

    return result


def main():
    print("=" * 60)
    print("  GREENBOTTLE — 참이슬 Video Generation Pipeline")
    print("  Step 1: Imagen 4 (creator + 참이슬 hero image)")
    print("  Step 2: Veo 3.1 (image-to-video animation)")
    print("=" * 60)

    for creator in all_creators():
        print(f"\n  @{creator.handle} ({creator.name_kr}):")
        generate_creator_video(creator)

    print(f"\nDone! Videos saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
