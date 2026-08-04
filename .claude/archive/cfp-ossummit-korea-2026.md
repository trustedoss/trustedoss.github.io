# CFP 작성 가이드 — Open Source Summit Korea 2026

**이벤트**: Linux Foundation Open Source Summit Korea 2026  
**일정**: 2026년 8월 11–12일, 서울  
**CFP 마감**: 2026년 4월 26일 23:59 KST  
**발표자**: 장학성 (Haksung Jang), SK텔레콤 Open Source Program Manager, OpenChain Korea Work Group Lead

---

## 핵심 포지셔닝

**"AI로 오픈소스 컴플라이언스를 민주화한다"**

Trusted OSS는 단순한 가이드가 아니라 **AI Agent가 회사별 맞춤 산출물을 자동 생성하는 오픈소스 킷**이다. OpenChain Korea WG Chair가 만들었다는 점에서 credibility가 강하다.

---

## Session Title

```
AI-Powered Open Source Risk Management: ISO Self-Certification Kit and 5-Level Governance Framework
```

---

## 추천 Track & Audience

- **Track**: OSS Enabling & Management
- **세부 토픽**: Operations Management & OSPOs
- **서브토픽**: Risk Management
  - "Compliance"는 라이선스 컴플라이언스 뉘앙스가 강해 ISO/IEC 5230만 다루는 것처럼 보일 수 있음
  - "Risk Management"는 라이선스 리스크(5230) + 보안 리스크(18974) + AI 코딩 리스크 + 공급망 리스크를 모두 포괄 — 발표 전체를 가장 정확하게 대표
- **Audience Level**: Intermediate (개념은 알지만 실무 적용 방법을 모르는 OSPO/개발자 대상)
- **언어**: Korean (한국어 발표 + 영문 슬라이드 조합 권장)

---

## Description 초안 (영문, ~900자 / 최대 1200자)

```
Open source compliance sounds expensive — consultants, lawyers,
complex tooling. But it doesn't have to be.

Trusted OSS is an open-source self-certification kit that guides
any organization from zero to ISO/IEC 5230 (license compliance)
and ISO/IEC 18974 (security assurance) conformance using AI agents.
No prior expertise required.

Built by the OpenChain Korea Work Group and released under CC BY 4.0,
the kit features:

• AI agents (Claude Code) that auto-generate company-specific
  compliance artifacts: OSS policy, SBOM, vulnerability response
  procedures, training curriculum, and conformance declaration
• DevSecOps pipelines (SAST, SCA, secret detection, IaC) ready to
  drop into any CI/CD environment
• A 5-level AI Coding Governance Maturity Model — from ad-hoc
  prompting (Level 1) to AI-augmented defense (findings-driven
  review, AI fuzzing) and continuous auto-remediation (Level 5).
  Teams self-assess where they stand and leave with a concrete
  next step.
• Browser-based tools requiring only an API key — no local setup

In this session, I'll walk through how any team can go from
no compliance process to a fully documented, self-certifiable
program in hours, not months. I'll also share how we're using
AI to close the compliance skills gap across Korean enterprises
and SMEs — making OpenChain certification accessible to all.

Attendees leave with a working toolkit they can clone and run today.
```

---

## "Benefits to the Ecosystem" 필드

```
1. Reduces the barrier to OpenChain ISO/IEC 5230 & 18974
   self-certification for SMEs and under-resourced teams
2. Demonstrates a replicable model for AI-assisted open source
   governance that any community can adopt
3. Provides immediately usable, CC BY 4.0 licensed tooling —
   attendees can fork and adapt for their own organizations
4. Advances the OpenChain ecosystem by growing the pool of
   certified organizations in Korea and Asia
```

---

## 발표 세션에서 강조할 포인트

### 1. "Why now?" — AI + 공급망 규제의 교차점

- EU CRA(Cyber Resilience Act), 미국 EO 14028 → SBOM/보안 보증 의무화 흐름
- 동시에 AI 코딩 도구가 라이선스 위험을 증폭시키는 새 현실
- 두 문제를 동시에 해결하는 접근

### 2. "From hours to minutes" 실증

- 기존: 컨설턴트 + 수개월 → 고비용
- Trusted OSS: Agent 실행 → 30분 내 첫 산출물 생성
- Live demo 또는 화면 캡처로 보여주면 강력

### 3. OpenChain 커뮤니티 연결고리

- KWG에서 만들고, KWG를 통해 검증된 내용임을 강조
- 이미 사용한 기업/팀 사례가 있다면 언급

### 4. AI Coding Governance 5단계 성숙도 모델 — 신선한 각도

- 청중이 자기 팀의 현재 위치를 즉각 진단할 수 있는 프레임워크
- 1단계(프롬프트 의존) → 2단계(Rules 내재화) → 3단계(CI/CD Hard Block) → 4단계(AI 방어 레이어) → 5단계(자동 교정)
- **4단계 "AI 공격에 AI 방어로"**: findings-driven 리뷰 + AI 퍼징 — 이 주제는 청중에게 가장 신선하게 느껴질 것
- 각 단계의 진입 비용(10분/30분/전담팀)을 명시해 현실적 로드맵 제시

---

## 슬라이드 구성안 (40분 기준)

| 슬라이드 | 내용                                                                                       |
| -------- | ------------------------------------------------------------------------------------------ |
| 1–2      | Problem: OSS compliance is broken for most orgs (비용, 전문성 부족, AI 코딩의 새 위험)     |
| 3        | Solution overview: Trusted OSS = 3-layer approach (체계구축 + AI코딩 거버넌스 + DevSecOps) |
| 4–5      | Layer 1: ISO/IEC 5230 & 18974 자체 인증 흐름 (Agent → 산출물 → 인증)                       |
| 6–7      | LIVE DEMO: Agent 실행 → policy 생성 (또는 녹화)                                            |
| 8        | "당신의 팀은 지금 몇 단계인가?" — 5단계 성숙도 매트릭스 한눈에 보기 (자가진단 slide)       |
| 9        | 1–2단계: 프롬프트 의존 → Rules 내재화 (지금 당장 할 수 있는 것, 설정 10분)                 |
| 10       | 3단계: CI/CD Hard Block — AI가 만든 코드도 파이프라인이 걸러낸다                           |
| 11       | **4단계 하이라이트**: "AI 공격에는 AI 방어로" — findings-driven 리뷰 · AI 퍼징             |
| 12       | 5단계: Dependabot·Renovate 자동 교정 → 공급망 보안 선순환 완성                             |
| 13       | Layer 3: DevSecOps CI/CD 자동화 (SBOM → 취약점 → PR 코멘트 플로우)                         |
| 14       | Architecture: 어떻게 오픈소스로 만들었나 (CC BY 4.0, Claude Code 기반)                     |
| 15       | Results & adoption (KWG 활용 현황, 기업 사례)                                              |
| 16       | How to contribute / get started (QR 코드 → trustedoss.github.io)                           |
| 17       | Q&A                                                                                        |

---

## 주의사항

- **"No product pitches"** 규칙: SK텔레콤 제품/서비스 언급은 최소화, 오픈소스 프로젝트와 커뮤니티에 집중
- **"Presented this talk before?"**: AI 코딩 거버넌스 포함 버전을 처음 발표하는 것이라면 No
- CFP 마감까지 시간이 촉박하므로 오늘 밤 제출 권장
