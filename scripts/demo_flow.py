#!/usr/bin/env python3
"""End-to-end demo script for K-Beauty Brand Agent.

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
    print("K-BEAUTY BRAND AGENT — E2E DEMO")
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
        "TIRTIR Mask Fit Red Cushion is the hero product with 40 shades globally, "
        "SPF 40, satin glow finish, #1 foundation on Amazon US and Japan",
        "tirtir", "product", tags=["cushion", "hero", "shade diversity"],
        keywords=["tirtir", "cushion", "foundation", "shades"],
    )
    memory.add_note(
        "ANUA Heartleaf 77% Soothing Toner is the #1 bestseller with 77% heartleaf concentration, "
        "28.6M+ TikTok views, Amazon #1 in Facial Toners",
        "anua", "product", tags=["toner", "hero", "heartleaf"],
        keywords=["anua", "toner", "heartleaf", "soothing"],
    )
    memory.add_note(
        "COSRX Advanced Snail 96 Mucin Power Essence — 96% snail mucin concentration, "
        "Amazon #1 Best Seller in Beauty, sales surged 90-1000% from 2023-2024",
        "cosrx", "product", tags=["essence", "hero", "snail mucin"],
        keywords=["cosrx", "snail", "mucin", "essence"],
    )

    print(f"  Loaded {len(triplets)} triplets, {len(brand_notes)} brand notes, {len(trend_notes)} trend notes")
    print(f"  Added 3 product-specific memory notes")

    for brand in ["tirtir", "anua", "cosrx"]:
        stats = memory.stats(brand)
        print(f"  {brand.upper()}: {stats['graph_entities']} entities, {stats['graph_triplets']} triplets")

    # ── Step 2: Brand Memory Search ────────────────────────────
    print("\n[2/6] Brand memory search with temporal decay...")

    queries = [
        ("tirtir", "cushion foundation shade diversity"),
        ("anua", "heartleaf toner sensitive skin"),
        ("cosrx", "snail mucin hydration essence"),
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

    print("\n  TIRTIR → neighbors of 'Mask Fit Red Cushion Foundation':")
    tirtir_neighbors = memory.graph_store.get_neighbors("tirtir", "Mask Fit Red Cushion Foundation", max_hops=1)
    for t in tirtir_neighbors[:5]:
        print(f"    {t.subject} → {t.predicate} → {t.object}")

    print("\n  COSRX → all predicates:")
    predicates = memory.graph_store.get_predicates("cosrx")
    print(f"    {predicates}")

    print("\n  ANUA → entities with HERO_INGREDIENT_OF:")
    anua_triplets = memory.graph_store.get_all_triplets("anua")
    hero = [t for t in anua_triplets if t.predicate == "HERO_INGREDIENT_OF"]
    for t in hero:
        print(f"    {t.subject} → {t.predicate} → {t.object}")

    # ── Step 4: Context Injection ──────────────────────────────
    print("\n[4/6] Building context injection for agents...")

    context = memory.build_context_injection("new product launch strategy for Gen Z", "tirtir")
    print(f"\n  Context length: {len(context)} chars")
    print(f"  Preview (first 300 chars):\n    {context[:300]}")

    # ── Step 5: Creative Brief ─────────────────────────────────
    print("\n[5/6] Generating creative brief...")

    brief = build_creative_brief(
        brand_name="TIRTIR",
        campaign_goal="Launch new matcha skincare line targeting Gen Z on TikTok",
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
        "TIRTIR", "Matcha Skin Toner",
        style="lifestyle flat lay photography",
        context="matcha powder, green tea leaves, morning skincare ritual",
    )
    print(f"\n  Imagen 4 prompt:\n    {img_prompt}")

    vid_prompt = build_product_video_prompt(
        "ANUA", "Heartleaf 77% Soothing Toner",
        style="ASMR product application",
        hero_ingredient="heartleaf extract",
    )
    print(f"\n  Veo 3.1 prompt:\n    {vid_prompt}")

    story_prompt = build_brand_story_prompt(
        "COSRX",
        "From a founder's sensitive skin struggle to the world's #1 snail mucin essence",
        mood="authentic and inspiring",
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
