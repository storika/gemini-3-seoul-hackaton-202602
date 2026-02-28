"""Parses seed_data_soju.json into KG triplets and memory notes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.config import SEED_DATA_PATH
from src.memory.schema import KGTriplet, MemoryNote, BrandNamespace

def load_seed_json(path: Path = SEED_DATA_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_triplets(data: dict) -> list[KGTriplet]:
    """Extract KG triplets for Soju brands."""
    triplets: list[KGTriplet] = []
    brands = data.get("brands", {})

    for brand_key, brand_data in brands.items():
        ns: BrandNamespace = brand_key  # type: ignore[assignment]
        brand_name = brand_data.get("identifiers", {}).get("name_en", brand_key.upper())

        # Parent company
        parent = brand_data.get("identifiers", {}).get("parent_company")
        if parent:
            triplets.append(KGTriplet(
                subject=brand_name, predicate="OWNED_BY", object=parent, brand_namespace=ns
            ))

        # Ambassador / Model History
        for model in brand_data.get("ambassador_history", []):
            model_name = model.get("name")
            if model_name:
                triplets.append(KGTriplet(
                    subject=brand_name, 
                    predicate="HIRED_MODEL", 
                    object=model_name, 
                    brand_namespace=ns,
                    attributes={"period": model.get("period", ""), "significance": model.get("significance", "")}
                ))

        # Historical Events
        for event in brand_data.get("historical_events", []):
            event_name = event.get("event")
            if event_name:
                triplets.append(KGTriplet(
                    subject=brand_name,
                    predicate="EXPERIENCED_EVENT",
                    object=event_name,
                    brand_namespace=ns,
                    attributes={"year": event.get("year", ""), "impact": event.get("sales_impact", "")}
                ))
        
        # Products
        for prod_key, prod_data in brand_data.get("products", {}).items():
            prod_name = prod_data.get("full_name", prod_key)
            triplets.append(KGTriplet(
                subject=brand_name, predicate="PRODUCES", object=prod_name, brand_namespace=ns,
                attributes={"abv": prod_data.get("abv", ""), "claim": prod_data.get("key_claim", "")}
            ))

    return triplets

def extract_memory_notes(data: dict) -> list[MemoryNote]:
    """Extract foundational notes and historical context."""
    notes: list[MemoryNote] = []
    brands = data.get("brands", {})

    for brand_key, brand_data in brands.items():
        ns: BrandNamespace = brand_key  # type: ignore[assignment]
        brand_name = brand_data.get("identifiers", {}).get("name_en", brand_key.upper())

        # Founding (High Significance = 1.0)
        founding = brand_data.get("founding", {})
        if founding:
            notes.append(MemoryNote(
                content=f"[{founding.get('year')}] {brand_name} origins: {founding.get('historical_origin')}",
                brand_namespace=ns,
                category="brand_identity",
                tags=["founding", "history"],
                keywords=[brand_name.lower(), "origin", "year"],
                significance=1.0  # Foundational truth
            ))

        # Philosophy (High Significance = 1.0)
        philosophy = brand_data.get("philosophy", {})
        if philosophy:
            notes.append(MemoryNote(
                content=f"{brand_name} mission: {philosophy.get('core_mission')}. Ethos: {philosophy.get('brand_ethos')}",
                brand_namespace=ns,
                category="brand_identity",
                tags=["philosophy", "ethos"],
                significance=1.0
            ))

        # Models (Medium Significance = 0.5)
        for model in brand_data.get("ambassador_history", []):
            notes.append(MemoryNote(
                content=f"{brand_name} model {model.get('name')} ({model.get('period')}): {model.get('significance')}",
                brand_namespace=ns,
                category="marketing",
                tags=["model", "ambassador", "marketing"],
                significance=0.6
            ))

        # Events (Medium Significance = 0.7)
        for event in brand_data.get("historical_events", []):
            notes.append(MemoryNote(
                content=f"Historical Event ({event.get('year')}): {event.get('event')} - {event.get('significance')} Impact: {event.get('sales_impact')}",
                brand_namespace=ns,
                category="history",
                tags=["event", "sales"],
                significance=0.7
            ))

    return notes

def extract_trend_notes(data: dict) -> list[MemoryNote]:
    """Extract shared industry trends."""
    notes: list[MemoryNote] = []
    trends = data.get("industry_context", {}).get("trends_over_time", {})
    
    for period, description in trends.items():
        notes.append(MemoryNote(
            content=f"Liquor Industry Trend ({period}): {description}",
            brand_namespace="chamisul", # shared
            category="trend",
            tags=["trend", "industry", "history"],
            significance=0.8
        ))
    return notes

def load_all(path: Path = SEED_DATA_PATH) -> tuple[list[KGTriplet], list[MemoryNote], list[MemoryNote]]:
    """Load everything: returns (triplets, brand_notes, trend_notes)."""
    data = load_seed_json(path)
    triplets = extract_triplets(data)
    brand_notes = extract_memory_notes(data)
    trend_notes = extract_trend_notes(data)
    return triplets, brand_notes, trend_notes
