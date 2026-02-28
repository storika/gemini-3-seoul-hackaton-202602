"""Tests for seed data loader — triplet and note extraction."""

from pathlib import Path

from src.data.seed_loader import load_seed_json, extract_triplets, extract_memory_notes, extract_trend_notes, load_all
from src.memory.schema import KGTriplet, MemoryNote
from src.config import SEED_DATA_PATH


def test_load_seed_json():
    data = load_seed_json(SEED_DATA_PATH)
    assert "brands" in data
    assert "chamisul" in data["brands"]
    assert "chumchurum" in data["brands"]
    assert "saero" in data["brands"]


def test_extract_triplets_not_empty():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    assert len(triplets) > 0
    assert all(isinstance(t, KGTriplet) for t in triplets)


def test_triplets_contain_all_brands():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    namespaces = {t.brand_namespace for t in triplets}
    assert "chamisul" in namespaces
    assert "chumchurum" in namespaces
    assert "saero" in namespaces


def test_triplets_have_key_predicates():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    predicates = {t.predicate for t in triplets}
    assert "PRODUCES" in predicates
    assert "OWNED_BY" in predicates
    assert "HIRED_MODEL" in predicates
    assert "EXPERIENCED_EVENT" in predicates


def test_triplets_hired_model():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    model_triplets = [t for t in triplets if t.predicate == "HIRED_MODEL"]
    assert len(model_triplets) >= 2  # multiple models across brands


def test_triplets_historical_events():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    event_triplets = [t for t in triplets if t.predicate == "EXPERIENCED_EVENT"]
    assert len(event_triplets) >= 1


def test_triplets_produces():
    data = load_seed_json(SEED_DATA_PATH)
    triplets = extract_triplets(data)
    products = [t for t in triplets if t.predicate == "PRODUCES"]
    assert len(products) >= 2


def test_extract_memory_notes():
    data = load_seed_json(SEED_DATA_PATH)
    notes = extract_memory_notes(data)
    assert len(notes) > 0
    assert all(isinstance(n, MemoryNote) for n in notes)

    # Check brand coverage
    namespaces = {n.brand_namespace for n in notes}
    assert "chamisul" in namespaces
    assert "chumchurum" in namespaces
    assert "saero" in namespaces


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
    assert len(triplets) > 10  # expecting relationships across 3 brands
    assert len(brand_notes) > 5
    assert len(trend_notes) > 2
