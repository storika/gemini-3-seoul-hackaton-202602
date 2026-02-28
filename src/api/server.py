"""FastAPI application for Soju Wars: 100-Year Brand Evolution Timeline."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes import timeline, kg, media

app = FastAPI(
    title="Soju Wars: 100-Year Brand Evolution",
    version="1.0.0",
    description="Timeline-based visualization of Korean soju brand wars + influencer evolution (1924-2026)",
)

# CORS — allow local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(timeline.router)
app.include_router(kg.router)
app.include_router(media.router)

# Generated videos directory (must mount before "/" catch-all)
_video_dir = Path(__file__).parent.parent.parent / "generated_videos"
_video_dir.mkdir(exist_ok=True)
app.mount("/videos", StaticFiles(directory=str(_video_dir)), name="videos")

# Generated images directory
_img_dir = Path(__file__).parent.parent.parent / "generated_images"
_img_dir.mkdir(exist_ok=True)
app.mount("/images", StaticFiles(directory=str(_img_dir)), name="images")

# Static files — legacy Vanilla JS SPA (disabled when using Next.js frontend)
# To re-enable: set SERVE_LEGACY_SPA=1
import os as _os
_web_dir = Path(__file__).parent.parent / "web"
if _web_dir.is_dir() and _os.getenv("SERVE_LEGACY_SPA"):
    app.mount("/", StaticFiles(directory=str(_web_dir), html=True), name="static")
