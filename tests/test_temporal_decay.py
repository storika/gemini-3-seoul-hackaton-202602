"""Tests for EWA temporal decay math."""

import math
from datetime import datetime, timedelta

from src.memory.temporal_decay import (
    compute_temporal_weight,
    compute_combined_score,
    half_life_days,
)


def test_weight_at_creation_is_one():
    now = datetime(2026, 1, 1)
    assert compute_temporal_weight(now, now=now) == 1.0


def test_weight_decreases_over_time():
    now = datetime(2026, 1, 1)
    w_10d = compute_temporal_weight(now - timedelta(days=10), now=now)
    w_50d = compute_temporal_weight(now - timedelta(days=50), now=now)
    assert 0 < w_50d < w_10d < 1.0


def test_half_life_default_alpha():
    hl = half_life_days(alpha=0.02)
    assert abs(hl - math.log(2) / 0.02) < 0.01
    # ~34.66 days
    assert 34 < hl < 35


def test_weight_at_half_life():
    alpha = 0.02
    hl = half_life_days(alpha)
    now = datetime(2026, 6, 1)
    created = now - timedelta(days=hl)
    w = compute_temporal_weight(created, now=now, alpha=alpha)
    assert abs(w - 0.5) < 0.001


def test_weight_at_one_year_near_zero():
    now = datetime(2026, 6, 1)
    created = now - timedelta(days=365)
    w = compute_temporal_weight(created, now=now, alpha=0.02)
    assert w < 0.001


def test_combined_score_weights():
    now = datetime(2026, 1, 1)
    created = now  # just created → temporal weight = 1.0
    similarity = 0.8

    score = compute_combined_score(similarity, created, now=now)
    expected = 0.6 * 0.8 + 0.4 * 1.0  # 0.88
    assert abs(score - expected) < 0.001


def test_combined_score_old_note():
    now = datetime(2026, 1, 1)
    created = now - timedelta(days=365)
    similarity = 0.9

    score = compute_combined_score(similarity, created, now=now)
    # temporal weight ≈ 0, so score ≈ 0.6 * 0.9 = 0.54
    assert 0.53 < score < 0.55


def test_future_creation_clamped():
    """Future dates should still return weight 1.0 (delta clamped to 0)."""
    now = datetime(2026, 1, 1)
    future = now + timedelta(days=10)
    w = compute_temporal_weight(future, now=now)
    assert w == 1.0


def test_custom_alpha():
    alpha = 0.1  # much faster decay
    hl = half_life_days(alpha)
    assert abs(hl - math.log(2) / 0.1) < 0.01
    # ~6.93 days
    assert 6 < hl < 7
