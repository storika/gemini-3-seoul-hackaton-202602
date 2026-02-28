"""
4 selected creator profiles from ClickHouse data.
Used as foundation for all personalized content generation.
"""

from dataclasses import dataclass, field


@dataclass
class Creator:
    handle: str
    name: str
    name_kr: str
    followers: int
    engagement_rate: float
    avg_likes: int
    avg_comments: int
    categories: list[str]
    bio: str
    collab_ratio: float
    content_style: str
    brand_fit_reasons: list[str]
    phone: str = ""  # for demo calls


CREATORS = [
    Creator(
        handle="jungha.0",
        name="Hayoung",
        name_kr="하영",
        followers=236_000,
        engagement_rate=0.74,
        avg_likes=1_746,
        avg_comments=48,
        categories=["fashion", "beauty", "model"],
        bio="Model & fashion creator. Premium aesthetic with editorial-style content.",
        collab_ratio=0.45,
        content_style="High-fashion editorial, clean minimalist shots, studio lighting. "
                       "Mix of Korean and English captions. Luxury brand partnerships.",
        brand_fit_reasons=[
            "Premium visual aesthetic aligns with Boksoondoga's artisanal positioning",
            "Fashion/beauty audience overlaps with premium alcohol demographic (25-35F)",
            "Editorial style elevates product imagery beyond typical influencer content",
            "236K followers provides broad reach for brand awareness campaign",
        ],
    ),
    Creator(
        handle="jayeonkim_",
        name="Jayeon Kim",
        name_kr="김자연",
        followers=10_000,
        engagement_rate=0.88,
        avg_likes=88,
        avg_comments=12,
        categories=["lifestyle", "business", "education"],
        bio="MIT MBA. Lifestyle & business content creator. Authentic storytelling.",
        collab_ratio=0.30,
        content_style="Thoughtful long-form captions, personal storytelling, lifestyle flat-lays. "
                       "Educational content about business and career. Bilingual KR/EN.",
        brand_fit_reasons=[
            "MIT MBA background adds credibility — 'smart choice' brand narrative",
            "Authentic storytelling style perfect for Boksoondoga's heritage story",
            "Higher engagement rate (0.88%) indicates deeply loyal audience",
            "Business/lifestyle niche reaches affluent, taste-conscious consumers",
        ],
    ),
    Creator(
        handle="hwajung95",
        name="Hwajung Chu",
        name_kr="추화정",
        followers=233_000,
        engagement_rate=0.95,
        avg_likes=2_213,
        avg_comments=72,
        categories=["music", "model", "lifestyle"],
        bio="Vocalist & model. Bilingual KR/CN. Highest video view counts.",
        collab_ratio=0.52,
        content_style="Dynamic video content, music performances, behind-the-scenes. "
                       "Bilingual Korean/Chinese captions. High production value reels.",
        brand_fit_reasons=[
            "Highest engagement rate (0.95%) among large accounts — content resonates deeply",
            "Video-first creator ideal for Boksoondoga's visual storytelling",
            "Bilingual KR/CN opens Chinese market — Boksoondoga's export opportunity",
            "Vocalist/artist identity matches brand's artisanal craft positioning",
        ],
    ),
    Creator(
        handle="bling_cuh__",
        name="Bling Chu",
        name_kr="블링츄",
        followers=26_000,
        engagement_rate=1.81,
        avg_likes=470,
        avg_comments=38,
        categories=["product review", "beauty", "lifestyle"],
        bio="Product reviewer. 88% collab ratio. Highest engagement of all candidates.",
        collab_ratio=0.88,
        content_style="Detailed product reviews, unboxing, before/after comparisons. "
                       "Honest and relatable tone. Heavy use of Korean slang and humor.",
        brand_fit_reasons=[
            "1.81% engagement rate — highest of all candidates, audience trusts her reviews",
            "88% collab ratio proves track record of successful brand partnerships",
            "Product review format ideal for showcasing Boksoondoga tasting experience",
            "Relatable, honest tone builds consumer trust for premium product trial",
        ],
    ),
]

# Map handle → Creator for easy lookup
CREATOR_MAP = {c.handle: c for c in CREATORS}


def get_creator(handle: str) -> Creator:
    """Get a creator by handle (with or without @)."""
    handle = handle.lstrip("@")
    return CREATOR_MAP[handle]


def all_creators() -> list[Creator]:
    return list(CREATORS)


if __name__ == "__main__":
    for c in CREATORS:
        print(f"\n@{c.handle} ({c.name_kr} / {c.name})")
        print(f"  Followers: {c.followers:,} | Engagement: {c.engagement_rate}%")
        print(f"  Avg Likes: {c.avg_likes:,} | Avg Comments: {c.avg_comments}")
        print(f"  Categories: {', '.join(c.categories)}")
        print(f"  Collab Ratio: {c.collab_ratio:.0%}")
        print(f"  Brand Fit: {c.brand_fit_reasons[0]}")
