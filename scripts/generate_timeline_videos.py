#!/usr/bin/env python3
"""Batch-generate Veo 3.1 videos for all timeline milestone events.

Usage:
    python scripts/generate_timeline_videos.py [--dry-run] [--event EVENT_ID]

Requires GOOGLE_API_KEY to be set.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.timeline.event_data import TIMELINE_EVENTS
from src.media.veo_client import generate_video

OUTPUT_DIR = Path(__file__).parent.parent / "generated_videos"


async def generate_for_event(event, dry_run: bool = False) -> bool:
    """Generate a video for a single timeline event."""
    output_path = OUTPUT_DIR / f"{event.id}.mp4"

    if output_path.exists():
        print(f"  [SKIP] {event.id} — already exists at {output_path}")
        return True

    print(f"  [GEN]  {event.id} — {event.title}")
    print(f"         Prompt: {event.video_prompt[:80]}...")

    if dry_run:
        print(f"         (dry run — skipping actual generation)")
        return True

    try:
        video_bytes = await generate_video(
            prompt=event.video_prompt,
            output_path=str(output_path),
            aspect_ratio="16:9",
            duration_seconds=8,
        )
        if video_bytes:
            print(f"         Saved to {output_path} ({len(video_bytes)} bytes)")
            return True
        else:
            print(f"         [FAIL] No video returned")
            return False
    except Exception as e:
        print(f"         [ERROR] {e}")
        return False


async def main():
    parser = argparse.ArgumentParser(description="Generate Veo 3.1 timeline videos")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without generating")
    parser.add_argument("--event", type=str, help="Generate for a specific event ID only")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    events = TIMELINE_EVENTS
    if args.event:
        events = [e for e in events if e.id == args.event]
        if not events:
            print(f"Event '{args.event}' not found.")
            sys.exit(1)

    print(f"K-Beauty Timeline Video Generator")
    print(f"{'=' * 50}")
    print(f"Events: {len(events)}  |  Output: {OUTPUT_DIR}")
    if args.dry_run:
        print(f"Mode: DRY RUN")
    print()

    success = 0
    failed = 0
    for event in events:
        ok = await generate_for_event(event, dry_run=args.dry_run)
        if ok:
            success += 1
        else:
            failed += 1

    print()
    print(f"Done: {success} success, {failed} failed, {len(events)} total")


if __name__ == "__main__":
    asyncio.run(main())
