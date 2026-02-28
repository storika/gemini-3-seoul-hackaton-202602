"""
Generate hyper-personalized Korean call scripts using Gemini 3 Flash.
Each script references the creator's real data.
Output: output/scripts/{handle}.txt
"""

import os
import pathlib
from google import genai

from creators import all_creators, Creator
from brand import BRAND, brand_summary

OUTPUT_DIR = pathlib.Path(__file__).parent / "output" / "scripts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def build_prompt(creator: Creator) -> str:
    return f"""당신은 복순도가(Boksoondoga) 브랜드의 인플루언서 마케팅 매니저입니다.
아래 크리에이터에게 협업을 제안하는 전화 통화 스크립트를 작성해주세요.

=== 브랜드 정보 ===
{brand_summary()}
캠페인 목표: {BRAND['campaign_goal']}

=== 크리에이터 정보 ===
- 인스타그램: @{creator.handle} ({creator.name_kr} / {creator.name})
- 팔로워: {creator.followers:,}명
- 인게이지먼트: {creator.engagement_rate}%
- 평균 좋아요: {creator.avg_likes:,} | 평균 댓글: {creator.avg_comments}
- 카테고리: {', '.join(creator.categories)}
- 콘텐츠 스타일: {creator.content_style}
- 협업 비율: {creator.collab_ratio:.0%}
- 브랜드 핏:
{chr(10).join(f'  • {reason}' for reason in creator.brand_fit_reasons)}

=== 스크립트 요구사항 ===
1. 한국어로 작성 (자연스러운 대화체)
2. 60-90초 분량 (약 200-300자)
3. 크리에이터의 실제 데이터를 구체적으로 언급 (팔로워 수, 인게이지먼트, 콘텐츠 스타일)
4. 왜 이 크리에이터가 복순도가에 완벽한 파트너인지 설명
5. 자연스럽고 따뜻한 톤 — 비즈니스 제안이지만 진정성 있게
6. 마지막에 다음 단계 제안 (미팅, 제품 발송 등)

스크립트만 작성해주세요. 제목이나 설명 없이 바로 대사로 시작하세요."""


def generate_script(creator: Creator) -> str:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=build_prompt(creator),
    )
    return response.text


def main():
    print("Generating personalized call scripts...\n")
    for creator in all_creators():
        print(f"  @{creator.handle} ({creator.name_kr})...", end=" ", flush=True)
        script = generate_script(creator)
        out_path = OUTPUT_DIR / f"{creator.handle}.txt"
        out_path.write_text(script, encoding="utf-8")
        print(f"✓ ({len(script)} chars)")

    print(f"\nDone! Scripts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
