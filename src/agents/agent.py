"""Root agent orchestrator — ADK entry point.

Routes requests to sub-agents:
  - trend_pipeline: Search + analyze K-beauty trends
  - content_pipeline: Creative content generation + brand validation
  - brand_guard: Standalone brand identity verification
"""

from google.adk.agents import LlmAgent

from src.agents.trend_analyzer.agent import trend_pipeline
from src.agents.brand_guard.agent import create_brand_guard
from src.agents.creative_director.agent import content_pipeline

from .root_tools import (
    set_active_brand_tool,
    get_memory_context_tool,
    save_to_memory_tool,
    get_brand_stats_tool,
)


root_agent = LlmAgent(
    name="liquor_director",
    model="gemini-3-flash-preview",
    instruction=(
        "You are the Korean Liquor Brand Director, an AI assistant that helps manage and grow "
        "Korean Soju brands based on 100 years of historical data. You have deep knowledge of Chamisul, Chum Churum, and Saero.\n\n"
        "## Your Capabilities\n"
        "1. **Trend Analysis**: Research and analyze liquor market trends\n"
        "2. **Content Creation**: Generate campaign visuals (images + videos)\n"
        "3. **Brand Verification**: Ensure content aligns with brand identity and history\n"
        "4. **Memory Management**: Store and retrieve brand knowledge\n\n"
        "## How to Route Requests\n"
        "- For trend research → delegate to `trend_pipeline`\n"
        "- For content/creative work → delegate to `content_pipeline`\n"
        "- For brand verification only → delegate to `brand_guard`\n"
        "- For memory/knowledge queries → use your tools directly\n\n"
        "## Important\n"
        "- Always set the active brand before processing brand-specific requests\n"
        "- Use memory context to ground all responses in brand facts\n"
        "- When creating content, always route through brand_guard for validation\n"
        "- Maintain brand voice consistency for each brand\n\n"
        "## Brand Profiles\n"
        "- **Chamisul**: 100-year original, clean bamboo charcoal filtration, IU as the longest-serving model.\n"
        "- **Chum Churum**: Soft alkaline water, famous for the 'shake it' campaign with Lee Hyori.\n"
        "- **Saero**: Zero sugar pioneer, virtual character (Saerogumi) marketing, MZ generation focus.\n\n"
        "Always respond in the user's language (Korean or English)."
    ),
    tools=[
        set_active_brand_tool,
        get_memory_context_tool,
        save_to_memory_tool,
        get_brand_stats_tool,
    ],
    sub_agents=[trend_pipeline, content_pipeline, create_brand_guard("standalone_brand_guard")],
)
