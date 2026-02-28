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
        brand_namespace: Brand to check against (tirtir, anua, cosrx).
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
        brand_namespace: Brand to verify (tirtir, anua, cosrx).
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


check_brand_alignment_tool = FunctionTool(check_brand_alignment)
check_ingredient_accuracy_tool = FunctionTool(check_ingredient_accuracy)
