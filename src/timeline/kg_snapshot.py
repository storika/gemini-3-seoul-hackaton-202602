"""Build a KG snapshot at a given point in time.

Applies timeline events up to a target date onto a NetworkX DiGraph,
then annotates every node/edge with its temporal weight using
the existing compute_temporal_weight() from src.memory.temporal_decay.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import networkx as nx

from src.memory.temporal_decay import compute_temporal_weight
from .event_data import TIMELINE_EVENTS
from .events import TimelineEvent, KGMutation
from .fol_evidence import FOL_EVIDENCE

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

    for event in TIMELINE_EVENTS:
        if event.date > target_date:
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
    for evt in TIMELINE_EVENTS:
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
