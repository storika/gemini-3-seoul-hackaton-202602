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
        content="Chamisul Original is the flagship soju with bamboo charcoal filtration",
        brand_namespace="chamisul",
        category="product",
        tags=["soju", "hero"],
        keywords=["chamisul", "soju", "bamboo"],
    )
    results = memory.search("bamboo charcoal soju", "chamisul", k=5)
    assert len(results) >= 1
    assert "chamisul" in results[0]["document"].lower()


def test_add_triplet_and_graph():
    memory = BrandMemorySystem()
    t = KGTriplet(
        subject="Chamisul",
        predicate="PRODUCES",
        object="Chamisul Original",
        brand_namespace="chamisul",
    )
    memory.add_triplet(t)
    assert memory.graph_store.triplet_count("chamisul") == 1
    assert memory.graph_store.entity_count("chamisul") == 2


def test_graph_expansion():
    memory = BrandMemorySystem()
    memory.add_triplet(KGTriplet(
        subject="Chamisul", predicate="PRODUCES", object="Chamisul Original",
        brand_namespace="chamisul",
    ))
    memory.add_triplet(KGTriplet(
        subject="Chamisul Original", predicate="CONTAINS_INGREDIENT", object="Bamboo Charcoal",
        brand_namespace="chamisul",
    ))
    expanded = memory.expand_with_graph("chamisul", ["Chamisul"], max_hops=2)
    objects = {t.object for t in expanded}
    assert "Bamboo Charcoal" in objects


def test_brand_namespace_isolation():
    memory = BrandMemorySystem()
    memory.add_note(
        content="Chamisul is the original Korean soju brand with 100 years of history",
        brand_namespace="chamisul",
        category="brand_identity",
    )
    memory.add_note(
        content="Chum Churum is a soft alkaline water soju brand",
        brand_namespace="chumchurum",
        category="brand_identity",
    )
    chamisul_results = memory.search("Korean soju brand", "chamisul", k=5)
    churum_results = memory.search("Korean soju brand", "chumchurum", k=5)

    # Each should find their own brand's note
    assert len(chamisul_results) >= 1
    assert len(churum_results) >= 1
    assert "chamisul" in chamisul_results[0]["document"].lower()
    assert "chum churum" in churum_results[0]["document"].lower()


def test_temporal_reranking():
    memory = BrandMemorySystem()
    now = datetime(2026, 2, 1)
    old = now - timedelta(days=200)

    # Add old note first (should rank lower)
    old_note = MemoryNote(
        content="Saero zero sugar soju is gaining popularity",
        brand_namespace="saero",
        category="product",
        created_at=old,
    )
    memory._notes_cache[old_note.id] = old_note
    memory.vector_store.add_note(old_note)

    # Add recent note
    new_note = MemoryNote(
        content="Saero zero sugar soju captured 10% market share in 2024",
        brand_namespace="saero",
        category="product",
        created_at=now,
    )
    memory._notes_cache[new_note.id] = new_note
    memory.vector_store.add_note(new_note)

    results = memory.search("zero sugar soju", "saero", k=2, now=now)
    assert len(results) == 2
    # Recent note should have higher combined score
    assert results[0]["combined_score"] >= results[1]["combined_score"]


def test_seeded_memory_search():
    memory = _build_seeded_memory()
    results = memory.search("bamboo charcoal soju filtration", "chamisul", k=3)
    assert len(results) >= 1


def test_seeded_memory_triplets():
    memory = _build_seeded_memory()
    results = memory.get_weighted_triplets("zero sugar soju", "saero", k=5)
    assert len(results) >= 1


def test_build_context_injection():
    memory = _build_seeded_memory()
    ctx = memory.build_context_injection("alkaline water soft soju", "chumchurum")
    assert len(ctx) > 0
    assert "No relevant memory found" not in ctx


def test_stats():
    memory = _build_seeded_memory()
    stats = memory.stats("chamisul")
    assert stats["graph_triplets"] > 0
    assert stats["graph_entities"] > 0
