"""Integration tests for the ADK agent system.

These tests verify agent structure and tool wiring without requiring API keys.
Tests that need live API calls are marked with @pytest.mark.requires_api.
"""

import pytest


def test_root_agent_structure():
    """Verify root agent has correct sub-agents and tools."""
    from src.agents.agent import root_agent

    assert root_agent.name == "kbeauty_director"
    sub_names = [a.name for a in root_agent.sub_agents]
    assert "trend_pipeline" in sub_names
    assert "content_pipeline" in sub_names
    assert "standalone_brand_guard" in sub_names


def test_trend_pipeline_structure():
    """Verify trend pipeline has searcher and analyzer."""
    from src.agents.trend_analyzer.agent import trend_pipeline

    sub_names = [a.name for a in trend_pipeline.sub_agents]
    assert "trend_searcher" in sub_names
    assert "trend_analyzer" in sub_names


def test_content_pipeline_structure():
    """Verify content pipeline has creative director and brand guard."""
    from src.agents.creative_director.agent import content_pipeline

    sub_names = [a.name for a in content_pipeline.sub_agents]
    assert "creative_director" in sub_names
    assert "pipeline_brand_guard" in sub_names


def test_root_tools_set_active_brand():
    """Test set_active_brand tool."""
    from src.agents.root_tools import set_active_brand

    result = set_active_brand("tirtir")
    assert result["status"] == "active"
    assert result["brand"] == "tirtir"


def test_root_tools_set_active_brand_invalid():
    from src.agents.root_tools import set_active_brand

    result = set_active_brand("unknown_brand")
    assert "error" in result


def test_root_tools_get_memory_context():
    from src.agents.root_tools import get_memory_context
    result = get_memory_context("cushion foundation", "tirtir")
    assert "brand" in result
    assert "context" in result


def test_root_tools_save_to_memory():
    from src.agents.root_tools import save_to_memory

    result = save_to_memory(
        content="Test memory note for integration",
        brand_namespace="anua",
        category="product",
        tags="test,integration",
    )
    assert result["status"] == "saved"
    assert result["brand"] == "anua"


def test_root_tools_get_brand_stats():
    from src.agents.root_tools import get_brand_stats

    result = get_brand_stats()
    assert "tirtir" in result
    assert "anua" in result
    assert "cosrx" in result


def test_creative_director_tools():
    """Test creative director tool functions directly."""
    from src.agents.creative_director.tools import (
        generate_image,
        generate_video,
        build_creative_brief,
    )

    img_result = generate_image("TIRTIR", "Mask Fit Red Cushion")
    assert img_result["status"] == "prompt_ready"
    assert "TIRTIR" in img_result["prompt"]

    vid_result = generate_video("COSRX", "Snail 96 Mucin Essence", hero_ingredient="snail mucin")
    assert vid_result["status"] == "prompt_ready"
    assert "snail mucin" in vid_result["prompt"]

    brief = build_creative_brief("ANUA", "New heartleaf product launch", "TikTok")
    assert brief["brand"] == "ANUA"
    assert brief["platform"] == "TikTok"
    assert "brand_guidelines" in brief


def test_media_prompt_builders():
    """Test media prompt builder utilities."""
    from src.media.imagen_client import build_product_image_prompt, build_lifestyle_image_prompt
    from src.media.veo_client import build_product_video_prompt, build_brand_story_prompt

    img_prompt = build_product_image_prompt("TIRTIR", "Mask Fit Red Cushion")
    assert "TIRTIR" in img_prompt
    assert "Korean beauty" in img_prompt

    lifestyle = build_lifestyle_image_prompt("ANUA", "Morning skincare ritual")
    assert "ANUA" in lifestyle

    vid_prompt = build_product_video_prompt("COSRX", "Snail Mucin Essence", hero_ingredient="snail mucin")
    assert "snail mucin" in vid_prompt

    story = build_brand_story_prompt("TIRTIR", "shade diversity journey")
    assert "TIRTIR" in story
