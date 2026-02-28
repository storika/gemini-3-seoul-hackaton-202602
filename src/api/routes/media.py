"""Media generation API routes (Veo 3.1 video)."""

from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/media", tags=["media"])

VIDEO_OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "generated_videos"


class VideoRequest(BaseModel):
    event_id: str
    prompt: str
    aspect_ratio: str = "16:9"
    duration_seconds: int = 8


@router.post("/generate-video")
async def generate_video(req: VideoRequest):
    """Generate a video via Veo 3.1 for a timeline event.

    Returns the path to the generated video file.
    Requires GOOGLE_API_KEY to be set in the environment.
    """
    output_path = VIDEO_OUTPUT_DIR / f"{req.event_id}.mp4"

    if output_path.exists():
        return {"status": "cached", "path": str(output_path), "event_id": req.event_id}

    try:
        from src.media.veo_client import generate_video as veo_generate
        video_bytes = await veo_generate(
            prompt=req.prompt,
            output_path=str(output_path),
            aspect_ratio=req.aspect_ratio,
            duration_seconds=req.duration_seconds,
        )
        if video_bytes is None:
            raise HTTPException(status_code=502, detail="Veo generation returned no video")
        return {"status": "generated", "path": str(output_path), "event_id": req.event_id}
    except ImportError:
        raise HTTPException(status_code=501, detail="google-genai not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/video/{event_id}")
async def get_video_status(event_id: str):
    """Check if a generated video exists for the given event."""
    path = VIDEO_OUTPUT_DIR / f"{event_id}.mp4"
    if path.exists():
        return {"status": "available", "path": f"/videos/{event_id}.mp4"}
    return {"status": "not_found"}
