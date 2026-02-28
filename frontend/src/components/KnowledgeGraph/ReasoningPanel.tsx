"use client";

import { useTimelineStore } from "@/stores/timeline-store";
import { BRAND_COLORS } from "@/lib/constants";
import type { KGNode } from "@/lib/types";

interface ReasoningChain {
  eventId: string;
  eventTitle: string;
  eventDate: string;
  brand: string;
  predicates: string[];
  rule: string;
  conclusion: string;
  weight: number;
}

export default function ReasoningPanel() {
  const snapshot = useTimelineStore((s) => s.snapshot);
  const events = useTimelineStore((s) => s.events);

  const folNodes: KGNode[] = snapshot?.fol_nodes ?? [];
  if (folNodes.length === 0) return null;

  // Map event_id → event info
  const eventMap = new Map(events.map((e) => [e.id, e]));

  // Group nodes by event_id
  const grouped = new Map<string, KGNode[]>();
  for (const n of folNodes) {
    if (!n.event_id) continue;
    const list = grouped.get(n.event_id) ?? [];
    list.push(n);
    grouped.set(n.event_id, list);
  }

  // Build chains sorted by temporal_weight (most relevant first)
  const chains: ReasoningChain[] = [];
  for (const [eventId, nodes] of grouped) {
    const ev = eventMap.get(eventId);
    const predicates = nodes
      .filter((n) => n.type === "fol_predicate")
      .map((n) => n.label_ko || n.label);
    const rule = nodes.find((n) => n.type === "fol_rule");
    const conclusion = nodes.find((n) => n.type === "fol_conclusion");
    const maxWeight = Math.max(...nodes.map((n) => n.temporal_weight));

    chains.push({
      eventId,
      eventTitle: ev?.title_ko || eventId,
      eventDate: ev?.date?.slice(0, 4) || "",
      brand: nodes[0]?.brand || "",
      predicates,
      rule: rule?.label_ko || rule?.label || "",
      conclusion: conclusion?.label_ko || conclusion?.label || "",
      weight: maxWeight,
    });
  }

  chains.sort((a, b) => b.weight - a.weight);

  return (
    <div className="reasoning-panel">
      <div className="reasoning-header">
        <h3>Reasoning Graph</h3>
        <span className="reasoning-count">{chains.length} chains</span>
      </div>
      <div className="reasoning-list">
        {chains.map((chain) => {
          const brandColor = BRAND_COLORS[chain.brand] || "#888";
          const opacity = Math.max(0.4, Math.min(1, chain.weight + 0.3));
          return (
            <article
              key={chain.eventId}
              className="reasoning-chain"
              style={{ borderLeftColor: brandColor, opacity }}
            >
              <div className="reasoning-era">
                <span className="reasoning-year">{chain.eventDate}</span>
                <span className="reasoning-title">{chain.eventTitle}</span>
              </div>
              <div className="reasoning-flow">
                <div className="reasoning-predicates">
                  {chain.predicates.map((p, i) => (
                    <span key={i} className="reasoning-predicate">{p}</span>
                  ))}
                </div>
                <div className="reasoning-arrow">&#8595;</div>
                <div className="reasoning-rule">{chain.rule}</div>
                <div className="reasoning-arrow">&#8595;</div>
                <div className="reasoning-conclusion">{chain.conclusion}</div>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
