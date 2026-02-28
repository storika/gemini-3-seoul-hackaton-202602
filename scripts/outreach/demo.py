"""
End-to-end hackathon demo runner.
Walks through the full Greenbottle pipeline in ~3 minutes.
Run: python3 demo.py
"""

import os
import sys
import time
import pathlib
import subprocess

BASE_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def print_header(title: str, emoji: str = ""):
    """Print a formatted section header."""
    width = 60
    print(f"\n{'='*width}")
    print(f"  {emoji}  {title}")
    print(f"{'='*width}\n")


def print_sub(text: str):
    print(f"  → {text}")


def pause(seconds: float = 2.0, msg: str = ""):
    """Pause with optional message."""
    if msg:
        print(f"\n  [{msg} — press Enter to continue or wait {seconds}s]", end="", flush=True)
    try:
        import select
        ready, _, _ = select.select([sys.stdin], [], [], seconds)
        if ready:
            sys.stdin.readline()
    except Exception:
        time.sleep(seconds)
    print()


def section_discovery():
    """Section 1: Creator Discovery (30s)"""
    print_header("STEP 1: Creator Discovery & Brand Fit Analysis", "🔍")
    print("  Storika's Social Ontology identified 4 ideal creators for 복순도가:\n")

    from creators import all_creators
    for c in all_creators():
        print(f"  ┌─ @{c.handle} ({c.name_kr})")
        print(f"  │  {c.followers:,} followers · {c.engagement_rate}% engagement · {c.collab_ratio:.0%} collab ratio")
        print(f"  │  Categories: {', '.join(c.categories)}")
        print(f"  │  Fit: {c.brand_fit_reasons[0]}")
        print(f"  └─\n")

    pause(5, "Creator Discovery complete")


def section_voice():
    """Section 2: Personalized Voice Outreach (45s)"""
    print_header("STEP 2: Hyper-Personalized Voice Outreach", "📞")

    scripts_dir = OUTPUT_DIR / "scripts"
    voice_dir = OUTPUT_DIR / "voice"

    from creators import all_creators
    for c in all_creators():
        script_file = scripts_dir / f"{c.handle}.txt"
        voice_file = voice_dir / f"{c.handle}.mp3"

        print(f"  @{c.handle} ({c.name_kr}):")

        if script_file.exists():
            script = script_file.read_text(encoding="utf-8")
            # Show first 150 chars of script
            preview = script[:150].replace("\n", " ")
            print(f"  Script: \"{preview}...\"")
        else:
            print("  Script: [not generated yet]")

        if voice_file.exists():
            size_kb = voice_file.stat().st_size // 1024
            print(f"  Audio: ✓ {size_kb}KB MP3 (ElevenLabs Lily voice)")
        else:
            root_mp3 = BASE_DIR / f"call_{c.handle.split('.')[0].replace('_', '')}.mp3"
            if root_mp3.exists():
                print(f"  Audio: ✓ (generic version available)")
            else:
                print("  Audio: [not generated yet]")

        # Play audio sample if available and on macOS
        if voice_file.exists() and sys.platform == "darwin":
            print("  Playing 5-second sample...", end=" ", flush=True)
            try:
                proc = subprocess.Popen(
                    ["afplay", str(voice_file)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                time.sleep(5)
                proc.terminate()
                print("✓")
            except Exception:
                print("(playback unavailable)")
        print()

    pause(3, "Voice Outreach complete")


def section_guidelines():
    """Section 3: Content Guidelines (30s)"""
    print_header("STEP 3: Per-Creator Content Guidelines", "📋")

    guidelines_dir = OUTPUT_DIR / "guidelines"

    from creators import all_creators
    for c in all_creators():
        guide_file = guidelines_dir / f"{c.handle}.md"
        if guide_file.exists():
            content = guide_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            # Show section headers
            headers = [l for l in lines if l.startswith("## ")]
            print(f"  @{c.handle}: {len(content):,} chars, sections: {', '.join(h.replace('## ', '') for h in headers[:5])}")
        else:
            print(f"  @{c.handle}: [not generated yet]")

    pause(3, "Guidelines complete")


def section_posts():
    """Section 3b: Ready-to-Post Content"""
    print_header("STEP 3b: Ready-to-Post Social Content", "📱")

    posts_dir = OUTPUT_DIR / "posts"

    from creators import all_creators
    for c in all_creators():
        post_file = posts_dir / f"{c.handle}.md"
        if post_file.exists():
            content = post_file.read_text(encoding="utf-8")
            post_count = content.count("### Post")
            print(f"  @{c.handle}: {post_count} post packages, {len(content):,} chars")
            # Show first post concept
            for line in content.split("\n"):
                if line.startswith("### Post"):
                    print(f"    {line}")
                    break
        else:
            print(f"  @{c.handle}: [not generated yet]")

    pause(3, "Posts complete")


def section_creator_content():
    """Section 4: Personalized Creator Content (45s)"""
    print_header("STEP 4: Influencer Content (Gemini 3 + Imagen 4)", "🧑‍🎨")
    print("  Two-step AI pipeline:")
    print("    1. Gemini 3 Flash analyzes creator's real photos from our DB")
    print("    2. Imagen 4 generates personalized content based on analysis\n")

    content_dir = OUTPUT_DIR / "creator_content"

    from creators import all_creators
    import json
    for c in all_creators():
        creator_dir = content_dir / c.handle
        if creator_dir.exists():
            analysis_file = creator_dir / "analysis.json"
            images = sorted(creator_dir.glob("*.png"))
            images = [i for i in images if "_raw" not in i.name]

            print(f"  @{c.handle} ({c.name_kr}):")
            if analysis_file.exists():
                analysis = json.loads(analysis_file.read_text())
                appearance = analysis.get("appearance", "")[:80]
                print(f"    Gemini Analysis: \"{appearance}...\"")

            print(f"    Generated: {len(images)} content pieces")
            for img in images:
                size_kb = img.stat().st_size // 1024
                print(f"      {img.stem}: {size_kb}KB")

            # Open first image on macOS
            if images and sys.platform == "darwin":
                try:
                    subprocess.Popen(
                        ["open", str(images[0])],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except Exception:
                    pass
        else:
            print(f"  @{c.handle}: [not generated yet]")
        print()

    pause(3, "Creator Content complete")


def section_carousel():
    """Section 5: Carousel Images (45s)"""
    print_header("STEP 5: AI-Generated Carousel (Imagen 4)", "🖼")

    carousel_dir = OUTPUT_DIR / "carousel"

    from creators import all_creators
    for c in all_creators():
        creator_dir = carousel_dir / c.handle
        if creator_dir.exists():
            slides = sorted(creator_dir.glob("slide_*_*.png"))
            slides = [s for s in slides if "_raw" not in s.name]
            print(f"  @{c.handle}: {len(slides)} slides")
            for slide in slides:
                size_kb = slide.stat().st_size // 1024
                name = slide.stem.split("_", 2)[-1] if "_" in slide.stem else slide.stem
                print(f"    {name}: {size_kb}KB")

            # Open first slide on macOS
            if slides and sys.platform == "darwin":
                try:
                    subprocess.Popen(
                        ["open", str(slides[0])],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except Exception:
                    pass
        else:
            print(f"  @{c.handle}: [not generated yet]")
        print()

    pause(3, "Carousel complete")


def section_video():
    """Section 6: Short-Form Video — Imagen 4 hero + Veo 3.1 image-to-video (30s)"""
    print_header("STEP 6: 참이슬 Video (Imagen 4 → Veo 3.1 Image-to-Video)", "🎬")
    print("  Pipeline: Imagen 4 generates creator + 참이슬 hero image")
    print("            → Veo 3.1 animates into 5-8s vertical video\n")

    video_dir = OUTPUT_DIR / "video"

    from creators import all_creators
    for c in all_creators():
        creator_dir = video_dir / c.handle
        if creator_dir.exists():
            hero = creator_dir / "chamisul_hero.png"
            videos = list(creator_dir.glob("*.mp4"))
            prompts = list(creator_dir.glob("*.txt"))
            if hero.exists():
                size_kb = hero.stat().st_size // 1024
                print(f"  @{c.handle}: ✓ Hero image ({size_kb}KB)", end="")
                if videos:
                    for v in videos:
                        size_mb = v.stat().st_size / (1024 * 1024)
                        print(f" → Video {v.name} ({size_mb:.1f}MB)")
                else:
                    print(" → Video pending")
            elif prompts:
                print(f"  @{c.handle}: Image prompt saved (generation pending)")
            else:
                print(f"  @{c.handle}: [not generated yet]")
        else:
            print(f"  @{c.handle}: [not generated yet]")

    pause(3, "Video complete")


def section_swap():
    """Section 7: Product Swap Demo (30s)"""
    print_header("STEP 7: Product Swap — Same Aesthetic, Different Product", "🔄")

    swap_dir = OUTPUT_DIR / "swap"
    if swap_dir.exists():
        images = sorted(swap_dir.glob("*.png"))
        images = [i for i in images if "_raw" not in i.name]
        if images:
            print("  Same scene, same lighting, 3 different products:\n")
            for img in images:
                size_kb = img.stat().st_size // 1024
                name = img.stem.replace("_", " ").title()
                print(f"    {name}: {size_kb}KB")

            # Open images on macOS
            if sys.platform == "darwin":
                try:
                    for img in images:
                        subprocess.Popen(
                            ["open", str(img)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        time.sleep(0.5)
                except Exception:
                    pass

            print("\n  Key insight: Prompt engineering keeps the aesthetic consistent")
            print("  while only swapping the product — enabling scalable content")
            print("  across multiple brand partnerships.")
        else:
            print("  [not generated yet]")
    else:
        print("  [not generated yet]")

    pause(3, "Product Swap complete")


def section_summary():
    """Final summary."""
    print_header("GREENBOTTLE: Full Pipeline Summary", "🟢")
    print("  Hyper-Personalized Influencer Outreach Pipeline\n")
    print("  ┌──────────────────────────────────────────────────────────┐")
    print("  │  Creator Discovery    → 4 data-backed selections        │")
    print("  │  Voice Outreach       → Personalized Korean calls       │")
    print("  │  Content Guidelines   → Per-creator brand guides        │")
    print("  │  Social Posts         → Ready-to-publish content        │")
    print("  │  Creator Content      → Gemini analyzes + Imagen creates│")
    print("  │  Carousel Images      → Imagen 4 + Korean text          │")
    print("  │  Short-Form Video     → Imagen 4 + Veo 3.1 image-to-video│")
    print("  │  Product Swap         → Consistent aesthetic swap        │")
    print("  └──────────────────────────────────────────────────────────┘\n")
    print("  Gemini 3 Features Used:")
    print("    • gemini-3-flash-preview — Multimodal analysis + content generation")
    print("    • imagen-4.0-generate-001 — Personalized influencer content + carousel")
    print("    • veo-3.1-generate-preview — Vertical 1080p video")
    print("    • ClickHouse → Gemini → Imagen pipeline (DB-driven AI content)")
    print("    • Product Swapping — Prompt engineering for consistency")
    print("    • 1M Token Context — Full brand + creator data in single prompt\n")
    print("  Built by Storika for Gemini 3 Seoul Hackathon 🇰🇷")


def main():
    print("\n" + "=" * 60)
    print("  GREENBOTTLE")
    print("  Hyper-Personalized Influencer Outreach Pipeline")
    print("  Gemini 3 Seoul Hackathon — February 28, 2026")
    print("=" * 60)

    pause(2, "Starting demo")

    section_discovery()
    section_voice()
    section_guidelines()
    section_posts()
    section_creator_content()
    section_carousel()
    section_video()
    section_swap()
    section_summary()

    print("\n  Demo complete! 🎉\n")


if __name__ == "__main__":
    main()
