"""ChromaDB wrapper with per-brand namespace isolation."""

from __future__ import annotations

from typing import Any

import chromadb
from chromadb.config import Settings

from src.config import CHROMA_PERSIST_DIR
from .schema import MemoryNote, KGTriplet


class BrandVectorStore:
    """Manages ChromaDB collections with brand-level isolation.

    Each brand gets two collections:
      - {brand}_notes: MemoryNote embeddings
      - {brand}_triplets: KGTriplet text embeddings
    """

    def __init__(self, persist_dir: str = CHROMA_PERSIST_DIR) -> None:
        self._client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False,
            is_persistent=True,
        ))
        self._collections: dict[str, chromadb.Collection] = {}

    def _get_collection(self, name: str) -> chromadb.Collection:
        if name not in self._collections:
            self._collections[name] = self._client.get_or_create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collections[name]

    # ── Notes ──────────────────────────────────────────────────

    def add_note(self, note: MemoryNote) -> None:
        coll = self._get_collection(f"{note.brand_namespace}_notes")
        coll.upsert(
            ids=[note.id],
            documents=[note.content],
            metadatas=[{
                "category": note.category,
                "tags": ",".join(note.tags),
                "keywords": ",".join(note.keywords),
                "created_at": note.created_at.isoformat(),
                "brand_namespace": note.brand_namespace,
                "significance": note.significance,
            }],
        )

    def search_notes(
        self,
        brand_namespace: str,
        query: str,
        k: int = 10,
        category_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        coll = self._get_collection(f"{brand_namespace}_notes")
        where = {"category": category_filter} if category_filter else None
        results = coll.query(
            query_texts=[query],
            n_results=min(k, coll.count() or 1),
            where=where,
        )
        return self._unpack_results(results)

    # ── Triplets ───────────────────────────────────────────────

    def add_triplet(self, triplet: KGTriplet) -> None:
        coll = self._get_collection(f"{triplet.brand_namespace}_triplets")
        coll.upsert(
            ids=[triplet.id],
            documents=[triplet.text],
            metadatas=[{
                "subject": triplet.subject,
                "predicate": triplet.predicate,
                "object": triplet.object,
                "created_at": triplet.created_at.isoformat(),
                "confidence": triplet.confidence,
                "brand_namespace": triplet.brand_namespace,
            }],
        )

    def search_triplets(
        self,
        brand_namespace: str,
        query: str,
        k: int = 20,
    ) -> list[dict[str, Any]]:
        coll = self._get_collection(f"{brand_namespace}_triplets")
        if coll.count() == 0:
            return []
        results = coll.query(
            query_texts=[query],
            n_results=min(k, coll.count()),
        )
        return self._unpack_results(results)

    # ── Shared ─────────────────────────────────────────────────

    def add_shared_note(self, note: MemoryNote) -> None:
        """Add a note to the shared (cross-brand) collection."""
        coll = self._get_collection("shared_notes")
        coll.upsert(
            ids=[note.id],
            documents=[note.content],
            metadatas=[{
                "category": note.category,
                "tags": ",".join(note.tags),
                "keywords": ",".join(note.keywords),
                "created_at": note.created_at.isoformat(),
                "brand_namespace": "shared",
            }],
        )

    def search_shared_notes(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        coll = self._get_collection("shared_notes")
        if coll.count() == 0:
            return []
        results = coll.query(query_texts=[query], n_results=min(k, coll.count()))
        return self._unpack_results(results)

    # ── Utilities ──────────────────────────────────────────────

    @staticmethod
    def _unpack_results(results: dict) -> list[dict[str, Any]]:
        """Convert ChromaDB query results into a flat list of dicts."""
        items: list[dict[str, Any]] = []
        if not results or not results.get("ids"):
            return items
        for i, doc_id in enumerate(results["ids"][0]):
            item: dict[str, Any] = {"id": doc_id}
            if results.get("documents"):
                item["document"] = results["documents"][0][i]
            if results.get("metadatas"):
                item["metadata"] = results["metadatas"][0][i]
            if results.get("distances"):
                # ChromaDB cosine distance → similarity = 1 - distance
                item["similarity"] = 1.0 - results["distances"][0][i]
            items.append(item)
        return items

    def reset(self) -> None:
        """Delete all collections. Use only in tests."""
        for name in list(self._collections):
            self._client.delete_collection(name)
        self._collections.clear()
