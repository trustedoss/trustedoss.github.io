# 발표 준비 — Open Source Summit Korea 2026

**세션**: AI-Powered Open Source Risk Management: ISO Self-Certification Kit and 5-Level AI Coding Governance
**일시**: 2026-08-12(수) 13:35~14:15 KST · **장소**: Rose · **길이**: 40분 슬롯(실질 35분)
**행사**: 2026-08-10~12, 서울 · **트랙**: OSS Enabling & Management
**발표자**: 장학성, SK텔레콤 Open Source Program Manager / OpenChain Korea Work Group Lead

> 이 문서는 CFP 제출본(2026-04)을 발표 준비용으로 갱신한 것이다. 제출 원문은 아래 "제출한
> Description"에 그대로 보존한다.

---

## 핵심 포지셔닝

**"AI로 오픈소스 컴플라이언스를 민주화한다"**

Trusted OSS는 가이드가 아니라 **AI Agent가 회사별 맞춤 산출물을 자동 생성하는 오픈소스 킷**이다.
OpenChain Korea Work Group에서 만들고 검증했다는 점이 신뢰의 근거다.

---

## 최종 발표 구성 (35분 + 전환 여유)

슬롯은 13:35~14:15(40분)이다. 다음 발표자가 14:15에 시작하므로 **실질 가용 시간은 35분**으로
두고, 남는 5분은 입퇴장과 장비 전환에 배정한다. 리허설도 35분 기준으로 실측한다.

| 구간                     | 시간 | 내용                                                                |
| ------------------------ | ---- | ------------------------------------------------------------------- |
| 문제 제기                | 3분  | 사고 사례 → 규제(CISA 2026·EU CRA) → AI 코딩이 더한 새 위험         |
| 전체 지도                | 2분  | 두 덩어리 + TRUSCA 위치를 한 장에. 이후 모든 슬라이드가 이 지도 위  |
| 1부 — ISO 자체 인증 키트 | 9분  | 흐름 2분 / SBOM 생성의 간극 1.5분 / 녹화 데모 4.5분 / 등재 절차 1분 |
| 2부 — AI 코딩 거버넌스   | 10분 | 5단계 자가진단 4분 / 4단계 AI 방어 3분 / 에이전트·MCP 3분           |
| TRUSCA — 인증 이후       | 5분  | 왜 필요한가 2분 / 무엇인가 2분 / 로드맵 1분                         |
| 시작 방법                | 1분  | QR, CC BY 4.0, 기여                                                 |
| Q&A                      | 5분  | 못 받은 질문은 세션 후 개별 대응으로 넘긴다                         |

시간이 지연될 때 축소 순서: Q&A → TRUSCA 로드맵 1분 → 4단계 AI 방어 3분. 1부 데모와 5단계
자가진단은 세션의 핵심이므로 마지막까지 유지한다.

### 서사의 뼈대

1부와 2부가 마지막에 한 지점에서 만난다. 키트가 제공하는 범위는 체계 수립과 산출물 생성까지이고,
ISO/IEC 18974 가 요구하는 것은 지속 운영이다. 인증 선언으로 종료되지 않는다는 점을 청중이
인식한 시점에 TRUSCA 를 제시하면 홍보가 아니라 논리적 귀결로 전달된다. TRUSCA 로드맵의
1순위가 "에이전트가 패키지를 반입하기 전에 정책을 조회하는 MCP 서버"이므로, 2부의 에이전트
거버넌스와 직접 연결된다.

닫는 문장: **"AI 에이전트를 통제하는 이야기로 시작해, 그 에이전트가 스스로 정책을 조회하게 만드는
지점에서 1부와 2부가 만납니다."**

---

## 구간별 상세

### 1. 문제 제기 (3분, 슬라이드 3장)

13:35는 점심 직후이므로 목차로 시작하지 않는다. 사고 사례부터 제시한다.
세 장이 각각 뒤의 본문과 연결되도록 구성한다.

- **① 오픈소스 공급망 위험** — XZ Utils(2024), Log4Shell(2021). 구성 요소를 파악하지 못하면
  영향 범위조차 판단할 수 없다. 기존에 알려진 문제로 짧게 둔다
- **② AI 코딩이 바꾼 조건** — 세션 제목의 절반을 여기서 설명한다. 세 가지다.
  AI 가 제안한 의존성이 사람의 검토를 거치지 않고 반입되고, 생성된 코드는 기존 rule 에 없는
  형태를 만들며, agent 가 MCP 로 외부 tool 을 호출하면 그 tool 자체가 공급망 입력이 된다.
  기존 통제는 사람이 코드를 작성한다는 전제 위에 설계되었다는 점이 요지다 → **2부로 연결**
- **③ 규제 요구와 대응 수단의 격차** — EU CRA 보고 의무 2026-09-11, 전면 적용 2027-12-11.
  CISA 2026 최소 요소(2026-07-29, 행사 2주 전)가 NTIA 2021 을 대체하며 component hash 와
  license 가 권고에서 필수가 됐고 적용 범위가 AI software 와 SaaS 까지 넓어졌다.
  그러나 납품되는 SBOM 은 요구 수준에 미치지 못한다. 공급사는 SBOM 개념부터 생소하고,
  생성 방법도 모르며, 도구를 살 예산도 없다. 무료 도구를 안내해 생성하게 해도 transitive
  dependency 누락, PURL 누락 같은 결함으로 최소 요소를 채우지 못한다.
  **"만들지 못한다"가 아니라 "만들어도 요구 수준에 못 미친다"가 문제의 핵심이다.**
  폐쇄망과 "소스 없음"은 문제로 들지 않는다(도구가 로컬 실행되고, 공급사는 대체로 자기 소스를
  가지고 있다)
  → **8번 슬라이드(BomLens)로 연결**

CISA 기준 변경을 **이 가이드가** 이미 반영했다는 점을 한 줄 언급한다. 도구(BomLens·TRUSCA)의
구현 여부는 별개 사안이므로 혼동하지 않는다.

③이 1부의 BomLens 대목과 문제·해결 쌍을 이룬다. 이 구조 덕분에 BomLens 는 도구 소개가 아니라
발표가 제기한 문제의 답 위치에 놓인다.

### 2. 전체 지도 (2분)

체계 구축과 AI 코딩 거버넌스 두 덩어리, 그리고 그 바깥의 TRUSCA 를 한 장에 담는다.
DevSecOps 는 별도 상자로 그리지 않는다. 5단계 모델이 성숙도 판단 틀이고 DevSecOps 가이드는
그 3단계·5단계의 구현 방법이므로, 상자로 두면 설명 없이 지나가는 항목이 생긴다.
사이트에서는 독립 메뉴이므로 19번 시작하기 슬라이드에서 안내한다.

### 3. 1부 — ISO 자체 인증 키트 (9분)

- 흐름(2분): agent 9종 → 산출물 24종 → 갭 분석 → 선언문. 5230 과 18974 의 공통 기반이 크다는 점.
  산출물을 낭독하지 않고 화면으로 제시한다
- **SBOM 정확도(1.5분)**: 문제 제기 세 번째 항목을 여기서 받는다. 누락이 생기는 원인은
  **의존성 트리가 빌드해야 확정된다**는 점이다. 로컬 런타임과 빌드 도구가 프로젝트와 맞지 않으면
  도구가 실패하지 않고 부분 결과만 내고, 공급사는 그대로 납품한다.
  **BomLens**(Apache-2.0)는 빌드 환경을 Docker image 하나로 제공해 이 지점을 해소한다
  (Java·Python·Node.js·Ruby·PHP·Rust·Go·.NET·Swift·C/C++). 설치 프로그램과 웹 UI 가 있어
  CLI 를 모르는 담당자도 쓸 수 있고, 받은 SBOM 을 형식 요건 대비로 점검하는 기능(`--analyze`)도
  있다. 4번 슬라이드의 네 가지 문제에 각각 대응한다
- 데모(4.5분): **녹화본 2배속 + 말로 해설.** 라이브 실행 금지(콘퍼런스 와이파이 위험)
- 등재 절차(1분): 체크리스트 내려받기 → 자체 점검 → get-started 온라인 신청 폼

### 4. 2부 — AI 코딩 거버넌스 (10분)

- 5단계 자가진단(4분): "지금 우리 팀은 몇 단계인가". 표가 복잡하면 전달되지 않는다.
  거수를 요구하지 않고 **3초 침묵**으로 판단할 시간을 준다
- 4단계 하이라이트(3분): AI 공격에 AI 방어 — findings-driven 리뷰, AI 퍼징.
  3단계 도구가 추린 결과만 AI에 넘겨 토큰을 아끼는 구조
- 에이전트·MCP 거버넌스(3분): KWG 가이드가 다루지 않는 영역이라 신선도가 가장 높다.
  `postmark-mcp` 사례(1.0.15 까지 정상, 이후 버전에서 숨은 BCC 로 전체 발신 메일 외부 복사)로
  버전 고정이 필요한 근거를 제시한다. 데이터 반출 경로 판정을 포함한 통제 6가지

### 5. TRUSCA — 인증 이후 (5분)

- **왜 필요한가(2분)**: 가이드가 제공하는 범위는 체계와 1회성 산출물까지다. 18974 는 주간 단위
  취약점 DB 갱신, VEX 판정, 라이선스 정책 게이트의 지속 운영을 요구한다. 이 지점에서 상용 SCA
  도입 비용 때문에 중단되는 경우가 많다
- **무엇인가(2분)**: Apache-2.0 self-hosted SCA. cdxgen 기반 30개 이상 생태계 탐지,
  Trivy 통합 DB(NVD·OSV·GHSA·EPSS·KEV, 주간 갱신), VEX 수출입과 7단계 triage,
  라이선스 3계층 정책과 NOTICE 자동 생성, CI 게이트, RBAC·감사 로그.
  폐쇄망 자체 호스팅이 국내 기업 상당수에 중요한 조건
- **로드맵(1분)**: 도달 가능성(reachability) 분석, 에이전트 pre-flight 정책 MCP 서버.
  2부 와 연결하며 마무리한다
- 링크: https://github.com/trustedoss/trusca · https://trustedoss.github.io/trusca/

---

## 모델과 도구의 경계

**5단계 모델에 TRUSCA를 행으로 넣지 않는다.** 모델은 통제 방식의 성숙도이지 도구 목록이 아니다.
특정 도구를 넣으면 (1) 어떤 조직이든 자기 위치를 찾을 수 있어야 하는 모델의 일반성이 깨지고,
(2) 벤더 중립이라는 이 프로젝트의 자산이 훼손된다. 자가진단 슬라이드에서 청중이 "결국 도구를
팔려는 프레임"으로 읽으면 그 순간 설득력을 잃는다.

다루는 대상도 다르다. 5단계는 AI가 만든 코드의 위험을, TRUSCA는 의존성 위험을 다룬다. 사람이
쓰든 AI가 쓰든 의존성 관리는 필요하므로 별개다.

대신 **구현 선택지로 연결한다.** 3단계 SCA 자리에서 syft·grype가 파일 단위로 하는 일을 TRUSCA는
플랫폼으로 하고, 5단계 지속 모니터링 자리에서 Dependabot·Renovate 옆에 선다. TRUSCA 구간에서
"3단계와 5단계를 도구 조합이 아니라 플랫폼 하나로 구현하면 이렇게 된다"고 이으면, 모델은 중립을
지키고 TRUSCA는 그 기준을 만족하는 구현 하나로 자리잡는다.

에이전트 pre-flight 정책 조회(TRUSCA 로드맵)는 기존 단계에 들어가지 않는다. 규칙으로 부탁하는
2단계도, CI에서 사후 차단하는 3단계도 아니고, 에이전트가 패키지를 넣기 전에 조회하는 방식이라
그 사이에 새 지점을 연다. **"모델이 아직 담지 못한 다음 단계"**로 발표를 닫는다.

### BomLens를 어디서 다루는가

소개 이유는 소속이 아니라 **공급망 보안의 실제 공백을 메우기 때문이다.** 전 세계 공급사가 정확한
SBOM 을 만들어야 하는데 쓸 만한 수단이 없어 못 만든다. 이 사실을 문제 제기에서 세우고 1부 에서
받는 구조로 배치한다. 그러면 도구 소개가 아니라 발표가 제기한 문제의 답이 된다.

- **1부, SBOM 생성 대목 (1.5분, 주 배치)** — 소스 없는 납품물과 폐쇄망이라는 공백을 명시한 뒤
  BomLens 를 답으로 놓는다. 로컬 실행, 소스·컨테이너·바이너리·펌웨어 입력, CycloneDX + 고지문 +
  위험·보안 리포트 + ML-BOM 출력. Apache-2.0 명시
- **TRUSCA 구간 (한 줄)** — TRUSCA 의 규제 크로스워크 데이터가 BomLens 에서 온 것이라는 사실
  (TRUSCA CHANGELOG Unreleased 항목, `THIRD_PARTY_NOTICES.md` 귀속 표기). 오픈소스 프로젝트끼리
  실제로 데이터를 주고받는 사례로 말한다

표현 주의: **"최적의 도구"라고 단정하지 않는다.** 비교 평가를 제시할 게 아니면 근거 요구를 받는다.
"펌웨어와 바이너리에서도 SBOM 을 만들 수 있다"는 구체적 능력만으로 다른 무료 도구와 충분히 갈린다.
톤은 "우리 회사가 만든"이 아니라 **"Apache-2.0으로 공개된"**에 방점을 둔다.

---

## 지켜야 할 선

- **No product pitches** 규칙. TRUSCA는 Apache-2.0이라 소개 자체는 문제없으나, 상용 도구와
  기능을 나열해 비교하지 않는다. 이 로드맵의 출발점이 Black Duck 주최 웨비나 질문 분석이었고
  행사에 관계자가 있을 수 있다. **"상용보다 낫다"가 아니라 "예산·폐쇄망 제약이 있는 팀에게
  선택지가 하나 더 있다"**로 프레이밍한다
- SK텔레콤 언급은 소속 소개 한 번으로 충분
- 인접 세션과의 역할 분담: OpenChain 2027 전략(Meixia Wang), "SBOMs Aren't Enough"(정용재·
  Justin Cappos)가 방향과 원리를 다룬다. 우리 세션은 **"그래서 내일 아침에 무엇을 실행하나"**를
  맡는다. SBOM 생성 자체보다 산출물 생성과 AI 코딩 시대의 새 위험에 무게를 싣는다

---

## 준비 목록 (D-3, 2026-08-09 기준)

- [x] 슬라이드 구성안 + 발표 스크립트 작성 — `.claude/talk-script-ossummit-2026.md` (20장, 30분).
      슬라이드는 한국어 문장 + 영어 키워드
- [ ] 영문 전용 슬라이드 별도 판 — 배포용. 위 구성을 그대로 옮긴다
- [ ] **CISA 2026 최소 요소 구현 주체 확인** — 공개 저장소에서는 BomLens·TRUSCA 어느 쪽에서도
      확인되지 않았다(TRUSCA 크로스워크 기준선은 BSI TR-03183-2·NTIA·EU AI Act). 릴리스에
      들어갔다면 버전 번호와 함께 말하고, 아직이면 "대응 진행 중"으로 표현한다
- [ ] **데모 녹화** (가장 오래 걸림) — Agent 실행 → 정책 생성까지. 실패 시 재촬영 여유 확보.
      2배속 재생 기준 5분에 맞춘다
- [ ] **5단계 자가진단 슬라이드** — 3초 안에 자기 위치를 찾을 수 있어야 한다. 복잡하면 실패
- [ ] 전체 지도 슬라이드 (체계 구축 · AI 코딩 거버넌스 + TRUSCA)
- [ ] CISA 2026 최소 요소 슬라이드 1장
- [ ] `postmark-mcp` 사례 슬라이드 — 사실 경계 주의(악성 시작 버전은 추정, ActiveCampaign
      연관은 미확인)
- [ ] SBOM 생성의 간극 슬라이드 + BomLens 1장 — 소스 없는 납품물·폐쇄망을 왼쪽에, 입력과 출력을
      오른쪽에 두면 1.5분에 들어간다
- [ ] TRUSCA 3장 (왜 / 무엇 / 로드맵)
- [ ] QR 코드 — trustedoss.github.io
- [ ] 리허설 1회 — **35분** 안에 들어가는지 실측. TRUSCA를 넣어 빠듯하므로 필수
- [ ] 오프라인 폴백 — 네트워크 없이도 슬라이드·녹화가 재생되는지 확인

---

## 4월 CFP 이후 프로젝트 변경 (발표에 반영할 것)

| 변경                              | 발표 반영 지점                              |
| --------------------------------- | ------------------------------------------- |
| 에이전트·MCP 도구 거버넌스 페이지 | 2부 신규 3분 (KWG 미커버 영역, 신선도 최상) |
| CISA 2026 SBOM 최소 요소          | 문제 제기 (행사 2주 전 뉴스)                |
| 5.4 AI SBOM 챕터(BomLens 실측)    | 1부 SBOM 생성의 간극 1.5분 (주 배치)        |
| AI 생성 코드 법적 고려 페이지     | 질문 대비 (저작권 귀속, Thaler 2026-03)     |
| TRUSCA 연계                       | 신규 구간 5분                               |
| 브라우저 도구 6종                 | 시작 방법 (API 키만으로 즉시 사용)          |

---

## 제출한 Description (2026-04 원문, 수정 금지)

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

### Benefits to the Ecosystem (제출 원문)

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
