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
            "[1820] King George IV ascends the throne — Industrial Revolution accelerates across Britain",
            "[1823] British Excise Act transforms spirits — legal distilling ushers in a new era for Scotch",
            "[1820s] Post-Napoleonic Britain rebuilds — commerce and trade expand across the Empire",
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
            "[1860] Queen Victoria's reign — height of the British Empire, global trade routes open",
            "[1860s] Scottish whisky exports surge as the Empire's commercial networks span every continent",
            "[1865] Alexander Walker establishes 'Old Highland Whisky' as a recognizable global brand",
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
            "[1908] Edwardian Britain — the Belle Époque era, peak of European cultural confidence",
            "[1908] The advertising industry emerges — brand identity becomes a competitive weapon",
            "[1909] Bernard Partridge refines the Striding Man — adding urban sophistication to the icon",
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
            "[1909] Dawn of the 20th century — the golden age of blended Scotch whisky begins",
            "[1909] Color-coded labeling — a pioneering innovation in consumer product differentiation",
            "[1910s] Eve of World War I — British Empire at its zenith, Scotch exports at record highs",
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
            "[1934] Reign of King George V — post-Great Depression recovery, the Crown reasserts authority",
            "[1933] Prohibition repealed in America — the global spirits market roars back to life",
            "[1930s] Storm clouds over Europe — the world braces for a second great conflict",
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
            "[1945] World War II ends — an era of reconstruction begins, the world celebrates victory",
            "[1945] United Nations founded — new world order emerges, global trade barriers begin to fall",
            "[1940s] Post-war economic boom across the West — Scotch whisky spreads to every corner of the globe",
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
            "[1992] Cold War ends — global markets liberalize, the era of luxury consumption dawns",
            "[1992] Maastricht Treaty — European integration deepens, free trade flows accelerate",
            "[1990s] The premium whisky revolution — shattering the 'blended = inferior' prejudice worldwide",
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
            "[1997] Asian Financial Crisis — global instability triggers mega-mergers in the spirits industry",
            "[1997] Tony Blair's New Labour — Britain modernizes, London becomes the world's financial capital",
            "[1990s] Global spirits consolidation — the age of mega-corporations reshapes the industry landscape",
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
            "[1999] Millennium eve — Y2K anxiety and dot-com euphoria collide as the world stands at a crossroads",
            "[1999] The Striding Man reverses direction — walking forward into the new millennium, never looking back",
            "[1999] Dot-com bubble peaks — a paradigm shift in marketing, storytelling, and brand building begins",
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
            "[2009] Global financial crisis aftermath — consumers crave authenticity over excess",
            "[2009] YouTube transforms global media — long-form branded content finds its audience online",
            "[2009] The longest single-take tracking shot in advertising history — cinema meets commerce",
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
            "[2013] Asia's luxury market expands — Seoul becomes a key battleground for premium global brands",
            "[2013] Jude Law stars in 'A Gentleman's Wager' — short film advertising reaches new heights",
            "[2013] Global whisky renaissance — premium Scotch demand surges across Asia-Pacific markets",
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
            "[2019] Korea-Japan trade tensions — consumer boycott of Japanese products reshapes the whisky landscape",
            "[2019] Global cocktail renaissance — the highball movement sweeps from Tokyo to Seoul to London",
            "[2019] Gen Z drinking culture shifts worldwide — 'light and sophisticated' replaces 'strong and straight'",
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
            "[2021] COVID-19 year two — home drinking accelerates globally, premium whisky sales surge worldwide",
            "[2021] CL sets a milestone — first Asian woman to headline a major global spirits campaign",
            "[2021] Edinburgh £35M visitor centre opens — brand experience marketing reaches its apex on Princes Street",
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
            "[2024] Korean whisky market hits all-time high — Gen MZ drives global premium spirits demand",
            "[2024] Post-pandemic redefinition of success — diversity and personal fulfillment replace corporate ladder",
            "[2024] Blue Label dominates Korea's premium gift market — 'symbol of success' positioning solidified",
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
            "[2025] Sabrina Carpenter becomes Gen Z's global icon — pop star × whisky sets a new collaboration formula",
            "[2025] The cocktail/mixology revolution — whisky shifts from neat pours to creative mixed drinks worldwide",
            "[2025] Global whisky market projected to exceed $100B — young consumers lead unprecedented growth",
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
            "[2026] The AGI debate intensifies — AI begins autonomously designing brand strategies across industries",
            "[2026] Johnnie Walker turns 206 — the world's longest-running whisky brand embraces artificial intelligence",
            "[2026] AI revolution in global spirits — data-driven precision marketing becomes reality at scale",
        ],
        market_share={"블루 라벨": 16.0, "블랙 라벨": 15.0, "레드 라벨": 16.0},
        market_sales={"조니워커 한국": "~2,500억원 (추정)"},
    ),
]
