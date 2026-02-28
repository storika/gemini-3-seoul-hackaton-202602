"""Session management — tracks conversation context and generates summaries."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .schema import SessionSummary, BrandNamespace


class SessionManager:
    """Manages conversation sessions and context injection."""

    def __init__(self) -> None:
        self._sessions: dict[str, SessionSummary] = {}
        self._active_session_id: str | None = None
        self._active_brand: BrandNamespace | None = None
        self._message_buffer: list[dict[str, str]] = []

    @property
    def active_brand(self) -> BrandNamespace | None:
        return self._active_brand

    @active_brand.setter
    def active_brand(self, brand: BrandNamespace | None) -> None:
        self._active_brand = brand

    def start_session(self, brand_namespace: BrandNamespace | None = None) -> str:
        """Start a new session, returns session_id."""
        session = SessionSummary(brand_namespace=brand_namespace)
        self._sessions[session.session_id] = session
        self._active_session_id = session.session_id
        self._active_brand = brand_namespace
        self._message_buffer = []
        return session.session_id

    def add_message(self, role: str, content: str) -> None:
        """Buffer a message in the current session."""
        self._message_buffer.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def get_current_session(self) -> SessionSummary | None:
        if self._active_session_id:
            return self._sessions.get(self._active_session_id)
        return None

    async def summarize_session(self) -> SessionSummary | None:
        """Summarize the current session using Gemini."""
        if not self._active_session_id or not self._message_buffer:
            return None

        from src.llm.gemini_client import generate_text

        messages_text = "\n".join(
            f"[{m['role']}]: {m['content']}" for m in self._message_buffer[-20:]
        )

        prompt = (
            "Summarize the following Korean liquor brand conversation. "
            "Extract: 1) A brief summary (2-3 sentences), "
            "2) Key decisions made, 3) Topics discussed.\n\n"
            "Format your response as:\n"
            "SUMMARY: <summary>\n"
            "DECISIONS: <comma-separated decisions>\n"
            "TOPICS: <comma-separated topics>\n\n"
            f"Conversation:\n{messages_text}"
        )

        result = await generate_text(prompt, temperature=0.3)

        session = self._sessions[self._active_session_id]
        for line in result.split("\n"):
            line = line.strip()
            if line.startswith("SUMMARY:"):
                session.summary = line[len("SUMMARY:"):].strip()
            elif line.startswith("DECISIONS:"):
                session.key_decisions = [
                    d.strip() for d in line[len("DECISIONS:"):].split(",") if d.strip()
                ]
            elif line.startswith("TOPICS:"):
                session.topics_discussed = [
                    t.strip() for t in line[len("TOPICS:"):].split(",") if t.strip()
                ]

        return session

    def get_session_context(self) -> str:
        """Build context from recent sessions for prompt injection."""
        recent = sorted(
            self._sessions.values(),
            key=lambda s: s.created_at,
            reverse=True,
        )[:3]

        if not recent:
            return ""

        parts = ["## Recent Session Context"]
        for s in recent:
            if s.summary:
                parts.append(f"- Session {s.session_id[:8]}: {s.summary}")
                if s.key_decisions:
                    parts.append(f"  Decisions: {', '.join(s.key_decisions)}")
        return "\n".join(parts)

    def end_session(self) -> str | None:
        """End the current session and return the session_id."""
        sid = self._active_session_id
        self._active_session_id = None
        self._message_buffer = []
        return sid
