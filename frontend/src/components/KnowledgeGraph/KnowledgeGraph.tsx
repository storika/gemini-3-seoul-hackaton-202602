"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import { useTimelineStore } from "@/stores/timeline-store";
import { useKGRenderer } from "./useKGRenderer";
import NodePopup from "./NodePopup";
import type { ModelEntry } from "@/lib/types";

interface NodeData {
  id: string;
  type: string;
  label: string;
  brand: string;
  weight: number;
  connections: { other: string; rel: string; dir: string }[];
}

export default function KnowledgeGraph() {
  const containerRef = useRef<HTMLDivElement>(null);
  const snapshot = useTimelineStore((s) => s.snapshot);
  const folVisible = useTimelineStore((s) => s.folVisible);
  const toggleFOL = useTimelineStore((s) => s.toggleFOL);
  const { update, handleNodeClick } = useKGRenderer(containerRef);
  const [selectedNode, setSelectedNode] = useState<NodeData | null>(null);
  const [popupPos, setPopupPos] = useState({ x: 0, y: 0 });
  const [modelGallery, setModelGallery] = useState<ModelEntry[]>([]);

  // Load model gallery
  useEffect(() => {
    fetch("/api/timeline/models")
      .then((r) => r.json())
      .then(setModelGallery)
      .catch(() => {});
  }, []);

  // Wire node click
  useEffect(() => {
    handleNodeClick((data) => {
      if (!data) {
        setSelectedNode(null);
        return;
      }
      setSelectedNode(data);
      setPopupPos({ x: 100, y: 60 });
    });
  }, [handleNodeClick]);

  // Update graph on snapshot change
  useEffect(() => {
    if (snapshot) update(snapshot, folVisible);
  }, [snapshot, folVisible, update]);

  const nodeCount = snapshot?.nodes.length ?? 0;
  const edgeCount = snapshot?.edges.length ?? 0;
  const eventCount = snapshot?.stats.active_events ?? 0;

  return (
    <section className="kg-panel">
      <div className="kg-stats">
        <span>{nodeCount} nodes</span>
        <span>{edgeCount} edges</span>
        <span>{eventCount} events</span>
        <button
          className={`fol-toggle${folVisible ? " active" : ""}`}
          onClick={toggleFOL}
          title="Toggle FOL Evidence Layer"
        >
          <span style={{ fontSize: 12, fontWeight: 700 }}>&and;</span> FOL
        </button>
      </div>
      <div ref={containerRef} className="cy-container" />
      <NodePopup
        node={selectedNode}
        modelGallery={modelGallery}
        position={popupPos}
        onClose={() => setSelectedNode(null)}
      />
    </section>
  );
}
