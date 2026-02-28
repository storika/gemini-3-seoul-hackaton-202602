"""Brand Guard tools — memory-backed verification functions."""

from __future__ import annotations

from google.adk.tools import FunctionTool

from src.memory.memory_system import BrandMemorySystem


def _get_memory() -> BrandMemorySystem:
    if not hasattr(_get_memory, "_instance"):
        _get_memory._instance = BrandMemorySystem()
    return _get_memory._instance


def check_brand_alignment(brand_namespace: str, content: str) -> dict:
    """Check if content aligns with brand identity and values.

    Args:
        brand_namespace: Brand to check against (chamisul, chumchurum, saero).
        content: The content to evaluate for brand alignment.

    Returns:
        Dict with brand identity notes and alignment assessment context.
    """
    memory = _get_memory()

    # Search for brand identity information
    identity_notes = memory.search(
        f"{brand_namespace} brand identity ethos values",
        brand_namespace,
        k=5,
        category_filter="brand_identity",
    )

    # Search for relevant marketing guidelines
    marketing_notes = memory.search(
        content,
        brand_namespace,
        k=3,
        category_filter="marketing",
    )

    return {
        "brand_identity": [
            {"content": n.get("document", ""), "score": n.get("combined_score", 0)}
            for n in identity_notes
        ],
        "marketing_guidelines": [
            {"content": n.get("document", ""), "score": n.get("combined_score", 0)}
            for n in marketing_notes
        ],
        "brand_namespace": brand_namespace,
    }


def check_ingredient_accuracy(brand_namespace: str, product_name: str, claimed_ingredients: str) -> dict:
    """Verify ingredient claims against the knowledge graph.

    Args:
        brand_namespace: Brand to verify (chamisul, chumchurum, saero).
        product_name: Name of the product being checked.
        claimed_ingredients: Comma-separated list of claimed ingredients.

    Returns:
        Dict with verified facts and any discrepancies found.
    """
    memory = _get_memory()

    # Search KG for product ingredient facts
    triplets = memory.get_weighted_triplets(
        f"{product_name} ingredients",
        brand_namespace,
        k=15,
    )

    # Also check graph relationships directly
    graph_triplets = memory.graph_store.get_neighbors(brand_namespace, product_name, max_hops=1)
    ingredient_facts = [
        t for t in graph_triplets
        if t.predicate in ("CONTAINS_INGREDIENT", "HERO_INGREDIENT_OF")
    ]

    return {
        "known_ingredients": [
            {"subject": t.subject, "predicate": t.predicate, "object": t.object}
            for t in ingredient_facts
        ],
        "vector_search_results": [
            {"fact": t.get("document", ""), "score": t.get("combined_score", 0)}
            for t in triplets[:10]
        ],
        "claimed_ingredients": [i.strip() for i in claimed_ingredients.split(",")],
    }


def verify_creator_brand_fit(brand_namespace: str, creator_data: dict) -> dict:
    """Strictly verify creator-brand fit using a composite score and risk check.

    Args:
        brand_namespace: Brand to check (chamisul, chumchurum, saero).
        creator_data: Full creator metadata from vectorized_clickhouse_samples.json.

    Returns:
        Dict with PASSED/FAILED status, Final Score, and detailed breakdown.
    """
    affinity_matrix = creator_data.get("brand_fit_logic", {}).get("soju_affinity_matrix", {})
    visual_archetype = creator_data.get("visual_persona_deep", {}).get("beauty_archetype", {})
    risk_mgmt = creator_data.get("risk_management", {})

    # 1. Affinity (0.4)
    affinity_map = {
        "chamisul": affinity_matrix.get("chamisul_clean_index", 0),
        "chumchurum": affinity_matrix.get("chumchurum_soft_index", 0),
        "saero": affinity_matrix.get("saero_zero_hip_index", 0),
        "jinro": affinity_matrix.get("jinro_retro_index", 0),
    }
    affinity_score = affinity_map.get(brand_namespace, 0)

    # 2. Visual Consistency (0.3)
    # Define primary archetypes for each brand
    visual_map = {
        "chamisul": (visual_archetype.get("pure_innocent", 0) + visual_archetype.get("healthy_vitality", 0)) / 2,
        "chumchurum": (visual_archetype.get("lovely_juicy", 0) + visual_archetype.get("moody_cinematic", 0)) / 2,
        "saero": (visual_archetype.get("hip_crush", 0) + visual_archetype.get("quirky_individualistic", 0)) / 2,
        "jinro": (visual_archetype.get("vintage_analog", 0) + visual_archetype.get("elegant_classic", 0)) / 2,
    }
    visual_consistency_score = visual_map.get(brand_namespace, 0)

    # 3. Risk Score (0.3) - Safety high, Overlap low
    brand_safety = risk_mgmt.get("brand_safety_score", 0)
    competitor_overlap = risk_mgmt.get("competitor_overlap_index", 0)
    risk_score = (brand_safety + (1.0 - competitor_overlap)) / 2

    # Final Composite Score
    final_score = (affinity_score * 0.4) + (visual_consistency_score * 0.3) + (risk_score * 0.3)

    # Critical Failure Checks
    passed = final_score >= 0.7
    reason = "Meets strict brand-creator correlation threshold."

    if final_score < 0.7:
        reason = f"Final Score {final_score:.2f} is below strict threshold (0.70)."
    if competitor_overlap > 0.6:
        passed = False
        reason = f"Critical Risk: Competitor overlap ({competitor_overlap}) is too high."
    if brand_safety < 0.8:
        passed = False
        reason = f"Critical Risk: Brand safety score ({brand_safety}) is below 0.8."

    return {
        "creator_id": creator_data.get("creator_id", "unknown"),
        "brand_namespace": brand_namespace,
        "passed": passed,
        "final_score": round(final_score, 3),
        "breakdown": {
            "affinity": round(affinity_score, 3),
            "visual_consistency": round(visual_consistency_score, 3),
            "risk_score": round(risk_score, 3)
        },
        "reason": reason
    }


check_brand_alignment_tool = FunctionTool(check_brand_alignment)
check_ingredient_accuracy_tool = FunctionTool(check_ingredient_accuracy)
verify_creator_brand_fit_tool = FunctionTool(verify_creator_brand_fit)
