"""Build a KG snapshot at a given point in time.

Applies timeline events up to a target date onto a NetworkX DiGraph,
then annotates every node/edge with its temporal weight using
the existing compute_temporal_weight() from src.memory.temporal_decay.
"""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime
from typing import Any

import networkx as nx

from src.memory.temporal_decay import compute_temporal_weight
from .event_data import TIMELINE_EVENTS
from .event_data_whisky import WHISKY_TIMELINE_EVENTS
from .events import TimelineEvent, KGMutation
from .fol_evidence import FOL_EVIDENCE
from .model_gallery import MODEL_GALLERY, SojuModel

ALL_EVENTS = TIMELINE_EVENTS + WHISKY_TIMELINE_EVENTS

# Timeline-specific alpha: half-life ≈ 2310 days (~6.3 years).
# Much gentler than the memory alpha (0.02) since we span 100+ years (1924-2026).
TIMELINE_ALPHA = 0.0003


def _apply_mutation(G: nx.DiGraph, mut: KGMutation, event: TimelineEvent) -> None:
    """Apply a single KG mutation to the graph."""
    if mut.action == "add_node" and mut.node_id:
        G.add_node(
            mut.node_id,
            label=mut.label,
            node_type=mut.node_type,
            brand=mut.brand or event.brand,
            added_date=event.date.isoformat(),
            event_id=event.id,
        )
    elif mut.action == "add_edge" and mut.source and mut.target:
        # Ensure source/target nodes exist (defensive)
        for nid in (mut.source, mut.target):
            if nid not in G:
                G.add_node(nid, label=nid, node_type="unknown", brand=event.brand,
                           added_date=event.date.isoformat(), event_id=event.id)
        G.add_edge(
            mut.source,
            mut.target,
            relation=mut.relation,
            brand=event.brand,
            added_date=event.date.isoformat(),
            event_id=event.id,
        )


def build_kg_snapshot(
    target_date: datetime,
    brand_filter: str | None = None,
    alpha: float = TIMELINE_ALPHA,
    include_fol: bool = False,
    industry_filter: str | None = None,
) -> dict[str, Any]:
    """Build a KG snapshot at *target_date*.

    Args:
        target_date: The point in time to compute the snapshot for.
        brand_filter: If set, only include events for this brand (+ "multi").
        alpha: Temporal decay rate for weight computation.
        include_fol: If True, include FOL evidence layer nodes/edges.

    Returns:
        {
            "nodes": [...],
            "edges": [...],
            "fol_nodes": [...] (if include_fol),
            "fol_edges": [...] (if include_fol),
            "stats": {...},
            "current_event": {...} | None
        }
    """
    G = nx.DiGraph()
    active_events: list[TimelineEvent] = []
    active_event_ids: set[str] = set()

    for event in ALL_EVENTS:
        if event.date > target_date:
            continue
        if industry_filter and industry_filter != "all" and event.industry != industry_filter:
            continue
        if brand_filter and brand_filter != "all" and event.brand != brand_filter and event.brand != "multi":
            continue
        active_events.append(event)
        active_event_ids.add(event.id)
        for mut in event.kg_mutations:
            _apply_mutation(G, mut, event)

    # Annotate temporal weights
    nodes_out: list[dict[str, Any]] = []
    for nid, data in G.nodes(data=True):
        added = datetime.fromisoformat(data["added_date"])
        tw = compute_temporal_weight(added, now=target_date, alpha=alpha)
        nodes_out.append({
            "id": nid,
            "label": data.get("label", nid),
            "type": data.get("node_type", "unknown"),
            "brand": data.get("brand", ""),
            "temporal_weight": round(tw, 4),
            "added_date": data["added_date"],
            "event_id": data.get("event_id", ""),
        })

    edges_out: list[dict[str, Any]] = []
    for src, tgt, data in G.edges(data=True):
        added = datetime.fromisoformat(data["added_date"])
        tw = compute_temporal_weight(added, now=target_date, alpha=alpha)
        edges_out.append({
            "source": src,
            "target": tgt,
            "relation": data.get("relation", ""),
            "brand": data.get("brand", ""),
            "temporal_weight": round(tw, 4),
            "added_date": data["added_date"],
            "event_id": data.get("event_id", ""),
        })

    brands_present = {n["brand"] for n in nodes_out if n["brand"]}
    current_event = active_events[-1] if active_events else None

    result: dict[str, Any] = {
        "nodes": nodes_out,
        "edges": edges_out,
        "stats": {
            "total_nodes": len(nodes_out),
            "total_edges": len(edges_out),
            "active_events": len(active_events),
            "brands": sorted(brands_present),
        },
        "current_event": _serialize_event(current_event) if current_event else None,
    }

    # FOL evidence layer
    if include_fol:
        fol_nodes, fol_edges = _build_fol_layer(
            active_event_ids, target_date, brand_filter, alpha
        )
        result["fol_nodes"] = fol_nodes
        result["fol_edges"] = fol_edges

    return result


def _build_fol_layer(
    active_event_ids: set[str],
    target_date: datetime,
    brand_filter: str | None,
    alpha: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Build FOL evidence nodes/edges for active events."""
    fol_nodes: list[dict[str, Any]] = []
    fol_edges: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    # Find event dates for temporal weight computation
    event_dates: dict[str, datetime] = {}
    for evt in ALL_EVENTS:
        event_dates[evt.id] = evt.date

    for fol in FOL_EVIDENCE:
        if fol.event_id not in active_event_ids:
            continue
        if brand_filter and brand_filter != "all" and fol.brand != brand_filter and fol.brand != "multi":
            continue

        evt_date = event_dates.get(fol.event_id, target_date)
        tw = compute_temporal_weight(evt_date, now=target_date, alpha=alpha)

        for node in fol.nodes:
            if node.id not in seen_ids:
                seen_ids.add(node.id)
                fol_nodes.append({
                    "id": node.id,
                    "label": node.label,
                    "label_ko": node.label_ko,
                    "type": node.node_type,
                    "brand": node.brand,
                    "temporal_weight": round(tw, 4),
                    "event_id": node.event_id,
                    "layer": "fol",
                })

        for edge in fol.edges:
            fol_edges.append({
                "source": edge.source,
                "target": edge.target,
                "relation": edge.relation,
                "brand": edge.brand,
                "temporal_weight": round(tw, 4),
                "event_id": edge.event_id,
                "layer": "fol",
            })

    return fol_nodes, fol_edges


def _serialize_event(event: TimelineEvent) -> dict[str, Any]:
    return {
        "id": event.id,
        "date": event.date.isoformat(),
        "brand": event.brand,
        "title": event.title,
        "title_ko": event.title_ko,
        "description": event.description,
        "category": event.category,
        "video_prompt": event.video_prompt,
        "impact_score": event.impact_score,
        "kg_mutation_count": len(event.kg_mutations),
        "news_headlines": event.news_headlines,
        "industry": event.industry,
        "market_share": event.market_share,
        "market_sales": event.market_sales,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# LIVE Mode: Composite Ideal Ambassador Recommendation
# ═══════════════════════════════════════════════════════════════════════════════

# Alpha tuned so a 50-year-old ambassador still has ~22 % weight.
_LIVE_ALPHA = 0.00008


def compute_live_recommendation(
    industry_filter: str | None = None,
    brand_filter: str | None = None,
    alpha: float = _LIVE_ALPHA,
) -> dict[str, Any]:
    """Score all ambassadors using temporal decay and return a ranked composite.

    Returns:
        {
            "ambassadors": [{"name", "brand", "percent", "score", "events", "years"}],
            "synthesis": {
                "narrative_ko": str,
                "narrative_en": str,
                "fol_chains": [{predicate, rule, conclusion, brand, weight}],
            }
        }
    """
    now = datetime(2026, 2, 28)

    # ── 1. filter models by industry ────────────────────────────────────────
    models = MODEL_GALLERY
    _whisky_types = {"scotch_whisky"}
    if industry_filter and industry_filter != "all":
        if industry_filter == "whisky":
            models = [m for m in models if m.product_type in _whisky_types]
        else:
            models = [m for m in models if m.product_type not in _whisky_types]
    if brand_filter and brand_filter != "all":
        models = [m for m in models if m.brand == brand_filter]

    # ── 2. build event lookup ───────────────────────────────────────────────
    events_by_brand: dict[str, list[TimelineEvent]] = defaultdict(list)
    for evt in ALL_EVENTS:
        if industry_filter and industry_filter != "all" and evt.industry != industry_filter:
            continue
        events_by_brand[evt.brand].append(evt)
        if evt.brand == "multi":
            # multi-brand events count for all brands
            pass  # already in "multi" bucket; we check both below

    def _event_impact(model: SojuModel) -> float:
        """Average impact_score of events matching this model's brand & era."""
        matched: list[float] = []
        for brand_key in (model.brand, "multi"):
            for evt in events_by_brand.get(brand_key, []):
                yr = evt.date.year
                if model.start_year <= yr <= model.end_year:
                    matched.append(evt.impact_score)
        return sum(matched) / len(matched) if matched else 1.0

    # ── 3. score each model entry ───────────────────────────────────────────
    raw: dict[str, float] = defaultdict(float)  # name → aggregated score
    meta: dict[str, dict[str, Any]] = {}  # name → first-seen metadata

    for m in models:
        midpoint_year = (m.start_year + m.end_year) / 2
        mid_date = datetime(int(midpoint_year), 7, 1)
        days = max(0, (now - mid_date).days)

        temporal_weight = math.exp(-alpha * days)
        event_impact = _event_impact(m)
        duration_bonus = min(1.0, (m.end_year - m.start_year) / 10)
        score = temporal_weight * event_impact * (1 + duration_bonus)

        raw[m.name] += score
        if m.name not in meta:
            meta[m.name] = {
                "brand": m.brand,
                "start_year": m.start_year,
                "end_year": m.end_year,
                "events": [],
            }
        # widen year range if same name appears in multiple entries
        info = meta[m.name]
        info["start_year"] = min(info["start_year"], m.start_year)
        info["end_year"] = max(info["end_year"], m.end_year)

    if not raw:
        return {"ambassadors": [], "synthesis": _empty_synthesis()}

    # ── 4. normalize to percentages ─────────────────────────────────────────
    total = sum(raw.values())
    ranked = sorted(raw.items(), key=lambda kv: kv[1], reverse=True)

    ambassadors: list[dict[str, Any]] = []
    for name, score in ranked[:10]:  # top 10
        pct = round(score / total * 100, 1)
        if pct < 1.0:
            break
        info = meta[name]
        ambassadors.append({
            "name": name,
            "brand": info["brand"],
            "percent": pct,
            "score": round(score, 4),
            "years": f"{info['start_year']}–{info['end_year']}",
        })

    # ── 5. synthesis from FOL conclusions ───────────────────────────────────
    synthesis = _build_live_synthesis(ambassadors, industry_filter, now, alpha)

    return {"ambassadors": ambassadors, "synthesis": synthesis}


def _build_live_synthesis(
    ambassadors: list[dict[str, Any]],
    industry_filter: str | None,
    now: datetime,
    alpha: float,
) -> dict[str, Any]:
    """Extract FOL conclusions from top ambassadors and compose a narrative."""
    # Collect all active event IDs for this industry
    active_ids: set[str] = set()
    for evt in ALL_EVENTS:
        if industry_filter and industry_filter != "all" and evt.industry != industry_filter:
            continue
        active_ids.add(evt.id)

    event_dates: dict[str, datetime] = {e.id: e.date for e in ALL_EVENTS}

    # Gather FOL conclusions weighted by temporal proximity
    fol_chains: list[dict[str, Any]] = []
    for fol in FOL_EVIDENCE:
        if fol.event_id not in active_ids:
            continue
        evt_date = event_dates.get(fol.event_id, now)
        tw = compute_temporal_weight(evt_date, now=now, alpha=alpha)

        predicates = [n.label_ko or n.label for n in fol.nodes if n.node_type == "fol_predicate"]
        rule_node = next((n for n in fol.nodes if n.node_type == "fol_rule"), None)
        conc_node = next((n for n in fol.nodes if n.node_type == "fol_conclusion"), None)
        if not conc_node:
            continue
        fol_chains.append({
            "predicates": predicates,
            "rule": rule_node.label_ko or rule_node.label if rule_node else "",
            "conclusion": conc_node.label_ko or conc_node.label if conc_node else "",
            "brand": fol.brand,
            "weight": round(tw, 4),
        })

    fol_chains.sort(key=lambda c: c["weight"], reverse=True)
    top_chains = fol_chains[:7]

    # Build narrative from top ambassador names + top FOL conclusions
    top_names = [a["name"] for a in ambassadors[:5]]
    top_conclusions = [c["conclusion"] for c in top_chains[:5]]

    if industry_filter == "whisky":
        narrative_ko = (
            f"200년간의 위스키 앰배서더 데이터를 시간가중 분석한 결과, "
            f"현재 최적의 앰배서더 DNA는 {', '.join(top_names[:3])}의 속성을 조합한 형태입니다. "
            + (" ".join(top_conclusions[:3]) if top_conclusions else "")
        )
        narrative_en = (
            f"Temporal-weighted analysis of 200 years of whisky ambassador data suggests "
            f"the ideal ambassador DNA combines attributes of {', '.join(top_names[:3])}. "
        )
    else:
        narrative_ko = (
            f"100년간의 소주 앰배서더 데이터를 시간가중 분석한 결과, "
            f"현재 최적의 앰배서더 DNA는 {', '.join(top_names[:3])}의 속성을 조합한 형태입니다. "
            + (" ".join(top_conclusions[:3]) if top_conclusions else "")
        )
        narrative_en = (
            f"Temporal-weighted analysis of 100 years of soju ambassador data suggests "
            f"the ideal ambassador DNA combines attributes of {', '.join(top_names[:3])}. "
        )

    return {
        "narrative_ko": narrative_ko,
        "narrative_en": narrative_en,
        "fol_chains": top_chains,
    }


def _empty_synthesis() -> dict[str, Any]:
    return {"narrative_ko": "", "narrative_en": "", "fol_chains": []}
