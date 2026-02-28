"""Trend analyzer tools — memory-powered trend functions."""

from __future__ import annotations

from google.adk.tools import FunctionTool

from src.memory.memory_system import BrandMemorySystem


def _get_memory() -> BrandMemorySystem:
    """Lazy singleton for memory system."""
    if not hasattr(_get_memory, "_instance"):
        _get_memory._instance = BrandMemorySystem()
    return _get_memory._instance


def search_brand_trends(brand_namespace: str, query: str) -> dict:
    """Search brand memory for trend-related information.

    Args:
        brand_namespace: Brand to search (tirtir, anua, cosrx).
        query: The trend or topic to search for.

    Returns:
        Dict with relevant trend notes and triplets.
    """
    memory = _get_memory()
    notes = memory.search(query, brand_namespace, k=5, category_filter="trend")
    triplets = memory.get_weighted_triplets(query, brand_namespace, k=10)

    return {
        "notes": [{"content": n.get("document", ""), "score": n.get("combined_score", 0)} for n in notes],
        "triplets": [{"fact": t.get("document", ""), "score": t.get("combined_score", 0)} for t in triplets],
    }


search_brand_trends_tool = FunctionTool(search_brand_trends)
