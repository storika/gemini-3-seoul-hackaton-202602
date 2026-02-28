"""
Shared utility for adding Korean text overlays on images and video.
- overlay_text_on_image(): Pillow-based text rendering
- overlay_text_on_video(): FFmpeg drawtext filter
"""

import pathlib
import subprocess
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = pathlib.Path(__file__).parent / "assets" / "fonts"
DEFAULT_FONT = FONT_DIR / "Pretendard-Bold.otf"
REGULAR_FONT = FONT_DIR / "Pretendard-Regular.otf"
SEMIBOLD_FONT = FONT_DIR / "Pretendard-SemiBold.otf"


def get_font(size: int = 48, weight: str = "bold") -> ImageFont.FreeTypeFont:
    """Load Pretendard font at given size."""
    font_map = {"bold": DEFAULT_FONT, "regular": REGULAR_FONT, "semibold": SEMIBOLD_FONT}
    font_path = font_map.get(weight, DEFAULT_FONT)
    return ImageFont.truetype(str(font_path), size)


def overlay_text_on_image(
    img_path: str | pathlib.Path,
    text: str,
    position: tuple[int, int] = (50, 50),
    font_size: int = 48,
    font_weight: str = "bold",
    color: str = "#FFFFFF",
    stroke_color: str = "#000000",
    stroke_width: int = 2,
    output_path: str | pathlib.Path | None = None,
    max_width: int | None = None,
) -> pathlib.Path:
    """Add text overlay to an image using Pillow.

    Args:
        img_path: Input image path
        text: Text to overlay (supports Korean)
        position: (x, y) top-left position
        font_size: Font size in pixels
        font_weight: "bold", "regular", or "semibold"
        color: Text color (hex)
        stroke_color: Outline color for readability
        stroke_width: Outline thickness
        output_path: Where to save (defaults to {input}_text.png)
        max_width: If set, wraps text to fit within this pixel width
    """
    img_path = pathlib.Path(img_path)
    img = Image.open(img_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = get_font(font_size, font_weight)

    # Simple word wrapping for Korean text
    if max_width:
        lines = _wrap_text(draw, text, font, max_width)
        text = "\n".join(lines)

    draw.text(
        position,
        text,
        font=font,
        fill=color,
        stroke_fill=stroke_color,
        stroke_width=stroke_width,
    )

    result = Image.alpha_composite(img, overlay)
    if output_path is None:
        output_path = img_path.parent / f"{img_path.stem}_text{img_path.suffix}"
    output_path = pathlib.Path(output_path)
    result.save(output_path)
    return output_path


def _wrap_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap text (including Korean) to fit within max_width pixels."""
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] > max_width and current_line:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    return lines


def overlay_text_on_video(
    video_path: str | pathlib.Path,
    text: str,
    output_path: str | pathlib.Path | None = None,
    font_size: int = 48,
    color: str = "white",
    position: str = "center",
    start_time: float = 0.0,
    duration: float | None = None,
    style: str = "tiktok",
) -> pathlib.Path:
    """Add text overlay to video using FFmpeg drawtext.

    Args:
        video_path: Input video path
        text: Text to overlay
        output_path: Where to save (defaults to {input}_text.mp4)
        font_size: Font size
        color: FFmpeg color name or hex
        position: "center", "top", "bottom", or custom "x=100:y=200"
        start_time: When text appears (seconds)
        duration: How long text shows (None = entire video)
        style: "tiktok" for bold with shadow, "minimal" for clean
    """
    video_path = pathlib.Path(video_path)
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_text{video_path.suffix}"
    output_path = pathlib.Path(output_path)

    font_path = str(DEFAULT_FONT).replace(":", "\\:")
    escaped_text = text.replace("'", "'\\''").replace(":", "\\:")

    # Position mapping
    pos_map = {
        "center": "x=(w-text_w)/2:y=(h-text_h)/2",
        "top": "x=(w-text_w)/2:y=80",
        "bottom": "x=(w-text_w)/2:y=h-text_h-120",
    }
    pos = pos_map.get(position, position)

    # Style-specific filter
    if style == "tiktok":
        drawtext = (
            f"drawtext=fontfile='{font_path}':text='{escaped_text}':"
            f"fontsize={font_size}:fontcolor={color}:{pos}:"
            f"borderw=3:bordercolor=black:shadowcolor=black@0.5:shadowx=2:shadowy=2"
        )
    else:
        drawtext = (
            f"drawtext=fontfile='{font_path}':text='{escaped_text}':"
            f"fontsize={font_size}:fontcolor={color}:{pos}"
        )

    # Time constraints
    if start_time > 0 or duration:
        enable_parts = []
        if start_time > 0:
            enable_parts.append(f"gte(t,{start_time})")
        if duration:
            enable_parts.append(f"lte(t,{start_time + duration})")
        enable = "*".join(enable_parts)
        drawtext += f":enable='{enable}'"

    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", drawtext,
        "-codec:a", "copy",
        str(output_path),
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def create_title_card(
    text: str,
    width: int = 1080,
    height: int = 1080,
    bg_color: str = "#1A1A1A",
    text_color: str = "#F5F0E8",
    font_size: int = 64,
    output_path: str | pathlib.Path = "title_card.png",
) -> pathlib.Path:
    """Create a standalone title card image with centered text."""
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    font = get_font(font_size, "bold")

    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2

    draw.text((x, y), text, font=font, fill=text_color)
    output_path = pathlib.Path(output_path)
    img.save(output_path)
    return output_path


if __name__ == "__main__":
    # Quick test
    card = create_title_card(
        "복순도가 × 크리에이터",
        output_path=pathlib.Path(__file__).parent / "output" / "test_title.png",
    )
    print(f"Created test title card: {card}")
