"""Memoria-style Exponential Weighted Average (EWA) temporal decay.

w_i = e^(-α · x_i)
  - α: decay rate (default 0.02)
  - x_i: days since creation

~35 days → weight ≈ 0.50
~115 days → weight ≈ 0.10
~365 days → weight ≈ 0.0007 (effectively forgotten)
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta

from src.config import TEMPORAL_DECAY_ALPHA, SIMILARITY_WEIGHT, TEMPORAL_WEIGHT


def compute_temporal_weight(
    created_at: datetime,
    now: datetime | None = None,
    alpha: float = TEMPORAL_DECAY_ALPHA,
    significance: float = 0.5,
) -> float:
    """Compute EWA temporal weight for a memory item.

    Returns a value in (0, 1] where 1.0 means "just created".
    Significance (0.0 to 1.0) slows down the decay:
    - 1.0 significance: Alpha is reduced by 90% (stays relevant for decades)
    - 0.5 significance: Standard alpha
    - 0.0 significance: Alpha is doubled (fleeting trend)
    """
    if now is None:
        now = datetime.utcnow()
    
    # Adjust alpha based on significance
    # If sig=1.0, adj_alpha = alpha * 0.1
    # If sig=0.5, adj_alpha = alpha * 1.0
    # If sig=0.0, adj_alpha = alpha * 2.0
    adj_alpha = alpha * (2.0 - 1.8 * significance) if significance > 0.5 else alpha * (2.0 - 2.0 * significance + 1.0)
    # Simpler linear mapping for hackathon clarity:
    # 0.0 -> 2.0*alpha
    # 0.5 -> 1.0*alpha
    # 1.0 -> 0.1*alpha
    if significance >= 0.5:
        # Map [0.5, 1.0] to [1.0, 0.1]
        adj_alpha = alpha * (1.0 - (significance - 0.5) * 1.8)
    else:
        # Map [0.0, 0.5] to [2.0, 1.0]
        adj_alpha = alpha * (2.0 - significance * 2.0)

    delta_days = max((now - created_at).total_seconds() / 86400, 0.0)
    return math.exp(-adj_alpha * delta_days)


def compute_combined_score(
    similarity: float,
    created_at: datetime,
    now: datetime | None = None,
    alpha: float = TEMPORAL_DECAY_ALPHA,
    sim_weight: float = SIMILARITY_WEIGHT,
    temp_weight: float = TEMPORAL_WEIGHT,
    significance: float = 0.5,
) -> float:
    """Combine vector similarity with temporal decay.

    final = sim_weight * similarity + temp_weight * temporal_weight
    """
    tw = compute_temporal_weight(created_at, now=now, alpha=alpha, significance=significance)
    return sim_weight * similarity + temp_weight * tw


def half_life_days(alpha: float = TEMPORAL_DECAY_ALPHA) -> float:
    """Return the number of days until weight drops to 0.5."""
    return math.log(2) / alpha
