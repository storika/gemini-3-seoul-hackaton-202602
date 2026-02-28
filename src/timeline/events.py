"""TimelineEvent dataclass for brand identity evolution milestones."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class KGMutation:
    """A single knowledge-graph mutation (node or edge addition)."""

    action: str  # "add_node" or "add_edge"
    # Node fields
    node_id: str = ""
    node_type: str = ""  # brand, product, ingredient, person, award, market, event
    label: str = ""
    brand: str = ""
    # Edge fields
    source: str = ""
    target: str = ""
    relation: str = ""


@dataclass
class TimelineEvent:
    """A single milestone in the brand identity evolution timeline."""

    id: str
    date: datetime
    brand: str  # "jinro", "chamisul", "chum_churum", "saero", or "multi"
    title: str
    title_ko: str
    description: str
    category: str  # "founding", "product_launch", "viral", "award", "corporate", "campaign", "expansion", "model_change", "market_shift"
    industry: str = "soju"
    kg_mutations: list[KGMutation] = field(default_factory=list)
    video_prompt: str = ""
    impact_score: float = 1.0  # 1.0~5.0 scale for visual emphasis
    news_headlines: list[str] = field(default_factory=list)
    market_share: dict[str, float] = field(default_factory=dict)  # brand → share %
    market_sales: dict[str, str] = field(default_factory=dict)  # brand → annual sales (억원)
