"""Trend analysis pipeline — Google Search + memory-based analysis.

ADK constraint: google_search must be the only tool on its agent,
so we split into trend_searcher (search-only) and trend_analyzer (LLM analysis).
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search


# Sub-agent 1: Search-only (google_search requires being the sole tool)
trend_searcher = LlmAgent(
    name="trend_searcher",
    model="gemini-3-flash-preview",
    instruction=(
        "You are a Korean liquor/soju trend researcher. Search for the latest soju market trends, "
        "product innovations, and market developments.\n\n"
        "When given a research query, use Google Search to find current information about:\n"
        "- Soju trending products and flavors\n"
        "- Social media viral products (TikTok, Instagram)\n"
        "- Market data and consumer behavior shifts\n"
        "- New brand launches and competitive moves\n\n"
        "Summarize your findings clearly with source references. "
        "Focus on actionable insights for Korean liquor brand strategy."
    ),
    tools=[google_search],
)

# Sub-agent 2: Analysis (no tools — uses state from previous step)
trend_analyzer_llm = LlmAgent(
    name="trend_analyzer",
    model="gemini-3-flash-preview",
    instruction=(
        "You are a Korean liquor/soju trend analyst with deep knowledge of Korean soju brands. "
        "Analyze the search results from the previous step in the context of the active brand's "
        "memory and identity.\n\n"
        "Your analysis should:\n"
        "1. Identify which trends are relevant to the active brand\n"
        "2. Assess alignment with brand identity and positioning\n"
        "3. Suggest opportunities and risks\n"
        "4. Recommend specific product/marketing actions\n\n"
        "Use the brand memory context provided in the state to ground your analysis.\n\n"
        "Brand memory context:\n{memory_context}"
    ),
)

# Combined pipeline
trend_pipeline = SequentialAgent(
    name="trend_pipeline",
    sub_agents=[trend_searcher, trend_analyzer_llm],
    description="Search for Korean liquor/soju trends and analyze them in brand context",
)
