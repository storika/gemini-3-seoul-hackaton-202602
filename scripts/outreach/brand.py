"""
Boksoondoga (복순도가) brand data for content generation.
"""

BRAND = {
    "name_kr": "복순도가",
    "name_en": "Boksoondoga",
    "tagline_kr": "제주 전통 쌀 막걸리",
    "tagline_en": "Jeju Premium Rice Wine",
    "founded": 2012,
    "origin": "Jeju Island, South Korea",
    "story": (
        "복순도가 is a premium craft makgeolli (rice wine) born on Jeju Island. "
        "Founded in 2012, it revives traditional Korean brewing with Jeju's pristine water "
        "and locally grown rice. The name '복순도가' comes from the founder's grandmother, "
        "representing generational craft passed down through family. Each bottle is naturally "
        "fermented — no artificial additives, no pasteurization — creating a living, "
        "breathing drink that embodies Jeju's terroir."
    ),
    "products": [
        {
            "name_kr": "복순도가 손막걸리",
            "name_en": "Boksoondoga Son Makgeolli",
            "type": "Traditional Makgeolli",
            "abv": 6.0,
            "description": "Handcrafted unfiltered rice wine. Creamy, slightly sweet, naturally carbonated.",
            "price_range": "₩12,000-15,000",
            "visual": "Milky white in traditional ceramic bottle, elegant minimalist label",
        },
        {
            "name_kr": "복순도가 스파클링",
            "name_en": "Boksoondoga Sparkling",
            "type": "Sparkling Makgeolli",
            "abv": 5.0,
            "description": "Naturally sparkling rice wine. Lighter, effervescent, champagne-like finish.",
            "price_range": "₩15,000-18,000",
            "visual": "Clear glass bottle with modern label, golden-white liquid with fine bubbles",
        },
    ],
    "values": [
        "Jeju terroir and local ingredients",
        "Traditional brewing meets modern craft",
        "Natural fermentation, no additives",
        "Generational heritage and family story",
        "Premium positioning — not commodity makgeolli",
    ],
    "visual_identity": {
        "colors": ["Warm white (#F5F0E8)", "Jeju volcanic black (#1A1A1A)", "Soft gold (#C4A86B)"],
        "mood": "Clean, premium, artisanal. Jeju nature + modern minimalism.",
        "photography_style": "Natural light, Jeju landscapes, craft process shots, lifestyle moments",
        "avoid": "Cheap party vibes, overcrowded visuals, neon colors, generic stock feel",
    },
    "target_audience": {
        "primary": "Korean women 25-35, urban professionals, interested in premium food/drink",
        "secondary": "International foodies, K-culture enthusiasts, craft alcohol connoisseurs",
        "psychographic": "Values authenticity, willing to pay premium for craft quality, "
                         "Instagram-active, seeks 'hidden gem' discoveries",
    },
    "social_presence": {
        "instagram": "@boksoondoga",
        "website_kr": "https://boksoondoga.com",
        "website_en": "https://en.boksoondoga.com",
    },
    "campaign_goal": (
        "Partner with 4 carefully selected creators to produce authentic, "
        "personalized content that positions 복순도가 as the premium makgeolli "
        "choice for modern Korean lifestyle. Each creator brings a unique angle — "
        "fashion aesthetic, intellectual credibility, artistic expression, and "
        "trusted product reviews."
    ),
    "key_hashtags": [
        "#복순도가", "#boksoondoga", "#제주막걸리", "#프리미엄막걸리",
        "#전통주", "#크래프트막걸리", "#제주도", "#makgeolli",
    ],
}


def brand_summary() -> str:
    """One-paragraph brand summary for prompt injection."""
    b = BRAND
    return (
        f"{b['name_kr']} ({b['name_en']}) — {b['tagline_en']}. "
        f"Founded {b['founded']} on {b['origin']}. "
        f"Products: {b['products'][0]['name_en']} ({b['products'][0]['abv']}% ABV) and "
        f"{b['products'][1]['name_en']} ({b['products'][1]['abv']}% ABV). "
        f"Values: {', '.join(b['values'][:3])}. "
        f"Target: {b['target_audience']['primary']}."
    )


def brand_visual_prompt() -> str:
    """Visual style guide for image/video generation prompts."""
    v = BRAND["visual_identity"]
    return (
        f"Visual style: {v['mood']} "
        f"Colors: {', '.join(v['colors'])}. "
        f"Photography: {v['photography_style']}. "
        f"AVOID: {v['avoid']}."
    )


if __name__ == "__main__":
    print("=== Brand Summary ===")
    print(brand_summary())
    print("\n=== Visual Prompt ===")
    print(brand_visual_prompt())
    print(f"\n=== Products ({len(BRAND['products'])}) ===")
    for p in BRAND["products"]:
        print(f"  {p['name_kr']} — {p['type']}, {p['abv']}% ABV")
