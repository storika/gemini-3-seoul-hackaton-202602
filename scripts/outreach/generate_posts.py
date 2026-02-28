"""
Generate ready-to-post Instagram/TikTok content using Gemini 3 Flash.
Per-creator captions, hashtags, and content concepts.
Output: output/posts/{handle}.md
"""

import os
import pathlib
from google import genai

from creators import all_creators, Creator
from brand import BRAND, brand_summary, brand_visual_prompt

OUTPUT_DIR = pathlib.Path(__file__).parent / "output" / "posts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def build_prompt(creator: Creator) -> str:
    return f"""You are a top-tier social media content creator specializing in Korean influencer marketing.
Create a complete ready-to-post content package for the creator below partnering with Boksoondoga.

=== BRAND ===
{brand_summary()}
Visual: {brand_visual_prompt()}
Campaign: {BRAND['campaign_goal']}
Brand hashtags: {', '.join(BRAND['key_hashtags'])}

=== CREATOR ===
- Handle: @{creator.handle} ({creator.name_kr} / {creator.name})
- Followers: {creator.followers:,} | Engagement: {creator.engagement_rate}%
- Categories: {', '.join(creator.categories)}
- Content Style: {creator.content_style}
- Bio: {creator.bio}

=== GENERATE 3 POST PACKAGES ===

For each post, provide:

### Post [N]: [Concept Name]

**Platform**: Instagram Feed / Instagram Reels / TikTok
**Format**: Carousel / Single Image / Reel / TikTok Video

**Visual Concept**:
(Detailed description of what the image/video should show — specific enough for AI generation)

**Caption (Korean)**:
(Written in {creator.name_kr}'s voice and style. Natural Korean, matching their typical caption length and tone.)

**Caption (English translation)**:
(For reference)

**Hashtag Set**:
(15-20 hashtags: brand + trending + creator-specific + content-specific)

**Posting Notes**:
(Best time to post, engagement tips, CTA strategy)

---

IMPORTANT:
- Write captions in the creator's actual voice (study their content style description)
- Captions should feel like the creator wrote them, not a brand
- Include natural Korean expressions and tone appropriate to their audience
- Each post should have a different angle/concept
- At least one post should be video-first (Reels/TikTok)"""


def generate_posts(creator: Creator) -> str:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=build_prompt(creator),
    )
    return response.text


def main():
    print("Generating ready-to-post content...\n")
    for creator in all_creators():
        print(f"  @{creator.handle} ({creator.name_kr})...", end=" ", flush=True)
        posts = generate_posts(creator)
        out_path = OUTPUT_DIR / f"{creator.handle}.md"
        out_path.write_text(posts, encoding="utf-8")
        print(f"✓ ({len(posts)} chars)")

    print(f"\nDone! Posts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
