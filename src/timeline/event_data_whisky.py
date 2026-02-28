"""Timeline events for Johnnie Walker Scotch Whisky brand evolution (1820-2026).

Each event includes KG mutations, Veo 3.1 video prompts, and news headlines.
Mirrors the soju event_data.py pattern but for the whisky industry.
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


# ── Johnnie Walker Brand + Ambassador events ────────────────────────────────

WHISKY_TIMELINE_EVENTS: list[TimelineEvent] = [
    # 1 ─ 존 워커 킬마녹 식료품점 개업
    TimelineEvent(
        id="jw-001",
        date=_dt(1820, 1),
        brand="jw_global",
        title="John Walker Opens His Shop in Kilmarnock",
        title_ko="존 워커, 킬마녹 식료품점 개업",
        description="존 워커가 스코틀랜드 킬마녹에서 식료품점을 열고 위스키 블렌딩을 시작. 아들 알렉산더 워커가 'Old Highland Whisky'를 만들며 브랜드 본격화. 200년 위스키 제국의 시초.",
        category="founding",
        industry="whisky",
        impact_score=5.0,
        kg_mutations=[
            _node("johnnie_walker", "brand", "Johnnie Walker (조니워커)", "jw_global"),
            _node("john_walker", "person", "John Walker (존 워커)", "jw_global"),
            _node("kilmarnock", "market", "Kilmarnock, Scotland", "jw_global"),
            _node("scotch_whisky_market", "market", "Scotch Whisky Market", "jw_global"),
            _edge("john_walker", "johnnie_walker", "FOUNDED"),
            _edge("johnnie_walker", "kilmarnock", "FOUNDED_IN"),
            _edge("johnnie_walker", "scotch_whisky_market", "ACTIVE_IN_MARKET"),
        ],
        video_prompt="Historic Scottish grocery shop in 1820: atmospheric footage of a stone-built Kilmarnock shop. John Walker blending whisky by hand among barrels and shelves of provisions. Warm candlelight, period costumes. Text: 'Johnnie Walker'. Documentary restoration style.",
        news_headlines=[
            "[1820] 조지 4세 즉위 — 영국 산업혁명 가속기, 스코틀랜드 위스키 산업 태동",
            "[1820s] 세금 완화와 합법 증류소 시대 — 밀조 시대 종식의 서막",
            "[1823] 영국 소비세법(Excise Act) — 합법 위스키 생산의 새 시대",
        ],
        market_share={"조니워커": 1.0},
        market_sales={"조니워커": "~미상"},
    ),
    # 2 ─ 사각형 병 & 24도 라벨 도입
    TimelineEvent(
        id="jw-002",
        date=_dt(1860, 6),
        brand="jw_global",
        title="Square Bottle & 24° Angled Label",
        title_ko="사각형 병 & 24도 기울어진 라벨 도입",
        description="운송 시 깨짐 방지를 위한 사각형 병과 진열대에서 눈에 띄는 24도 기울어진 라벨 도입. 아들 알렉산더 워커의 혁신으로 조니워커의 아이코닉한 패키지 디자인 확립.",
        category="product_launch",
        industry="whisky",
        impact_score=3.5,
        kg_mutations=[
            _node("square_bottle", "product", "Square Bottle Design", "jw_global"),
            _node("alexander_walker", "person", "Alexander Walker", "jw_global"),
            _edge("alexander_walker", "square_bottle", "DESIGNED"),
            _edge("johnnie_walker", "square_bottle", "ADOPTED"),
        ],
        video_prompt="Victorian-era innovation: close-up of the iconic square bottle being crafted by hand. Side-by-side comparison with round bottles breaking during transport. The 24-degree angled label being applied. Elegant, product design documentary style.",
        news_headlines=[
            "[1860] 빅토리아 여왕 시대 — 대영제국 전성기, 글로벌 무역 확대",
            "[1860s] 스코틀랜드 위스키의 국제 수출 본격화",
            "[1865] 'Old Highland Whisky' 브랜드 확립, 글로벌 유통 시작",
        ],
        market_share={"조니워커": 3.0},
        market_sales={"조니워커": "~미상"},
    ),
    # 3 ─ 스트라이딩 맨 로고 탄생
    TimelineEvent(
        id="jw-003",
        date=_dt(1908, 3),
        brand="jw_global",
        title="The Striding Man Logo Is Born",
        title_ko="스트라이딩 맨 로고 탄생",
        description="Tom Browne이 탑햇과 테일코트를 입고 활보하는 신사 캐릭터를 디자인. 스피릿 브랜드 최초의 캐릭터 로고이자, 100년 넘게 사랑받는 아이코닉 심볼의 시작.",
        category="campaign",
        industry="whisky",
        impact_score=5.0,
        kg_mutations=[
            _node("striding_man", "product", "Striding Man Logo", "jw_global"),
            _node("tom_browne", "person", "Tom Browne (톰 브라운)", "jw_global"),
            _edge("tom_browne", "striding_man", "DESIGNED"),
            _edge("johnnie_walker", "striding_man", "ADOPTED"),
        ],
        video_prompt="Art history moment: illustrator Tom Browne sketching the Striding Man on parchment. The gentleman in top hat and tailcoat materializes from ink strokes. Evolution montage: 1908 original → modern minimalist. Art documentary style.",
        news_headlines=[
            "[1908] 에드워드 7세 시대 — 벨 에포크(아름다운 시대), 유럽 문화 전성기",
            "[1908] 광고 산업 성장기 — 브랜드 아이덴티티의 개념 등장",
            "[1909] Bernard Partridge 리디자인 — 도시적 세련미 추가",
        ],
        market_share={"조니워커": 5.0},
        market_sales={"조니워커": "~미상"},
    ),
    # 4 ─ 레드 & 블랙 라벨 명명
    TimelineEvent(
        id="jw-004",
        date=_dt(1909, 6),
        brand="multi",
        title="Red & Black Label Naming System",
        title_ko="레드 라벨 & 블랙 라벨 공식 명명",
        description="컬러 라벨 체계의 시작. 레드 라벨(블렌디드)과 블랙 라벨(12년 숙성)의 공식 명명으로 조니워커의 제품 포트폴리오 전략이 확립됨.",
        category="product_launch",
        industry="whisky",
        impact_score=4.5,
        kg_mutations=[
            _node("jw_red_label", "product", "Red Label (레드 라벨)", "jw_red"),
            _node("jw_black_label", "product", "Black Label (블랙 라벨)", "jw_black"),
            _edge("johnnie_walker", "jw_red_label", "PRODUCES"),
            _edge("johnnie_walker", "jw_black_label", "PRODUCES"),
        ],
        video_prompt="Brand architecture: two bottles side by side — vibrant red label and sophisticated black label emerging from a shared heritage. Color coding visualized as a revolutionary concept. Split-screen: elegant product showcase. Premium branding documentary.",
        news_headlines=[
            "[1909] 20세기 초 — 블렌디드 스카치 위스키의 황금기 시작",
            "[1909] 컬러 라벨 체계 — 소비자 직관적 제품 구분의 선구자",
            "[1910s] 1차 세계대전 전야 — 영국 제국 전성기, 스카치 수출 급증",
        ],
        market_share={"레드 라벨": 4.0, "블랙 라벨": 2.0},
        market_sales={"레드 라벨": "~미상", "블랙 라벨": "~미상"},
    ),
    # 5 ─ 왕실 보증 획득
    TimelineEvent(
        id="jw-005",
        date=_dt(1934, 1),
        brand="jw_global",
        title="Royal Warrant from King George V",
        title_ko="조지 5세 왕실 보증(Royal Warrant) 획득",
        description="영국 왕실이 조니워커를 공식 인정. 왕실 보증은 최고 품질의 상징으로, 조니워커의 프리미엄 포지셔닝을 공고히 함.",
        category="award",
        industry="whisky",
        impact_score=4.0,
        kg_mutations=[
            _node("royal_warrant", "award", "Royal Warrant (왕실 보증)", "jw_global"),
            _node("king_george_v", "person", "King George V", "jw_global"),
            _edge("king_george_v", "royal_warrant", "GRANTED"),
            _edge("johnnie_walker", "royal_warrant", "ACHIEVED"),
        ],
        video_prompt="Royal ceremony: King George V's seal being applied to Johnnie Walker certificate. Buckingham Palace backdrop. Transition to vintage Johnnie Walker bottles with Royal Warrant emblem. Regal, prestigious atmosphere.",
        news_headlines=[
            "[1934] 조지 5세 치세 — 대공황 이후 회복기, 영국 왕실의 권위 재확인",
            "[1934] 금주법 폐지(미국, 1933) 이후 — 글로벌 주류 시장 부활",
            "[1930s] 2차 세계대전 전운 — 유럽 긴장 고조",
        ],
        market_share={"조니워커": 12.0},
        market_sales={"조니워커": "~미상"},
    ),
    # 6 ─ 세계 1위 스카치
    TimelineEvent(
        id="jw-006",
        date=_dt(1945, 6),
        brand="jw_red",
        title="Red Label: World's #1 Scotch Whisky",
        title_ko="레드 라벨, 세계 최다 판매 스카치 등극",
        description="레드 라벨이 세계에서 가장 많이 팔리는 스카치 위스키의 자리에 오름. 글로벌 No.1 스카치 위스키의 지위를 확립.",
        category="award",
        industry="whisky",
        impact_score=5.0,
        kg_mutations=[
            _node("world_no1_scotch", "award", "World #1 Scotch Whisky", "jw_red"),
            _node("global_market", "market", "Global Scotch Market", "jw_red"),
            _edge("jw_red_label", "world_no1_scotch", "ACHIEVED"),
            _edge("jw_red_label", "global_market", "DOMINATES"),
        ],
        video_prompt="Post-war triumph: montage of Johnnie Walker Red Label bottles being shipped worldwide. Victory celebrations, soldiers toasting. Globe spinning with export routes illuminated. Triumphant, golden-age documentary.",
        news_headlines=[
            "[1945] 제2차 세계대전 종전 — 세계 재건의 시대, 축하의 술 수요 폭증",
            "[1945] UN 창설 — 새로운 국제 질서, 글로벌 무역 확대",
            "[1940s] 전후 경제 부흥 — 스카치 위스키의 글로벌 확산 가속",
        ],
        market_share={"레드 라벨": 20.0, "블랙 라벨": 8.0},
        market_sales={"레드 라벨": "~미상", "블랙 라벨": "~미상"},
    ),
    # 7 ─ 블루 라벨 출시
    TimelineEvent(
        id="jw-007",
        date=_dt(1992, 6),
        brand="jw_blue",
        title="Blue Label Launch: Ultra-Premium Standard",
        title_ko="블루 라벨 출시: 울트라 프리미엄의 새 기준",
        description="희귀 캐스크 핸드 셀렉트 원액만을 사용한 블루 라벨 출시. 울트라 프리미엄 블렌디드 스카치의 새 기준을 제시하며, 한국 시장에서 '성공'과 '축하'의 상징이 됨.",
        category="product_launch",
        industry="whisky",
        impact_score=5.0,
        kg_mutations=[
            _node("jw_blue_label", "product", "Blue Label (블루 라벨)", "jw_blue"),
            _node("ultra_premium", "market", "Ultra-Premium Whisky Market", "jw_blue"),
            _edge("johnnie_walker", "jw_blue_label", "PRODUCES"),
            _edge("jw_blue_label", "ultra_premium", "DEFINES"),
        ],
        video_prompt="Ultra-premium reveal: Blue Label bottle materializing in dramatic lighting. Master blender hand-selecting rare casks in an ancient warehouse. Liquid gold pouring into crystal glass. Luxurious, cinematic product showcase.",
        news_headlines=[
            "[1992] 냉전 종식 — 글로벌 경제 자유화, 럭셔리 소비 시대 개막",
            "[1992] 한국 경제 성장 — 프리미엄 수입 주류 수요 급증",
            "[1990s] 프리미엄 위스키 시장 급성장 — '블렌디드=저급'이라는 편견 타파",
        ],
        market_share={"레드 라벨": 18.0, "블랙 라벨": 12.0, "블루 라벨": 2.0},
        market_sales={"레드 라벨": "~미상", "블랙 라벨": "~미상", "블루 라벨": "~미상"},
    ),
    # 8 ─ 디아지오 출범
    TimelineEvent(
        id="jw-008",
        date=_dt(1997, 12),
        brand="jw_global",
        title="Diageo Formation: World's Largest Spirits Group",
        title_ko="디아지오(Diageo) 출범, 조니워커 편입",
        description="기네스(Guinness)와 그랜드 메트로폴리탄(Grand Metropolitan)의 합병으로 세계 최대 주류 그룹 디아지오 출범. 조니워커가 디아지오의 핵심 브랜드로 편입되며 글로벌 마케팅 역량 강화.",
        category="corporate",
        industry="whisky",
        impact_score=4.0,
        kg_mutations=[
            _node("diageo", "brand", "Diageo (디아지오)", "jw_global"),
            _edge("diageo", "johnnie_walker", "OWNS"),
            _edge("johnnie_walker", "diageo", "PART_OF"),
        ],
        video_prompt="Corporate mega-merger: Guinness and Grand Metropolitan logos merging into Diageo. Boardroom handshake. Johnnie Walker bottles showcased as crown jewel of the new group. Corporate documentary, sleek graphics.",
        news_headlines=[
            "[1997] 아시아 외환위기 — 글로벌 금융 불안 속 초대형 M&A",
            "[1997] 한국 IMF 구제금융 — 수입 주류 시장 일시 위축",
            "[1990s] 글로벌 주류 산업 통합 시대 — 거대 그룹 중심으로 재편",
        ],
        market_share={"레드 라벨": 17.0, "블랙 라벨": 13.0, "블루 라벨": 3.0},
        market_sales={"레드 라벨": "~미상", "블랙 라벨": "~미상", "블루 라벨": "~미상"},
    ),
    # 9 ─ Keep Walking 캠페인
    TimelineEvent(
        id="jw-009",
        date=_dt(1999, 6),
        brand="jw_global",
        title="'Keep Walking' Campaign: $2.2B Impact",
        title_ko="'Keep Walking' 캠페인 런칭",
        description="BBH London 제작, £1억 글로벌 론칭. 스트라이딩 맨 방향을 좌→우로 전환하여 '전진'의 의미 강화. 1999-2008년간 $22억 추가 매출 창출. 브랜드 역사상 가장 성공적인 캠페인.",
        category="campaign",
        industry="whisky",
        impact_score=5.0,
        kg_mutations=[
            _node("keep_walking", "event", "Keep Walking Campaign", "jw_global"),
            _node("harvey_keitel", "person", "Harvey Keitel (하비 카이텔)", "jw_red"),
            _node("bbh_london", "brand", "BBH London", "jw_global"),
            _edge("bbh_london", "keep_walking", "CREATED"),
            _edge("harvey_keitel", "jw_red_label", "ENDORSES"),
            _edge("keep_walking", "johnnie_walker", "BOOSTED_AWARENESS"),
            _edge("keep_walking", "striding_man", "REDESIGNED"),
        ],
        video_prompt="Legendary campaign launch: Harvey Keitel walking through a Roman colosseum with a lion. The Striding Man logo flipping direction left to right. 'KEEP WALKING' text materializing. Cinematic, epic advertising masterpiece recreation.",
        news_headlines=[
            "[1999] 밀레니엄 전야 — Y2K 불안과 새 시대에 대한 기대 공존",
            "[1999] 닷컴 버블 최고조 — 디지털 혁명 시대의 마케팅 패러다임 전환",
            "[1999] 스트라이딩 맨 방향 전환 — '전진=미래' 메시지의 시각적 혁신",
        ],
        market_share={"레드 라벨": 19.0, "블랙 라벨": 14.0, "블루 라벨": 4.0},
        market_sales={"조니워커 전체": "~$30억 (글로벌)"},
    ),
    # 10 ─ 로버트 칼라일 원테이크 광고
    TimelineEvent(
        id="jw-010",
        date=_dt(2009, 10),
        brand="jw_black",
        title="'The Man Who Walked Around The World'",
        title_ko="로버트 칼라일, 6.5분 원테이크 전설",
        description="로버트 칼라일이 스코틀랜드 해안을 걸으며 조니워커 브랜드 역사를 들려주는 6.5분 원테이크 광고. 광고 역사상 최장 트래킹 숏으로 기록.",
        category="campaign",
        industry="whisky",
        impact_score=4.5,
        kg_mutations=[
            _node("robert_carlyle", "person", "Robert Carlyle (로버트 칼라일)", "jw_black"),
            _node("walked_around_world", "event", "The Man Who Walked Around The World", "jw_black"),
            _edge("robert_carlyle", "jw_black_label", "ENDORSES"),
            _edge("robert_carlyle", "walked_around_world", "STARRED_IN"),
            _edge("walked_around_world", "keep_walking", "EXTENDS"),
        ],
        video_prompt="Legendary one-take: Robert Carlyle walking along a Scottish coastal path, narrating Johnnie Walker's 200-year history. Wind, waves, dramatic cliffs. Unbroken 6.5-minute tracking shot. Cinematic masterpiece, raw Scottish landscape.",
        news_headlines=[
            "[2009] 글로벌 금융위기 이후 회복기 — 프리미엄 브랜드 스토리텔링 시대",
            "[2009] 유튜브 시대 — 온라인 바이럴 광고의 새 지평",
            "[2009] 광고 역사상 최장 원테이크 트래킹 숏 — 영화적 광고의 정점",
        ],
        market_share={"레드 라벨": 18.0, "블랙 라벨": 16.0, "블루 라벨": 5.0},
        market_sales={"조니워커 전체": "~$40억 (글로벌)"},
    ),
    # 11 ─ 조니워커 하우스 서울
    TimelineEvent(
        id="jw-011",
        date=_dt(2013, 9),
        brand="jw_blue",
        title="Johnnie Walker House Seoul Opens",
        title_ko="조니워커 하우스 서울 오픈",
        description="전 세계 세 번째 조니워커 하우스가 서울에 오픈(상하이, 베이징 다음). 한국 시장에 대한 디아지오의 전략적 투자와 프리미엄 체험 마케팅의 시작.",
        category="expansion",
        industry="whisky",
        impact_score=3.5,
        kg_mutations=[
            _node("jw_house_seoul", "market", "JW House Seoul (조니워커 하우스 서울)", "jw_blue"),
            _node("korea_whisky_market", "market", "Korea Whisky Market", "jw_blue"),
            _node("jude_law", "person", "Jude Law (주드 로)", "jw_black"),
            _edge("johnnie_walker", "jw_house_seoul", "EXPANDED_TO"),
            _edge("jw_house_seoul", "korea_whisky_market", "TARGETS"),
            _edge("jude_law", "jw_black_label", "ENDORSES"),
        ],
        video_prompt="Luxury experience space: modern Seoul skyline transitioning into an elegant Johnnie Walker House interior. Whisky tasting sessions, rare bottle displays. Jude Law in 'A Gentleman's Wager' short film scenes. Premium Korean lifestyle.",
        news_headlines=[
            "[2013] 한국 프리미엄 주류 시장 성장 — 위스키 바 문화 확산",
            "[2013] 주드 로 'A Gentleman's Wager' — 단편영화 형식의 새로운 광고 실험",
            "[2013] 아시아 럭셔리 시장 확대 — 블루 라벨, '성공의 상징'으로 자리잡기",
        ],
        market_share={"블랙 라벨": 15.0, "블루 라벨": 8.0, "레드 라벨": 12.0},
        market_sales={"조니워커 한국": "~800억원 (추정)"},
    ),
    # 12 ─ 한국 하이볼 트렌드
    TimelineEvent(
        id="jw-012",
        date=_dt(2019, 6),
        brand="jw_red",
        title="Korean Highball Trend Goes Mainstream",
        title_ko="한국 하이볼 트렌드 본격화",
        description="디아지오 코리아가 레드 라벨 하이볼 바 프랜차이즈를 확대. 젊은 세대의 위스키 진입장벽을 낮추며 편의점·바에서 하이볼 문화를 주도.",
        category="market_shift",
        industry="whisky",
        impact_score=4.0,
        kg_mutations=[
            _node("highball_trend", "event", "Korean Highball Trend", "jw_red"),
            _node("diageo_korea", "brand", "Diageo Korea (디아지오 코리아)", "jw_global"),
            _node("mz_generation", "market", "MZ Generation Whisky Consumers", "jw_red"),
            _edge("diageo_korea", "highball_trend", "DROVE"),
            _edge("jw_red_label", "highball_trend", "BENEFITED_FROM"),
            _edge("highball_trend", "mz_generation", "TARGETS_DEMOGRAPHIC"),
        ],
        video_prompt="Trendy Korean bar scene: bartender crafting a perfect Johnnie Walker Red Label highball. Young Koreans clinking glasses. Convenience store shelves stocked with highball kits. Split: traditional whisky drinking vs modern highball culture. Vibrant, youthful energy.",
        news_headlines=[
            "[2019] 일본 불매운동 — 일본 위스키 대안으로 스카치 수요 급증",
            "[2019] 하이볼 바 프랜차이즈 확대 — 편의점에서도 하이볼 키트 판매",
            "[2019] MZ세대 음주 문화 변화 — '가볍고 세련되게' 트렌드",
        ],
        market_share={"레드 라벨": 22.0, "블랙 라벨": 14.0, "블루 라벨": 7.0},
        market_sales={"조니워커 한국": "~1,200억원 (추정)"},
    ),
    # 13 ─ CL 글로벌 캠페인 + 에든버러 센터
    TimelineEvent(
        id="jw-013",
        date=_dt(2021, 6),
        brand="jw_blue",
        title="CL: Asian Face of Keep Walking",
        title_ko="씨엘, Keep Walking 아시아 대표",
        description="2NE1 출신 CL(이채린)이 'Keep Walking' 글로벌 캠페인의 아시아 대표로 발탁. 한국 솔로 최초 빌보드 Top 100 기록 보유. 같은 해 에든버러 프린시스 스트리트에 £3,500만 방문객 센터 오픈.",
        category="model_change",
        industry="whisky",
        impact_score=4.0,
        kg_mutations=[
            _node("cl", "person", "CL (씨엘, 이채린)", "jw_blue"),
            _node("edinburgh_center", "market", "Edinburgh Visitor Centre", "jw_global"),
            _node("christina_hendricks", "person", "Christina Hendricks (크리스티나 헨드릭스)", "jw_blue"),
            _edge("cl", "jw_blue_label", "ENDORSES"),
            _edge("cl", "keep_walking", "FEATURED_IN"),
            _edge("johnnie_walker", "edinburgh_center", "EXPANDED_TO"),
            _edge("christina_hendricks", "jw_blue_label", "ENDORSES"),
        ],
        video_prompt="K-pop meets whisky: CL in a powerful Keep Walking campaign scene. Bold fashion, neon Seoul backdrop. Transition to Edinburgh's Princes Street visitor centre opening. Cultural bridge between East and West. Dynamic, contemporary energy.",
        news_headlines=[
            "[2021] 코로나19 팬데믹 2년차 — 홈술 트렌드 가속, 프리미엄 위스키 매출 급증",
            "[2021] CL, 아시아 여성 아티스트로서 글로벌 주류 광고 역사에 새 이정표",
            "[2021] 에든버러 £3,500만 방문객 센터 — 브랜드 체험 마케팅의 정점",
        ],
        market_share={"블랙 라벨": 14.0, "블루 라벨": 10.0, "레드 라벨": 20.0},
        market_sales={"조니워커 한국": "~1,500억원 (추정)"},
    ),
    # 14 ─ 한국 4인 앰배서더 체제
    TimelineEvent(
        id="jw-014",
        date=_dt(2024, 6),
        brand="jw_blue",
        title="4-Ambassador 'Cheers to My Success' Campaign",
        title_ko="4인 앰배서더 'Cheers to My Success' 체제",
        description="조인성, 쟈니(NCT 127), 허니제이, 손종원 셰프의 4인 앰배서더 체제. 한국 전용 블루 라벨 캠페인으로 '성공은 나만의 만족'이라는 메시지를 전달. GQ Korea 협업.",
        category="model_change",
        industry="whisky",
        impact_score=5.0,
        kg_mutations=[
            _node("jo_insung", "person", "Jo In-sung (조인성)", "jw_blue"),
            _node("johnny_nct", "person", "Johnny NCT 127 (쟈니)", "jw_blue"),
            _node("honey_j", "person", "Honey J (허니제이)", "jw_blue"),
            _node("son_jongwon", "person", "Son Jong-won (손종원)", "jw_blue"),
            _node("cheers_campaign", "event", "Cheers to My Success Campaign", "jw_blue"),
            _edge("jo_insung", "jw_blue_label", "ENDORSES"),
            _edge("johnny_nct", "jw_blue_label", "ENDORSES"),
            _edge("honey_j", "jw_blue_label", "ENDORSES"),
            _edge("son_jongwon", "jw_blue_label", "ENDORSES"),
            _edge("cheers_campaign", "jw_blue_label", "PROMOTES"),
            _edge("cheers_campaign", "korea_whisky_market", "TARGETS"),
        ],
        video_prompt="Korean premium lifestyle: Jo In-sung, Johnny (NCT 127), Honey J, and Chef Son Jong-won in a cinematic Blue Label campaign. Each representing a different face of success. GQ magazine aesthetic. Seoul luxury nightlife. Text: 'Cheers to My Success'. Premium, aspirational.",
        news_headlines=[
            "[2024] 한국 위스키 시장 역대 최대 — MZ세대 프리미엄 수요 폭발",
            "[2024] 4인 앰배서더 전략 — 배우, 아이돌, 댄서, 셰프로 다양한 '성공' 정의",
            "[2024] 블루 라벨, 한국 프리미엄 선물 시장 1위 — '성공의 상징' 포지셔닝 확립",
        ],
        market_share={"블루 라벨": 14.0, "블랙 라벨": 13.0, "레드 라벨": 18.0},
        market_sales={"조니워커 한국": "~2,000억원 (추정)"},
    ),
    # 15 ─ 사브리나 카펜터 글로벌 파트너십
    TimelineEvent(
        id="jw-015",
        date=_dt(2025, 3),
        brand="jw_black",
        title="Sabrina Carpenter: Next-Gen Global Partnership",
        title_ko="사브리나 카펜터, 차세대 글로벌 파트너십",
        description="사브리나 카펜터와 다년 글로벌 파트너십 체결. 'Short n' Sweet' 투어 연계, 블랙 라벨 칵테일 중심 마케팅. 차세대 위스키 소비층 공략의 새 장.",
        category="model_change",
        industry="whisky",
        impact_score=4.0,
        kg_mutations=[
            _node("sabrina_carpenter", "person", "Sabrina Carpenter (사브리나 카펜터)", "jw_black"),
            _node("next_gen_whisky", "market", "Next-Gen Whisky Consumers", "jw_black"),
            _edge("sabrina_carpenter", "jw_black_label", "ENDORSES"),
            _edge("sabrina_carpenter", "next_gen_whisky", "TARGETS_DEMOGRAPHIC"),
        ],
        video_prompt="Pop meets whisky: Sabrina Carpenter in a vibrant Black Label cocktail campaign. 'Short n Sweet' tour energy meets sophisticated whisky culture. Young, diverse audience raising glasses. Modern, colorful, Gen-Z aesthetic.",
        news_headlines=[
            "[2025] 사브리나 카펜터, Z세대 글로벌 아이콘 — 팝 스타×위스키 협업의 새 공식",
            "[2025] 위스키 칵테일 문화 확산 — 전통 니트에서 믹솔로지로 트렌드 전환",
            "[2025] 글로벌 위스키 시장 $1,000억 돌파 전망 — 젊은 소비층이 성장 주도",
        ],
        market_share={"블랙 라벨": 15.0, "블루 라벨": 15.0, "레드 라벨": 17.0},
        market_sales={"조니워커 한국": "~2,300억원 (추정)"},
    ),
    # 16 ─ Space-Time AI Director 2026
    TimelineEvent(
        id="jw-016",
        date=_dt(2026, 1),
        brand="multi",
        title="Space-Time AI Director: 200 Years of Whisky Intelligence",
        title_ko="Space-Time AI 디렉터: 위스키 200년의 지능",
        description="200년의 역사적 데이터, 글로벌 캠페인 분석, 앰배서더 영향력, 소비자 심리를 통합한 AI 디렉터 시스템. 최적의 모델-브랜드 매칭과 시장별 캠페인 전략을 자동 도출.",
        category="market_shift",
        industry="whisky",
        impact_score=4.5,
        kg_mutations=[
            _node("whisky_ai_director", "event", "Whisky Space-Time AI Director", "multi"),
            _edge("whisky_ai_director", "keep_walking", "EVOLVES_FROM"),
            _edge("whisky_ai_director", "cheers_campaign", "ANALYZES"),
            _edge("whisky_ai_director", "korea_whisky_market", "DRIVES"),
        ],
        video_prompt="Grand finale: holographic timeline of 200 years of Johnnie Walker history. From Kilmarnock shop to global empire. All ambassadors appearing in sequence. AI system analyzing every data point. Text: 'Space-Time Director'. Epic, cinematic masterpiece.",
        news_headlines=[
            "[2026] AGI 논쟁 본격화 — AI가 브랜드 전략을 스스로 설계하는 시대",
            "[2026] 조니워커 206주년 — 세계 최장수 위스키 브랜드의 새로운 도전",
            "[2026] 글로벌 주류 시장 AI 혁명 — 데이터 기반 초정밀 마케팅의 실현",
        ],
        market_share={"블루 라벨": 16.0, "블랙 라벨": 15.0, "레드 라벨": 16.0},
        market_sales={"조니워커 한국": "~2,500억원 (추정)"},
    ),
]
