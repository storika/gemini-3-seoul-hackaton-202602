"""Knowledge Graph snapshot API routes."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Query

from src.timeline.kg_snapshot import build_kg_snapshot, TIMELINE_ALPHA

router = APIRouter(prefix="/api/kg", tags=["kg"])


@router.get("/snapshot")
def kg_snapshot(
    date: str = Query(..., description="ISO date string, e.g. 2023-06-15"),
    brand: str = Query("all", description="Brand filter: chamisul, chumchurum, saero, or all"),
    alpha: float = Query(TIMELINE_ALPHA, description="Temporal decay alpha"),
    include_fol: bool = Query(False, description="Include FOL evidence layer"),
):
    """Return a KG snapshot at the given date."""
    target = datetime.fromisoformat(date)
    brand_filter = brand if brand != "all" else None
    return build_kg_snapshot(target, brand_filter=brand_filter, alpha=alpha, include_fol=include_fol)
