"""Timeline API routes."""

from __future__ import annotations

from fastapi import APIRouter

from src.timeline.event_data import TIMELINE_EVENTS
from src.timeline.kg_snapshot import _serialize_event
from src.timeline.model_gallery import MODEL_GALLERY, serialize_model

router = APIRouter(prefix="/api/timeline", tags=["timeline"])


@router.get("/events")
def list_events(brand: str | None = None):
    """Return all timeline events, optionally filtered by brand."""
    events = TIMELINE_EVENTS
    if brand and brand != "all":
        events = [e for e in events if e.brand == brand or e.brand == "multi"]
    return [_serialize_event(e) for e in events]


@router.get("/models")
def list_models(brand: str | None = None, product_type: str | None = None):
    """Return model gallery entries, optionally filtered by brand and/or product_type."""
    models = MODEL_GALLERY
    if brand and brand != "all":
        models = [m for m in models if m.brand == brand]
    if product_type and product_type != "all":
        models = [m for m in models if m.product_type == product_type]
    return [serialize_model(m) for m in models]


@router.get("/range")
def timeline_range():
    """Return the date range of available events."""
    dates = [e.date for e in TIMELINE_EVENTS]
    return {
        "min_date": min(dates).isoformat(),
        "max_date": max(dates).isoformat(),
        "total_events": len(TIMELINE_EVENTS),
        "brands": sorted({e.brand for e in TIMELINE_EVENTS}),
    }
