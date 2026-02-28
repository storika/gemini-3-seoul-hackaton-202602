"""Integration tests for the ADK agent system.

These tests verify agent structure and tool wiring without requiring API keys.
Tests that need live API calls are marked with @pytest.mark.requires_api.
"""

import pytest


def test_root_agent_structure():
    """Verify root agent has correct sub-agents and tools."""
    from src.agents.agent import root_agent

    assert root_agent.name == "liquor_director"
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

    result = set_active_brand("chamisul")
    assert result["status"] == "active"
    assert result["brand"] == "chamisul"


def test_root_tools_set_active_brand_invalid():
    from src.agents.root_tools import set_active_brand

    result = set_active_brand("unknown_brand")
    assert "error" in result


def test_root_tools_get_memory_context():
    from src.agents.root_tools import get_memory_context
    result = get_memory_context("bamboo charcoal soju", "chamisul")
    assert "brand" in result
    assert "context" in result


def test_root_tools_save_to_memory():
    from src.agents.root_tools import save_to_memory

    result = save_to_memory(
        content="Test memory note for integration",
        brand_namespace="chumchurum",
        category="product",
        tags="test,integration",
    )
    assert result["status"] == "saved"
    assert result["brand"] == "chumchurum"


def test_root_tools_get_brand_stats():
    from src.agents.root_tools import get_brand_stats

    result = get_brand_stats()
    assert "chamisul" in result
    assert "chumchurum" in result
    assert "saero" in result


@pytest.mark.requires_api
async def test_creative_director_tools():
    """Test creative director tool functions directly."""
    from src.agents.creative_director.tools import (
        generate_image,
        generate_video,
        build_creative_brief,
    )

    img_result = await generate_image("Chamisul", "Chamisul Original")
    assert img_result["status"] == "prompt_ready"
    assert "Chamisul" in img_result["prompt"]

    vid_result = await generate_video("Saero", "Saero Zero Sugar", hero_ingredient="zero sugar")
    assert vid_result["status"] == "prompt_ready"
    assert "zero sugar" in vid_result["prompt"]

    brief = build_creative_brief("CHUM CHURUM", "New alkaline soju launch", "TikTok")
    assert brief["brand"] == "CHUM CHURUM"
    assert brief["platform"] == "TikTok"
    assert "brand_guidelines" in brief


def test_media_prompt_builders():
    """Test media prompt builder utilities."""
    from src.media.imagen_client import build_product_image_prompt, build_lifestyle_image_prompt
    from src.media.veo_client import build_product_video_prompt, build_brand_story_prompt

    img_prompt = build_product_image_prompt("Chamisul", "Chamisul Original")
    assert "Chamisul" in img_prompt
    assert "Korean soju" in img_prompt

    lifestyle = build_lifestyle_image_prompt("Chum Churum", "Evening social gathering")
    assert "Chum Churum" in lifestyle

    vid_prompt = build_product_video_prompt("Saero", "Saero Zero Sugar", hero_ingredient="zero sugar")
    assert "zero sugar" in vid_prompt

    story = build_brand_story_prompt("Chamisul", "100-year soju heritage journey")
    assert "Chamisul" in story
