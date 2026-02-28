export interface TimelineEvent {
  id: string;
  date: string;
  brand: string;
  title: string;
  title_ko: string;
  description: string;
  category: string;
  industry: string;
  video_prompt: string;
  impact_score: number;
  news_headlines: string[];
  market_share: Record<string, number>;
  market_sales: Record<string, string>;
  kg_mutation_count: number;
}

export interface KGNode {
  id: string;
  label: string;
  label_ko?: string;
  type: string;
  brand: string;
  temporal_weight: number;
  added_date: string;
  event_id?: string;
}

export interface KGEdge {
  source: string;
  target: string;
  relation: string;
  brand: string;
  temporal_weight: number;
}

export interface KGSnapshot {
  nodes: KGNode[];
  edges: KGEdge[];
  fol_nodes?: KGNode[];
  fol_edges?: KGEdge[];
  current_event?: TimelineEvent | null;
  stats: {
    active_events: number;
    total_nodes: number;
    total_edges: number;
  };
}

export interface ModelEntry {
  id: string;
  name: string;
  name_ko: string;
  brand: string;
  product_type: string;
  start_year: number;
  end_year: number;
  image_url: string;
  company_ko?: string;
  era_note?: string;
}

export interface VideoStatus {
  status: "available" | "not_found" | "generating" | "generated" | "cached" | "error";
  path?: string;
  detail?: string;
}

// ── LIVE Mode ────────────────────────────────────────────────────────────────

export interface LiveAmbassador {
  name: string;
  brand: string;
  percent: number;
  score: number;
  years: string;
}

export interface LiveFOLChain {
  predicates: string[];
  rule: string;
  conclusion: string;
  brand: string;
  weight: number;
}

export interface LiveSynthesis {
  narrative_ko: string;
  narrative_en: string;
  fol_chains: LiveFOLChain[];
}

export interface LiveRecommendation {
  ambassadors: LiveAmbassador[];
  synthesis: LiveSynthesis;
}
