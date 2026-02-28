"use client";

import type { ModelEntry } from "@/lib/types";
import {
  buildPersonPopup,
  buildBrandPopup,
  buildProductPopup,
  buildAwardPopup,
  buildMarketPopup,
  buildIngredientPopup,
  buildFOLPopup,
  buildGenericPopup,
} from "./popup-builders";

interface NodeData {
  id: string;
  type: string;
  label: string;
  brand: string;
  weight: number;
  connections: { other: string; rel: string; dir: string }[];
}

interface Props {
  node: NodeData | null;
  modelGallery: ModelEntry[];
  position: { x: number; y: number };
  onClose: () => void;
}

export default function NodePopup({ node, modelGallery, position, onClose }: Props) {
  if (!node) return null;

  let content: React.ReactNode;
  switch (node.type) {
    case "person":
      content = buildPersonPopup(node.label, node.brand, node.weight, node.connections, modelGallery);
      break;
    case "brand":
      content = buildBrandPopup(node.label, node.brand, node.weight, node.connections);
      break;
    case "product":
      content = buildProductPopup(node.label, node.brand, node.weight, node.connections);
      break;
    case "award":
      content = buildAwardPopup(node.label, node.weight, node.connections);
      break;
    case "market":
      content = buildMarketPopup(node.label, node.weight, node.connections);
      break;
    case "ingredient":
      content = buildIngredientPopup(node.label, node.weight, node.connections);
      break;
    case "fol_predicate":
    case "fol_rule":
    case "fol_conclusion":
      content = buildFOLPopup(node.label, node.type, node.brand, node.weight, node.connections);
      break;
    default:
      content = buildGenericPopup(node.label, node.type, node.weight, node.connections);
  }

  return (
    <div
      className="node-popup"
      style={{ left: position.x, top: position.y }}
    >
      <button className="node-popup-close" onClick={onClose}>
        &times;
      </button>
      {content}
    </div>
  );
}
