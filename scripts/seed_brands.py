#!/usr/bin/env python3
"""Load seed data into the memory system."""

import sys
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.seed_loader import load_all
from src.memory.memory_system import BrandMemorySystem


def main() -> None:
    print("Loading seed data...")
    triplets, brand_notes, trend_notes = load_all()

    print(f"  Triplets: {len(triplets)}")
    print(f"  Brand notes: {len(brand_notes)}")
    print(f"  Trend notes: {len(trend_notes)}")

    memory = BrandMemorySystem()

    # Load triplets
    print("\nLoading triplets into graph + vector store...")
    for t in triplets:
        memory.add_triplet(t)

    # Load brand notes
    print("Loading brand notes into vector store...")
    for note in brand_notes:
        memory.vector_store.add_note(note)
        memory._notes_cache[note.id] = note

    # Load trend notes as shared
    print("Loading trend notes into shared collection...")
    for note in trend_notes:
        memory.add_shared_note(note)

    # Print stats
    print("\n=== Memory Stats ===")
    for brand in ["tirtir", "anua", "cosrx"]:
        stats = memory.stats(brand)
        print(f"  {brand.upper()}: {stats}")

    # Quick test search
    print("\n=== Quick Search Test ===")
    results = memory.search("cushion foundation", "tirtir", k=3)
    for r in results:
        print(f"  [{r.get('combined_score', 0):.3f}] {r.get('document', '')[:80]}")

    print("\nSeed loading complete!")
    return memory


if __name__ == "__main__":
    main()
