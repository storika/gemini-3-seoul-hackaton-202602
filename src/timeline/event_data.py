"""Timeline events for Korean Soju brand wars + influencer model evolution (1924-2026).

Each event includes KG mutations, Veo 3.1 video prompts, and news headlines.
"""

from __future__ import annotations

from datetime import datetime

from .events import TimelineEvent, KGMutation

# ── helpers ──────────────────────────────────────────────────────────────────


def _node(node_id: str, node_type: str, label: str, brand: str) -> KGMutation:
    return KGMutation(action="add_node", node_id=node_id, node_type=node_type, label=label, brand=brand)


def _edge(source: str, target: str, relation: str) -> KGMutation:
    return KGMutation(action="add_edge", source=source, target=target, relation=relation)


def _dt(y: int, m: int, d: int = 15) -> datetime:
    return datetime(y, m, d)


# ── Soju Brand + Influencer events ──────────────────────────────────────────

TIMELINE_EVENTS: list[TimelineEvent] = [
    # 1 ─ 진로 탄생
    TimelineEvent(
        id="soju-001",
        date=_dt(1924, 1),
        brand="jinro",
        title="Jinro Founded: Birth of Korean Soju",
        title_ko="진로(JINRO)의 탄생: 민족의 소주",
        description="진천양조상회에서 진로 소주 탄생. 35도의 독한 술로 시작된 한국 소주의 원천. 평남 용강군에서 시작해 대한민국을 대표하는 주류 브랜드로 성장.",
        category="founding",
        industry="soju",
        impact_score=5.0,
        kg_mutations=[
            _node("jinro", "brand", "Jinro (진로)", "jinro"),
            _node("jinro_origin", "event", "Pyeongnam Yonggang Founding", "jinro"),
            _node("korea_soju_market", "market", "Korea Soju Market", "jinro"),
            _node("traditional_soju", "product", "Traditional Soju (35도)", "jinro"),
            _edge("jinro", "jinro_origin", "FOUNDED_IN"),
            _edge("jinro", "korea_soju_market", "ACTIVE_IN_MARKET"),
            _edge("jinro", "traditional_soju", "PRODUCES"),
        ],
        video_prompt="Historic Korean distillery in 1924: grainy sepia-tone footage of traditional soju production. Workers hand-crafting bottles in a small Pyeongnam workshop. Steam rising from copper stills. Text: '진로'. Documentary restoration style.",
        news_headlines=[
            "[1924] 일제강점기, 조선 민족 자본으로 양조업 시작 — 독립운동 자금 조성 배경",
            "[1920s] 세계적 금주법 시대 (미국 Prohibition), 반면 동아시아 주류산업 성장기",
            "[1924] 조선총독부 주세령 하에서도 민족 브랜드로서의 상징적 의미",
        ],
        market_share={"진로": 5.0},
        market_sales={"진로": "~50만원 (추정)"},
    ),
    # 2 ─ 서울 이전 & 전국화
    TimelineEvent(
        id="soju-002",
        date=_dt(1954, 6),
        brand="jinro",
        title="Jinro Moves to Seoul, National Expansion",
        title_ko="진로 서울 이전, 전국화 시작",
        description="한국전쟁 이후 서울 영등포로 공장 이전. 전국 유통망 확보와 함께 대한민국 대표 소주로 자리잡기 시작.",
        category="expansion",
        industry="soju",
        impact_score=3.5,
        kg_mutations=[
            _node("seoul_factory", "market", "Seoul Yeongdeungpo Factory", "jinro"),
            _edge("jinro", "seoul_factory", "EXPANDED_TO"),
        ],
        video_prompt="Post-war Korea reconstruction: black and white footage of a new factory being built in Seoul Yeongdeungpo. Workers carrying soju cases onto trucks. Transition from rubble to a thriving production line. Hopeful, documentary style.",
        news_headlines=[
            "[1953] 한국전쟁 휴전 — 폐허 속 재건 시작, 국민 위안의 술문화 형성",
            "[1954] 이승만 정부 경제 부흥 정책, 경공업 중심 산업화 가속",
            "[1950s] 냉전 격화, 한미동맹 강화 — 미군 PX 통한 양주 문화 유입",
        ],
        market_share={"진로": 25.0},
        market_sales={"진로": "~120억원"},
    ),
    # 3 ─ 진로 시장 1위 등극
    TimelineEvent(
        id="soju-003",
        date=_dt(1970, 1),
        brand="jinro",
        title="Jinro Becomes #1 Soju Brand",
        title_ko="진로, 국내 소주 시장 점유율 1위",
        description="진로가 국내 소주 시장 점유율 1위를 달성. '소주=진로'라는 등식을 확립하며 한국 주류 산업의 절대 강자로 군림.",
        category="award",
        industry="soju",
        impact_score=4.0,
        kg_mutations=[
            _node("market_no1", "award", "Korea Soju Market #1", "jinro"),
            _edge("jinro", "market_no1", "ACHIEVED"),
        ],
        video_prompt="Market dominance: 1970s Korean bars and restaurants filled with Jinro bottles. Retro advertisements, neon signs. A montage of working-class Koreans sharing soju. Nostalgic, warm tones. Korean economic miracle backdrop.",
        news_headlines=[
            "[1970] 박정희 정부 새마을운동 — 경제 고도성장기, 노동자의 술 소주 수요 폭발",
            "[1972] 유신 헌법 선포 — 정치적 억압 속 서민의 위안이 된 소주 한 잔",
            "[1970s] 중동 건설 붐, 오일쇼크 — 고된 노동과 함께한 소주의 전성기",
        ],
        market_share={"진로": 50.0},
        market_sales={"진로": "~3,200억원"},
    ),
    # 4 ─ 참이슬 혁명
    TimelineEvent(
        id="soju-004",
        date=_dt(1998, 10),
        brand="chamisul",
        title="Chamisul Revolution: 'Soju is Purity'",
        title_ko="참이슬 혁명: '소주는 깨끗함이다'",
        description="23도 '참이슬'의 등장. 대나무 숯 정제 공법으로 소주 시장의 패러다임을 바꿈. 출시 6개월 만에 1억 병 판매라는 기록 수립.",
        category="product_launch",
        industry="soju",
        impact_score=5.0,
        kg_mutations=[
            _node("chamisul", "product", "Chamisul (참이슬)", "chamisul"),
            _node("bamboo_charcoal", "ingredient", "Bamboo Charcoal Filtration", "chamisul"),
            _node("hitejinro", "brand", "HiteJinro (하이트진로)", "chamisul"),
            _edge("hitejinro", "chamisul", "PRODUCES"),
            _edge("chamisul", "bamboo_charcoal", "HERO_INGREDIENT_OF"),
            _edge("jinro", "hitejinro", "EVOLVED_INTO"),
        ],
        video_prompt="Revolutionary product launch: Chamisul soju bottle emerging from a cascade of bamboo charcoal. Filtration process in dramatic close-up. 1998 Korea: IMF crisis backdrop, people finding comfort in a clean new soju. Text: '참이슬'. Cinematic, emotional.",
        news_headlines=[
            "[1997] IMF 외환위기 — 대한민국 경제 패닉, 서민경제 붕괴의 시대",
            "[1998] 금모으기 운동 — 국난 극복의 국민적 단결, 위기 속 위안의 술문화",
            "[1999] 김대중 정부 구조조정 — 대량 실업, 소주 소비량 역대 최고 기록",
        ],
        market_share={"진로(참이슬)": 52.0, "경월소주": 12.0, "무학": 8.0},
        market_sales={"진로(참이슬)": "~4,800억원", "경월소주": "~1,100억원", "무학": "~740억원"},
    ),
    # 5 ─ 이영애 참이슬 모델
    TimelineEvent(
        id="soju-005",
        date=_dt(1999, 3),
        brand="chamisul",
        title="Lee Young-ae: First Icon of Chamisul",
        title_ko="이영애, 참이슬 첫 아이콘",
        description="대장금 이전의 이영애가 참이슬의 '깨끗함' 이미지를 완성. 청순한 이미지로 소주 광고의 새로운 공식을 확립.",
        category="model_change",
        industry="soju",
        impact_score=4.0,
        kg_mutations=[
            _node("lee_youngae", "person", "Lee Young-ae (이영애)", "chamisul"),
            _node("purity_image", "event", "Purity Image Campaign", "chamisul"),
            _edge("lee_youngae", "chamisul", "ENDORSES"),
            _edge("lee_youngae", "purity_image", "ESTABLISHED"),
        ],
        video_prompt="Elegant 90s Korean advertisement: Lee Young-ae in a serene studio, pouring Chamisul into a glass. Soft lighting, minimalist set. Her gentle smile embodies purity. Transition to bamboo forest. Classic K-commercial aesthetic, nostalgic warmth.",
        news_headlines=[
            "[1999] IMF 구조조정 한파 — 소주 한 잔이 유일한 위로가 된 실직 가장들의 시대",
            "[2000] 남북정상회담 (6.15 선언) — 화해 무드 속 '깨끗한 새 시작'의 국민 정서",
            "[2000s] 한류 1.0 시대 개막 — 겨울연가·대장금이 아시아를 휩쓸다",
        ],
        market_share={"참이슬": 54.0, "경월소주": 10.0, "무학": 7.5},
        market_sales={"참이슬": "~5,400억원", "경월소주": "~1,000억원", "무학": "~750억원"},
    ),
    # 6 ─ 처음처럼 출시
    TimelineEvent(
        id="soju-006",
        date=_dt(2006, 2),
        brand="chum_churum",
        title="Chum Churum Launch: Alkaline Water Innovation",
        title_ko="처음처럼 출시: 알칼리 환원수 혁신",
        description="롯데주류의 '처음처럼' 출시. 세계 최초 알칼리 환원수 소주로 참이슬 독주에 도전장을 던짐.",
        category="product_launch",
        industry="soju",
        impact_score=4.5,
        kg_mutations=[
            _node("chum_churum", "product", "Chum Churum (처음처럼)", "chum_churum"),
            _node("alkaline_water", "ingredient", "Alkaline Reduced Water", "chum_churum"),
            _node("lotte_liquor", "brand", "Lotte Liquor (롯데주류)", "chum_churum"),
            _edge("lotte_liquor", "chum_churum", "PRODUCES"),
            _edge("chum_churum", "alkaline_water", "HERO_INGREDIENT_OF"),
        ],
        video_prompt="Product innovation reveal: Chum Churum bottle with molecular visualization of alkaline reduced water. Lab science meets Korean drinking culture. Smooth pour into a soju glass. Fresh, modern commercial aesthetic.",
        news_headlines=[
            "[2006] 노무현 정부 — 부동산 폭등, 사회 양극화 심화로 서민 불만 고조",
            "[2006] 월드컵 독일 대회, 한국 16강 탈락 — '붉은 악마' 세대의 아쉬움",
            "[2006] Web 2.0 시대, 싸이월드 전성기 — 디지털 소통 문화의 확산",
        ],
        market_share={"참이슬": 52.0, "처음처럼": 8.0, "무학": 7.0},
        market_sales={"참이슬": "~6,200억원", "처음처럼": "~960억원", "무학": "~840억원"},
    ),
    # 7 ─ 이효리 처음처럼
    TimelineEvent(
        id="soju-007",
        date=_dt(2006, 6),
        brand="chum_churum",
        title="Lee Hyori's 'Shake It': Marketing Revolution",
        title_ko="이효리의 '흔들어라': 마케팅 혁명",
        description="이효리의 '흔들어 마시는 소주' 캠페인이 전국적 화제. '참이슬 독주'를 깨고 시장 점유율 10%대 돌파. 소주 광고 역사상 가장 성공적인 바이럴 캠페인.",
        category="viral",
        industry="soju",
        impact_score=5.0,
        kg_mutations=[
            _node("lee_hyori", "person", "Lee Hyori (이효리)", "chum_churum"),
            _node("shake_behavior", "event", "Shake Drinking Culture", "chum_churum"),
            _node("shake_campaign", "event", "'Shake It' Campaign", "chum_churum"),
            _edge("lee_hyori", "chum_churum", "ENDORSES"),
            _edge("lee_hyori", "shake_behavior", "INTRODUCED"),
            _edge("shake_campaign", "shake_behavior", "CREATED"),
            _edge("shake_campaign", "chum_churum", "BOOSTED_AWARENESS"),
        ],
        video_prompt="Iconic marketing moment: Lee Hyori shaking a soju bottle in a vibrant recreation of the legendary commercial. 2006 Korean nightlife energy. Split screen: the shake gesture rippling through bars across Korea. Energetic, retro-modern style.",
        news_headlines=[
            "[2006] 북한 1차 핵실험 — 한반도 긴장 고조, 국민 불안 속 소비문화 변화",
            "[2007] 서브프라임 위기 전조 — 글로벌 금융 불안, 한국 수출 경기 정점",
            "[2008] 이명박 정부 출범, 광우병 촛불시위 — 정치 격변기의 대중문화 폭발",
        ],
        market_share={"참이슬": 50.0, "처음처럼": 13.5, "무학": 6.5},
        market_sales={"참이슬": "~6,500억원", "처음처럼": "~1,750억원", "무학": "~845억원"},
    ),
    # 8 ─ 참이슬 도수 인하 경쟁
    TimelineEvent(
        id="soju-008",
        date=_dt(2012, 1),
        brand="chamisul",
        title="ABV Wars: Soju Gets Lighter",
        title_ko="도수 인하 전쟁: 소주가 가벼워지다",
        description="참이슬 19.5도 → 17.8도까지 도수 인하 경쟁 심화. 처음처럼도 17도대로 맞불. 여성·젊은 층 소비자 확대가 목표.",
        category="market_shift",
        industry="soju",
        impact_score=3.5,
        kg_mutations=[
            _node("abv_wars", "event", "ABV Lowering Wars", "chamisul"),
            _node("young_consumers", "market", "Young & Female Consumers", "chamisul"),
            _edge("chamisul", "abv_wars", "TRIGGERED"),
            _edge("chum_churum", "abv_wars", "TRIGGERED"),
            _edge("abv_wars", "young_consumers", "TARGETS_DEMOGRAPHIC"),
        ],
        video_prompt="Market shift visualization: soju bottles with ABV numbers ticking down from 23 to 17.8. Infographic style: old generation (35도) vs new generation (17도). Young Korean professionals at modern bars. Data-driven documentary style.",
        news_headlines=[
            "[2012] 박근혜-문재인 대선 — 세대 갈등 심화, MZ 정치 참여 시작",
            "[2012] 싸이 '강남스타일' 빌보드 2위 — 한류 글로벌화의 새 장",
            "[2013] 세월호 이전, 경제민주화 논쟁 — 사회 전반의 변화 요구",
        ],
        market_share={"참이슬": 48.0, "처음처럼": 16.5, "무학": 5.5},
        market_sales={"참이슬": "~7,200억원", "처음처럼": "~2,475억원", "무학": "~825억원"},
    ),
    # 9 ─ 아이유 참이슬
    TimelineEvent(
        id="soju-009",
        date=_dt(2014, 6),
        brand="chamisul",
        title="IU: The Longest-Running Soju Model Icon",
        title_ko="아이유의 참이슬: 이슬의 인간화",
        description="역대 최장수 모델 아이유가 참이슬의 얼굴이 됨. 젊은 층과 여성 고객을 완전히 흡수한 '깨끗함'의 상징. 소주 모델 역사의 새로운 장을 열다.",
        category="model_change",
        industry="soju",
        impact_score=5.0,
        kg_mutations=[
            _node("iu", "person", "IU (아이유)", "chamisul"),
            _node("purity_symbol", "event", "IU = Living Purity Symbol", "chamisul"),
            _node("longest_model", "award", "Longest-Running Soju Model", "chamisul"),
            _edge("iu", "chamisul", "ENDORSES"),
            _edge("iu", "purity_symbol", "SYMBOLIZES"),
            _edge("iu", "longest_model", "ACHIEVED"),
        ],
        video_prompt="Celebrity meets brand: IU in a clean, dewy Chamisul commercial. Glass-skin close-up, soft lighting. Transition from product shot to her gentle smile. A montage of her Chamisul campaigns across years. Text: '처음처럼 깨끗한'. Pure, aspirational.",
        news_headlines=[
            "[2014] 세월호 참사 — 대한민국 사회 전체가 애도에 잠기다, 안전 불감증 각성",
            "[2016] 촛불혁명, 박근혜 탄핵 — 시민 민주주의의 승리, 국민 정서 대전환",
            "[2020] COVID-19 팬데믹 — K-방역 세계 주목, '집콕 문화' 속 홈술 시대 개막",
        ],
        market_share={"참이슬": 50.5, "처음처럼": 15.0, "무학": 5.0},
        market_sales={"참이슬": "~8,600억원", "처음처럼": "~2,550억원", "무학": "~850억원"},
    ),
    # 10 ─ 참이슬 vs 처음처럼 전면전
    TimelineEvent(
        id="soju-010",
        date=_dt(2017, 1),
        brand="multi",
        title="Peak Soju Wars: Chamisul vs Chum Churum",
        title_ko="소주 전쟁 최고조: 참이슬 vs 처음처럼",
        description="아이유(참이슬) vs 수지(처음처럼), 소주 모델 대결이 소비자 문화현상으로 확대. 편의점 앞 포스터 전쟁, SNS 팬덤 대결까지.",
        category="viral",
        industry="soju",
        impact_score=4.0,
        kg_mutations=[
            _node("suzy", "person", "Suzy (수지)", "chum_churum"),
            _node("soju_wars_peak", "event", "IU vs Suzy Soju Model Wars", "multi"),
            _edge("suzy", "chum_churum", "ENDORSES"),
            _edge("soju_wars_peak", "iu", "FEATURES"),
            _edge("soju_wars_peak", "suzy", "FEATURES"),
        ],
        video_prompt="Cultural phenomenon: split screen of IU (Chamisul) and Suzy (Chum Churum) advertisements side by side. Convenience store poster battles. SNS fan wars montage. Korean pop culture meets soju marketing. Dramatic, documentary style.",
        news_headlines=[
            "[2017] 문재인 정부 출범 — 촛불 이후 개혁 기대감, 청년 실업 사회문제화",
            "[2017] BTS 빌보드 진출 — K-POP 글로벌 패권 시대, 팬덤 경제의 폭발",
            "[2018] 남북정상회담 판문점 — 한반도 평화 무드, 국민 희망의 순간",
        ],
        market_share={"참이슬": 48.0, "처음처럼": 17.0, "무학": 5.0},
        market_sales={"참이슬": "1조 600억원", "처음처럼": "~3,740억원", "무학": "~1,100억원"},
    ),
    # 11 ─ 진로이즈백
    TimelineEvent(
        id="soju-011",
        date=_dt(2019, 4),
        brand="jinro",
        title="Jinro Is Back: Retro Revival Phenomenon",
        title_ko="진로이즈백: 레트로 부활 현상",
        description="하이트진로가 '진로이즈백'으로 레트로 소주 열풍 주도. 두꺼비 캐릭터와 옛날 진로 디자인 복각으로 MZ 세대 공략 대성공.",
        category="product_launch",
        industry="soju",
        impact_score=4.5,
        kg_mutations=[
            _node("jinro_is_back", "product", "Jinro Is Back (진로이즈백)", "jinro"),
            _node("toad_character", "person", "Toad Character (두꺼비)", "jinro"),
            _node("retro_trend", "event", "Retro Revival Trend", "jinro"),
            _edge("hitejinro", "jinro_is_back", "PRODUCES"),
            _edge("toad_character", "jinro_is_back", "ENDORSES"),
            _edge("jinro_is_back", "retro_trend", "RODE"),
        ],
        video_prompt="Retro revival: old-school Jinro bottle design with the iconic toad character. Split between 1970s grainy footage and modern bars. Young people excitedly discovering their grandparents' soju. Nostalgic yet fresh, Instagram-worthy aesthetic.",
        news_headlines=[
            "[2019] 일본 수출규제 (노재팬 운동) — 경제 보복에 분노한 국민, 국산품 애용 붐",
            "[2019] 홍콩 민주화 시위, 미중 무역전쟁 격화 — 동아시아 질서 재편기",
            "[2020] 코로나19 팬데믹 시작 — '레트로 향수'와 '뉴트로 문화'로 위안 찾는 MZ세대",
        ],
        market_share={"참이슬": 43.0, "진로이즈백": 7.0, "처음처럼": 15.5, "무학": 4.5},
        market_sales={"참이슬": "~9,900억원", "진로이즈백": "~1,610억원", "처음처럼": "~3,570억원", "무학": "~1,035억원"},
    ),
    # 12 ─ 새로 출시 (제로 슈거)
    TimelineEvent(
        id="soju-012",
        date=_dt(2022, 9),
        brand="saero",
        title="Saero Launch: Zero Sugar Revolution",
        title_ko="새로 출시: 제로 슈거 혁명",
        description="롯데칠성 '새로' 출시. 당류 0% 제로 슈거 소주와 버추얼 캐릭터 '새로구미'로 MZ 세대 열광. 소주 업계의 판을 흔든 게임 체인저.",
        category="product_launch",
        industry="soju",
        impact_score=5.0,
        kg_mutations=[
            _node("saero", "product", "Saero (새로)", "saero"),
            _node("zero_sugar", "ingredient", "Zero Sugar Formula", "saero"),
            _node("saerogumi", "person", "Saerogumi (새로구미)", "saero"),
            _node("lotte_chilsung", "brand", "Lotte Chilsung (롯데칠성)", "saero"),
            _edge("lotte_chilsung", "saero", "PRODUCES"),
            _edge("saero", "zero_sugar", "HERO_INGREDIENT_OF"),
            _edge("saerogumi", "saero", "ENDORSES"),
            _edge("lotte_liquor", "lotte_chilsung", "EVOLVED_INTO"),
        ],
        video_prompt="MZ generation disruption: Saero soju bottle with Saerogumi virtual character animation. Zero sugar data overlay. Young Korean consumers at trendy bars. Split between animated character world and real-life nightlife. Vibrant, futuristic K-style.",
        news_headlines=[
            "[2022] 러시아-우크라이나 전쟁 — 글로벌 공급망 위기, 인플레이션 시대",
            "[2022] 윤석열 정부 출범 — MZ세대 정치 양극화, 건강·웰빙 트렌드 가속",
            "[2023] ChatGPT 열풍, AI 시대 본격 개막 — 기술이 소비문화를 바꾸다",
        ],
        market_share={"참이슬": 38.0, "새로": 10.0, "진로이즈백": 6.5, "처음처럼": 14.0},
        market_sales={"참이슬": "~9,120억원", "새로": "~2,400억원", "진로이즈백": "~1,560억원", "처음처럼": "~3,360억원"},
    ),
    # 13 ─ 참이슬 x 제로 대응
    TimelineEvent(
        id="soju-013",
        date=_dt(2023, 3),
        brand="chamisul",
        title="Chamisul Zero Sugar Counterattack",
        title_ko="참이슬, 제로 슈거 맞불 대응",
        description="새로의 제로 슈거 돌풍에 하이트진로가 '참이슬 제로 슈거'로 반격. 기존 브랜드 파워와 제로 트렌드를 결합.",
        category="market_shift",
        industry="soju",
        impact_score=3.5,
        kg_mutations=[
            _node("chamisul_zero", "product", "Chamisul Zero Sugar", "chamisul"),
            _edge("hitejinro", "chamisul_zero", "PRODUCES"),
            _edge("chamisul_zero", "zero_sugar", "CONTAINS_INGREDIENT"),
            _edge("chamisul_zero", "saero", "COMPETES_WITH"),
        ],
        video_prompt="Brand counterattack: Chamisul bottle transforming with a 'Zero Sugar' label materializing. Side-by-side with IU and Saerogumi. Market share graph showing the battle. Competitive, high-stakes business drama style.",
        news_headlines=[
            "[2023] 이스라엘-하마스 전쟁 — 세계 분쟁 다발, 글로벌 불확실성 최고조",
            "[2023] 금리 인상기, 영끌 세대 고통 — 소비 위축 속 '가성비' 재부상",
            "[2024] 한국 인구 자연감소 가속 — 저출생 위기 속 1인 가구 음주문화 변화",
        ],
        market_share={"참이슬": 36.0, "새로": 14.0, "진로이즈백": 6.0, "처음처럼": 13.0},
        market_sales={"참이슬": "~8,640억원", "새로": "~3,360억원", "진로이즈백": "~1,440억원", "처음처럼": "~3,120억원"},
    ),
    # 14 ─ 소주 글로벌 수출 급증
    TimelineEvent(
        id="soju-014",
        date=_dt(2024, 6),
        brand="multi",
        title="K-Soju Goes Global: Export Record",
        title_ko="K-Soju 글로벌화: 수출 역대 최고치",
        description="한류와 K-콘텐츠 효과로 소주 수출액 역대 최고치 경신. 미국, 동남아, 유럽에서 소주 수요 폭발. '소주=한국' 등식 확립.",
        category="expansion",
        industry="soju",
        impact_score=4.0,
        kg_mutations=[
            _node("global_ksoju", "market", "Global K-Soju Export", "multi"),
            _node("us_market", "market", "US Soju Market", "multi"),
            _node("sea_market", "market", "Southeast Asia Soju Market", "multi"),
            _edge("chamisul", "global_ksoju", "ACTIVE_IN_MARKET"),
            _edge("saero", "global_ksoju", "ACTIVE_IN_MARKET"),
            _edge("jinro_is_back", "global_ksoju", "ACTIVE_IN_MARKET"),
            _edge("global_ksoju", "us_market", "INCLUDES"),
            _edge("global_ksoju", "sea_market", "INCLUDES"),
        ],
        video_prompt="Global expansion montage: Korean soju bottles on shelves in New York, Tokyo, Paris, Bangkok. Diverse international consumers trying soju for the first time. World map with export routes glowing. K-wave meets spirits industry. Cinematic, triumphant.",
        news_headlines=[
            "[2024] 미국 대선 트럼프 재당선 — 보호무역주의 강화, 글로벌 통상 지형 변화",
            "[2024] K-콘텐츠 글로벌 최전성기 — 넷플릭스·K-POP이 만든 한국 소프트파워",
            "[2024] 글로벌 인플레이션 완화 조짐 — 소비 심리 회복, 프리미엄 주류 수요 증가",
        ],
        market_share={"참이슬": 34.0, "새로": 17.0, "진로이즈백": 5.5, "처음처럼": 12.0},
        market_sales={"참이슬": "~8,500억원", "새로": "~4,250억원", "진로이즈백": "~1,375억원", "처음처럼": "~3,000억원"},
    ),
    # 15 ─ AI 마케팅 시대
    TimelineEvent(
        id="soju-015",
        date=_dt(2025, 6),
        brand="multi",
        title="AI-Powered Soju Marketing Begins",
        title_ko="AI 소주 마케팅 시대 개막",
        description="하이트진로·롯데칠성 모두 AI 기반 소비자 분석 및 타겟 마케팅 도입. 100년 역사 데이터와 실시간 트렌드를 결합한 하이퍼-타겟팅 전략.",
        category="market_shift",
        industry="soju",
        impact_score=3.5,
        kg_mutations=[
            _node("ai_marketing", "event", "AI-Powered Marketing Era", "multi"),
            _edge("ai_marketing", "chamisul", "OPTIMIZES"),
            _edge("ai_marketing", "saero", "OPTIMIZES"),
            _edge("ai_marketing", "hitejinro", "ADOPTED_BY"),
            _edge("ai_marketing", "lotte_chilsung", "ADOPTED_BY"),
        ],
        video_prompt="Futuristic marketing: holographic data dashboards analyzing 100 years of soju consumer data. AI algorithms matching models to demographics. Split between traditional Korean drinking culture and cutting-edge AI visualization. Sci-fi meets tradition.",
        news_headlines=[
            "[2025] AI가 일상이 된 시대 — Gemini·Claude 등 AI 에이전트 활용 보편화",
            "[2025] 한국 1인당 GDP 4만 달러 돌파 — 선진국 반열, 소비문화 고급화",
            "[2025] 기후위기 가속, ESG 경영 필수화 — 친환경 패키징·저탄소 제조 트렌드",
        ],
        market_share={"참이슬": 33.0, "새로": 19.0, "처음처럼": 11.0, "진로이즈백": 5.0},
        market_sales={"참이슬": "~8,250억원", "새로": "~4,750억원", "처음처럼": "~2,750억원", "진로이즈백": "~1,250억원"},
    ),
    # 16 ─ Space-Time Director 2026
    TimelineEvent(
        id="soju-016",
        date=_dt(2026, 1),
        brand="multi",
        title="Space-Time AI Director: 100 Years of Soju Intelligence",
        title_ko="Space-Time AI 디렉터: 소주 100년의 지능",
        description="100년의 역사적 데이터, 뉴스, 인플루언서 영향력, 소비자 심리를 통합한 AI 디렉터 시스템. 최적의 모델-브랜드 매칭과 캠페인 전략을 자동 도출.",
        category="market_shift",
        industry="soju",
        impact_score=4.5,
        kg_mutations=[
            _node("spacetime_director", "event", "Space-Time AI Director System", "multi"),
            _edge("spacetime_director", "ai_marketing", "EVOLVES_FROM"),
            _edge("spacetime_director", "global_ksoju", "DRIVES"),
        ],
        video_prompt="Grand finale: holographic timeline of 100 years of soju history, all brands and models appearing in sequence. AI system analyzing every data point. Convergence into a unified intelligence. Text: 'Space-Time Director'. Epic, cinematic masterpiece.",
        news_headlines=[
            "[2026] AGI 논쟁 본격화 — AI가 인간의 창의성을 대체할 것인가",
            "[2026] 한반도 정세 새 국면 — 남북 경제협력 재논의, 통일 담론 부활",
            "[2026] 소주 100주년 (1924-2026) — 한 세기의 민족 음료, 글로벌 K-Spirit로 진화",
        ],
        market_share={"참이슬": 31.0, "새로": 21.0, "처음처럼": 10.5, "진로이즈백": 5.0},
        market_sales={"참이슬": "~8,060억원", "새로": "~5,460억원", "처음처럼": "~2,730억원", "진로이즈백": "~1,300억원"},
    ),
]
