"""Data schemas for the memory system — A-Mem style notes + Memoria KG triplets."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal
import uuid


BrandNamespace = Literal["chamisul", "chumchurum", "saero"]
NoteCategory = Literal["product", "marketing", "trend", "brand_identity", "ingredient", "competitive"]


def _new_id() -> str:
    return uuid.uuid4().hex[:12]


@dataclass
class MemoryNote:
    """A-Mem style atomic memory note."""

    content: str
    brand_namespace: BrandNamespace
    category: NoteCategory
    id: str = field(default_factory=_new_id)
    context: str = ""          # Gemini-generated contextual summary
    keywords: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    connections: list[str] = field(default_factory=list)  # related note IDs
    created_at: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    significance: float = 0.5  # 0.0 (fleeting) to 1.0 (foundational)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "brand_namespace": self.brand_namespace,
            "content": self.content,
            "context": self.context,
            "keywords": self.keywords,
            "tags": self.tags,
            "category": self.category,
            "connections": self.connections,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "significance": self.significance,
        }

    @classmethod
    def from_dict(cls, data: dict) -> MemoryNote:
        data = dict(data)
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class KGTriplet:
    """Memoria-style knowledge graph triplet."""

    subject: str
    predicate: str
    object: str
    brand_namespace: BrandNamespace
    id: str = field(default_factory=_new_id)
    attributes: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 1.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "brand_namespace": self.brand_namespace,
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "attributes": self.attributes,
            "created_at": self.created_at.isoformat(),
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: dict) -> KGTriplet:
        data = dict(data)
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)

    @property
    def text(self) -> str:
        """Human-readable representation for embedding."""
        attrs = ", ".join(f"{k}={v}" for k, v in self.attributes.items()) if self.attributes else ""
        base = f"{self.subject} → {self.predicate} → {self.object}"
        return f"{base} ({attrs})" if attrs else base


@dataclass
class SessionSummary:
    """Summary of a conversation session for context injection."""

    session_id: str = field(default_factory=_new_id)
    brand_namespace: BrandNamespace | None = None
    summary: str = ""
    key_decisions: list[str] = field(default_factory=list)
    topics_discussed: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "brand_namespace": self.brand_namespace,
            "summary": self.summary,
            "key_decisions": self.key_decisions,
            "topics_discussed": self.topics_discussed,
            "created_at": self.created_at.isoformat(),
        }
