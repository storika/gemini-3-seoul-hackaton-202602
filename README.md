# Soju Wars: 100-Year Brand Evolution

**Gemini 3.0 Seoul Hackathon 2026**

이 프로젝트는 한국 소주 시장의 100년 역사(1924~2026)를 기반으로 브랜드의 진화와 마케팅 트렌드를 시각화하고, AI 에이전트를 통해 새로운 브랜드 전략과 크리에이티브 콘텐츠를 생성하는 멀티 에이전트 시스템입니다.

---

## 🏗️ Project Architecture & Google Stack

이 프로젝트는 최신 Google AI 기술 스택을 전방위적으로 활용하여 구축되었습니다.

### 1. Multi-Agent Orchestration: Google ADK (Agent Development Kit)
Google ADK를 사용하여 복잡한 워크플로우를 자율적으로 수행하는 전문 에이전트들을 구축했습니다.
- **Root Agent (Soju Director)**: `LlmAgent`를 사용하여 전체 시스템을 지휘하고 사용자 요청에 따라 적절한 하위 에이전트로 작업을 라우팅합니다.
- **Trend Analyzer**: `SequentialAgent`와 `google_search` 도구를 결합하여 실시간 시장 트렌드와 역사적 맥락을 조사합니다.
- **Creative Director**: `imagen-4.0` 및 `veo-3.1`과 통합되어 브랜드 아이덴티티에 맞는 이미지와 비디오 광고 시놉시스를 생성합니다.
- **Brand Guard**: `LlmAgent`를 통해 생성된 콘텐츠가 브랜드의 역사적 사실(예: 특정 연도의 모델, 도수 등)과 일치하는지 검증하여 Hallucination을 방지합니다.

### 2. Core LLM: Gemini 3.0 Flash Preview
모든 에이전트의 두뇌로 **Gemini 3.0 Flash Preview**를 채택했습니다.
- **특징**: 초고속 추론 속도와 확장된 컨텍스트 윈도우를 통해 100년 치의 방대한 브랜드 데이터를 실시간으로 분석하고 처리합니다.
- **활용**: 복잡한 추론, 데이터 구조화(Graph-to-Text), 그리고 에이전트 간의 정교한 협업 로직을 수행합니다.

### 3. Generative Media: Imagen 4.0 & Veo 3.1
최신 미디어 생성 모델을 사용하여 브랜드의 과거를 재현하고 미래를 제안합니다.
- **Imagen 4.0**: 고해상도 제품 이미지 및 라이프스타일 캠페인 비주얼 생성.
- **Veo 3.1**: 브랜드 스토리텔링을 위한 고품질의 숏폼 광고 영상 생성.
- **Integration**: `google-genai` SDK를 직접 연동하여 프롬프트 최적화 및 결과물 관리를 자동화했습니다.

### 4. Advanced RAG: Hybrid Memory System
- **Vector Store (ChromaDB)**: 시맨틱 검색을 통한 관련 정보 추출.
- **Knowledge Graph (NetworkX)**: 엔티티 간의 관계(브랜드-모델-이벤트)를 정교하게 추적.
- **Temporal Decay**: 시간에 따른 정보의 중요도를 계산하여, 현재 시점(Timeline)에 가장 적합한 맥락을 Gemini에게 전달합니다.

---

## 🌟 Key Features

1. **Interactive 100-Year Timeline**: 1924년부터 2026년까지 소주 브랜드의 변화를 실시간으로 탐색.
2. **Dynamic Knowledge Graph**: 시간에 따라 브랜드의 지식 네트워크가 어떻게 확장되고 연결되는지 시각화.
3. **AI Campaign Generator**: 특정 시점의 트렌드를 반영한 광고 이미지 및 영상 즉시 생성.
4. **Hallucination-Free Guardrail**: Brand Guard 에이전트가 모든 생성 결과물을 역사적 사실(Seed Data)과 대조 검증.

---

## 📂 Structure
- `src/agents/`: Google ADK 기반 멀티 에이전트 로직.
- `src/media/`: Imagen 및 Veo 클라이언트 인터페이스.
- `src/memory/`: 그래프 데이터베이스와 벡터 DB를 결합한 하이브리드 메모리.
- `src/api/`: FastAPI 기반 백엔드.
- `frontend/`: Next.js 기반의 타임라인 시각화 인터페이스.
- `GEMINI.md`: 기술적 상세 구현 및 에이전트 설계 사양.

---

## 🚀 Getting Started

1. **Environment Setup**:
   ```bash
   cp .env.example .env
   # GOOGLE_API_KEY 입력 (Gemini 3.0, Imagen, Veo 권한 필요)
   ```

2. **Installation**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Run Server**:
   ```bash
   python -m src.api.server
   ```

4. **Run Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
