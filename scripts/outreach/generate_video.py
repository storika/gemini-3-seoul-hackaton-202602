"""
Generate short-form video using Veo 3.1 (via Gemini API) with text overlays.
5-8 second vertical video (9:16, 1080p) per creator.
Output: output/video/{handle}/
"""

import os
import pathlib
import time
from google import genai

from creators import all_creators, Creator
from brand import BRAND, brand_summary, brand_visual_prompt
from product_reference import get_product_description

OUTPUT_DIR = pathlib.Path(__file__).parent / "output" / "video"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def build_video_prompt(creator: Creator) -> str:
    """Build video generation prompt tailored to creator's aesthetic."""
    visual = BRAND["visual_identity"]

    # Get actual product description from Gemini analysis of the real bottle image
    product_desc = get_product_description("boksoondoga")

    # Creator-specific scene direction
    style_map = {
        "fashion": (
            f"A stylish woman's hand elegantly picks up {product_desc} "
            f"from a marble table, pours milky white makgeolli into a crystal glass. "
            f"Slow motion pour with soft bokeh lights in background. "
            f"Fashion editorial lighting, warm tones."
        ),
        "lifestyle": (
            f"Warm golden hour scene — hands clink glasses of Boksoondoga sparkling makgeolli "
            f"on a cozy Seoul rooftop. {product_desc} on the table. "
            f"Camera slowly pulls back revealing the cityscape. "
            f"Authentic, candid energy. Natural lighting."
        ),
        "music": (
            f"Cinematic close-up: condensation drips down {product_desc} "
            f"as soft ambient music plays. Camera slowly rises to reveal "
            f"a beautiful Jeju sunset reflected in the glass. "
            f"Artistic, moody, music-video quality."
        ),
        "product review": (
            f"Satisfying unboxing sequence — hands unwrap tissue paper to reveal "
            f"{product_desc}. "
            f"Camera circles the products with soft overhead lighting. "
            f"ASMR-style, satisfying reveal energy."
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
        f"Vertical video (9:16 aspect ratio), 1080p quality. "
        f"5-8 seconds duration. {visual['mood']} "
        f"Color palette: warm white, volcanic black, soft gold. "
        f"Premium craft Korean alcohol brand. Cinematic quality."
    )


def generate_video(prompt: str, output_path: pathlib.Path) -> pathlib.Path | None:
    """Generate video using Veo via Gemini API."""
    try:
        # Use Veo 3.1 for video generation
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=genai.types.GenerateVideosConfig(
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
            # Download the video
            video_data = client.files.download(file=video.video)
            output_path.write_bytes(video_data)
            return output_path

    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
            print(f"\n    Veo API not available: {e}")
            print("    Creating placeholder video description instead...")
            _create_placeholder(prompt, output_path)
            return output_path
        print(f"\n    Video generation error: {e}")
    return None


def _create_placeholder(prompt: str, output_path: pathlib.Path):
    """Create a text placeholder when video API is unavailable."""
    desc_path = output_path.with_suffix(".txt")
    desc_path.write_text(
        f"VIDEO PROMPT (for manual generation or demo):\n\n{prompt}\n\n"
        f"Specs: 9:16 vertical, 1080p, 5-8 seconds\n",
        encoding="utf-8",
    )


def generate_creator_video(creator: Creator):
    """Generate video for a single creator."""
    creator_dir = OUTPUT_DIR / creator.handle
    creator_dir.mkdir(parents=True, exist_ok=True)

    prompt = build_video_prompt(creator)
    output_path = creator_dir / f"{creator.handle}_boksoondoga.mp4"

    print(f"    Generating video...", end=" ", flush=True)
    result = generate_video(prompt, output_path)

    if result and result.suffix == ".mp4":
        size_mb = result.stat().st_size / (1024 * 1024)
        print(f"✓ ({size_mb:.1f}MB)")
    elif result:
        print("✓ (placeholder created)")
    else:
        print("FAILED")

    # Save prompt for reference
    prompt_path = creator_dir / "prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")

    return result


def main():
    print("Generating short-form videos...\n")
    for creator in all_creators():
        print(f"  @{creator.handle} ({creator.name_kr}):")
        generate_creator_video(creator)
        print()

    print(f"Done! Videos saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
