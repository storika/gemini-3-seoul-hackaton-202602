"""Tests for the integrated BrandMemorySystem."""

from datetime import datetime, timedelta

from src.memory.memory_system import BrandMemorySystem
from src.memory.schema import KGTriplet, MemoryNote
from src.data.seed_loader import load_all
from src.config import SEED_DATA_PATH


def _build_seeded_memory() -> BrandMemorySystem:
    """Helper: create a memory system loaded with seed data."""
    triplets, brand_notes, trend_notes = load_all(SEED_DATA_PATH)
    memory = BrandMemorySystem()

    for t in triplets:
        memory.add_triplet(t)
    for note in brand_notes:
        memory.vector_store.add_note(note)
        memory._notes_cache[note.id] = note
    for note in trend_notes:
        memory.add_shared_note(note)

    return memory


def test_add_note_and_search():
    memory = BrandMemorySystem()
    memory.add_note(
        content="TIRTIR Mask Fit Red Cushion is the hero product with 40 shades globally",
        brand_namespace="tirtir",
        category="product",
        tags=["cushion", "hero"],
        keywords=["tirtir", "cushion", "foundation"],
    )
    results = memory.search("cushion foundation", "tirtir", k=5)
    assert len(results) >= 1
    assert "cushion" in results[0]["document"].lower()


def test_add_triplet_and_graph():
    memory = BrandMemorySystem()
    t = KGTriplet(
        subject="TIRTIR",
        predicate="PRODUCES",
        object="Mask Fit Red Cushion",
        brand_namespace="tirtir",
    )
    memory.add_triplet(t)
    assert memory.graph_store.triplet_count("tirtir") == 1
    assert memory.graph_store.entity_count("tirtir") == 2


def test_graph_expansion():
    memory = BrandMemorySystem()
    memory.add_triplet(KGTriplet(
        subject="TIRTIR", predicate="PRODUCES", object="Mask Fit Red Cushion",
        brand_namespace="tirtir",
    ))
    memory.add_triplet(KGTriplet(
        subject="Mask Fit Red Cushion", predicate="CONTAINS_INGREDIENT", object="Hyaluronic acid",
        brand_namespace="tirtir",
    ))
    expanded = memory.expand_with_graph("tirtir", ["TIRTIR"], max_hops=2)
    objects = {t.object for t in expanded}
    assert "Hyaluronic acid" in objects


def test_brand_namespace_isolation():
    memory = BrandMemorySystem()
    memory.add_note(
        content="TIRTIR is a K-beauty cushion brand",
        brand_namespace="tirtir",
        category="brand_identity",
    )
    memory.add_note(
        content="ANUA is a heartleaf-focused skincare brand",
        brand_namespace="anua",
        category="brand_identity",
    )
    tirtir_results = memory.search("K-beauty brand", "tirtir", k=5)
    anua_results = memory.search("K-beauty brand", "anua", k=5)

    # Each should find their own brand's note
    assert len(tirtir_results) >= 1
    assert len(anua_results) >= 1
    assert "tirtir" in tirtir_results[0]["document"].lower()
    assert "anua" in anua_results[0]["document"].lower()


def test_temporal_reranking():
    memory = BrandMemorySystem()
    now = datetime(2026, 2, 1)
    old = now - timedelta(days=200)

    # Add old note first (should rank lower)
    old_note = MemoryNote(
        content="COSRX snail mucin essence is popular",
        brand_namespace="cosrx",
        category="product",
        created_at=old,
    )
    memory._notes_cache[old_note.id] = old_note
    memory.vector_store.add_note(old_note)

    # Add recent note
    new_note = MemoryNote(
        content="COSRX snail mucin saw 90-1000% sales surge in 2024",
        brand_namespace="cosrx",
        category="product",
        created_at=now,
    )
    memory._notes_cache[new_note.id] = new_note
    memory.vector_store.add_note(new_note)

    results = memory.search("snail mucin", "cosrx", k=2, now=now)
    assert len(results) == 2
    # Recent note should have higher combined score
    assert results[0]["combined_score"] >= results[1]["combined_score"]


def test_seeded_memory_search():
    memory = _build_seeded_memory()
    results = memory.search("cushion foundation shade diversity", "tirtir", k=3)
    assert len(results) >= 1


def test_seeded_memory_triplets():
    memory = _build_seeded_memory()
    results = memory.get_weighted_triplets("snail mucin essence", "cosrx", k=5)
    assert len(results) >= 1


def test_build_context_injection():
    memory = _build_seeded_memory()
    ctx = memory.build_context_injection("heartleaf toner skincare", "anua")
    assert len(ctx) > 0
    assert "No relevant memory found" not in ctx


def test_stats():
    memory = _build_seeded_memory()
    stats = memory.stats("tirtir")
    assert stats["graph_triplets"] > 0
    assert stats["graph_entities"] > 0
