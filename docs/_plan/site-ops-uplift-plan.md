# 사이트 운영 인프라 상향 계획 (검색, 웹폰트, 측정, 잔존 이슈)

작성일: 2026-07-18. 배경: 디자인 검토(2026-07-18) 후 "글로벌 SaaS 문서 사이트 수준" 갭 평가에서
문서 버저닝을 제외한 나머지 격차를 보완하기로 결정.

## 확정된 결정사항

- 웹 분석: GoatCounter (오픈소스, 무료, 쿠키 없음, 동의 배너 불필요)
- 검색: Algolia DocSearch 신청 (승인 전까지 현재 로컬 검색 유지)
- 한국어 웹폰트: Pretendard를 한글 폴백으로 추가 (Roboto 유지, 최소 변경)
- 문서 버저닝: 범위 제외 (가이드 성격상 불필요)

## 사전 파악된 사실

- DocsRating(`website/core/DocsRating.tsx`)은 `window.ga`(구 Universal Analytics)로 이벤트를
  전송한다. UA는 2023년 종료된 서비스라 현재 평가 데이터가 어디에도 수집되지 않는다.
  문구도 영어 하드코딩이며, svg에 onClick만 있어 키보드 접근이 불가능하다(접근성 이슈).
- 검색은 `@easyops-cn/docusaurus-search-local`(`docusaurus.config.ts:58`), 분석 도구는 미설정.
- CI는 `.github/workflows/`에 deploy, pre-merge 등 6개 워크플로우 보유. Lighthouse 잡 없음.
- `/en/reference/samples/conformance`에 broken anchor 3건이 빌드 경고로 잔존
  (en policy의 permitted-licenses 앵커 1건, en process의 checklist 및 vulnerability 앵커 2건).

## 공통 실행 장치 (모든 Phase 적용)

1. 청크 단위(4파일 이하) 수정 후 `bash .claude/scripts/verify.sh` 12/12 PASS와
   `cd website && npm run build` 통과를 확인하고 개별 커밋(영문 메시지).
2. Phase 종료마다 quality-gate:gate-verifier 에이전트로 독립 판정(DoD 역순 점검).
3. 이 계획 문서를 먼저 커밋하고, 진행 상황은 `docs/_plan/STATUS.md`에 갱신.
4. `website/src` 변경은 스코프 완화 가드레일(최소 변경, POSITIONING §5 중립 토큰) 준수.

---

## Phase 0 — 외부 신청 접수와 잔존 이슈 정리 (반나절)

외부 승인 대기 시간이 긴 항목을 먼저 걸어 두고, 리스크 없는 정리부터 처리한다.

### 0-1. Algolia DocSearch 신청 [사용자 액션]

- https://docsearch.algolia.com/apply 에서 신청: 사이트 URL(https://trustedoss.github.io),
  저장소 URL, 소유자 이메일. 공개 기술 문서라 무료 요건을 충족한다.
- 승인까지 며칠에서 몇 주 소요. 승인 메일의 appId, searchApiKey, indexName은 Phase 3에서 사용.

### 0-2. en conformance broken anchor 3건 수정

- en 번역본에서 헤딩 텍스트가 달라 앵커 id가 어긋난 것이 원인.
  en policy와 en process 페이지의 실제 생성 앵커를 확인한 뒤, 링크를 실제 앵커로 고치거나
  헤딩에 명시적 앵커(`{#anchor-id}`)를 부여해 ko와 en의 앵커를 일치시킨다.
- 대상: `/en/reference/samples/conformance`가 참조하는 3개 앵커.

### 0-3. 앵커 회귀 방지

- 앵커 0건 확인 후 `docusaurus.config.ts`에 `onBrokenAnchors: 'throw'`를 추가해
  이후 빌드에서 앵커 깨짐이 경고가 아닌 실패가 되게 한다.

DoD: 신청 접수 완료, ko와 en 빌드 경고 0건, verify 12/12, 커밋 완료.

---

## Phase 1 — Pretendard 웹폰트 (반나절)

### 1-1. POSITIONING.md 근거 기록

- §5 가드레일에 따라 폰트 토큰 변경 근거를 §6 수렴 현황에 한 줄 추가:
  Pretendard는 SIL OFL 오픈소스 폰트로 벤더 비귀속이며 중립 토큰 원칙을 유지한다.
  라틴 우선 폰트는 Roboto를 유지하고 한글 렌더링만 통일한다.

### 1-2. 폰트 도입 (self-host)

- npm `pretendard` 패키지 설치 후 `customTheme.scss`에서 가변 폰트의
  dynamic subset css(`pretendardvariable-dynamic-subset.css`)를 import.
  유니코드 레인지별 분할 서브셋이라 초기 로드가 작고 `font-display: swap`이 포함돼 있다.
  GitHub Pages 정적 호스팅이므로 CDN 의존 없이 번들에 포함한다.

### 1-3. 폰트 토큰 반영

- `--ifm-font-family-base`에서 Roboto 다음, 시스템 한글 폰트 앞에
  `"Pretendard Variable"`을 추가. 폰트 폴백은 글리프 단위로 동작하므로
  라틴은 Roboto, 한글은 Pretendard로 렌더된다.

### 1-4. 검증

- 대표 5페이지(랜딩, docs 개요, docs 본문, devsecops, reference 샘플)를
  ko와 en, 라이트와 다크에서 스크린샷 확인. computed font-family로 적용 확인.
- 네트워크 탭에서 초기 로드 서브셋 용량(수십 KB 수준) 확인, 레이아웃 이동(CLS) 없는지 확인.

DoD: 폰트 적용 확인, 빌드와 verify 통과, POSITIONING 근거 기록, 커밋 완료.

---

## Phase 2 — 측정 인프라 (1일에서 2일)

### 2-1. GoatCounter 도입 [사용자 액션 1건 포함]

- 사용자: https://www.goatcounter.com 에서 무료 계정과 사이트 코드 생성(예: trustedoss).
- 구현: Docusaurus는 client-side routing이라 count.js만으로는 페이지 전환이 집계되지 않는다.
  `website/src/clientModules/goatcounter.ts`를 신설해 `onRouteDidUpdate`에서
  `window.goatcounter.count()`를 호출하고, `docusaurus.config.ts`의 scripts와
  clientModules에 등록한다. 로컬 개발 환경에서는 전송하지 않도록 호스트 가드를 넣는다.

### 2-2. DocsRating 재작동과 접근성 수정

- `window.ga` 호출을 GoatCounter 이벤트(`goatcounter.count({path, event: true})`)로 교체.
  path 형식: `rating/{문서 id}/{up|down}`.
- 문구를 Translate로 감싸 ko와 en 모두 제공("이 페이지가 도움이 되었나요?").
- svg 직접 클릭 구조를 button 요소로 감싸 키보드 접근과 스크린리더 라벨을 보장.

### 2-3. Lighthouse CI

- `.github/workflows/lighthouse.yml` 신설(treosh/lighthouse-ci-action 사용).
  빌드 산출물을 serve한 뒤 대표 6개 URL(랜딩, docs 2개, devsecops, ai-coding, reference)을 측정.
- 기준: performance 90, accessibility 95, best-practices 95, seo 90.
  도입 초기에는 warn으로 시작해 2주 안정화 후 error로 승격.
- PR에 점수 리포트 코멘트가 남도록 설정.

### 2-4. 접근성 감사와 수정

- `@axe-core/playwright` 기반 스캔 스크립트(`.claude/scripts/a11y-scan.mjs`)를 만들어
  대표 페이지를 라이트와 다크에서 스캔. critical과 serious 위반을 수정한다.
  예상 유형: 색 대비, aria-label 누락, landmark 구조, 링크 텍스트.
- 스캔 스크립트는 verify.sh와 별도로 두고, 수동 실행 절차를 harness-guide에 기록.

### 2-5. 운영 루틴 문서화

- 월 1회 점검 체크리스트를 `.claude/harness-guide.md`에 추가:
  GoatCounter 대시보드(상위와 하위 페이지, 평가 이벤트 비율),
  Algolia no-results 쿼리(Phase 3 이후), Lighthouse 추이.
  점검 결과는 progress.md에 한 줄로 기록한다.

DoD: 실사이트에서 방문과 평가 이벤트가 GoatCounter에 집계됨, Lighthouse 잡 green,
a11y critical 0건, gate-verifier 독립 판정 통과, 커밋 완료.

---

## Phase 3 — Algolia DocSearch 전환 (승인 도착 시, 반나절)

### 3-1. 검색 교체

- 승인 메일의 자격 정보로 `themeConfig.algolia` 설정(contextualSearch: true로 ko와 en 분리).
- `@easyops-cn/docusaurus-search-local`을 themes 배열과 package.json에서 제거.
- 교체는 단일 커밋으로 분리해 문제 시 revert만으로 로컬 검색에 복귀할 수 있게 한다.

### 3-2. 크롤러 확인

- Algolia Crawler 대시보드에서 Docusaurus 기본 셀렉터 템플릿으로 색인이 생성되는지,
  ko와 en 페이지가 모두 수집되는지 확인.

### 3-3. 스모크 테스트

- 대표 쿼리 10개(SBOM, 취약점, OpenChain, 라이선스, 오타 케이스 포함)를 ko와 en에서
  검색해 기대 문서가 상위에 노출되는지 확인. 결과를 STATUS.md에 기록.

DoD: ko와 en 검색 정상, 오타 보정 동작 확인, 빌드와 verify 통과, 커밋 완료.

---

## 일정 요약

| Phase | 내용                               | 규모    | 선행 조건        |
| ----- | ---------------------------------- | ------- | ---------------- |
| 0     | DocSearch 신청, broken anchor 정리 | 반나절  | 없음             |
| 1     | Pretendard 웹폰트                  | 반나절  | 없음             |
| 2     | GoatCounter, Lighthouse CI, 접근성 | 1일~2일 | GoatCounter 가입 |
| 3     | DocSearch 전환                     | 반나절  | Algolia 승인     |

사용자 액션은 2건: DocSearch 신청(0-1), GoatCounter 가입(2-1). 나머지는 에이전트가 수행한다.

## 리스크와 대응

- DocSearch 승인 지연이나 거절: Phase 3만 보류되고 나머지는 영향 없음.
  거절 시 로컬 검색 한국어 튜닝(대안 경로)으로 전환.
- 폰트 용량 우려: dynamic subset으로 초기 로드를 제한하고, 문제 시 import 한 줄 revert로 복귀.
- Lighthouse 점수 미달: 도입 초기 warn 운영이라 CI가 막히지 않으며, 미달 항목은
  후속 청크로 수정한다.
