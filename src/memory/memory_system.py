"""BrandMemorySystem — A-Mem + Memoria hybrid memory layer.

Combines:
- Vector similarity search (ChromaDB)
- Knowledge graph neighbor expansion (NetworkX)
- Temporal decay re-ranking (EWA)
- LLM-powered enrichment (Gemini 3)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .schema import MemoryNote, KGTriplet, BrandNamespace
from .vector_store import BrandVectorStore
from .graph_store import BrandGraphStore
from .temporal_decay import compute_combined_score, compute_temporal_weight
from src.config import DEFAULT_SEARCH_K, DEFAULT_TRIPLET_K


class BrandMemorySystem:
    """Unified memory interface per brand namespace."""

    def __init__(
        self,
        vector_store: BrandVectorStore | None = None,
        graph_store: BrandGraphStore | None = None,
    ) -> None:
        self.vector_store = vector_store or BrandVectorStore()
        self.graph_store = graph_store or BrandGraphStore()
        self._notes_cache: dict[str, MemoryNote] = {}  # id → note

    # ── Write Operations ──────────────────────────────────────

    def add_note(
        self,
        content: str,
        brand_namespace: BrandNamespace,
        category: str,
        tags: list[str] | None = None,
        keywords: list[str] | None = None,
        context: str = "",
        connections: list[str] | None = None,
        significance: float = 0.5,
    ) -> MemoryNote:
        """Add a memory note (synchronous — no LLM enrichment)."""
        note = MemoryNote(
            content=content,
            brand_namespace=brand_namespace,
            category=category,
            tags=tags or [],
            keywords=keywords or [],
            context=context,
            connections=connections or [],
            significance=significance,
        )
        self._notes_cache[note.id] = note
        self.vector_store.add_note(note)
        return note

    async def add_note_enriched(
        self,
        content: str,
        brand_namespace: BrandNamespace,
        category: str,
        tags: list[str] | None = None,
    ) -> MemoryNote:
        """Add a note with Gemini-powered enrichment (keywords, context, connections)."""
        from src.llm.gemini_client import extract_keywords, generate_context, find_connections

        keywords = await extract_keywords(content)
        context = await generate_context(content, keywords)

        # Find connections among existing notes
        candidates = [
            {"id": n.id, "content": n.content}
            for n in self._notes_cache.values()
            if n.brand_namespace == brand_namespace
        ]
        connection_ids = await find_connections(content, candidates)

        note = MemoryNote(
            content=content,
            brand_namespace=brand_namespace,
            category=category,
            tags=tags or [],
            keywords=keywords,
            context=context,
            connections=connection_ids,
        )
        self._notes_cache[note.id] = note
        self.vector_store.add_note(note)
        return note

    def add_triplet(self, triplet: KGTriplet) -> None:
        """Add a KG triplet to both graph and vector stores."""
        self.graph_store.add_triplet(triplet)
        self.vector_store.add_triplet(triplet)

    def add_shared_note(self, note: MemoryNote) -> None:
        """Add a cross-brand note to the shared collection."""
        self._notes_cache[note.id] = note
        self.vector_store.add_shared_note(note)

    # ── Read Operations ───────────────────────────────────────

    def search(
        self,
        query: str,
        brand_namespace: BrandNamespace,
        k: int = DEFAULT_SEARCH_K,
        category_filter: str | None = None,
        now: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Search notes with vector similarity + temporal decay re-ranking."""
        raw_results = self.vector_store.search_notes(
            brand_namespace=brand_namespace,
            query=query,
            k=k * 2,  # fetch more for re-ranking
            category_filter=category_filter,
        )

        # Re-rank with temporal decay
        scored: list[dict[str, Any]] = []
        for item in raw_results:
            created_str = item.get("metadata", {}).get("created_at", "")
            try:
                created_at = datetime.fromisoformat(created_str) if created_str else datetime.utcnow()
            except ValueError:
                created_at = datetime.utcnow()

            similarity = item.get("similarity", 0.5)
            significance = item.get("metadata", {}).get("significance", 0.5)
            combined = compute_combined_score(similarity, created_at, now=now, significance=significance)
            item["combined_score"] = combined
            item["temporal_weight"] = compute_temporal_weight(created_at, now=now, significance=significance)
            scored.append(item)

        scored.sort(key=lambda x: x["combined_score"], reverse=True)

        # Update access counts
        for item in scored[:k]:
            note = self._notes_cache.get(item["id"])
            if note:
                note.access_count += 1

        return scored[:k]

    def get_weighted_triplets(
        self,
        query: str,
        brand_namespace: BrandNamespace,
        k: int = DEFAULT_TRIPLET_K,
        now: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Search KG triplets with EWA temporal weighting."""
        raw = self.vector_store.search_triplets(brand_namespace, query, k=k * 2)

        scored: list[dict[str, Any]] = []
        for item in raw:
            created_str = item.get("metadata", {}).get("created_at", "")
            try:
                created_at = datetime.fromisoformat(created_str) if created_str else datetime.utcnow()
            except ValueError:
                created_at = datetime.utcnow()

            similarity = item.get("similarity", 0.5)
            combined = compute_combined_score(similarity, created_at, now=now)
            item["combined_score"] = combined
            scored.append(item)

        scored.sort(key=lambda x: x["combined_score"], reverse=True)
        return scored[:k]

    def expand_with_graph(
        self,
        brand_namespace: BrandNamespace,
        entities: list[str],
        max_hops: int = 1,
    ) -> list[KGTriplet]:
        """Expand query results by traversing KG neighbors."""
        seen_ids: set[str] = set()
        results: list[KGTriplet] = []
        for entity in entities:
            neighbors = self.graph_store.get_neighbors(brand_namespace, entity, max_hops=max_hops)
            for t in neighbors:
                if t.id not in seen_ids:
                    seen_ids.add(t.id)
                    results.append(t)
        return results

    def build_context_injection(
        self,
        query: str,
        brand_namespace: BrandNamespace,
        now: datetime | None = None,
    ) -> str:
        """Build a memory context string for agent prompt injection."""
        # 1. Search notes
        notes = self.search(query, brand_namespace, k=5, now=now)

        # 2. Search triplets
        triplets = self.get_weighted_triplets(query, brand_namespace, k=10, now=now)

        # 3. Extract entities from top triplets for graph expansion
        entities = set()
        for t in triplets[:5]:
            meta = t.get("metadata", {})
            if meta.get("subject"):
                entities.add(meta["subject"])
            if meta.get("object"):
                entities.add(meta["object"])

        # 4. Graph expansion
        expanded = self.expand_with_graph(brand_namespace, list(entities), max_hops=1)

        # 5. Also search shared notes
        shared = self.vector_store.search_shared_notes(query, k=3)

        # Build context string
        parts: list[str] = []

        if notes:
            parts.append("## Brand Memory Notes")
            for n in notes:
                score = n.get("combined_score", 0)
                parts.append(f"- [{score:.2f}] {n.get('document', '')}")

        if triplets:
            parts.append("\n## Knowledge Graph Facts")
            for t in triplets[:10]:
                parts.append(f"- {t.get('document', '')}")

        if expanded:
            parts.append("\n## Related Knowledge (Graph Expansion)")
            for t in expanded[:5]:
                parts.append(f"- {t.text}")

        if shared:
            parts.append("\n## Industry Context")
            for s in shared:
                parts.append(f"- {s.get('document', '')}")

        return "\n".join(parts) if parts else "No relevant memory found."

    # ── Stats ─────────────────────────────────────────────────

    def stats(self, brand_namespace: BrandNamespace) -> dict[str, int]:
        return {
            "notes_cached": sum(
                1 for n in self._notes_cache.values()
                if n.brand_namespace == brand_namespace
            ),
            "graph_entities": self.graph_store.entity_count(brand_namespace),
            "graph_triplets": self.graph_store.triplet_count(brand_namespace),
        }

    async def consolidate_memories(self, brand_namespace: BrandNamespace, category: str) -> MemoryNote | None:
        """Find redundant notes in a category and consolidate them into a single high-weight note."""
        from src.llm.gemini_client import summarize_memories

        # 1. Fetch all notes for this brand/category
        notes = [
            n for n in self._notes_cache.values()
            if n.brand_namespace == brand_namespace and n.category == category
        ]

        if len(notes) < 3:
            return None

        # 2. Use Gemini to create a consolidated summary
        note_texts = [n.content for n in notes]
        summary_content = await summarize_memories(brand_namespace, category, note_texts)

        # 3. Add the new consolidated note
        consolidated_note = await self.add_note_enriched(
            content=f"[CONSOLIDATED] {summary_content}",
            brand_namespace=brand_namespace,
            category=category,
            tags=["consolidated", "core_knowledge"],
        )

        return consolidated_note
