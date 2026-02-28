"use client";

import { useRef, useEffect, useCallback } from "react";
import cytoscape, { type Core } from "cytoscape";
import { cyStylesheet } from "./kg-styles";
import {
  BRAND_COLORS,
  NODE_SHAPES,
  FOL_COLORS,
} from "@/lib/constants";
import type { KGSnapshot } from "@/lib/types";

function getVisualState(weight: number) {
  if (weight >= 0.8) return { opacity: 1.0, glow: true, pulse: true, state: "just-occurred" };
  if (weight >= 0.5) return { opacity: 0.85, glow: true, pulse: false, state: "active" };
  if (weight >= 0.2) return { opacity: 0.65, glow: false, pulse: false, state: "fading" };
  if (weight >= 0.05) return { opacity: 0.4, glow: false, pulse: false, state: "nearly-forgotten" };
  return { opacity: 0.2, glow: false, pulse: false, state: "inactive" };
}

export function useKGRenderer(containerRef: React.RefObject<HTMLDivElement | null>) {
  const cyRef = useRef<Core | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const cy = cytoscape({
      container: containerRef.current,
      style: cyStylesheet as any,
      layout: { name: "preset" },
      minZoom: 0.3,
      maxZoom: 3,
      wheelSensitivity: 0.3,
    });
    cyRef.current = cy;

    // Cytoscape needs a resize after container layout settles
    const resizeTimer = setTimeout(() => cy.resize(), 100);

    return () => {
      clearTimeout(resizeTimer);
      cy.destroy();
      cyRef.current = null;
    };
  }, [containerRef]);

  const update = useCallback((snapshot: KGSnapshot, folVisible: boolean) => {
    const cy = cyRef.current;
    if (!cy) return;

    const elements: cytoscape.ElementDefinition[] = [];

    snapshot.nodes.forEach((node) => {
      const vis = getVisualState(node.temporal_weight);
      const color = BRAND_COLORS[node.brand] || BRAND_COLORS[""];
      const shape = NODE_SHAPES[node.type] || NODE_SHAPES.unknown;
      const baseSize = node.type === "brand" ? 50 : node.type === "person" ? 40 : 30;
      const size = vis.pulse ? baseSize * 1.3 : baseSize;

      elements.push({
        group: "nodes",
        data: {
          id: node.id,
          label: node.label,
          color,
          opacity: vis.opacity,
          shape,
          size,
          borderWidth: vis.state === "inactive" ? 2 : 1,
          borderStyle: vis.state === "inactive" ? "dashed" : "solid",
          shadowBlur: vis.glow ? (vis.pulse ? 18 : 10) : 0,
          shadowOpacity: vis.glow ? 0.6 : 0,
          weight: node.temporal_weight,
          brand: node.brand,
          nodeType: node.type,
        },
      });
    });

    snapshot.edges.forEach((edge) => {
      const vis = getVisualState(edge.temporal_weight);
      const color = BRAND_COLORS[edge.brand] || BRAND_COLORS[""];

      elements.push({
        group: "edges",
        data: {
          id: `${edge.source}-${edge.relation}-${edge.target}`,
          source: edge.source,
          target: edge.target,
          relation: edge.relation,
          color,
          opacity: vis.opacity * 0.7,
          lineStyle: vis.state === "inactive" ? "dashed" : "solid",
        },
      });
    });

    // FOL layer
    if (snapshot.fol_nodes) {
      snapshot.fol_nodes.forEach((node) => {
        const vis = getVisualState(node.temporal_weight);
        const folColor = FOL_COLORS[node.type] || "#FFD54F";
        const shape = NODE_SHAPES[node.type] || "round-triangle";
        const baseSize = node.type === "fol_rule" ? 32 : node.type === "fol_conclusion" ? 36 : 26;

        elements.push({
          group: "nodes",
          data: {
            id: node.id,
            label: node.label,
            color: folColor,
            opacity: vis.opacity * 0.9,
            shape,
            size: baseSize,
            borderWidth: 2,
            borderStyle: "solid",
            shadowBlur: vis.glow ? 8 : 0,
            shadowOpacity: vis.glow ? 0.4 : 0,
            weight: node.temporal_weight,
            brand: node.brand,
            nodeType: node.type,
          },
          classes: folVisible ? "fol-node" : "fol-node fol-hidden",
        });
      });
    }

    if (snapshot.fol_edges) {
      snapshot.fol_edges.forEach((edge) => {
        const vis = getVisualState(edge.temporal_weight);
        const relColor =
          edge.relation === "SUPPORTS" ? "#FF8A65" :
          edge.relation === "IMPLIES" ? "#FFD54F" : "#81C784";

        elements.push({
          group: "edges",
          data: {
            id: `fol-${edge.source}-${edge.relation}-${edge.target}`,
            source: edge.source,
            target: edge.target,
            relation: edge.relation,
            color: relColor,
            opacity: vis.opacity * 0.5,
            lineStyle: "dashed",
          },
          classes: folVisible ? "fol-edge" : "fol-edge fol-hidden",
        });
      });
    }

    cy.elements().remove();
    cy.add(elements);

    if (elements.length > 0) {
      cy.resize();
      const layout = cy.layout({
        name: "cose",
        animate: true,
        animationDuration: 600,
        nodeRepulsion: () => 6000,
        idealEdgeLength: () => 80,
        gravity: 0.3,
        padding: 30,
        randomize: false,
        componentSpacing: 60,
      } as any);
      layout.on("layoutstop", () => cy.fit(undefined, 30));
      layout.run();
    }
  }, []);

  const handleNodeClick = useCallback(
    (callback: (data: { id: string; type: string; label: string; brand: string; weight: number; connections: { other: string; rel: string; dir: string }[] }) => void) => {
      const cy = cyRef.current;
      if (!cy) return;

      cy.on("tap", "node", (evt) => {
        const node = evt.target;
        const nodeId = node.data("id");

        cy.elements().removeClass("highlighted neighbor dimmed");
        cy.elements().addClass("dimmed");
        node.removeClass("dimmed").addClass("highlighted");
        const neighborhood = node.neighborhood();
        neighborhood.removeClass("dimmed").addClass("neighbor");
        neighborhood.connectedEdges().removeClass("dimmed").addClass("highlighted");
        node.connectedEdges().removeClass("dimmed").addClass("highlighted");

        const connections: { other: string; rel: string; dir: string }[] = [];
        node.connectedEdges().forEach((edge: any) => {
          const src = edge.source().data("label");
          const tgt = edge.target().data("label");
          const rel = edge.data("relation");
          const other = edge.source().data("id") === nodeId ? tgt : src;
          const dir = edge.source().data("id") === nodeId ? "\u2192" : "\u2190";
          connections.push({ other, rel, dir });
        });

        callback({
          id: nodeId,
          type: node.data("nodeType"),
          label: node.data("label"),
          brand: node.data("brand"),
          weight: node.data("weight"),
          connections,
        });
      });

      cy.on("tap", (evt) => {
        if (evt.target === cy) {
          cy.elements().removeClass("highlighted neighbor dimmed");
          callback(null as any);
        }
      });
    },
    []
  );

  return { cyRef, update, handleNodeClick };
}
