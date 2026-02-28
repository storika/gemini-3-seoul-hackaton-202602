#!/usr/bin/env python3
"""End-to-end demo script for Soju Brand Agent.

Demonstrates:
1. Seed data loading → KG + memory
2. Brand memory search with temporal decay
3. Cross-brand knowledge graph traversal
4. Context injection for agent prompts
5. Creative brief generation
6. Media prompt building (Imagen 4 / Veo 3.1)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.seed_loader import load_all
from src.memory.memory_system import BrandMemorySystem
from src.memory.session_manager import SessionManager
from src.agents.creative_director.tools import generate_image, generate_video, build_creative_brief
from src.media.imagen_client import build_product_image_prompt, build_lifestyle_image_prompt
from src.media.veo_client import build_product_video_prompt, build_brand_story_prompt


def main() -> None:
    print("=" * 60)
    print("SOJU BRAND AGENT — E2E DEMO")
    print("=" * 60)

    # ── Step 1: Seed Data ──────────────────────────────────────
    print("\n[1/6] Loading seed data...")
    triplets, brand_notes, trend_notes = load_all()
    memory = BrandMemorySystem()

    for t in triplets:
        memory.add_triplet(t)
    for note in brand_notes:
        memory.vector_store.add_note(note)
        memory._notes_cache[note.id] = note
    for note in trend_notes:
        memory.add_shared_note(note)

    # Add product-specific notes for richer search results
    memory.add_note(
        "Chamisul Original is the flagship soju with bamboo charcoal filtration, "
        "16.9% ABV, #1 soju brand in Korea for decades",
        "chamisul", "product", tags=["soju", "hero", "bamboo charcoal"],
        keywords=["chamisul", "soju", "bamboo", "original"],
    )
    memory.add_note(
        "Chum Churum is known for its soft taste using alkaline water, "
        "famous 'shake it' campaign with Lee Hyori, popular among younger drinkers",
        "chumchurum", "product", tags=["soju", "hero", "alkaline water"],
        keywords=["chumchurum", "soju", "alkaline", "soft"],
    )
    memory.add_note(
        "Saero is the zero-sugar soju pioneer with virtual character Saerogumi, "
        "targeting MZ generation, rapid market share growth since 2022 launch",
        "saero", "product", tags=["soju", "hero", "zero sugar"],
        keywords=["saero", "soju", "zero sugar", "MZ"],
    )

    print(f"  Loaded {len(triplets)} triplets, {len(brand_notes)} brand notes, {len(trend_notes)} trend notes")
    print(f"  Added 3 product-specific memory notes")

    for brand in ["chamisul", "chumchurum", "saero"]:
        stats = memory.stats(brand)
        print(f"  {brand.upper()}: {stats['graph_entities']} entities, {stats['graph_triplets']} triplets")

    # ── Step 2: Brand Memory Search ────────────────────────────
    print("\n[2/6] Brand memory search with temporal decay...")

    queries = [
        ("chamisul", "bamboo charcoal filtration original soju"),
        ("chumchurum", "alkaline water soft taste"),
        ("saero", "zero sugar soju MZ generation"),
    ]

    for brand, query in queries:
        print(f"\n  Q: [{brand.upper()}] {query}")
        results = memory.search(query, brand, k=3)
        for r in results:
            score = r.get("combined_score", 0)
            doc = r.get("document", "")[:80]
            print(f"    [{score:.3f}] {doc}")

    # ── Step 3: Knowledge Graph Traversal ──────────────────────
    print("\n[3/6] Knowledge graph traversal...")

    print("\n  Chamisul → neighbors of 'Chamisul Original':")
    chamisul_neighbors = memory.graph_store.get_neighbors("chamisul", "Chamisul Original", max_hops=1)
    for t in chamisul_neighbors[:5]:
        print(f"    {t.subject} → {t.predicate} → {t.object}")

    print("\n  Saero → all predicates:")
    predicates = memory.graph_store.get_predicates("saero")
    print(f"    {predicates}")

    print("\n  Chum Churum → entities with HIRED_MODEL:")
    churum_triplets = memory.graph_store.get_all_triplets("chumchurum")
    models = [t for t in churum_triplets if t.predicate == "HIRED_MODEL"]
    for t in models:
        print(f"    {t.subject} → {t.predicate} → {t.object}")

    # ── Step 4: Context Injection ──────────────────────────────
    print("\n[4/6] Building context injection for agents...")

    context = memory.build_context_injection("new zero-sugar soju launch strategy for MZ generation", "chamisul")
    print(f"\n  Context length: {len(context)} chars")
    print(f"  Preview (first 300 chars):\n    {context[:300]}")

    # ── Step 5: Creative Brief ─────────────────────────────────
    print("\n[5/6] Generating creative brief...")

    brief = build_creative_brief(
        brand_name="CHAMISUL",
        campaign_goal="Launch new premium soju targeting MZ generation on TikTok",
        target_platform="TikTok",
        content_type="product_launch",
    )
    print(f"  Brand: {brief['brand']}")
    print(f"  Platform: {brief['platform']}")
    print(f"  Guidelines: {brief['brand_guidelines']}")
    print(f"  Deliverables: {brief['deliverables']}")

    # ── Step 6: Media Prompts ──────────────────────────────────
    print("\n[6/6] Building media generation prompts...")

    img_prompt = build_product_image_prompt(
        "Chamisul", "Chamisul Original",
        style="lifestyle flat lay photography",
        context="bamboo charcoal, Korean drinking culture, evening social gathering",
    )
    print(f"\n  Imagen 4 prompt:\n    {img_prompt}")

    vid_prompt = build_product_video_prompt(
        "Chum Churum", "Chum Churum Original",
        style="cinematic product reveal",
        hero_ingredient="alkaline water",
    )
    print(f"\n  Veo 3.1 prompt:\n    {vid_prompt}")

    story_prompt = build_brand_story_prompt(
        "Saero",
        "From zero-sugar innovation to capturing the MZ generation with Saerogumi",
        mood="modern and energetic",
    )
    print(f"\n  Brand story prompt:\n    {story_prompt}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nTo run with live API (Gemini 3 + Imagen 4 + Veo 3.1):")
    print("  export GOOGLE_API_KEY=your-key-here")
    print("  adk run src/agents")


if __name__ == "__main__":
    main()
