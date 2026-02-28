"""Root agent tools — memory management and brand switching."""

from __future__ import annotations

from google.adk.tools import FunctionTool

from src.memory.memory_system import BrandMemorySystem
from src.memory.session_manager import SessionManager
from src.config import VALID_BRAND_NAMESPACES

# Shared instances
_memory: BrandMemorySystem | None = None
_session: SessionManager | None = None


def _get_memory() -> BrandMemorySystem:
    global _memory
    if _memory is None:
        _memory = BrandMemorySystem()
    return _memory


def _get_session() -> SessionManager:
    global _session
    if _session is None:
        _session = SessionManager()
    return _session


def set_memory_system(memory: BrandMemorySystem) -> None:
    """Allow external code to inject a pre-loaded memory system."""
    global _memory
    _memory = memory


def set_active_brand(brand_namespace: str) -> dict:
    """Set the active brand for the current session.

    Args:
        brand_namespace: The brand to activate (chamisul, chumchurum, saero).

    Returns:
        Confirmation with brand stats.
    """
    brand = brand_namespace.lower()
    if brand not in VALID_BRAND_NAMESPACES:
        return {"error": f"Invalid brand. Choose from: {', '.join(VALID_BRAND_NAMESPACES)}"}

    session = _get_session()
    session.active_brand = brand
    memory = _get_memory()
    stats = memory.stats(brand)

    return {
        "status": "active",
        "brand": brand,
        "stats": stats,
    }


def get_memory_context(query: str, brand_namespace: str = "") -> dict:
    """Retrieve relevant memory context for a query.

    Args:
        query: The search query.
        brand_namespace: Brand to search. If empty, uses active brand.

    Returns:
        Memory context with notes, triplets, and industry data.
    """
    session = _get_session()
    brand = brand_namespace.lower() if brand_namespace else (session.active_brand or "chamisul")

    if brand not in VALID_BRAND_NAMESPACES:
        return {"error": f"Invalid brand. Choose from: {', '.join(VALID_BRAND_NAMESPACES)}"}

    memory = _get_memory()
    context = memory.build_context_injection(query, brand)

    return {
        "brand": brand,
        "context": context,
    }


def save_to_memory(
    content: str,
    brand_namespace: str,
    category: str = "product",
    tags: str = "",
) -> dict:
    """Save new information to brand memory.

    Args:
        content: The information to store.
        brand_namespace: Brand namespace (chamisul, chumchurum, saero).
        category: Note category (product, marketing, trend, brand_identity, ingredient, competitive).
        tags: Comma-separated tags.

    Returns:
        Confirmation with note ID.
    """
    brand = brand_namespace.lower()
    if brand not in VALID_BRAND_NAMESPACES:
        return {"error": f"Invalid brand. Choose from: {', '.join(VALID_BRAND_NAMESPACES)}"}

    memory = _get_memory()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    note = memory.add_note(
        content=content,
        brand_namespace=brand,
        category=category,
        tags=tag_list,
    )

    return {
        "status": "saved",
        "note_id": note.id,
        "brand": brand,
        "category": category,
    }


def get_brand_stats(brand_namespace: str = "") -> dict:
    """Get memory statistics for a brand.

    Args:
        brand_namespace: Brand to check. If empty, returns all brands.

    Returns:
        Memory statistics per brand.
    """
    memory = _get_memory()

    if brand_namespace:
        brand = brand_namespace.lower()
        return {brand: memory.stats(brand)}

    return {brand: memory.stats(brand) for brand in VALID_BRAND_NAMESPACES}


set_active_brand_tool = FunctionTool(set_active_brand)
get_memory_context_tool = FunctionTool(get_memory_context)
save_to_memory_tool = FunctionTool(save_to_memory)
get_brand_stats_tool = FunctionTool(get_brand_stats)
