"""Tests for brand guard tools — memory-backed verification."""

from src.agents.brand_guard.tools import check_brand_alignment, check_ingredient_accuracy
from src.memory.memory_system import BrandMemorySystem
from src.memory.schema import KGTriplet, MemoryNote
from src.data.seed_loader import load_all
from src.config import SEED_DATA_PATH

import src.agents.brand_guard.tools as guard_tools


def _seed_memory() -> BrandMemorySystem:
    triplets, brand_notes, trend_notes = load_all(SEED_DATA_PATH)
    memory = BrandMemorySystem()
    for t in triplets:
        memory.add_triplet(t)
    for note in brand_notes:
        memory.vector_store.add_note(note)
        memory._notes_cache[note.id] = note
    for note in trend_notes:
        memory.add_shared_note(note)
    # Inject into guard tools module
    guard_tools._get_memory._instance = memory
    return memory


def test_check_brand_alignment_returns_identity():
    _seed_memory()
    result = check_brand_alignment("chamisul", "Clean bamboo charcoal soju with pure taste")
    assert "brand_identity" in result
    assert len(result["brand_identity"]) > 0
    assert result["brand_namespace"] == "chamisul"


def test_check_brand_alignment_chumchurum():
    _seed_memory()
    result = check_brand_alignment("chumchurum", "Soft alkaline water soju for smooth drinking")
    assert "brand_identity" in result
    assert len(result["brand_identity"]) > 0


def test_check_ingredient_accuracy():
    _seed_memory()
    result = check_ingredient_accuracy(
        "saero",
        "Saero Zero Sugar",
        "Zero sugar, purified water, rice",
    )
    assert "claimed_ingredients" in result
    assert len(result["claimed_ingredients"]) == 3
    assert "vector_search_results" in result


def test_check_ingredient_accuracy_chamisul():
    _seed_memory()
    result = check_ingredient_accuracy(
        "chamisul",
        "Chamisul Original",
        "Bamboo charcoal, purified water, rice",
    )
    assert "Bamboo charcoal" in result["claimed_ingredients"]
