"""Timeline API routes."""

from __future__ import annotations

from fastapi import APIRouter

from src.timeline.event_data import TIMELINE_EVENTS
from src.timeline.event_data_whisky import WHISKY_TIMELINE_EVENTS
from src.timeline.kg_snapshot import _serialize_event, compute_live_recommendation
from src.timeline.model_gallery import MODEL_GALLERY, serialize_model

router = APIRouter(prefix="/api/timeline", tags=["timeline"])

ALL_EVENTS = TIMELINE_EVENTS + WHISKY_TIMELINE_EVENTS

_WHISKY_PRODUCT_TYPES = {"scotch_whisky"}


@router.get("/events")
def list_events(brand: str | None = None, industry: str | None = None):
    """Return all timeline events, optionally filtered by brand and/or industry."""
    events = ALL_EVENTS
    if industry and industry != "all":
        events = [e for e in events if e.industry == industry]
    if brand and brand != "all":
        events = [e for e in events if e.brand == brand or e.brand == "multi"]
    return [_serialize_event(e) for e in events]


@router.get("/models")
def list_models(brand: str | None = None, product_type: str | None = None, industry: str | None = None):
    """Return model gallery entries, optionally filtered by brand, product_type, and/or industry."""
    models = MODEL_GALLERY
    if industry and industry != "all":
        if industry == "whisky":
            models = [m for m in models if m.product_type in _WHISKY_PRODUCT_TYPES]
        else:
            models = [m for m in models if m.product_type not in _WHISKY_PRODUCT_TYPES]
    if brand and brand != "all":
        models = [m for m in models if m.brand == brand]
    if product_type and product_type != "all":
        models = [m for m in models if m.product_type == product_type]
    return [serialize_model(m) for m in models]


@router.get("/range")
def timeline_range(industry: str | None = None):
    """Return the date range of available events."""
    events = ALL_EVENTS
    if industry and industry != "all":
        events = [e for e in events if e.industry == industry]
    dates = [e.date for e in events]
    return {
        "min_date": min(dates).isoformat(),
        "max_date": max(dates).isoformat(),
        "total_events": len(events),
        "brands": sorted({e.brand for e in events}),
    }


@router.get("/live-recommendation")
def live_recommendation(industry: str | None = None, brand: str | None = None):
    """Return composite ideal ambassador recommendation using temporal decay."""
    return compute_live_recommendation(
        industry_filter=industry,
        brand_filter=brand,
    )
