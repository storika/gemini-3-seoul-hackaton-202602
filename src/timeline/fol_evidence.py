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
               "민족자본(진로)", "jinro", "soju-001"),
            _p("fol_colonial_era", "ColonialResistance(Symbol)",
               "일제강점기 저항 상징", "jinro", "soju-001"),
            _r("fol_rule_heritage", "NationalCapital ^ ColonialResistance -> HeritageAuth",
               "민족자본 + 저항상징 -> 정통성", "jinro", "soju-001"),
            _c("fol_conc_heritage", "HeritageAuthenticity(Jinro)",
               "진로 정통성 확보", "jinro", "soju-001"),
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
               "경제 고도성장기", "jinro", "soju-003"),
            _p("fol_labor_class", "LaborClass(NeedRelief)",
               "노동자 위안 수요", "jinro", "soju-003"),
            _p("fol_national_dist", "NationalDistribution(Jinro)",
               "전국 유통망 확보", "jinro", "soju-003"),
            _r("fol_rule_no1", "EconBoom ^ LaborDemand ^ Distribution -> MarketDominance",
               "경제성장 + 노동수요 + 유통 -> 시장지배", "jinro", "soju-003"),
            _c("fol_conc_no1", "MarketDominance(Jinro, 50%)",
               "진로 시장점유율 50% 달성", "jinro", "soju-003"),
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
               "대나무숯 정제 공법", "chamisul", "soju-004"),
            _p("fol_imf_crisis", "EconomicCrisis(IMF, 1997)",
               "IMF 외환위기", "chamisul", "soju-004"),
            _p("fol_affordable", "Affordable(Soju) ^ EscapeNeed(People)",
               "저렴한 위안", "chamisul", "soju-004"),
            _r("fol_rule_purity", "BambooCharcoal -> PurityPerception -> ConsumerTrust",
               "대나무숯 -> 깨끗함 인식 -> 소비자 신뢰", "chamisul", "soju-004"),
            _r("fol_rule_crisis", "IMFCrisis ^ AffordableEscape -> DemandSurge",
               "경제위기 + 저렴한위안 -> 수요폭발", "chamisul", "soju-004"),
            _c("fol_conc_100m", "SalesRecord(100M bottles, 6months)",
               "6개월 1억병 판매 기록", "chamisul", "soju-004"),
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
               "이영애 청순 이미지", "chamisul", "soju-005"),
            _p("fol_brand_fit", "BrandFit(Purity, Actress)",
               "브랜드-모델 적합도", "chamisul", "soju-005"),
            _r("fol_rule_endorsement", "PureActress ^ PurityBrand -> EffectiveEndorsement",
               "청순배우 + 깨끗한브랜드 -> 효과적 광고", "chamisul", "soju-005"),
            _c("fol_conc_formula", "NewFormula(SojuAd = TopActress + Purity)",
               "소주광고 공식 확립", "chamisul", "soju-005"),
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
               "알칼리 환원수 차별화", "chum_churum", "soju-006"),
            _p("fol_health_trend", "HealthConscious(Consumers, 2000s)",
               "2000년대 건강 트렌드", "chum_churum", "soju-006"),
            _p("fol_monopoly_break", "MonopolyChallenge(vs Chamisul)",
               "참이슬 독점 도전", "chum_churum", "soju-006"),
            _r("fol_rule_niche", "AlkalineDiff ^ HealthTrend -> MarketNiche",
               "알칼리차별화 + 건강트렌드 -> 시장틈새", "chum_churum", "soju-006"),
            _c("fol_conc_duopoly", "Duopoly(Chamisul, ChumChurum)",
               "양강 구도 형성", "chum_churum", "soju-006"),
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
               "이효리 섹시 아이콘", "chum_churum", "soju-007"),
            _p("fol_action_cue", "PhysicalAction(Shake) ^ Memorable",
               "흔들기 행동 각인", "chum_churum", "soju-007"),
            _p("fol_viral_pre_sns", "ViralPotential(PreSNS, WOM)",
               "SNS 이전 입소문 바이럴", "chum_churum", "soju-007"),
            _r("fol_rule_viral_shake", "SexyIcon ^ MemorableAction ^ Viral -> CulturalPhenomenon",
               "섹시아이콘 + 행동각인 + 바이럴 -> 문화현상", "chum_churum", "soju-007"),
            _c("fol_conc_shake", "MarketShareBreakthrough(ChumChurum, 13.5%)",
               "처음처럼 점유율 13.5% 돌파", "chum_churum", "soju-007"),
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
               "여성 소비자 증가", "chamisul", "soju-008"),
            _p("fol_mild_pref", "Preference(Mild, <20%ABV)",
               "저도수 선호", "chamisul", "soju-008"),
            _r("fol_rule_abv", "FemaleGrowth ^ MildPref -> ABVRace",
               "여성증가 + 저도수선호 -> 도수인하경쟁", "chamisul", "soju-008"),
            _c("fol_conc_abv", "MarketExpansion(Young + Female)",
               "젊은층+여성 시장 확대", "chamisul", "soju-008"),
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
               "국민 아이콘 IU", "chamisul", "soju-009"),
            _p("fol_consistency", "LongTermConsistency(Model, 10+years)",
               "10년+ 장기 모델 일관성", "chamisul", "soju-009"),
            _p("fol_parasocial", "ParasocialBond(Fans, IU)",
               "팬과 아이유의 유사사회적 유대", "chamisul", "soju-009"),
            _r("fol_rule_iu", "NationalIcon ^ Consistency ^ ParasocialBond -> BrandLoyalty",
               "국민아이콘 + 일관성 + 유대 -> 브랜드충성", "chamisul", "soju-009"),
            _c("fol_conc_loyalty", "BrandLoyalty(Chamisul, Unshakeable)",
               "참이슬 불변의 브랜드 충성도", "chamisul", "soju-009"),
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
               "팬덤 라이벌리", "multi", "soju-010"),
            _p("fol_sns_amplify", "SNSAmplification(Instagram, Twitter)",
               "SNS 증폭 효과", "multi", "soju-010"),
            _r("fol_rule_wars", "FandomRivalry ^ SNS -> CulturalWar -> FreeMarketing",
               "팬덤대결 + SNS -> 문화전쟁 -> 무료마케팅", "multi", "soju-010"),
            _c("fol_conc_total_grow", "TotalMarketGrowth(Both brands benefit)",
               "전체 시장 확대 (양쪽 다 수혜)", "multi", "soju-010"),
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
               "뉴트로 트렌드", "jinro", "soju-011"),
            _p("fol_grandpa_soju", "NostalgiaFor(GrandpaEra)",
               "할아버지 시대 향수", "jinro", "soju-011"),
            _p("fol_toad_meme", "Memeability(ToadCharacter)",
               "두꺼비 밈 가능성", "jinro", "soju-011"),
            _p("fol_heritage_1924", "Heritage(1924, 100years)",
               "1924년 100년 전통", "jinro", "soju-011"),
            _r("fol_rule_retro", "Newtro ^ Nostalgia ^ Meme ^ Heritage -> ViralRetroHit",
               "뉴트로 + 향수 + 밈 + 전통 -> 바이럴 레트로 히트", "jinro", "soju-011"),
            _c("fol_conc_retro", "CategoryCreation(RetroSoju, 7% share)",
               "레트로 소주 카테고리 창출 (7%)", "jinro", "soju-011"),
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
               "MZ세대 건강의식", "saero", "soju-012"),
            _p("fol_virtual_native", "DigitalNative(MZ) ^ VirtualCharacter(Saerogumi)",
               "디지털네이티브 + 버추얼캐릭터", "saero", "soju-012"),
            _p("fol_category_void", "CategoryVoid(ZeroSugarSoju)",
               "제로슈거 소주 카테고리 부재", "saero", "soju-012"),
            _r("fol_rule_zero", "HealthMZ ^ DigitalNative ^ CategoryVoid -> DisruptiveAdoption",
               "건강MZ + 디지털 + 카테고리공백 -> 파괴적혁신", "saero", "soju-012"),
            _c("fol_conc_disrupt", "MarketDisruption(Saero, 10% in 6mo)",
               "새로 6개월 만에 10% 점유", "saero", "soju-012"),
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
               "참이슬 1위 브랜드 파워", "chamisul", "soju-013"),
            _p("fol_fast_follow", "FastFollower(Strategy)",
               "패스트 팔로워 전략", "chamisul", "soju-013"),
            _r("fol_rule_counter", "BrandPower ^ FastFollower ^ ZeroTrend -> DefensiveSuccess",
               "브랜드파워 + 패스트팔로워 + 제로트렌드 -> 방어 성공", "chamisul", "soju-013"),
            _c("fol_conc_defend", "MarketDefense(Chamisul holds #1)",
               "참이슬 1위 방어 성공", "chamisul", "soju-013"),
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
               "한류 효과 (드라마, K-POP)", "multi", "soju-014"),
            _p("fol_kdrama_soju", "ProductPlacement(Soju, KDrama)",
               "K드라마 소주 PPL", "multi", "soju-014"),
            _p("fol_curiosity", "CulturalCuriosity(Global, Korean)",
               "한국문화 호기심", "multi", "soju-014"),
            _r("fol_rule_global", "Hallyu ^ PPL ^ Curiosity -> GlobalDemand",
               "한류 + PPL + 호기심 -> 글로벌 수요", "multi", "soju-014"),
            _c("fol_conc_export", "ExportRecord(AllTimehigh, 2024)",
               "수출 역대 최고치 (2024)", "multi", "soju-014"),
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
               "100년 역사 데이터", "multi", "soju-016"),
            _p("fol_ai_capability", "AICapability(TemporalReasoning)",
               "AI 시간추론 능력", "multi", "soju-016"),
            _p("fol_consumer_signal", "RealTimeSignals(SocialMedia, Sales)",
               "실시간 소비자 시그널", "multi", "soju-016"),
            _r("fol_rule_ai_dir", "100yrData ^ AI ^ Signals -> OptimalStrategy",
               "100년데이터 + AI + 시그널 -> 최적전략", "multi", "soju-016"),
            _c("fol_conc_ai_dir", "AutonomousDirector(BrandStrategy)",
               "자율 브랜드 전략 디렉터", "multi", "soju-016"),
        ],
        edges=[
            _e("fol_100yr_data", "fol_rule_ai_dir", "SUPPORTS", "multi", "soju-016"),
            _e("fol_ai_capability", "fol_rule_ai_dir", "SUPPORTS", "multi", "soju-016"),
            _e("fol_consumer_signal", "fol_rule_ai_dir", "SUPPORTS", "multi", "soju-016"),
            _e("fol_rule_ai_dir", "fol_conc_ai_dir", "IMPLIES", "multi", "soju-016"),
            _e("fol_conc_ai_dir", "spacetime_director", "EXPLAINS", "multi", "soju-016"),
        ],
    ),
]
