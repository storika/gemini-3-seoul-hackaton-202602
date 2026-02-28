"""Tests for seed data loader — triplet and note extraction."""

from pathlib import Path

from src.data.seed_loader import load_seed_json, extract_triplets, extract_memory_notes, extract_trend_notes, load_all
from src.memory.schema import KGTriplet, MemoryNote
from src.config import SEED_DATA_PATH


def test_load_seed_json():
    data = load_seed_json(SEED_DATA_PATH)
    assert "brands" in data
    assert "tirtir" in data["brands"]
    assert "anua" in data["brands"]
    assert "cosrx" in data["brands"]


def test_extract_triplets_not_empty():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    assert len(triplets) > 0
    assert all(isinstance(t, KGTriplet) for t in triplets)


def test_triplets_contain_all_brands():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    namespaces = {t.brand_namespace for t in triplets}
    assert "tirtir" in namespaces
    assert "anua" in namespaces
    assert "cosrx" in namespaces


def test_triplets_have_key_predicates():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    predicates = {t.predicate for t in triplets}
    assert "PRODUCES" in predicates
    assert "CONTAINS_INGREDIENT" in predicates
    assert "SOLD_AT" in predicates
    assert "ACTIVE_IN_MARKET" in predicates
    assert "TARGETS_DEMOGRAPHIC" in predicates


def test_triplets_hero_ingredient():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    hero_triplets = [t for t in triplets if t.predicate == "HERO_INGREDIENT_OF"]
    assert len(hero_triplets) >= 2  # at least snail mucin + heartleaf


def test_triplets_endorsement():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    endorsements = [t for t in triplets if t.predicate == "ENDORSES"]
    assert len(endorsements) >= 1
    v_endorsement = [t for t in endorsements if "V" in t.subject]
    assert len(v_endorsement) == 1


def test_triplets_competition():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    competitions = [t for t in triplets if t.predicate == "COMPETES_WITH"]
    assert len(competitions) >= 2


def test_extract_memory_notes():
    data = load_seed_json(SEED_DATA_PATH)
    notes = extract_memory_notes(data)
    assert len(notes) > 0
    assert all(isinstance(n, MemoryNote) for n in notes)

    # Check brand coverage
    namespaces = {n.brand_namespace for n in notes}
    assert "tirtir" in namespaces
    assert "anua" in namespaces
    assert "cosrx" in namespaces


def test_memory_notes_have_categories():
    data = load_seed_json(SEED_DATA_PATH)
    notes = extract_memory_notes(data)
    categories = {n.category for n in notes}
    assert "brand_identity" in categories
    assert "marketing" in categories


def test_extract_trend_notes():
    data = load_seed_json(SEED_DATA_PATH)
    notes = extract_trend_notes(data)
    assert len(notes) > 0
    categories = {n.category for n in notes}
    assert "trend" in categories or "ingredient" in categories


def test_load_all():
    triplets, brand_notes, trend_notes = load_all(SEED_DATA_PATH)
    assert len(triplets) > 50  # expecting lots of relationships
    assert len(brand_notes) > 10
    assert len(trend_notes) > 5
