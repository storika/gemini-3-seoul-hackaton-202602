"""
Generate per-creator marketing content guidelines using Gemini 3 Flash.
Output: output/guidelines/{handle}.md
"""

import os
import pathlib
from google import genai

from creators import all_creators, Creator
from brand import BRAND, brand_summary, brand_visual_prompt

OUTPUT_DIR = pathlib.Path(__file__).parent / "output" / "guidelines"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def build_prompt(creator: Creator) -> str:
    products_info = "\n".join(
        f"  - {p['name_kr']} ({p['name_en']}): {p['type']}, {p['abv']}% ABV — {p['description']}"
        for p in BRAND["products"]
    )
    return f"""You are a senior influencer marketing strategist. Create detailed content guidelines
for the following creator's partnership with Boksoondoga (복순도가).

=== BRAND ===
{brand_summary()}
Visual: {brand_visual_prompt()}
Products:
{products_info}
Campaign: {BRAND['campaign_goal']}
Hashtags: {', '.join(BRAND['key_hashtags'])}

=== CREATOR ===
- Handle: @{creator.handle} ({creator.name_kr} / {creator.name})
- Followers: {creator.followers:,}
- Engagement Rate: {creator.engagement_rate}%
- Avg Likes: {creator.avg_likes:,} | Avg Comments: {creator.avg_comments}
- Categories: {', '.join(creator.categories)}
- Content Style: {creator.content_style}
- Collab Ratio: {creator.collab_ratio:.0%}
- Brand Fit Reasons:
{chr(10).join(f'  • {r}' for r in creator.brand_fit_reasons)}

=== OUTPUT FORMAT (Markdown) ===
# Content Guidelines: @{creator.handle} × 복순도가

## Brand Fit Analysis
(Why this creator is ideal for Boksoondoga — backed by their data)

## Recommended Content Themes
(3-5 specific content themes tailored to their style and audience)

## Content Do's
(5-7 specific dos aligned with their content style)

## Content Don'ts
(5-7 specific don'ts to avoid brand/audience mismatch)

## Posting Schedule & Format
(Recommended cadence, best post types, optimal times)

## Sample Captions
(2-3 sample captions in Korean, matching their voice)

## Hashtag Strategy
(Brand hashtags + trending + creator-specific recommendations)

Write in English with Korean terms where natural. Be specific — reference actual data points."""


def generate_guidelines(creator: Creator) -> str:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=build_prompt(creator),
    )
    return response.text


def main():
    print("Generating content guidelines...\n")
    for creator in all_creators():
        print(f"  @{creator.handle} ({creator.name_kr})...", end=" ", flush=True)
        guidelines = generate_guidelines(creator)
        out_path = OUTPUT_DIR / f"{creator.handle}.md"
        out_path.write_text(guidelines, encoding="utf-8")
        print(f"✓ ({len(guidelines)} chars)")

    print(f"\nDone! Guidelines saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
