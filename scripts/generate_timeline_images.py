#!/usr/bin/env python3
"""Batch-generate Imagen 4 images for timeline events.

For each event, generates:
  - hero image (actor/brand visual, 16:9)
  - news image per headline (16:9)

Usage:
    python scripts/generate_timeline_images.py [--dry-run] [--event EVENT_ID]

Requires GOOGLE_API_KEY to be set.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.timeline.event_data import TIMELINE_EVENTS
from src.media.imagen_client import generate_image

OUTPUT_DIR = Path(__file__).parent.parent / "generated_images"

# ── Hero image prompts (actor / brand visual per event) ──────────────────────

HERO_PROMPTS: dict[str, str] = {
    "soju-001": (
        "1920s Korean distillery workers in traditional clothing, crafting soju in a small workshop. "
        "Sepia-toned historical photograph style. Copper distillation equipment, steam rising. "
        "Cinematic, documentary restoration quality."
    ),
    "soju-002": (
        "1950s post-war Seoul reconstruction. Factory workers loading soju crates onto trucks "
        "in front of a newly built industrial building. Black and white photography style, "
        "hopeful atmosphere, Korean economic recovery era."
    ),
    "soju-003": (
        "1970s Korean working-class bar scene. Soju bottles on a worn wooden table, "
        "factory workers sharing drinks after a long day. Warm neon lighting, nostalgic atmosphere. "
        "Retro Korean street photography style."
    ),
    "soju-004": (
        "Dramatic product shot: a pristine soju bottle labeled 'Chamisul' emerging from cascading "
        "bamboo charcoal pieces. Crystal clear liquid catching light. Dark studio background "
        "with single spotlight. Premium commercial photography, 1998 Korean aesthetic."
    ),
    "soju-005": (
        "Elegant Korean actress in late 1990s fashion, gracefully holding a soju glass in a minimalist "
        "studio setting. Soft diffused lighting, serene expression embodying purity. "
        "Classic Korean commercial photography style. Full portrait, warm tones."
    ),
    "soju-006": (
        "Modern soju bottle with a fresh blue label, surrounded by molecular structure visualizations "
        "of alkaline water. Clean laboratory-meets-bar aesthetic. Futuristic product photography "
        "with science overlay graphics. 2006 Korean commercial style."
    ),
    "soju-007": (
        "Dynamic Korean female entertainer mid-dance, energetically shaking a soju bottle. "
        "2006 Korean nightclub lighting — neon blues and pinks. High energy commercial photography. "
        "Motion blur on the shaking bottle, sharp focus on the performer's confident expression."
    ),
    "soju-008": (
        "Infographic-style product comparison: multiple soju bottles arranged in descending size order, "
        "ABV numbers (35, 23, 19.5, 17.8) floating above each. Clean white background, "
        "modern data visualization meets product photography. Minimalist Korean design."
    ),
    "soju-009": (
        "Young Korean female singer-actress with a natural, innocent smile, delicately holding a "
        "Chamisul soju glass. Dewy skin, soft natural lighting, spring garden background with cherry blossoms. "
        "Pure, aspirational K-star commercial photography. Full portrait."
    ),
    "soju-010": (
        "Split-screen composition: two Korean female celebrities facing each other in competing soju ads. "
        "Left side green tones (Chamisul), right side blue tones (Chum Churum). "
        "Convenience store poster battle aesthetic. Dramatic K-commercial rivalry photography."
    ),
    "soju-011": (
        "Retro revival product shot: vintage-style green soju bottle with a cute cartoon toad character. "
        "1970s Korean bar atmosphere recreated with modern polish. Nostalgic color grading, "
        "Instagram-worthy retro aesthetic. Neon sign reading '진로이즈백'."
    ),
    "soju-012": (
        "Futuristic soju product with a nine-tailed fox virtual character (anime style) hovering behind "
        "a sleek zero-sugar soju bottle. Vibrant orange and electric blue color palette. "
        "Gen-Z aesthetic, digital art meets product photography. MZ generation style."
    ),
    "soju-013": (
        "Battle scene: two soju bottles (classic green vs new zero-sugar) facing off on a dramatic "
        "dark background with lightning between them. Market share graphs overlaid. "
        "Competitive corporate drama photography. Bloomberg terminal aesthetic."
    ),
    "soju-014": (
        "Korean soju bottles displayed in international settings: New York Times Square, Tokyo Shibuya, "
        "Paris cafe, Bangkok night market. Collage-style global expansion visual. "
        "Cinematic, National Geographic documentary photography style."
    ),
    "soju-015": (
        "Futuristic holographic dashboard showing AI analytics of soju consumer data over 100 years. "
        "Glowing data points, neural network visualization. Korean tech-noir aesthetic. "
        "Blade Runner meets Korean corporate innovation."
    ),
    "soju-016": (
        "Epic timeline montage: 100 years of Korean soju bottles arranged chronologically from 1924 to 2026. "
        "Traditional → modern evolution. Background transitions from sepia to full color. "
        "Grand cinematic finale composition. Museum exhibition quality photography."
    ),
}

# ── News image prompts (one per event, matching the era's key headline) ──────

NEWS_PROMPTS: dict[str, str] = {
    "soju-001": (
        "1920s colonial Korea under Japanese occupation. Korean independence activists gathered "
        "in a secret meeting room. Historical documentary style, sepia photograph restoration. "
        "Atmosphere of resistance and national identity."
    ),
    "soju-002": (
        "1953 Korean War aftermath: devastated Seoul landscape with buildings in ruins. "
        "Hopeful reconstruction workers amid rubble. UN aid trucks in background. "
        "Black and white war documentary photography style."
    ),
    "soju-003": (
        "1970s Korean economic miracle: Saemaul Undong (New Village Movement) poster in background, "
        "construction workers building highways and factories. Industrial growth montage. "
        "Retro Korean propaganda poster aesthetic meets documentary photography."
    ),
    "soju-004": (
        "1997 IMF crisis in Korea: long lines outside banks, 'Gold Collection Campaign' posters. "
        "Citizens donating gold rings and necklaces for national debt repayment. "
        "Emotional photojournalism style, powerful national solidarity moment."
    ),
    "soju-005": (
        "2000 Inter-Korean Summit: two leaders shaking hands at Pyongyang airport. "
        "Korean flags and peace doves. Historic moment of Korean peninsula hope. "
        "Political news photography, warm emotional lighting."
    ),
    "soju-006": (
        "2006 World Cup in Germany: Korean fans in red 'Red Devil' t-shirts watching a match "
        "on a giant outdoor screen in Seoul plaza. Passionate crowd, mixed emotions. "
        "Sports photojournalism, vibrant red sea of supporters."
    ),
    "soju-007": (
        "2006 North Korean nuclear test announcement: news anchors on Korean TV delivering breaking news. "
        "Tense atmosphere, military imagery in background. Korean peninsula tension. "
        "News broadcast screenshot aesthetic, urgent journalism style."
    ),
    "soju-008": (
        "2012 PSY Gangnam Style phenomenon: horse-riding dance silhouette against a backdrop of "
        "YouTube view counter reaching billions. K-pop goes global moment. "
        "Pop culture explosion photography, dynamic and colorful."
    ),
    "soju-009": (
        "2014 Sewol Ferry disaster memorial: yellow ribbons tied everywhere — on fences, trees, bridges. "
        "A nation in mourning. Candlelight vigil with thousands of citizens. "
        "Solemn, emotional photojournalism. Respectful documentary style."
    ),
    "soju-010": (
        "2017 Candlelight Revolution in Gwanghwamun: millions of citizens holding candles in Seoul plaza. "
        "Peaceful democratic protest that led to presidential impeachment. "
        "Aerial night photography, sea of golden candlelights. Historic democracy moment."
    ),
    "soju-011": (
        "2019 No Japan boycott movement: Korean consumers removing Japanese products from shelves. "
        "Protest signs reading 'NO NO JAPAN'. Korean economic nationalism moment. "
        "Documentary photojournalism, social movement photography."
    ),
    "soju-012": (
        "2022 Russia-Ukraine war: news footage of conflict alongside global supply chain disruption "
        "visualizations. World map with trade route blockages. Inflation graphs rising. "
        "Geopolitical crisis documentary photography, somber tones."
    ),
    "soju-013": (
        "2023 ChatGPT and AI revolution: person interacting with holographic AI interface. "
        "Digital transformation of everyday life. Futuristic but accessible technology. "
        "Tech magazine cover photography style, blue and white tones."
    ),
    "soju-014": (
        "2024 Korean Wave global peak: K-drama scene on Netflix, BTS concert in stadium, "
        "Korean food in international restaurants. Global soft power montage. "
        "Dynamic editorial photography, cultural export celebration."
    ),
    "soju-015": (
        "2025 AI agents in everyday life: person using AI assistant on multiple screens, "
        "smart home environment. Korean tech-forward lifestyle. "
        "Modern lifestyle photography, warm futuristic tones."
    ),
    "soju-016": (
        "2026 vision: unified Korean cultural identity — traditional hanbok meets modern fashion, "
        "AI technology alongside nature. DMZ turning green with peace. "
        "Aspirational editorial photography, hopeful and grand."
    ),
}


async def generate_for_event(event_id: str, prompt: str, filename: str, dry_run: bool) -> bool:
    out_path = OUTPUT_DIR / event_id
    out_file = out_path / filename

    if out_file.exists():
        print(f"  [SKIP] {out_file.name} — already exists")
        return True

    print(f"  [GEN]  {out_file.name}")
    print(f"         {prompt[:80]}...")

    if dry_run:
        print(f"         (dry run)")
        return True

    try:
        images = await generate_image(
            prompt=prompt,
            output_path=None,
            aspect_ratio="16:9",
            number_of_images=1,
        )
        if images:
            out_path.mkdir(parents=True, exist_ok=True)
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
    parser = argparse.ArgumentParser(description="Generate Imagen 4 timeline images")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--event", type=str, help="Generate for specific event ID only")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    events = TIMELINE_EVENTS
    if args.event:
        events = [e for e in events if e.id == args.event]
        if not events:
            print(f"Event '{args.event}' not found.")
            sys.exit(1)

    print(f"Soju Timeline Image Generator (Imagen 4)")
    print(f"{'=' * 50}")
    print(f"Events: {len(events)}  |  Output: {OUTPUT_DIR}")
    if args.dry_run:
        print(f"Mode: DRY RUN")
    print()

    success = 0
    failed = 0

    for event in events:
        eid = event.id
        print(f"--- {eid}: {event.title_ko} ---")

        # Hero image
        hero_prompt = HERO_PROMPTS.get(eid, "")
        if hero_prompt:
            ok = await generate_for_event(eid, hero_prompt, "hero.png", args.dry_run)
            success += ok
            failed += (not ok)

        # News image
        news_prompt = NEWS_PROMPTS.get(eid, "")
        if news_prompt:
            ok = await generate_for_event(eid, news_prompt, "news.png", args.dry_run)
            success += ok
            failed += (not ok)

        print()

    print(f"Done: {success} success, {failed} failed")


if __name__ == "__main__":
    asyncio.run(main())
