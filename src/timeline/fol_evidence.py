"""First-Order Logic (FOL) evidence layer for soju brand success factors.

Each FOL entry is tied to an event_id and provides causal reasoning
for why a brand succeeded at that point in time.

Node types:
  - fol_predicate: A logical condition or fact  (e.g., "Purity(BambooCharcoal)")
  - fol_rule:      A logical implication rule   (e.g., "P ^ Q -> R")
  - fol_conclusion: The resulting business outcome

Edge types:
  - SUPPORTS:  evidence -> rule
  - IMPLIES:   rule -> conclusion
  - EXPLAINS:  conclusion -> existing KG node
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FOLNode:
    id: str
    label: str
    label_ko: str
    node_type: str  # fol_predicate, fol_rule, fol_conclusion
    brand: str
    event_id: str  # linked timeline event


@dataclass
class FOLEdge:
    source: str
    target: str
    relation: str  # SUPPORTS, IMPLIES, EXPLAINS
    brand: str
    event_id: str


@dataclass
class FOLEvidence:
    """A complete FOL reasoning chain for one brand success factor."""
    event_id: str
    brand: str
    nodes: list[FOLNode] = field(default_factory=list)
    edges: list[FOLEdge] = field(default_factory=list)


# ── helpers ──────────────────────────────────────────────────────────────────

def _p(id: str, label: str, label_ko: str, brand: str, event_id: str) -> FOLNode:
    """Predicate node."""
    return FOLNode(id=id, label=label, label_ko=label_ko,
                   node_type="fol_predicate", brand=brand, event_id=event_id)

def _r(id: str, label: str, label_ko: str, brand: str, event_id: str) -> FOLNode:
    """Rule node."""
    return FOLNode(id=id, label=label, label_ko=label_ko,
                   node_type="fol_rule", brand=brand, event_id=event_id)

def _c(id: str, label: str, label_ko: str, brand: str, event_id: str) -> FOLNode:
    """Conclusion node."""
    return FOLNode(id=id, label=label, label_ko=label_ko,
                   node_type="fol_conclusion", brand=brand, event_id=event_id)

def _e(src: str, tgt: str, rel: str, brand: str, event_id: str) -> FOLEdge:
    return FOLEdge(source=src, target=tgt, relation=rel, brand=brand, event_id=event_id)


# ═══════════════════════════════════════════════════════════════════════════════
# FOL Evidence Data
# ═══════════════════════════════════════════════════════════════════════════════

FOL_EVIDENCE: list[FOLEvidence] = [

    # ── soju-001: Jinro Founded (1924) ──────────────────────────────────────
    FOLEvidence(
        event_id="soju-001", brand="jinro",
        nodes=[
            _p("fol_national_capital", "NationalCapital(Jinro)",
               "일제강점기, 대중은 민족자본 기업에 깊은 자부심을 느꼈다", "jinro", "soju-001"),
            _p("fol_colonial_era", "ColonialResistance(Symbol)",
               "조선의 술을 지킨다는 것 자체가 저항의 상징이었다", "jinro", "soju-001"),
            _r("fol_rule_heritage", "NationalCapital ^ ColonialResistance -> HeritageAuth",
               "민족의 자존심을 건 소주 → 진로는 '우리 술'이라는 정통성을 얻었다", "jinro", "soju-001"),
            _c("fol_conc_heritage", "HeritageAuthenticity(Jinro)",
               "진로 = 한국 소주의 정통성. 100년 브랜드 서사의 출발점", "jinro", "soju-001"),
        ],
        edges=[
            _e("fol_national_capital", "fol_rule_heritage", "SUPPORTS", "jinro", "soju-001"),
            _e("fol_colonial_era", "fol_rule_heritage", "SUPPORTS", "jinro", "soju-001"),
            _e("fol_rule_heritage", "fol_conc_heritage", "IMPLIES", "jinro", "soju-001"),
            _e("fol_conc_heritage", "jinro", "EXPLAINS", "jinro", "soju-001"),
        ],
    ),

    # ── soju-003: Jinro #1 (1970) ──────────────────────────────────────────
    FOLEvidence(
        event_id="soju-003", brand="jinro",
        nodes=[
            _p("fol_economic_boom", "EconomicBoom(Korea,1970s)",
               "70년대 경제 고도성장기, 공장과 건설현장의 노동자들이 폭발적으로 늘었다", "jinro", "soju-003"),
            _p("fol_labor_class", "LaborClass(NeedRelief)",
               "하루의 고된 노동 뒤 대중이 가장 원한 것은 저렴하고 센 한 잔의 위안이었다", "jinro", "soju-003"),
            _p("fol_national_dist", "NationalDistribution(Jinro)",
               "진로는 전국 구석구석 유통망을 깔아 어디서든 살 수 있었다", "jinro", "soju-003"),
            _r("fol_rule_no1", "EconBoom ^ LaborDemand ^ Distribution -> MarketDominance",
               "노동자의 위안 수요 + 전국 유통 → 진로가 시장을 지배하게 된 필연적 결과", "jinro", "soju-003"),
            _c("fol_conc_no1", "MarketDominance(Jinro, 50%)",
               "진로 점유율 50% 달성. 소주 = 진로인 시대", "jinro", "soju-003"),
        ],
        edges=[
            _e("fol_economic_boom", "fol_rule_no1", "SUPPORTS", "jinro", "soju-003"),
            _e("fol_labor_class", "fol_rule_no1", "SUPPORTS", "jinro", "soju-003"),
            _e("fol_national_dist", "fol_rule_no1", "SUPPORTS", "jinro", "soju-003"),
            _e("fol_rule_no1", "fol_conc_no1", "IMPLIES", "jinro", "soju-003"),
            _e("fol_conc_no1", "market_no1", "EXPLAINS", "jinro", "soju-003"),
        ],
    ),

    # ── soju-004: Chamisul Revolution (1998) ────────────────────────────────
    FOLEvidence(
        event_id="soju-004", brand="chamisul",
        nodes=[
            _p("fol_bamboo_purity", "PurificationMethod(BambooCharcoal)",
               "대나무숯 4회 정제 — '깨끗한 소주'라는 새로운 가치를 제시했다", "chamisul", "soju-004"),
            _p("fol_imf_crisis", "EconomicCrisis(IMF, 1997)",
               "IMF 외환위기, 대중은 불안과 좌절 속에서 저렴한 위안을 갈구했다", "chamisul", "soju-004"),
            _p("fol_affordable", "Affordable(Soju) ^ EscapeNeed(People)",
               "소주 한 병 가격은 커피보다 쌌고, 시대의 아픔을 달래는 최후의 사치였다", "chamisul", "soju-004"),
            _r("fol_rule_purity", "BambooCharcoal -> PurityPerception -> ConsumerTrust",
               "깨끗함이라는 메시지가 위기에 지친 소비자의 마음을 정화시켰다", "chamisul", "soju-004"),
            _r("fol_rule_crisis", "IMFCrisis ^ AffordableEscape -> DemandSurge",
               "경제위기의 고통 + 가장 저렴한 위안 → 소주 수요 폭발", "chamisul", "soju-004"),
            _c("fol_conc_100m", "SalesRecord(100M bottles, 6months)",
               "참이슬 6개월 만에 1억병 돌파. 위기가 만든 국민 소주의 탄생", "chamisul", "soju-004"),
        ],
        edges=[
            _e("fol_bamboo_purity", "fol_rule_purity", "SUPPORTS", "chamisul", "soju-004"),
            _e("fol_imf_crisis", "fol_rule_crisis", "SUPPORTS", "chamisul", "soju-004"),
            _e("fol_affordable", "fol_rule_crisis", "SUPPORTS", "chamisul", "soju-004"),
            _e("fol_rule_purity", "fol_conc_100m", "IMPLIES", "chamisul", "soju-004"),
            _e("fol_rule_crisis", "fol_conc_100m", "IMPLIES", "chamisul", "soju-004"),
            _e("fol_conc_100m", "chamisul", "EXPLAINS", "chamisul", "soju-004"),
        ],
    ),

    # ── soju-005: Lee Young-ae (1999) ───────────────────────────────────────
    FOLEvidence(
        event_id="soju-005", brand="chamisul",
        nodes=[
            _p("fol_actress_purity", "PureImage(LeeYoungae)",
               "IMF 이후 대중은 깨끗하고 순수한 것에 끌렸다. 이영애의 청순한 이미지가 그 시대감성에 정확히 부합했다", "chamisul", "soju-005"),
            _p("fol_brand_fit", "BrandFit(Purity, Actress)",
               "'깨끗한 소주' 참이슬 + '청순의 아이콘' 이영애 — 브랜드와 모델이 하나의 메시지가 되었다", "chamisul", "soju-005"),
            _r("fol_rule_endorsement", "PureActress ^ PurityBrand -> EffectiveEndorsement",
               "시대가 원한 순수함 × 브랜드 정체성 × 모델 이미지의 삼위일체 → 소주 광고의 공식이 탄생", "chamisul", "soju-005"),
            _c("fol_conc_formula", "NewFormula(SojuAd = TopActress + Purity)",
               "'소주 = 여배우 모델' 공식 확립. 이후 20년간 모든 소주 브랜드가 이 공식을 따랐다", "chamisul", "soju-005"),
        ],
        edges=[
            _e("fol_actress_purity", "fol_rule_endorsement", "SUPPORTS", "chamisul", "soju-005"),
            _e("fol_brand_fit", "fol_rule_endorsement", "SUPPORTS", "chamisul", "soju-005"),
            _e("fol_rule_endorsement", "fol_conc_formula", "IMPLIES", "chamisul", "soju-005"),
            _e("fol_conc_formula", "lee_youngae", "EXPLAINS", "chamisul", "soju-005"),
            _e("fol_conc_formula", "purity_image", "EXPLAINS", "chamisul", "soju-005"),
        ],
    ),

    # ── soju-006: Chum Churum Launch (2006) ─────────────────────────────────
    FOLEvidence(
        event_id="soju-006", brand="chum_churum",
        nodes=[
            _p("fol_alkaline_diff", "Differentiation(AlkalineWater)",
               "2000년대 웰빙 열풍, 대중은 몸에 좋은 것에 기꺼이 지갑을 열었다", "chum_churum", "soju-006"),
            _p("fol_health_trend", "HealthConscious(Consumers, 2000s)",
               "알칼리 환원수로 만든 소주라는 차별화가 건강 트렌드에 올라탔다", "chum_churum", "soju-006"),
            _p("fol_monopoly_break", "MonopolyChallenge(vs Chamisul)",
               "참이슬 독점에 싫증난 소비자들이 새로운 선택지를 기다리고 있었다", "chum_churum", "soju-006"),
            _r("fol_rule_niche", "AlkalineDiff ^ HealthTrend -> MarketNiche",
               "웰빙 트렌드 + 독점 피로감 → 처음처럼이 파고든 시장 틈새", "chum_churum", "soju-006"),
            _c("fol_conc_duopoly", "Duopoly(Chamisul, ChumChurum)",
               "소주 시장 양강 구도 형성. 소비자에게 '선택'이 생겼다", "chum_churum", "soju-006"),
        ],
        edges=[
            _e("fol_alkaline_diff", "fol_rule_niche", "SUPPORTS", "chum_churum", "soju-006"),
            _e("fol_health_trend", "fol_rule_niche", "SUPPORTS", "chum_churum", "soju-006"),
            _e("fol_monopoly_break", "fol_rule_niche", "SUPPORTS", "chum_churum", "soju-006"),
            _e("fol_rule_niche", "fol_conc_duopoly", "IMPLIES", "chum_churum", "soju-006"),
            _e("fol_conc_duopoly", "chum_churum", "EXPLAINS", "chum_churum", "soju-006"),
        ],
    ),

    # ── soju-007: Lee Hyori Shake It (2006) ─────────────────────────────────
    FOLEvidence(
        event_id="soju-007", brand="chum_churum",
        nodes=[
            _p("fol_sexy_image", "SexyIcon(LeeHyori)",
               "2000년대 중반 한류 열풍 속에서 이효리는 대한민국 최고의 섹시 아이콘이었다. 대중은 그녀의 자유분방함에 열광했다", "chum_churum", "soju-007"),
            _p("fol_action_cue", "PhysicalAction(Shake) ^ Memorable",
               "'흔들어라'는 단순한 동작이 술자리의 새로운 의식이 되었다. 몸으로 기억하는 광고의 탄생", "chum_churum", "soju-007"),
            _p("fol_viral_pre_sns", "ViralPotential(PreSNS, WOM)",
               "SNS가 없던 시대, 술자리마다 '흔들기'를 따라하며 입소문이 퍼졌다. 사람들이 직접 광고가 되었다", "chum_churum", "soju-007"),
            _r("fol_rule_viral_shake", "SexyIcon ^ MemorableAction ^ Viral -> CulturalPhenomenon",
               "시대의 섹시 아이콘 × 중독성 있는 행동 × 입소문 바이럴 → 마케팅이 아니라 문화현상이 되었다", "chum_churum", "soju-007"),
            _c("fol_conc_shake", "MarketShareBreakthrough(ChumChurum, 13.5%)",
               "처음처럼 점유율 13.5% 돌파. '흔들어' 캠페인은 한국 주류 광고의 전설이 되었다", "chum_churum", "soju-007"),
        ],
        edges=[
            _e("fol_sexy_image", "fol_rule_viral_shake", "SUPPORTS", "chum_churum", "soju-007"),
            _e("fol_action_cue", "fol_rule_viral_shake", "SUPPORTS", "chum_churum", "soju-007"),
            _e("fol_viral_pre_sns", "fol_rule_viral_shake", "SUPPORTS", "chum_churum", "soju-007"),
            _e("fol_rule_viral_shake", "fol_conc_shake", "IMPLIES", "chum_churum", "soju-007"),
            _e("fol_conc_shake", "lee_hyori", "EXPLAINS", "chum_churum", "soju-007"),
            _e("fol_conc_shake", "shake_campaign", "EXPLAINS", "chum_churum", "soju-007"),
        ],
    ),

    # ── soju-008: ABV Wars (2012) ───────────────────────────────────────────
    FOLEvidence(
        event_id="soju-008", brand="chamisul",
        nodes=[
            _p("fol_female_demand", "FemaleConsumers(Growing)",
               "2010년대, 여성의 사회 참여가 급증하며 회식과 술자리의 풍경이 달라졌다. 여성 소비자가 주류 시장의 핵심 변수로 떠올랐다", "chamisul", "soju-008"),
            _p("fol_mild_pref", "Preference(Mild, <20%ABV)",
               "강한 술을 원샷하는 문화 대신, 부드럽고 가벼운 한 잔을 즐기는 시대가 왔다. 20도 이하 소주를 찾는 목소리가 커졌다", "chamisul", "soju-008"),
            _r("fol_rule_abv", "FemaleGrowth ^ MildPref -> ABVRace",
               "여성 소비층 확대 + 저도수 선호 → 소주 브랜드들의 도수 인하 경쟁이 시작되었다", "chamisul", "soju-008"),
            _c("fol_conc_abv", "MarketExpansion(Young + Female)",
               "소주 시장의 타깃이 확장되었다. 젊은층과 여성이 소주의 새로운 주인공이 되었다", "chamisul", "soju-008"),
        ],
        edges=[
            _e("fol_female_demand", "fol_rule_abv", "SUPPORTS", "chamisul", "soju-008"),
            _e("fol_mild_pref", "fol_rule_abv", "SUPPORTS", "chamisul", "soju-008"),
            _e("fol_rule_abv", "fol_conc_abv", "IMPLIES", "chamisul", "soju-008"),
            _e("fol_conc_abv", "abv_wars", "EXPLAINS", "chamisul", "soju-008"),
            _e("fol_conc_abv", "young_consumers", "EXPLAINS", "chamisul", "soju-008"),
        ],
    ),

    # ── soju-009: IU x Chamisul (2014) ──────────────────────────────────────
    FOLEvidence(
        event_id="soju-009", brand="chamisul",
        nodes=[
            _p("fol_iu_national", "NationalIcon(IU) ^ CrossDemographic",
               "2014년 아이유는 남녀노소 누구나 좋아하는 '국민 여동생'이었다. 음악, 연기, 예능 — 모든 세대를 아우르는 아이콘", "chamisul", "soju-009"),
            _p("fol_consistency", "LongTermConsistency(Model, 10+years)",
               "참이슬은 아이유와 10년 넘게 함께했다. 광고 모델이 바뀌지 않는다는 것 자체가 신뢰의 메시지였다", "chamisul", "soju-009"),
            _p("fol_parasocial", "ParasocialBond(Fans, IU)",
               "팬들에게 아이유가 마시는 소주는 곧 '같이 마시는 소주'였다. 일방적 호감이 소비로 이어지는 팬덤 경제의 시작", "chamisul", "soju-009"),
            _r("fol_rule_iu", "NationalIcon ^ Consistency ^ ParasocialBond -> BrandLoyalty",
               "전 세대 아이콘 × 10년의 일관성 × 팬덤의 유대감 → 참이슬은 소주가 아니라 감정이 되었다", "chamisul", "soju-009"),
            _c("fol_conc_loyalty", "BrandLoyalty(Chamisul, Unshakeable)",
               "참이슬 = 아이유 = 한국의 소주. 흔들리지 않는 브랜드 충성도의 완성", "chamisul", "soju-009"),
        ],
        edges=[
            _e("fol_iu_national", "fol_rule_iu", "SUPPORTS", "chamisul", "soju-009"),
            _e("fol_consistency", "fol_rule_iu", "SUPPORTS", "chamisul", "soju-009"),
            _e("fol_parasocial", "fol_rule_iu", "SUPPORTS", "chamisul", "soju-009"),
            _e("fol_rule_iu", "fol_conc_loyalty", "IMPLIES", "chamisul", "soju-009"),
            _e("fol_conc_loyalty", "iu", "EXPLAINS", "chamisul", "soju-009"),
            _e("fol_conc_loyalty", "longest_model", "EXPLAINS", "chamisul", "soju-009"),
        ],
    ),

    # ── soju-010: IU vs Suzy Wars (2017) ────────────────────────────────────
    FOLEvidence(
        event_id="soju-010", brand="multi",
        nodes=[
            _p("fol_fandom_rivalry", "FandomRivalry(IU_fans, Suzy_fans)",
               "아이유 팬 vs 수지 팬, 참이슬 vs 처음처럼 — SNS에서 '내 소주가 더 낫다'는 팬덤 전쟁이 벌어졌다", "multi", "soju-010"),
            _p("fol_sns_amplify", "SNSAmplification(Instagram, Twitter)",
               "인스타그램과 트위터가 팬덤 대결을 실시간으로 증폭시켰다. 매일이 소주 브랜드 투표장이었다", "multi", "soju-010"),
            _r("fol_rule_wars", "FandomRivalry ^ SNS -> CulturalWar -> FreeMarketing",
               "팬덤 라이벌리 + SNS 실시간 증폭 → 광고비 한 푼 안 쓴 자발적 마케팅 전쟁", "multi", "soju-010"),
            _c("fol_conc_total_grow", "TotalMarketGrowth(Both brands benefit)",
               "결과적으로 양쪽 다 수혜. 팬덤 전쟁이 소주 전체 시장을 키웠다", "multi", "soju-010"),
        ],
        edges=[
            _e("fol_fandom_rivalry", "fol_rule_wars", "SUPPORTS", "multi", "soju-010"),
            _e("fol_sns_amplify", "fol_rule_wars", "SUPPORTS", "multi", "soju-010"),
            _e("fol_rule_wars", "fol_conc_total_grow", "IMPLIES", "multi", "soju-010"),
            _e("fol_conc_total_grow", "soju_wars_peak", "EXPLAINS", "multi", "soju-010"),
        ],
    ),

    # ── soju-011: Jinro Is Back (2019) ──────────────────────────────────────
    FOLEvidence(
        event_id="soju-011", brand="jinro",
        nodes=[
            _p("fol_retro_wave", "RetroTrend(Newtro, MZ)",
               "MZ세대는 경험하지 못한 과거에 매력을 느꼈다. '뉴트로'는 할아버지 세대의 감성을 힙하게 재해석하는 문화였다", "jinro", "soju-011"),
            _p("fol_grandpa_soju", "NostalgiaFor(GrandpaEra)",
               "할아버지가 마시던 초록병 소주, 그 투박한 레트로 감성이 오히려 MZ세대에게 '쿨'했다", "jinro", "soju-011"),
            _p("fol_toad_meme", "Memeability(ToadCharacter)",
               "두꺼비 캐릭터가 SNS 밈으로 퍼졌다. 귀엽고 유머러스한 이미지가 젊은 층의 자발적 확산을 이끌었다", "jinro", "soju-011"),
            _p("fol_heritage_1924", "Heritage(1924, 100years)",
               "1924년 설립, 100년 역사. 그 헤리티지가 뉴트로 열풍과 만나 진짜 '오리지널'의 무게를 갖게 되었다", "jinro", "soju-011"),
            _r("fol_rule_retro", "Newtro ^ Nostalgia ^ Meme ^ Heritage -> ViralRetroHit",
               "뉴트로 트렌드 × 레트로 향수 × 두꺼비 밈 × 100년 전통 → 레트로가 아니라 혁신이 되었다", "jinro", "soju-011"),
            _c("fol_conc_retro", "CategoryCreation(RetroSoju, 7% share)",
               "진로이즈백 점유율 7% 달성. 레트로 소주라는 새 카테고리가 탄생했다", "jinro", "soju-011"),
        ],
        edges=[
            _e("fol_retro_wave", "fol_rule_retro", "SUPPORTS", "jinro", "soju-011"),
            _e("fol_grandpa_soju", "fol_rule_retro", "SUPPORTS", "jinro", "soju-011"),
            _e("fol_toad_meme", "fol_rule_retro", "SUPPORTS", "jinro", "soju-011"),
            _e("fol_heritage_1924", "fol_rule_retro", "SUPPORTS", "jinro", "soju-011"),
            _e("fol_rule_retro", "fol_conc_retro", "IMPLIES", "jinro", "soju-011"),
            _e("fol_conc_retro", "jinro_is_back", "EXPLAINS", "jinro", "soju-011"),
            _e("fol_conc_retro", "toad_character", "EXPLAINS", "jinro", "soju-011"),
        ],
    ),

    # ── soju-012: Saero Zero Sugar (2022) ───────────────────────────────────
    FOLEvidence(
        event_id="soju-012", brand="saero",
        nodes=[
            _p("fol_health_mz", "HealthConscious(MZGen, ZeroSugar)",
               "코로나 이후 건강에 눈뜬 MZ세대, 탄산수부터 제로콜라까지 '제로' 열풍이 모든 음료를 휩쓸고 있었다", "saero", "soju-012"),
            _p("fol_virtual_native", "DigitalNative(MZ) ^ VirtualCharacter(Saerogumi)",
               "디지털 네이티브 MZ세대에게 가상 캐릭터 '새로구미'는 자연스러운 친구였다. 버추얼 아이돌 시대의 마케팅", "saero", "soju-012"),
            _p("fol_category_void", "CategoryVoid(ZeroSugarSoju)",
               "제로슈거 소주는 아무도 시도하지 않은 빈 자리였다. 모든 음료가 제로인데 소주만 예외일 이유가 없었다", "saero", "soju-012"),
            _r("fol_rule_zero", "HealthMZ ^ DigitalNative ^ CategoryVoid -> DisruptiveAdoption",
               "MZ 건강의식 × 디지털 네이티브 × 아무도 안 한 카테고리 → 파괴적 혁신의 조건이 완성되었다", "saero", "soju-012"),
            _c("fol_conc_disrupt", "MarketDisruption(Saero, 10% in 6mo)",
               "새로 6개월 만에 10% 점유율. 소주 시장에 100년 만의 게임체인저가 등장했다", "saero", "soju-012"),
        ],
        edges=[
            _e("fol_health_mz", "fol_rule_zero", "SUPPORTS", "saero", "soju-012"),
            _e("fol_virtual_native", "fol_rule_zero", "SUPPORTS", "saero", "soju-012"),
            _e("fol_category_void", "fol_rule_zero", "SUPPORTS", "saero", "soju-012"),
            _e("fol_rule_zero", "fol_conc_disrupt", "IMPLIES", "saero", "soju-012"),
            _e("fol_conc_disrupt", "saero", "EXPLAINS", "saero", "soju-012"),
            _e("fol_conc_disrupt", "saerogumi", "EXPLAINS", "saero", "soju-012"),
        ],
    ),

    # ── soju-013: Chamisul Zero Sugar Counterattack (2023) ──────────────────
    FOLEvidence(
        event_id="soju-013", brand="chamisul",
        nodes=[
            _p("fol_incumbent_power", "BrandPower(Chamisul, #1)",
               "참이슬은 20년 넘게 1위를 지킨 절대 강자. 유통망, 인지도, 브랜드 신뢰 모든 면에서 압도적이었다", "chamisul", "soju-013"),
            _p("fol_fast_follow", "FastFollower(Strategy)",
               "시장 1위가 빠르게 따라가면 후발주자의 혁신은 무력화된다. 참이슬은 제로슈거 제품을 신속하게 출시했다", "chamisul", "soju-013"),
            _r("fol_rule_counter", "BrandPower ^ FastFollower ^ ZeroTrend -> DefensiveSuccess",
               "절대적 브랜드 파워 + 신속한 따라잡기 + 제로 트렌드 동승 → 1위 방어 성공", "chamisul", "soju-013"),
            _c("fol_conc_defend", "MarketDefense(Chamisul holds #1)",
               "참이슬, 제로슈거 시장까지 흡수하며 1위 사수. 도전자의 혁신을 흡수하는 챔피언의 전략", "chamisul", "soju-013"),
        ],
        edges=[
            _e("fol_incumbent_power", "fol_rule_counter", "SUPPORTS", "chamisul", "soju-013"),
            _e("fol_fast_follow", "fol_rule_counter", "SUPPORTS", "chamisul", "soju-013"),
            _e("fol_rule_counter", "fol_conc_defend", "IMPLIES", "chamisul", "soju-013"),
            _e("fol_conc_defend", "chamisul_zero", "EXPLAINS", "chamisul", "soju-013"),
        ],
    ),

    # ── soju-014: K-Soju Global (2024) ──────────────────────────────────────
    FOLEvidence(
        event_id="soju-014", brand="multi",
        nodes=[
            _p("fol_hallyu_effect", "HallyuEffect(KDrama, KPop)",
               "BTS, 블랙핑크, 오징어게임 — 한류 콘텐츠가 전 세계를 사로잡으며 한국 문화 전체에 대한 관심이 폭발했다", "multi", "soju-014"),
            _p("fol_kdrama_soju", "ProductPlacement(Soju, KDrama)",
               "K드라마 속 소주 장면이 글로벌 시청자에게 '한국식 음주'를 각인시켰다. 드라마가 최고의 소주 광고가 되었다", "multi", "soju-014"),
            _p("fol_curiosity", "CulturalCuriosity(Global, Korean)",
               "한국 음식, 한국 술, 한국 문화 — 전 세계 MZ가 '한국적인 것'을 체험하고 싶어 했다", "multi", "soju-014"),
            _r("fol_rule_global", "Hallyu ^ PPL ^ Curiosity -> GlobalDemand",
               "한류 콘텐츠 × 드라마 PPL × 글로벌 호기심 → K-소주 글로벌 수요 폭발", "multi", "soju-014"),
            _c("fol_conc_export", "ExportRecord(AllTimehigh, 2024)",
               "2024년 소주 수출 역대 최고치. 한국의 술이 세계의 술이 되는 순간", "multi", "soju-014"),
        ],
        edges=[
            _e("fol_hallyu_effect", "fol_rule_global", "SUPPORTS", "multi", "soju-014"),
            _e("fol_kdrama_soju", "fol_rule_global", "SUPPORTS", "multi", "soju-014"),
            _e("fol_curiosity", "fol_rule_global", "SUPPORTS", "multi", "soju-014"),
            _e("fol_rule_global", "fol_conc_export", "IMPLIES", "multi", "soju-014"),
            _e("fol_conc_export", "global_ksoju", "EXPLAINS", "multi", "soju-014"),
        ],
    ),

    # ── soju-016: Space-Time Director (2026) ────────────────────────────────
    FOLEvidence(
        event_id="soju-016", brand="multi",
        nodes=[
            _p("fol_100yr_data", "HistoricalData(100years)",
               "1924년부터 2026년까지, 100년간 축적된 소주 산업의 모든 데이터. 모델, 광고, 매출, 트렌드의 기록", "multi", "soju-016"),
            _p("fol_ai_capability", "AICapability(TemporalReasoning)",
               "AI가 시간의 흐름 속에서 패턴을 읽는다. 과거의 성공과 실패에서 미래의 전략을 추론하는 시간추론 능력", "multi", "soju-016"),
            _p("fol_consumer_signal", "RealTimeSignals(SocialMedia, Sales)",
               "SNS 반응, 실시간 매출, 트렌드 변화 — 소비자가 보내는 모든 시그널을 실시간으로 포착", "multi", "soju-016"),
            _r("fol_rule_ai_dir", "100yrData ^ AI ^ Signals -> OptimalStrategy",
               "100년 역사 데이터 × AI 시간추론 × 실시간 시그널 → 과거를 읽고 미래를 예측하는 최적 전략 도출", "multi", "soju-016"),
            _c("fol_conc_ai_dir", "AutonomousDirector(BrandStrategy)",
               "AI가 시공간을 넘나들며 브랜드 전략을 디렉팅한다. 인간의 직관과 AI의 추론이 만나는 미래", "multi", "soju-016"),
        ],
        edges=[
            _e("fol_100yr_data", "fol_rule_ai_dir", "SUPPORTS", "multi", "soju-016"),
            _e("fol_ai_capability", "fol_rule_ai_dir", "SUPPORTS", "multi", "soju-016"),
            _e("fol_consumer_signal", "fol_rule_ai_dir", "SUPPORTS", "multi", "soju-016"),
            _e("fol_rule_ai_dir", "fol_conc_ai_dir", "IMPLIES", "multi", "soju-016"),
            _e("fol_conc_ai_dir", "spacetime_director", "EXPLAINS", "multi", "soju-016"),
        ],
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # Whisky Reasoning Graph
    # ═══════════════════════════════════════════════════════════════════════════

    # ── jw-001: John Walker Opens Shop (1820) ─────────────────────────────────
    FOLEvidence(
        event_id="jw-001", brand="jw_global",
        nodes=[
            _p("fol_jw_grocery", "GroceryExpertise(JohnWalker)",
               "1820, post-Napoleonic Britain — the Industrial Revolution was transforming commerce. Grocer John Walker applied tea-blending principles to an inconsistent whisky market", "jw_global", "jw-001"),
            _p("fol_jw_blending", "BlendingInnovation(Consistency)",
               "Consistency was what drinkers truly craved. Walker's blending technique guaranteed the same taste in every bottle", "jw_global", "jw-001"),
            _r("fol_rule_jw_origin", "GroceryExpertise ^ BlendingInnovation -> BrandFoundation",
               "A grocer's blending knowledge + consumer demand for reliability → the foundation of a whisky empire was laid", "jw_global", "jw-001"),
            _c("fol_conc_jw_origin", "BrandFoundation(JohnnieWalker, 200yr)",
               "From a small grocery shop to a 200-year dynasty. The first step of the world's most iconic whisky brand", "jw_global", "jw-001"),
        ],
        edges=[
            _e("fol_jw_grocery", "fol_rule_jw_origin", "SUPPORTS", "jw_global", "jw-001"),
            _e("fol_jw_blending", "fol_rule_jw_origin", "SUPPORTS", "jw_global", "jw-001"),
            _e("fol_rule_jw_origin", "fol_conc_jw_origin", "IMPLIES", "jw_global", "jw-001"),
            _e("fol_conc_jw_origin", "johnnie_walker", "EXPLAINS", "jw_global", "jw-001"),
        ],
    ),

    # ── jw-003: Striding Man Logo (1908) ──────────────────────────────────────
    FOLEvidence(
        event_id="jw-003", brand="jw_global",
        nodes=[
            _p("fol_jw_visual_id", "VisualIdentity(StridingMan)",
               "1908, the Edwardian era — Britain ruled a quarter of the globe. The Striding Man embodied the confidence of empire: a gentleman walking forward, unstoppable", "jw_global", "jw-003"),
            _p("fol_jw_first_mover", "FirstMover(CharacterLogo, Spirits)",
               "The first character logo in the spirits industry. You could recognize the brand without ever seeing the bottle", "jw_global", "jw-003"),
            _r("fol_rule_jw_icon", "VisualIdentity ^ FirstMover -> IconicBrand",
               "A striking visual identity + first-mover advantage in character branding → an icon that endures for over a century", "jw_global", "jw-003"),
            _c("fol_conc_jw_icon", "IconicRecognition(Global, 100yr+)",
               "The Striding Man stands alongside Nike's Swoosh and Apple's logo as one of the world's most recognized symbols", "jw_global", "jw-003"),
        ],
        edges=[
            _e("fol_jw_visual_id", "fol_rule_jw_icon", "SUPPORTS", "jw_global", "jw-003"),
            _e("fol_jw_first_mover", "fol_rule_jw_icon", "SUPPORTS", "jw_global", "jw-003"),
            _e("fol_rule_jw_icon", "fol_conc_jw_icon", "IMPLIES", "jw_global", "jw-003"),
            _e("fol_conc_jw_icon", "striding_man", "EXPLAINS", "jw_global", "jw-003"),
        ],
    ),

    # ── jw-004: Red & Black Label (1909) ──────────────────────────────────────
    FOLEvidence(
        event_id="jw-004", brand="multi",
        nodes=[
            _p("fol_jw_color_system", "ColorCoding(Red, Black)",
               "Red for approachable, Black for premium — a genius system where color alone communicates the tier instantly", "multi", "jw-004"),
            _p("fol_jw_portfolio", "PortfolioStrategy(Tiered)",
               "Multiple tiers under one brand roof. From first-time drinkers to connoisseurs, everyone finds their place", "multi", "jw-004"),
            _r("fol_rule_jw_tier", "ColorCoding ^ TieredPortfolio -> ConsumerClarity",
               "Intuitive color coding + tiered portfolio → consumers self-select their level within the brand", "multi", "jw-004"),
            _c("fol_conc_jw_tier", "BrandArchitecture(Scalable)",
               "Red, Black, Blue — the textbook of scalable brand architecture. Every spirits brand benchmarked this structure", "multi", "jw-004"),
        ],
        edges=[
            _e("fol_jw_color_system", "fol_rule_jw_tier", "SUPPORTS", "multi", "jw-004"),
            _e("fol_jw_portfolio", "fol_rule_jw_tier", "SUPPORTS", "multi", "jw-004"),
            _e("fol_rule_jw_tier", "fol_conc_jw_tier", "IMPLIES", "multi", "jw-004"),
            _e("fol_conc_jw_tier", "jw_red_label", "EXPLAINS", "multi", "jw-004"),
            _e("fol_conc_jw_tier", "jw_black_label", "EXPLAINS", "multi", "jw-004"),
        ],
    ),

    # ── jw-007: Blue Label (1992) ─────────────────────────────────────────────
    FOLEvidence(
        event_id="jw-007", brand="jw_blue",
        nodes=[
            _p("fol_jw_rare_cask", "RareCaskSelection(HandPicked)",
               "Only 1 in 10,000 casks is selected. The master blender's hand-picking created scarcity that defined value", "jw_blue", "jw-007"),
            _p("fol_jw_luxury_pos", "LuxuryPositioning(UltraPremium)",
               "Whisky elevated to the luxury category. Not selling a drink, but selling an experience — ultra-premium positioning", "jw_blue", "jw-007"),
            _p("fol_jw_gift_culture", "GiftCulture(Korea, Success)",
               "In Korea's gift culture — holidays, promotions, business success — Blue Label became the definitive gesture of respect", "jw_blue", "jw-007"),
            _r("fol_rule_jw_blue", "RareCask ^ Luxury ^ GiftCulture -> SymbolOfSuccess",
               "Extreme scarcity × luxury positioning × Korea's gift culture → 'the drink of the successful' was born as a symbol", "jw_blue", "jw-007"),
            _c("fol_conc_jw_blue", "CulturalSymbol(Success, Korea)",
               "Blue Label = symbol of success. It became the most meaningful gift one could give in Korea", "jw_blue", "jw-007"),
        ],
        edges=[
            _e("fol_jw_rare_cask", "fol_rule_jw_blue", "SUPPORTS", "jw_blue", "jw-007"),
            _e("fol_jw_luxury_pos", "fol_rule_jw_blue", "SUPPORTS", "jw_blue", "jw-007"),
            _e("fol_jw_gift_culture", "fol_rule_jw_blue", "SUPPORTS", "jw_blue", "jw-007"),
            _e("fol_rule_jw_blue", "fol_conc_jw_blue", "IMPLIES", "jw_blue", "jw-007"),
            _e("fol_conc_jw_blue", "jw_blue_label", "EXPLAINS", "jw_blue", "jw-007"),
        ],
    ),

    # ── jw-009: Keep Walking Campaign (1999) ──────────────────────────────────
    FOLEvidence(
        event_id="jw-009", brand="jw_global",
        nodes=[
            _p("fol_jw_progress_msg", "ProgressMessage(KeepWalking)",
               "1999 — the world stood between millennium anxiety and dot-com euphoria. 'Keep Walking' captured the zeitgeist: move forward, no matter what", "jw_global", "jw-009"),
            _p("fol_jw_celeb_auth", "CelebrityAuthenticity(HarveyKeitel)",
               "Harvey Keitel walked with conviction, not performance. In an era of celebrity excess, his authenticity felt like philosophy, not advertising", "jw_global", "jw-009"),
            _p("fol_jw_logo_flip", "LogoRedesign(LeftToRight)",
               "The Striding Man was flipped from left to right — never looking back, always walking forward. A visual manifesto for the new millennium", "jw_global", "jw-009"),
            _r("fol_rule_jw_keep", "Progress ^ Celebrity ^ LogoFlip -> CampaignMasterpiece",
               "Millennial zeitgeist × authentic celebrity × visual reinvention → not an ad campaign, but a cultural movement", "jw_global", "jw-009"),
            _c("fol_conc_jw_keep", "SalesImpact($2.2B, 10yr)",
               "$2.2 billion in incremental sales over a decade. 'Keep Walking' became the greatest spirits campaign in advertising history", "jw_global", "jw-009"),
        ],
        edges=[
            _e("fol_jw_progress_msg", "fol_rule_jw_keep", "SUPPORTS", "jw_global", "jw-009"),
            _e("fol_jw_celeb_auth", "fol_rule_jw_keep", "SUPPORTS", "jw_global", "jw-009"),
            _e("fol_jw_logo_flip", "fol_rule_jw_keep", "SUPPORTS", "jw_global", "jw-009"),
            _e("fol_rule_jw_keep", "fol_conc_jw_keep", "IMPLIES", "jw_global", "jw-009"),
            _e("fol_conc_jw_keep", "keep_walking", "EXPLAINS", "jw_global", "jw-009"),
        ],
    ),

    # ── jw-010: Robert Carlyle One-Take (2009) ────────────────────────────────
    FOLEvidence(
        event_id="jw-010", brand="jw_black",
        nodes=[
            _p("fol_jw_storytelling", "BrandStorytelling(200yr, OneTake)",
               "Post-2008 financial crisis — the world craved authentic stories over flashy ads. Robert Carlyle walked through Scottish highlands telling 200 years of history in a single take", "jw_black", "jw-010"),
            _p("fol_jw_youtube_era", "PlatformShift(YouTube, Viral)",
               "2009: YouTube was rewriting the rules of media. A 6-minute ad that would never air on TV found its global audience online", "jw_black", "jw-010"),
            _r("fol_rule_jw_onetake", "Storytelling ^ YouTubeEra -> ViralMasterpiece",
               "Cinematic storytelling in a post-crisis world + YouTube's rise as a media platform → a new standard for branded content was born", "jw_black", "jw-010"),
            _c("fol_conc_jw_onetake", "ContentMarketing(NewStandard)",
               "50 million YouTube views. This film became the textbook of branded content — proving long-form storytelling could thrive in the digital age", "jw_black", "jw-010"),
        ],
        edges=[
            _e("fol_jw_storytelling", "fol_rule_jw_onetake", "SUPPORTS", "jw_black", "jw-010"),
            _e("fol_jw_youtube_era", "fol_rule_jw_onetake", "SUPPORTS", "jw_black", "jw-010"),
            _e("fol_rule_jw_onetake", "fol_conc_jw_onetake", "IMPLIES", "jw_black", "jw-010"),
            _e("fol_conc_jw_onetake", "robert_carlyle", "EXPLAINS", "jw_black", "jw-010"),
        ],
    ),

    # ── jw-012: Korean Highball Trend (2019) ──────────────────────────────────
    FOLEvidence(
        event_id="jw-012", brand="jw_red",
        nodes=[
            _p("fol_jw_mz_barrier", "LowBarrier(Highball, MZ)",
               "The global cocktail renaissance reached Korea. Highball — just whisky, soda, and ice — became the easiest gateway into whisky for young drinkers", "jw_red", "jw-012"),
            _p("fol_jw_boycott", "JapanBoycott(2019) ^ ScotchAlternative",
               "2019 Korea-Japan trade tensions triggered a consumer boycott of Japanese products. Japanese whisky vanished from shelves — Scotch filled the void", "jw_red", "jw-012"),
            _p("fol_jw_cvs_channel", "ConvenienceStore(Distribution)",
               "Small-format whisky bottles hit convenience stores, making home highballs effortless. The 'home bar' culture exploded across Korea", "jw_red", "jw-012"),
            _r("fol_rule_jw_highball", "LowBarrier ^ Boycott ^ CVS -> HighballBoom",
               "Low entry barrier × Japan boycott windfall × convenience store distribution → the Korean highball boom erupted", "jw_red", "jw-012"),
            _c("fol_conc_jw_highball", "MarketExpansion(YoungWhiskyDrinkers)",
               "Young whisky drinkers multiplied rapidly. Whisky was no longer 'your father's drink' — a generational shift had begun", "jw_red", "jw-012"),
        ],
        edges=[
            _e("fol_jw_mz_barrier", "fol_rule_jw_highball", "SUPPORTS", "jw_red", "jw-012"),
            _e("fol_jw_boycott", "fol_rule_jw_highball", "SUPPORTS", "jw_red", "jw-012"),
            _e("fol_jw_cvs_channel", "fol_rule_jw_highball", "SUPPORTS", "jw_red", "jw-012"),
            _e("fol_rule_jw_highball", "fol_conc_jw_highball", "IMPLIES", "jw_red", "jw-012"),
            _e("fol_conc_jw_highball", "highball_trend", "EXPLAINS", "jw_red", "jw-012"),
        ],
    ),

    # ── jw-014: 4-Ambassador Campaign (2024) ──────────────────────────────────
    FOLEvidence(
        event_id="jw-014", brand="jw_blue",
        nodes=[
            _p("fol_jw_diverse_success", "DiverseSuccess(Actor, Idol, Dancer, Chef)",
               "Post-pandemic world redefined success — actor, idol, dancer, chef. Four ambassadors embodied the message: there is no single path to greatness", "jw_blue", "jw-014"),
            _p("fol_jw_local_campaign", "LocalizedCampaign(KoreaOnly)",
               "A global brand created a campaign exclusively for Korea. A bold recognition of the Korean market's cultural weight in the luxury spirits world", "jw_blue", "jw-014"),
            _p("fol_jw_premium_gift", "PremiumGiftMarket(#1, Korea)",
               "Korea's Lunar New Year and Chuseok gift market is a $2B industry. Blue Label reigns as the undisputed #1 premium gift", "jw_blue", "jw-014"),
            _r("fol_rule_jw_4amb", "DiverseSuccess ^ Localized ^ GiftMarket -> CulturalRelevance",
               "Diverse symbols of success × Korea-exclusive campaign × gift market dominance → maximum cultural relevance in a key market", "jw_blue", "jw-014"),
            _c("fol_conc_jw_4amb", "MarketLeadership(BlueLabel, Korea, #1Gift)",
               "Blue Label cemented its leadership in Korea's premium gift market. A masterclass in global brand localization", "jw_blue", "jw-014"),
        ],
        edges=[
            _e("fol_jw_diverse_success", "fol_rule_jw_4amb", "SUPPORTS", "jw_blue", "jw-014"),
            _e("fol_jw_local_campaign", "fol_rule_jw_4amb", "SUPPORTS", "jw_blue", "jw-014"),
            _e("fol_jw_premium_gift", "fol_rule_jw_4amb", "SUPPORTS", "jw_blue", "jw-014"),
            _e("fol_rule_jw_4amb", "fol_conc_jw_4amb", "IMPLIES", "jw_blue", "jw-014"),
            _e("fol_conc_jw_4amb", "cheers_campaign", "EXPLAINS", "jw_blue", "jw-014"),
        ],
    ),

    # ── jw-015: Sabrina Carpenter (2025) ──────────────────────────────────────
    FOLEvidence(
        event_id="jw-015", brand="jw_black",
        nodes=[
            _p("fol_jw_genz_icon", "GenZIcon(SabrinaCarpenter)",
               "2025: Gen Z reshapes global consumption. Pop star Sabrina Carpenter — her fanbase IS the next generation of whisky drinkers", "jw_black", "jw-015"),
            _p("fol_jw_cocktail_shift", "CocktailCulture(Mixology)",
               "The TikTok-driven cocktail renaissance means Gen Z prefers mixed drinks over neat pours. Whisky-based cocktails are the new social currency", "jw_black", "jw-015"),
            _r("fol_rule_jw_nextgen", "GenZIcon ^ CocktailCulture -> NextGenAdoption",
               "Gen Z global icon × cocktail/mixology movement → whisky finds its bridge to the next generation", "jw_black", "jw-015"),
            _c("fol_conc_jw_nextgen", "DemographicExpansion(GenZ, Whisky)",
               "Gen Z whisky adoption accelerates. Securing tomorrow's loyal customers today — the long game of brand building", "jw_black", "jw-015"),
        ],
        edges=[
            _e("fol_jw_genz_icon", "fol_rule_jw_nextgen", "SUPPORTS", "jw_black", "jw-015"),
            _e("fol_jw_cocktail_shift", "fol_rule_jw_nextgen", "SUPPORTS", "jw_black", "jw-015"),
            _e("fol_rule_jw_nextgen", "fol_conc_jw_nextgen", "IMPLIES", "jw_black", "jw-015"),
            _e("fol_conc_jw_nextgen", "sabrina_carpenter", "EXPLAINS", "jw_black", "jw-015"),
        ],
    ),

    # ── jw-016: Whisky AI Director (2026) ─────────────────────────────────────
    FOLEvidence(
        event_id="jw-016", brand="multi",
        nodes=[
            _p("fol_jw_200yr_data", "HistoricalData(200years, Whisky)",
               "From 1820 to 2026 — two centuries of whisky data. Ambassadors, campaigns, sales, and cultural shifts across the British Empire and beyond", "multi", "jw-016"),
            _p("fol_jw_ambassador_ai", "AmbassadorAnalysis(AI, CrossCultural)",
               "AI analyzes brand ambassadors across cultures and eras. Which person, in which moment, created the deepest resonance with consumers?", "multi", "jw-016"),
            _p("fol_jw_market_signal", "MarketSignals(Global, RealTime)",
               "Real-time signals from every market — social sentiment, sales trends, cultural shifts — unified into a single data stream", "multi", "jw-016"),
            _r("fol_rule_jw_ai", "200yrData ^ AmbassadorAI ^ Signals -> OptimalWhiskyStrategy",
               "200 years of brand wisdom × AI cross-cultural analysis × real-time global signals → the optimal whisky brand strategy, computed", "multi", "jw-016"),
            _c("fol_conc_jw_ai", "AutonomousDirector(WhiskyBrandStrategy)",
               "AI directs brand strategy by fusing two centuries of heritage with real-time intelligence. The ultimate convergence of tradition and innovation", "multi", "jw-016"),
        ],
        edges=[
            _e("fol_jw_200yr_data", "fol_rule_jw_ai", "SUPPORTS", "multi", "jw-016"),
            _e("fol_jw_ambassador_ai", "fol_rule_jw_ai", "SUPPORTS", "multi", "jw-016"),
            _e("fol_jw_market_signal", "fol_rule_jw_ai", "SUPPORTS", "multi", "jw-016"),
            _e("fol_rule_jw_ai", "fol_conc_jw_ai", "IMPLIES", "multi", "jw-016"),
            _e("fol_conc_jw_ai", "whisky_ai_director", "EXPLAINS", "multi", "jw-016"),
        ],
    ),
]
