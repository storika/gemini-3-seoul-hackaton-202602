"""Brand Guard agent — validates content against brand identity and memory."""

from google.adk.agents import LlmAgent

from .tools import check_brand_alignment_tool, check_ingredient_accuracy_tool

_BRAND_GUARD_INSTRUCTION = (
    "You are the Brand Guard for Korean Liquor brands. Your role is to ensure all content, "
    "campaigns, and product claims align with the brand's established identity, values, "
    "historical model choices, and factual product information.\n\n"
    "For every piece of content you review, check:\n"
    "1. **Brand Voice & Model Alignment**: Does the tone match the brand's ethos?\n"
    "   - Chamisul: Clean, pure, original, historically associated with models like IU or Lee Young-ae.\n"
    "   - Chum Churum: Soft, trendy, historically associated with models like Lee Hyori or Jennie.\n"
    "   - Saero: Zero sugar, modern, virtual character (Saerogumi) focused.\n\n"
    "2. **Historical Accuracy**: Are the claims, launch years, and historical sales impacts correct?\n"
    "3. **Visual Consistency**: Does the aesthetic match brand identity?\n"
    "4. **Cross-Brand Hallucination**: Ensure a model famous for one brand (e.g. Lee Hyori for Chum Churum) is NOT incorrectly associated with another (e.g. Chamisul).\n\n"
    "Use the brand memory tools to verify claims against stored knowledge.\n"
    "Return a structured assessment with PASS/FAIL and specific feedback."
)


def create_brand_guard(name: str = "brand_guard") -> LlmAgent:
    """Factory: create a fresh brand_guard instance (ADK disallows shared sub-agents)."""
    return LlmAgent(
        name=name,
        model="gemini-3-flash-preview",
        instruction=_BRAND_GUARD_INSTRUCTION,
        tools=[check_brand_alignment_tool, check_ingredient_accuracy_tool],
        description="Validates content against brand identity, facts, and guidelines",
    )


# Default instance for standalone use
brand_guard = create_brand_guard("brand_guard")
