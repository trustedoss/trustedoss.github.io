# TrustedOSS 개편 — 실행 현황 (resume용)

> 목적: 긴 세션에서 히스토리가 유실돼도 이 파일만 보면 즉시 재개 가능. 매 task 후 갱신·커밋한다.
> 최종 갱신: 2026-08-12

## 영문화 잔여 조사와 보완 계획 (2026-08-12) — 계획 수립 완료

> 조사 방법: 빌드된 `build/en/**/*.html` 87개에서 script·style·태그를 제거하고 한글을
> 추출했다. 소스가 아니라 실제 렌더 결과를 기준으로 삼아야 독자가 마주치는 것만 잡힌다.
> 결과: 31개 페이지에 한글 잔존. 언어 전환 드롭다운의 "한국어"는 정상이므로 제외했다.

### 1단계 — 영문 독자에게 한국어 산출물이 나가는 것 (기능 결함) — 완료

- [x] `website/static/tools/` 도구 9개를 `?lang=en` 사전 방식으로 통일했다.
      분석기 5개는 Claude API 프롬프트까지 언어 분기시켜 **생성 결과물도 영어로 나온다**
      (`T.buildPrompt(...)` 가 ko/en 두 벌을 갖는다). 데모 4개는 화면 문자열과
      IaC 샘플 코드의 주석까지 번역했다. 영문 페이지 iframe 11곳을 `?lang=en` 으로 연결
- [x] 영문 docs 5개 파일의 `` `시작` `` 입력 안내를 `` `start` `` 로 바꿨다

검증: 도구 9개를 브라우저에서 ko/en 양쪽으로 열어 확인했다. 빌드 HTML 정적 스캔은
JS 치환을 반영하지 못하므로 도구 페이지 판정에 쓰면 안 된다(소스에는 ko 폴백이 남는다).
빌드 중에 스캔하면 파일이 12개만 잡혀 오판하므로 빌드 완료 후에 센다.
결과: 영문 페이지 88개 중 한글 잔존 30개 (도구 10개는 위 이유로 정상, 나머지 20개가 2·3단계 몫).

### 2단계 — 영문 첫인상과 SEO — 완료

원인이 두 갈래였다. Hero 와 Prerequisite 는 이미 `<Translate>` 로 감싸져 있었는데
code.json 에 키 자체가 없어 한국어로 폴백되고 있었다. 코드의 번역 키와 code.json 을
전수 대조해 누락 6개를 찾았고, `npx docusaurus write-translations --locale en` 으로
추출한 뒤(기존 번역 0개 변경 확인) 영문을 채웠다. Showcase 의 문서 미리보기와
Heading 의 aria-label 은 아예 감싸지지 않은 raw 문자열이라 `translate()` 로 감쌌다.

- [x] 랜딩 Hero: cta.quickstart, terminal.progress, chip 3개. 터미널 창 경로도 로케일별로
      분리해 영문에서는 `agents/en/02-organization-designer` 가 보인다
- [x] Showcase 의 정책·선언문 미리보기 2개를 `translate()` 로 감쌌다
- [x] `theme/Heading/index.tsx` 의 aria-label·title ("링크 복사", "복사됨").
      모든 문서 헤딩마다 붙어 스크린리더에 노출되던 것
- [x] `components/Prerequisite/index.tsx` 의 aria-label 과 `prerequisite.label` 키
- [x] `docusaurus.config.ts` JSON-LD. `DOCUSAURUS_CURRENT_LOCALE` 로 분기해 영문 빌드에는
      영어 name·description 과 `inLanguage: 'en'` 이 들어간다
- [x] 페이지 하단 이전·다음 네비게이션. 원인은 Docusaurus 가 pagination 라벨을
      front matter(`pagination_label` → `sidebar_label` → title)에서 가져오기 때문이었다.
      sidebars.ts 의 label 은 사이드바 전용이라 `sidebar.docs.doc.*` 번역이 닿지 않는다.
      영문 문서 8개에 `pagination_label` 을 넣어 해결했다

결과: 영문 페이지의 한글 잔존이 도구 제외 20개에서 8개로 줄었고, 남은 8개는 전부 블로그(3단계)다.

### 3단계 — 주변 자산 — 완료

- [x] 블로그 `welcome` 글을 `i18n/en/docusaurus-plugin-content-blog/` 에 번역해 넣었다.
      이것으로 영문 사이트의 한글 잔존이 0이 됐다(도구 페이지의 ko 폴백 문자열 제외)
- [x] `llms.txt` 와 `llms-full.txt` 를 이중 언어로 다시 썼다. AI 크롤러가 읽는 파일이고
      정적 파일이라 로케일별로 나눌 수 없어, 영문 섹션을 앞에 두고 한국어 섹션을 유지했다.
      영문 URL(`/en/...`)과 `agents/en/`, 도구의 `?lang=en` 도 함께 안내한다
- [x] README 는 `README.en.md` 가 없는 게 아니라 한 파일 안에 영문 섹션이 이미 있었다
      (조사 때 잘못 봤다). 그 섹션이 `cd agents/02-...` 를 안내하던 것을 `agents/en/` 으로
      고치고, 양쪽 언어의 저장소 구조 트리에 `agents/en/` 과 `templates/en/` 을 넣었다
- [x] `samples/` — README 4개는 이중 언어로 만들고(한국어 섹션 유지 + 영문 섹션 추가),
      코드 주석과 출력 문자열은 영문으로 통일했다. 맥락 설명은 README 가 담당한다.
      편집 후 python·node 문법 검사와 JSON·XML 파싱으로 파일이 여전히 유효함을 확인했다

`manifest.json` 은 한국어지만 어디에서도 참조되지 않는다(`rel="manifest"` 링크가 없다).
영문화 대상이 아니라 정리 대상이므로 손대지 않았다.

### 처리 완료

- [x] 발표 슬라이드. 한글 잔존 521건으로 가장 많았지만 슬라이드 본문은 원래 영어였고,
      한글은 전부 발표자 노트(`.notes-src` 30개 블록)였다. 웹 공개본에는 노트가 필요 없으므로
      `deck/publish.sh` 가 복사할 때 노트 블록을 걷어내고 S 키 핸들러도 함께 막도록 고쳤다.
      노트를 지우고 S 키를 살려 두면 빈 발표자 패널이 열린다. `deck/index.html` 원본은
      노트를 그대로 유지한다. 한국어와 영문 talks 페이지의 조작 안내에서 S 키 항목을 뺐다.
      결과: 공개본 한글 0자, 슬라이드 23장 유지, 브라우저에서 이동·다크모드 정상

### 방향 확인이 필요한 것

- `output-sample/` 은 한국어지만 웹의 `reference/samples/` 영문판이 이미 번역돼 있어
  저장소를 직접 열 때만 노출된다. 우선순위가 낮다
- `CONTRIBUTING.md`·`POSITIONING.md`·`STYLEGUIDE.md` 는 기여자용이다
- 영문화 대상 아님: `.claude/` 하네스, `docs/_plan/`, `deck/`, 각 `CLAUDE.md`

## agents·templates 영문 트리 (2026-08-12) — 진행 중

> 계기: 영문 docs 12개 파일이 `cd agents/02-organization-designer` 를 그대로 안내하는데
> agent CLAUDE.md 18개와 templates 16개가 전부 한국어라, 영문 독자가 실행하면 한국어 질문을
> 받는다. 영문 샘플 산출물 페이지(`reference/samples/` 7개)는 이미 영문이라 결과도 어긋난다.
> 방식은 B안(영문 트리 분리) 확정. docs 를 ko/en 이중으로 관리하는 기존 구조와 맞춘다.

배치: `agents/en/<agent>/CLAUDE.md`, `templates/en/<category>/*.md`. output 경로는 공용(`output/`).

- [x] 1단계: `templates/en/` 16개 번역 (organization 3, policy 2, process 5, training 2, conformance 3)
      — 용어는 이미 영문화된 `reference/samples/` 7개 페이지에서 추출해 맞췄다
- [x] 2단계: `agents/en/` 체인 9개 + 마스터 `agents/en/CLAUDE.md`
      — 영문 섹션명은 `## Input questions` / `## Output deliverables` / `Behavior on session start`
      로 고정했다(4단계에서 스크립트가 이 문자열을 인식해야 한다). 경로는 `../../../output/...`
- [x] 3단계: `agents/en/` 독립 도구 8개 + prompts 2개
      (ai-coding-setup, devsecops-setup, iac-fixer, sast/secret/sbom-vuln-analyst,
      level2-automation/issue-tracker·pr-comment). 두 prompts 의 "한국어로 작성" 지시는
      "Write in English" 로 바꿨다
- [x] 4단계: `test-agent-specs.py` 를 TREES(ko·en) 구조로 확장했다. 트리마다 섹션 헤더
      문자열과 templates 접두사를 따로 두고, agents·templates 의 ko/en 파일 패리티까지
      한 스크립트에서 검사한다. validate-chain.py 는 output/ 만 보므로 수정 불필요
- [x] 5단계: 영문 docs 12개 파일의 `agents/...` → `agents/en/...` (46곳)
- [x] 6단계: verify.sh 13/13, `npm run build` ko·en 성공, 루트 CLAUDE.md·README·
      harness-guide 갱신. 영문 트리 한글 잔존 0건, 경로 방향 교차 확인 완료

커밋 완료. 슬라이드 세션이 덱 커밋을 마쳐 pre-commit 훅이 풀린 뒤 한 커밋으로 묶었다.
`.claude/STATUS.md` 는 그 세션의 자동 갱신 파일이라 제외했다.

동시 세션 주의 (2026-08-12): 발표 슬라이드 세션이 같은 저장소에서 `deck/index.html` 과
`website/static/reference/talks/.../slides.html` 을 편집 중이다. 그 세션이 스테이징 전체를
커밋하면서 `agents/en/` 19개 파일이 덱 커밋 `a16ffcf` 에 섞여 들어갔다(내용 손실은 없음).
그 세션이 끝날 때까지 이쪽은 커밋하지 않고 파일 작업만 진행한다.

각 단계 종료 시 동일 게이트: 파일 수 대조 → verify.sh → 이전 단계 산출물 회귀 확인.
반드시 조건부로 바꿀 것: `agents/ai-coding-setup/prompts/generate-rules.md:133` 과
`devsecops-setup/prompts/generate-pipeline.md:136` 의 "생성하는 모든 파일은 한국어로 작성한다".

## OSS Summit Korea 2026 발표 준비 (2026-08-04) — 진행 중

> 세션 확정: 2026-08-12(수) 13:35~14:15, Rose. 40분 슬롯(전환 여유 제외 실질 35분).
> 트랙 OSS Enabling & Management.
> 제목 "AI-Powered Open Source Risk Management: ISO Self-Certification Kit and 5-Level AI
> Coding Governance". 준비 문서: `.claude/talk-ossummit-korea-2026.md`

- [x] 4월 CFP 문서를 발표 준비 문서로 갱신 — 확정 세션 정보, 40분 구성, 준비 목록
- [x] 구성 확정: 양축 균형(ISO 키트 9분 + AI 코딩 거버넌스 10분) + TRUSCA 5분.
      두 축이 TRUSCA 로드맵의 에이전트 pre-flight MCP 서버에서 합류하는 서사
- [ ] 데모 녹화 (Agent 실행 → 정책 생성, 2배속 5분)
- [ ] 슬라이드 작성 — 전체 지도, 5단계 자가진단, CISA 2026, postmark-mcp, TRUSCA 3장
- [ ] 리허설 1회 (35분 실측)

## TRUSCA 4단계 제안과 참조 구현 정정 (2026-08-09) — 완료

> 계기: 5단계 모델 대비 TRUSCA 워크플로 점검에서 4단계만 비어 있음을 확인.
> 이슈 초안(`docs/_plan/trusca-issue-level4-ai-review.md`)을 전달했고 TRUSCA 팀이 구현·머지
> (PR #33, `ai-review.yml`, 2026-08-09). 회신에서 우리 참조 구현의 결함 여러 건이 지적됨.

- [x] 3·5단계 실전 사례 링크 — `strategy.md` 와 DevSecOps 영역별 페이지 4곳, container-security
- [x] docs 쪽 공개 운영 자산 링크 — 릴리스 SBOM(05-tools/sbom-management), SECURITY.md 와
      고지문(04-process), 워크플로 17개 분할(pipeline-design)
- [x] 참조 구현 정정 `4692084` — timeout·continue-on-error 부재(API 장애가 PR 을 red 로 만듦),
      코멘트 중복(마커로 갱신), 포크 PR 판정 유도(프롬프트에 데이터 취급 지시 + 한계 명시),
      모델 ID, "기존 산출물 재사용" 서술이 실제(재실행)와 어긋난 점, Trivy 단일 엔진 대안
- [x] 사실 오류 3건 — dependabot 6개 항목(5개 아님), dogfood-scan 은 수동 실행,
      IaC 는 대상 부재가 아니라 `trivy config` 미도입(charts/ 실재 확인)
- [x] 4단계 실전 사례 반영 `a89a472` — 머지 확인 후 "공개 사례가 드물다" 삭제하고 링크.
      비차단·PR 변경분만 검사·키 없으면 skip 세 가지를 참고 설계로 기록
- [x] `.gitignore` 에 브라우저 자동화 부산물 추가

회신 중 반박할 것: `actions/checkout@v7` 와 `github-script@v9` 는 실재한다(릴리스 확인).
TRUSCA 가 v4 를 쓰는 것은 저장소 관례이며 우리 가이드가 틀린 것은 아니다.

## 발표 자료 (2026-08-09) — 스크립트 완료, 슬라이드 제작은 별도 세션

> 슬라이드 21장 구성안 + 발표 스크립트: `.claude/talk-script-ossummit-2026.md`
> 준비 노트: `.claude/talk-ossummit-korea-2026.md`

- [x] 21장 구성 확정 — 발표 30분 50초 + Q&A 4분 30초 = 35분 20초. 슬라이드별 시작 시각·길이
      명시, 말할 내용을 분당 300자 기준으로 작성
- [x] 문제 제기 재구성 — 공급망 위험 / AI 코딩이 바꾼 조건 / 규제와 SBOM 품질의 격차.
      각 장이 뒤의 본문과 연결되도록 배치
- [x] 4단계를 4a·4b 두 갈래로 분리 — 4a 만으로는 12번이 제기한 사각지대가 남는다는 논리 결함 해소
- [x] TRUSCA 위치 재정의 — "선언 이후"가 아니라 거버넌스를 실제로 운영하는 플랫폼
- [x] 전체 링크 목록 + 예상 질문 6종 + 리허설 체크
- [ ] 슬라이드 제작 — 별도 세션에서 새로 시작하기로 결정(2026-08-10)

## 노후화 전수 검토 반영 (2026-08-04) — 완료

> 근거: 프로젝트 전 영역을 3분할해 독립 검토(Fable 5) — ISO 체계구축 트랙 / AI 코딩·DevSecOps
> 트랙 / 하네스·레퍼런스 자산. 외부 사실은 1차 출처로 재확인 후 반영.

- [x] 1단계 실제 실패 지점 4건 `6f7db55` — OpenChain 등재 절차를 실제 흐름(체크리스트 내려받기
      → 자체 점검 → get-started 온라인 신청 폼)으로 재작성(기존의 "Submit Conformance 버튼"은
      존재하지 않음), NTIA 2021 → CISA 2026 SBOM 최소 요소 대체 반영, Windsurf → Devin Desktop
      리브랜딩 완료(2026-06-02, Cascade → Devin Local, `.devin/rules/` 우선),
      Dependency-Track 실행 안내 정정(compose 파일 부재·포트 8081)
- [x] 2단계 표준·버전 갱신 `7351fd0` — G4.5 정정(18974는 취약점 0을 요구하지 않음),
      ISO 판 표기 통일, CycloneDX 1.7, EU CRA 2단계 시점, Thaler 상고 기각 2026-03,
      checkov-action `@master` → `@v12`, devsecops-setup 프롬프트에 액션 버전 참조표 신설,
      anchore severity-cutoff 기본값 medium 명시, issue-tracker API 키 질문 추가
- [x] 3단계 하네스 메타 문서 `bd036d1` — 삭제된 workshop/ 참조 제거, verify 항목 수 표기 정정,
      harness-guide 트리에 KWG 자산 등재, STATUS·progress 상태 표기 정정,
      일회성 문서 7종을 `.claude/archive/` 로 이동, 완료 계획서에 상태 배너
- [x] 4단계 ko/en 패리티 검사 — `check-i18n-parity.py` 신설 후 verify.sh [13/13] 로 편입.
      영어 드리프트가 가장 자주 재발한 결함인데 ko만 고쳐도 통과하던 구멍을 막음.
      역검증(en 파일 1개 임시 제거 → FAIL, 복원 → PASS) 확인

미확인으로 남긴 것: CISA 2026 최소 요소의 전체 필드 목록(원문 PDF 403), OpenChain Security
Assurance 스펙 버전 번호(1.0/1.1 판별 불가) — 둘 다 확인된 범위로만 서술하고 원문 링크를 달았다.

## 에이전트 거버넌스 핸드오프 반영 (2026-08-04) — 완료

> 근거: research 팀 핸드오프 `reports/agent-layer-governance/trustedoss-handoff.md` 5개 제안.
> 1차 출처 재검증 후 반영(CycloneDX 1.7 스키마 직접 확인, Snyk·Linux Foundation 원문 대조).
> 독립 검토(Fable 5)로 위치·구조 보완 6건을 계획에 반영한 뒤 실행.

- [x] 범위 admonition 신설 — 개발용 에이전트와 제품 내장 에이전트 구분. 본문이 "아래 4절",
      "아래 5절"로 절 번호를 직접 참조하므로 번호 절이 아니라 admonition 으로 배치
- [x] 3절 여섯 번째 통제 "데이터 반출 경로 판정" 추가 + 제목·도입문 출처 귀속 정정
      (여섯 번째의 근거는 Microsoft 권고가 아니라 Snyk 사례 분석)
- [x] 3절 출처별 심사 분기 표(4행) + 호스팅 플랫폼 심사 한 줄(Smithery — 침해 사고가 아니라
      제보로 수정된 취약점임을 명시)
- [x] 4절 agentgateway 행(Linux Foundation, Apache-2.0, 대체재 아닌 별도 통제 범위) +
      단계적 도입(로그 우선, 관측→경고→차단)
- [x] 6절 신설 "MCP 서버를 SBOM 에 등재하기" — CycloneDX services/components 배치와 한계
      (표준 기구 공식 지침 없음 명시). 기존 6·7절은 7·8절로 이동
- [x] docs/05-tools/sbom-generation 상호 링크 tip, STYLEGUIDE 약어표·용어집(ko/en) MCP 등재
- [x] en 쌍 3파일 동기화, verify 12/12 + build ko/en SUCCESS

미채택: 핸드오프 1절의 사건 3건 표 — 사례를 각 통제에 분산 배치하는 편이 페이지 밀도에 맞음.
`agent-governance.md` 128줄 → 198줄.

## 전 영역 완성도 상향 (2026-07-16 계획 수립) — 완료

> 근거: 멀티 에이전트 전수 감사(finder 22유닛 + P0/P1 적대적 검증, 총 160 에이전트).
> 발견 252건(확정 P0 24, 확정 P1 110, 미검증 P1 13, P2 101, 반박 4).
> 결과 정리: `full-audit-findings-2026-07.md` / 실행 계획: `excellence-plan.md`
> 사용자 결정: 전 영역 균형 상향, 대상 4개 영역 전부, 일정 제약 없음, 전수 감사 방식.

- [x] 전수 감사 실행 + 발견 문서화 + 6순위 실행 계획 수립
- [x] 1순위 A1~A6: P0 24건 완료 — A1 `f247fcf`, A2 `15b472d`, A3 `82d2eb8`, A4 `71154d7`,
      A5 `bb82edb`, A6 `807c45c`. 게이트 1(gate-verifier 역순 판정) 전 항목 PASS + verify 12/12.
      게이트 참고 1건: sktelecom.github.io 링크는 실재 공개 가이드 인용이라 예외 판정(보존)
- [x] 6순위 회수 대장 (ko만 고친 P0의 en 대응분) — 6순위 en 패리티 동기화에 흡수되어 완료:
      en checklist-mapping 5230 연도,
      en 01-setup 로그인 안내, en 05-sbom-management 주간 워크플로, en devsecops·ai-coding
      GitLab CI 예시(curl, dind, gitleaks, CKV ID), en 08 method2/method4는 D2 재번역에 포함
- [x] 2순위 B1~B3 완료 — B1 `eceb1e7`(공통 12, 산출물 24, 39%, 담당 5쌍 양방향), B2 `4a365d7`
      (conformance 템플릿 조항 ID 체계 통일, oss-policy §5 선택화, curriculum 3직군, CVD와 검토
      이력 샘플 보강), B3 `f66b0f9`(04 조건부 정합과 3-6 위치, 4.3.1 문구 단일화, 02 라벨과
      frontmatter). 게이트 2 전 항목 PASS + test-coverage 6/6 + verify 12/12.
      en 회수 대장 추가: en checklist-mapping, index, 07의 수치(12/8/11, 39%, 24), en 04-process
      조건부 서술, en 02 대화 라벨, en 05 4.3.1 문구
- [x] 3순위 H1~H3 완료 — `4fc1e47`, `f4c0b10`. verify.sh [2/12] website 스캔과 id 링크 폴백,
      [5/12] Windows 패턴과 5개 확장자, [6/12] 역방향 검사와 범위 확장, onBrokenLinks 'throw',
      validate-output 4파일, check-admonition 훅 소생(stdin JSON + ESM — 기존엔 이중으로 죽어
      있었음), 인라인 훅 2개 stdin 전환, sync-kwg 경로 절대화. 강화 검사 신규 위반 0건.
      게이트 3 전 항목 PASS(임시 위반 파일 역검증 포함) + verify 12/12.
      참고: 빌드 로그의 "not valid JSON" 78건은 변경 전에도 동일한 기존 이슈(조사 보류)
- [x] 4순위 C1~C4 완료 — C1 `8e40c5b`(인용 전환, open 교체, 펜스 복구, 버전 표), C2 `324cc01`
      (경로 기준 문단 9개 agent, Go와 기타 분기), C3 `e34876d`(도구 페이지 정정, output-sample
      원본 수정, 스킬 매핑에 임명장 추가와 admonition 형식, reference 7페이지 재생성),
      C4 `b45ff9e`(CLAUDE.md 빌드 제외, gtag 제거, Showcase 라벨, FinalCTA 과장 완화,
      quick-start 정리). 게이트 4는 1차 미통과(cdxgen 표 행 잔존, `1bee88b` 정정) 후 재판정 통과.
      게이트가 5순위 S2 대상으로 넘긴 잔여 인용 6곳: 05-sbom-gen:145, 07:111, 08 index:24,
      supply-chain:214, 06-training:78, method3-hooks:32
- [x] 5순위 완료 — `f5360d9` (89파일). 병렬 sweep 3개(docs 36건, agents·인프라 28건, website 22건) + STYLEGUIDE §7 상태·심각도 기호 예외 명문화 + Dependency-Track 표기 전면 표준화 +
      reference organization 페이지 §6 재동기화. 웹 sweep이 미참조 포크 잔재 4파일을 삭제
      (참조 0건과 ko·en 빌드 통과를 독립 재확인). 게이트 5 표본 15/15 + 회귀 5종 + 인프라
      스크립트 4종 + verify 12/12 전부 PASS. 정보성 관찰: reference 샘플 미러의 규정 문체는
      산출물 특성으로 보존
- [x] 6순위 완료 — 부분 `b589254`(한도 중단분 안전 커밋) + 완료 `eadd77b`. 10유닛 전부 종료:
      en 신규 2(ai-coding/iso-mapping, reference/glossary), 재번역 6(docker-cicd, tools-setup,
      08 index + method 4종, reference intro), 전 트리 diff 동기화(수치, URL, admonition,
      데모 iframe 절, 번역 json 키, 샘플 7페이지 'X Output' 라벨). 게이트 6 전 항목 PASS
      (파일 패리티 전수 누락 0·고아 0, P1 표본 13건, 잔존 결함 4종 스캔 0건, 수치 표본).
- [x] 마무리 — 콜드스타트 walkthrough(빌드 HTML 기준, 9단계): 차단급 0, 발견 6건(절감률
      35% 잔존 1곳, cd 후 확인 명령의 작업 디렉토리 함정 2곳, en 컴포넌트 한국어 렌더,
      샘플 페이지 인용 형식, pwd 따옴표) 전부 수정 — `e33395a`. en JourneyProgress·Term은
      code.json 키 21개 추가로 해소(빌드 HTML에서 영어 렌더 확인). verify 12/12.

**이니셔티브 결산**: 감사 발견 252건 중 반박 4건 제외 전량 처리(P0 24, P1 확정 110 + 미검증
13 검증 후 처리, P2 101). 게이트 6회 전부 독립 판정 통과(게이트 4는 1차 반려 후 재판정).
커밋 약 30개. 하네스 개선: verify.sh 맹점 4종 보강, 죽어 있던 admonition 훅 소생, 도구
agent 8종 스펙 검증 신설, onBrokenLinks/MarkdownLinks 'throw'.

## TRUSCA 명칭 갱신 + 웨비나 갭 반영 + 로드맵 (2026-07-09 승인) — 완료

> 근거: Black Duck OSSRA 2026 웨비나 질문 90건 분석. 질문 다수가 "상용 SCA 도입 장벽"(예산·인력·폐쇄망·
> 구축 공수)이며, TRUSCA(github.com/trustedoss/trusca, Apache-2.0 self-hosted SCA)가 그 대안.
> 발견: 저장소가 trustedoss-portal → trusca 로 개명됐고(2026-07-08), 구 URL trustedoss-portal 은 404 —
> 사이트 navbar Portal 링크가 현재 깨져 있음(발표 전 필수).

- [x] A1: TRUSCA 명칭·URL 갱신 — `35578f3`. 구 URL 404였던 navbar/footer 링크 복구, en navbar 키,
      sca.mdx tip ko/en. POSITIONING 은 개명 이력 주석으로 구 이름 1건 의도적 보존
- [x] A2: 갭 문서화 — 임시 완화 절(`aef4178`), 반입 게이트 패턴(`c63b556`), 협력사 SBOM 수신 검증(`9b95200`).
      폐쇄망은 A1 의 TRUSCA self-hosted tip 과 sbom-management 로 반영(별도 큰 문서는 KWG 금융권 범위)
- [x] B: 로드맵 제안서 `docs/_plan/trusca-roadmap.md` — `6245d70`. 웨비나 질문 근거 8항목,
      착수 순서 1위는 에이전트 pre-flight 정책 API + MCP 서버(사이트 agent-governance 와 결합)
- [x] 게이트: gate-verifier 판정 A1/A2/B + verify 12/12 전 항목 PASS (README 표본 대조 포함)

## 에이전트·MCP 도구 거버넌스 페이지 (2026-07-09 승인) — 완료

> 근거: The Hacker News 2026-07-07 기고 분석에서 확인한 신규 갭 (에이전트가 호출하는 MCP 도구의
> provenance·프롬프트 인젝션이 빌드 입력이라는 위협 모델 — KWG 미커버, 우리 트랙 고유 확장).
> 설계: website/ai-coding/agent-governance.md, 실전 적용 카테고리 (ai-security-review 다음).
> 도구 큐레이션: 스캔 mcp-scan(대안 Cisco mcp-scanner, Snyk agent-scan) / 중앙 통제 ToolHive
> (대안 agentic-community Gateway) / 클라이언트·산출물은 기존 자산(hooks, CI 게이트) 재결선.

- [x] M1: 사실 검증 — 정정 다수 확보 (mcp-scan 은 Snyk agent-scan 으로 승계, Cisco 는 3엔진 조합,
      ToolHive 는 접근 정책 표현, 5.5% 는 arXiv 2506.13538 의 1,899개 표본, OWASP MCP Top 10 은 Incubator)
- [x] M2: 페이지 작성 + 결선 — `99cfa27`
- [x] M3: en 쌍 + 결선 — `66f4b3c`
- [x] M4: gate-verifier 판정 전 항목 PASS (사실 충실성 7건 표본 대조 포함), 주의 1건(역방향 링크) 반영

미착수 잔여(같은 기사 분석에서): supply-chain.md Shai-Hulud 사례 추가, CI 게이트의 프롬프트 인젝션
최후 방어선 프레임 한 줄 — 사용자 승인 범위는 1번(이 페이지)만.

## 5.4 AI SBOM 실습 챕터 (2026-07-09 승인) — 완료 (실측 포함)

> 설계: followup-plan.md "추가 승인 과제" 절. 메인 BomLens, 대안 OWASP AIBOM Generator(KWG 링크).

- [x] C1: BomLens 모델 스캔 **실측 완료** (사용자 실행 + 홈 경로 재실행) — 산출물 11개 생성,
      bom.json 실측(specVersion 1.7, machine-learning-model, Apache-2.0, modelCard 존재).
      실측 발견 2건 챕터 반영(`3a41cf5`): security 리포트는 생성됨(취약점 0건이 정상),
      Docker Desktop 파일 공유 밖 경로에서는 산출물이 호스트로 복사되지 않음(경고 추가)
- [x] C2: 챕터 + 사이드바 5.4 + 결선 5지점 — `fa1c0fd`
- [x] C3: en 쌍 + 결선 — `9a0b12b`
- [x] C4: gate-verifier 판정 6항목 전부 PASS (명령 충실성은 공식 문서 축자 대조), 관찰 3건 반영 커밋

## 후속 작업 (followup-plan, 2026-07-09) — 완료

> 계획 승인본: docs/\_plan/followup-plan.md. 재개 시 미체크 청크부터.
> DoD = 수정 + en 쌍 + verify 12/12(커밋 게이트), 순위 종료마다 gate-verifier 역순 판정.

- [x] 1순위 S1: 고아 페이지 2건 삭제 — `91063fb`
- [x] 1순위 S2: iso42001.md 전재 축약 — `9f7a038`
- [x] 1순위 S3: devsecops mdx 4종 섹션 순서 — `55cd8c0`
- [x] 1순위 S4: SLA·VEX 정본 참조 — `75bed70`
- [x] 1순위 게이트: 역순 판정 전 항목 PASS (비차단 권고 1건은 K1 커밋에서 처리)
- [x] 2순위 B1~B3: BomLens 소개 — `68870eb`
- [x] 3순위 K1: 취약점 템플릿 상향 + 다운스트림 — `c9f16db`, `0732fd3`
- [x] 3순위 K2: 정책 용어 부록 — `0dde862` (en 정책 샘플 부록 부재는 P2-c 이월)
- [x] 3순위 K3: 조직 챔피언 모델·검증 담당 — `b85b243`
- [x] 2·3순위 게이트: 역순 판정 전 항목 PASS (BomLens 사실 교차 확인 포함)
- [x] 4순위 P2-a: 도구 명령 낡음 일괄 — `ad3b8fc`
- [x] 4순위 P2-b: 구조(사이드바 카테고리, 5.1~5.3, 단계 번호, 샘플 목차) — `7018957` / 문체·S2 — `e617cd2`
- [x] 4순위 P2-c: en 품질(admonition 전환, 정책 샘플 부록 복원 등) — `0202e61`
- [x] 4순위 P2-d: Rules 7곳 단일화 + 적용 확인 절 — `a919e83`, verify.sh 빌드 stderr 기록 — `e617cd2`
- [x] 최종 게이트: 4순위 역순 판정 1차 미통과(gitleaks detect 잔여 1건, `424b533` 수정) 후 **재판정 통과**.
      잔여 참고: reference/samples 의 상태·심각도 기호 S2 19건은 산출물 형식과 짝이라 의도적 보존.

## Summit P1 수정 작업 (2026-07-09) — 완료

> 근거: summit-review-findings.md P1 절. 범위: 동작·정확성 계열 13건 + Node20 액션 일괄.
> 구조 다듬기 4건(고아 페이지, iso42001 축약, mdx 순서, SLA 정본 참조)과 P2, KWG 잔여 4건은 발표 후 후속.

- [x] 청크 1: AI 코딩 도구 지형 5건 — agent 산출물 .cursor/rules 와 .windsurf/rules, CONVENTIONS.md 로 전환,
      Copilot 조직 지침·경로 한정 지침·AGENTS.md 반영, Windsurf 소속 정정(Cognition), AGENTS.md 공통 트랙,
      ISO 42001 조항 A.6/A.7/A.10 정정 — `29813b7`
- [x] 청크 2: EO 14028 재서술(EO 14306, OMB M-26-05, 위험 기반 전환) + CRA 2026-09-11 보고 의무 — `9ffcc57`
- [x] 청크 3: ISO 인용 3곳(3.3.2 사용 사례 처리, 교육 역량 문구, en 4.x 표기) + Artifex 소각하 기각·합의,
      Log4Shell 약 80만 건, XZ 개발·베타 한정 — `7728772`
- [x] 청크 4: reference 프로필 허위 안내 삭제, sbom-101 링크화, 04-process 6번째 프로세스 신설,
      verify 12/12 표기 일괄, README 시간·메뉴·산출물 표 정합(23문서+SBOM), KWG 출처와 CC BY 표기 — `3bf349a`
- [x] 청크 5: Node20 액션 일괄 상향(checkout v7, upload-artifact v7, gitleaks v3, codeql v4 + build-mode,
      scan-action v7 + outputs 경로) — `4703d83`
- [x] 최종 게이트: gate-verifier 역순 판정 **전 청크 PASS** + verify.sh 12/12

## AI SBOM 동기화 + 법적 고려 보강 (2026-07-09) — 완료

> 계획 승인본: `docs/_plan/ai-compliance-sync-plan.md`.

- [x] 청크 A1: sync-kwg-reference.sh 에 ai-sbom_guide 추가 + 19파일 동기화 — `31ffc42`
- [x] 청크 A2: kwg-mapping.yaml guide_mappings 3건 + drift 기준점 — `206d383`.
      게이트가 발견한 결함 2건 후속 수정: 스냅샷이 삭제 상태로 커밋돼 콜드 스타트 감지 불능(`8abd64e`
      복구), drift 스크립트가 매 실행 기준선을 재기록해 drift 은폐와 트리 오염 유발(`6ee0fa5` 읽기 전용화)
- [x] 청크 A3: sbom-101 "AI SBOM" 절 + iso42001 링크, en 쌍 — `3ca635f`
- [x] 청크 B0: 사실 검증 — KWG 원문 대비 정정 4건 확인(정량 귀속 기준 없음, Anthropic 제도명은
      Commercial ToS Section K, Microsoft 필터 조건 2026-04 제외, 표시 의무 주체는 제공 사업자)
- [x] 청크 B1+B2: legal-considerations.md 신설 + 사이드바, intro 표(누락 2행 보완), strategy 링크,
      templates/policy §5 원칙 4~6 추가 — `b46210b`
- [x] 청크 B3: en 쌍 — `8dbda10`
- [x] 최종 게이트: gate-verifier 역순 판정 1차 미통과(A2) 후 수정, **재판정 통과** + verify.sh 12/12

잔여 후속(선택): 상류 finance-oss-guide 와 iso 표준별 가이드 3종의 동기화 여부, AI SBOM 독자
전용 챕터(실습 포함), verify.sh 가 단계별 stderr 를 버려 실패 원인을 남기지 않는 문제 개선.

## Summit P0 수정 작업 (2026-07-09) — 완료

> 재개 방법: 아래 미체크 청크부터. DoD = 해당 수정 + en 쌍 동기화 + verify.sh 12/12,
> 전 청크 완료 후 ko/en 빌드 + gate-verifier 역순 판정. 근거는 summit-review-findings.md P0 절.

- [x] 청크 1 (P0-1): static/tools 6종 모델 ID 교체 (claude-sonnet-5) — `18e986d`
- [x] 청크 2 (P0-2): devsecops/iso-mapping.md 18974 표 재작성 + en 쌍 — `df27f07`
- [x] 청크 3 (P0-3): 동작 불능 안내 9건 교정 + en 쌍 6파일 — `c0f89f2`
- [x] 청크 4 (P0-4): og:image 도메인 교체 — `b1f3192`
- [x] 청크 5 (P0-5): en navbar 키, `__ISO13__` 4건, Hero Translate — `5a6af66`
- [x] 청크 6 (P0-6): KWG 재동기화(`8ba6b83`) + 의미론적 갭 분석 + 즉시 반영 2건 + 스냅샷 reset.
      즉시 반영: (a) kwg-mapping.yaml — 도구 10종과 18974 §4.x.x 매핑 추가,
      드리프트 오탐 2건(정책 템플릿 자체 절 번호, ISO 42001 조항)을 제외 목적으로 등재,
      (b) 통합 매핑 항목 수 표기 정정 25→31, 공통 10→11, 40%→약 35%
      (00-overview index+CLAUDE, intro, 07-conformance index+CLAUDE, en 쌍 3파일).
      표준별 입증자료 25개 표기(samples/conformance, 07 agent)는 상류 공식 집계와 일치해 유지.
- [x] 최종 게이트: gate-verifier 역순 독립 판정 **청크 1~6 전 항목 PASS** + verify.sh 12/12
      (ko/en 빌드는 커밋 게이트가 매 커밋 강제 — 전 커밋 통과). P0 종료.
      다음 작업: 보고서 P1 17건 (사용자 지시 대기), 위 "KWG 갭 분석 — 검토 후 결정" 7건.

### KWG 갭 분석 — 검토 후 결정 항목 (후속, 사용자 방향 필요)

> 갱신(2026-07-09): 아래 1번(동기화 범위 확장)은 사용자 지시로 후속 과제에서 제외.
> 나머지의 실행 계획은 docs/\_plan/followup-plan.md 참조 (BomLens 소개 과제 추가됨).

1. 동기화 범위 확장: 상류 신규 가이드 5종(ai-sbom_guide, finance-oss-guide, iso5230/18974/42001_guide)이
   sync-kwg-reference.sh 범위 밖. 최소 ai-sbom_guide 추가 권고(발표 주제 직결).
2. templates/process/vulnerability-response.md — CVSS v3.1/v4.0 병기, EPSS와 CISA KEV 보조 지표,
   KISA KNVD, VEX 통지 형식 (상류 요구 상향 반영).
3. templates/policy/oss-policy.md — OSPO/OSPM/OSRB 용어 정의 (coverage-matrix 갭 #1과 묶어 처리).
4. 02-organization — §4.1.2.6 검증 담당 역할, 팀별 1인 챔피언, 실명 표기 권고.
5. website/ai-coding — AI 생성 코드 저작권 귀속, 공급자 IP 보증, EU AI Act §50/한국 AI 기본법
   표시 의무 3주제 보강 (현재 미커버, 상류 7-ai-compliance §5 신설 대응).
6. docs/05-tools — 상류 신규 도구 가이드 3종(cdxgen-dt, scanoss, onot) 외부 링크 추가.
7. kwg-mapping.yaml guide_mappings 에 0-openchain, 7-ai-compliance 항목 추가(감시 사각지대 해소).

## Summit 대비 사이트 개선 검토 (2026-07-09) — 보고 완료, 수정 진행 중 (위 작업 로그)

Open Source Summit Korea 발표 대비 전수 검토. 결과: `docs/_plan/summit-review-findings.md`.
방법: 로컬 하네스 점검 + 독립 검토 에이전트 7개(최신성 3, 구조 2, 가치 1, 일관성 1) + gate-verifier 교차 검증.

- **P0 6묶음 (발표 전 필수)**: 브라우저 도구 6종이 은퇴 모델(claude-sonnet-4-20250514, 2026-06-15 retired)
  하드코딩으로 불능 추정 / devsecops iso-mapping 의 18974 매핑 표 스펙 불일치(존재하지 않는 §4.2.3 포함) /
  따라 하면 동작 안 하는 안내 7건(Aider, hooks, Skill 형식, semgrep-action, nuclei-action, secrets-if, cdxgen 이미지) /
  og:image 가 미해석 도메인(trustedoss.dev) / en navbar 한국어 노출 + `__ISO13__` 4건 /
  KWG 동기화 2026-04-15 정지(이후 70커밋, AI SBOM 가이드 등 미반영)
- **P1 17건**: AI 코딩 도구 지형(AGENTS.md 표준화, Cursor 형식, Copilot 조직 지침, Windsurf 소속),
  EO 14028 낡음, Node20 액션 일괄, ISO 인용 오매핑 3건, 법적 사례 서술, 고아 페이지 2건,
  iso42001 KWG 전재 + 출처 미표기, 수치 불일치(verify.sh 11/11 표기 등), CC BY 표기 미완
- **P2 40여 건**: 도구 명령 소소한 낡음, docs/website 구조 다듬기, en 품질, ko-style 잔여(S2 35, S3 78)
- 잘 유지되는 것: 61페이지 중 53페이지 고유 가치 명확, ISO 존재하지 않는 조항 인용 0건, verify.sh 12/12

다음 작업: 보고서 승인 후 "권고 실행 순서"(보고서 말미) 1번부터 — 즉시 항목은 모델 ID 교체,
og:image 도메인, en navbar 키, 18974 매핑 표, `__ISO13__` 4건.

## 콜드스타트 발견 수정 작업 (2026-06-10) — 완료

> **재개 방법**: 아래 미체크 청크부터 진행. DoD = 해당 항목 수정 + en 쌍 동기화 +
> `verify.sh` 12/12 + (glossary/Term 변경 시 `cd website && npm run build`) 통과 후 커밋.
> 발견 상세·근거는 `docs/_plan/cold-start-findings.md` (M1~M4, m1~m9).

### 청크 체크리스트

- [x] **청크 0**: 이 작업 로그 신설 + 커밋
- [x] **청크 1 (M1·M2)**: `.github/workflows/sync-agents.yml`에 samples/, output-sample/
      추가 (on.push.paths + rsync 2줄, 기존 패턴 그대로). `.github/agents-repo/README.md`가
      구조를 나열하면 두 디렉토리 항목 추가
- [x] **청크 2 (M3·M4)**: quick-start.md §2 `:::tip` 직전에 클론 선행 안내+명령 추가 /
      OSV Maven name을 `org.apache.logging.log4j:log4j-core`로 수정
      (tools-setup.md 74·88행, vulnerability/CLAUDE.md 65행, en tools-setup.md 74·88행).
      주의: sbom-generation index·sbom-101의 `log4j-core`는 SBOM name 필드라 수정 금지
- [x] **청크 3 (m1~m9)**: 01-setup 도구 표 Docker "필수"→"챕터 05만 사용(대체 경로 있음)"(m1),
      체크리스트 docker 항목 생략 단서(m2), quick-start Term 풀이 openchain·자체인증(m3,
      필요 시 `website/src/data/glossary.ts` 키 추가), sbom-generation licenses 빈 값
      주의문(m4), vulnerability 예시 "12개"→"4개"(m5), docker-cicd cdxgen 폴백 출력 경로
      output/sbom/ 일치(m6, 수정 후 Docker 실측), 트러블슈팅 파일 공유 행 추가(m7),
      05-tools index grype→OSV·Dependency-Track(m8), agent 완료 확인 `ls output/organization/`
      한 줄(quick-start·01-setup, m9). **전부 en 쌍 동일 수정**
- [x] **청크 4 (최종 게이트)**: gate-verifier 독립 판정 **13/13 PASS** (역순 검사, OSV curl
      실호출 확인, verify.sh 12/12). M4 curl 실측(7건 반환)·m6 cdxgen 실측(output/sbom/ 생성,
      components 2) 완료. cold-start-findings.md에 처리 결과 기록.
      게이트가 발견한 범위 밖 기존 결함: en sbom-101.md `__ISO13__` 플레이스홀더 4건
      (커밋 052d283 유입) — 후속 후보로 등록
- [x] **push 후 검증**: sync 워크플로우(run 27249199927) success → trustedoss-agents 새 클론에
      samples/와 output-sample/ 추적 파일 37개 확인, 샘플 3종 존재, 문서 명령
      `cp output-sample/sbom/fixture-sample.cdx.json output/sbom/` 성공(components 5) — M1·M2 최종 확정

## 콜드스타트 실사용자 검증 (2026-06-10) — 발견 보고 완료, 수정은 후속

사전 지식 차단 에이전트 2개(P1 스타트업/Docker 불가, P2 중견기업/풀코스)가 공개 사이트만
보고 00→07을 따라가며 명령을 실제 실행. 결과: `docs/_plan/cold-start-findings.md`.

- **major 4건**: 공개 클론 저장소(trustedoss-agents)에 samples/ 부재(M1, 빈 SBOM 조용한 실패),
  output-sample/ 부재(M2, Docker-없이 분기 막힘), quick-start 클론 안내 누락(M3),
  OSV Maven 패키지명 형식 오류(M4, 문서 명령이 `{}` 반환)
- minor 9건 (문서 한 줄 수정 수준), 잘 작동한 것 4건, 체인 검증 9/9 PASS
- **다음 작업(후속)**: M1·M2는 trustedoss-agents 동기화 범위 결정 필요. M3·M4는 문서 한 줄 수정.

## 재개 방법

1. `git checkout feat/ia-kwg-revamp`
2. 계획 정독: `docs/_plan/improvement-plan.md` (승인본). 실행 규약은 그 파일 "실행 규약" 절.
3. KWG 커버리지 근거: `.claude/reference/kwg-coverage-matrix.md`
4. 아래 "다음 작업"부터 이어서 진행. 매 task는 완료 정의(DoD) 통과 시에만 완료 처리.

## 작업 브랜치

`feat/ia-kwg-revamp` (main에서 분기, task별 커밋, Co-Authored-By 트레일러 금지)

## 완료 정의(DoD) 요약

task 고유 수용 기준 + `cd website && npm run build`(ko/en) + `verify.sh` 12/12 + (UI면) 헤드리스 캡처 + (KWG면) 커버리지 100%. KO(주 로케일) 빌드는 broken link 0이어야 함.

## 진행 상태

| #   | 작업                                             | 상태 |
| --- | ------------------------------------------------ | ---- |
| 12  | 메뉴 라벨(오픈소스 관리, AI 코딩 거버넌스)       | 완료 |
| 13  | KWG 커버리지 매트릭스                            | 완료 |
| 14  | 정책 템플릿 KWG 정렬(용어 정의·사내 공개·추적성) | 완료 |
| 15  | 온보딩: 5분 빠른 시작 + 내게 맞는 시작 경로      | 완료 |
| 16  | AI 에이전트 허브 페이지                          | 완료 |
| 17  | 05-tools 통합 인덱스 + 세 기둥 cross-link        | 완료 |
| 18  | P1: 단일 출처, 검색, 매핑 정본                   | 완료 |
| 19  | 도구(onot/sbom-tools) + POSITIONING 차별화       | 완료 |

마일스톤: **P0-0(#13, #14), P0(#15, #16, #17), P1(#18), 마무리(#19), P2 완성도(#9·#10·#11) + 브랜드 수렴 전부 완료.**

## P2 완성도 + 브랜드 (브랜치 feat/p2-completeness)

- DevSecOps/AI코딩 사이드바 대칭화(P2 #11, `6c25e52`): 양쪽 4카테고리 정합 + AI코딩 orphan 3페이지 편입.
- 진행 가시화(P2 #10, `003c521`): JourneyProgress(7단계 진행률, localStorage) + Prerequisite(전제조건 배지). MDXComponents 전역 등록.
- 레퍼런스 정합(P2 #9, `0c46ca0`): Best Practice 표 보완, "준비 중" 8곳 실제 링크화, 에이전트 가이드 링크, 용어집 보강.
- 브랜드 토큰(`56cc53a`): 수렴은 이미 코드에 적용돼 있었음(주색 Material/Google 블루 #1a73e8, 폰트 Roboto). POSITIONING §6 기록만 실제와 일치시킴. 색 변경 없음. 포털 측 수렴은 별도 과제.
- 검증: verify.sh 12/12, ko/en 빌드 0 broken.

## 후속(미완) 항목 — 전부 처리 완료

- 프로세스 템플릿 추적성 헤더: **완료**(`4f4cbb4`). templates/process/\* 6개 + output-sample/process 5개 + reference/samples/process에 KWG 6대 프로세스 정렬 헤더 표면화.
- 정책 샘플 §10 drift: **완료**(`4f4cbb4`). reference/samples/policy에 §10(정책 변경 요청·운영) 보강.
- en 패리티: **완료**(`7ed96f7`). 정본 2페이지 EN 번역, 본문 4개 단일출처 동기화, 온보딩 4페이지 번역. en i18n quirk(4건)는 미번역 폴백이 원인이었고 번역 추가로 해소 — 이제 **ko/en 모두 broken link 0**.
- ko-style 잔재: **완료**(`9739f49`). 가운뎃점 나열 S2 7건 정리(checklist-mapping, devsecops/intro, POSITIONING §1~3). 07-conformance §감사이력의 부분충족 표시 기호(다이아몬드 이모지)는 gap-analysis 산출물의 상태 범례(충족/부분충족/미충족)와 일치하는 의미 기호라 보존. S3 화살표 장식 25건은 권고 수준이라 보류.
- `00-overview/index.md` 본문 축약 보류 — 온보딩 진입은 quick-start + 랜딩 CTA + 에이전트 허브로 달성.

## 다음 작업 (계획 전 범위 + 후속 종료)

계획의 P0-0부터 마무리(#19)까지, 그리고 위 후속 4건까지 전부 완료. 잔여 후보(선택): S3 화살표(→) 산문 정리, en 본문의 산발적 미번역 코드주석.

갱신(2026-07-18): 다음 이니셔티브로 사이트 운영 인프라 상향(검색, 웹폰트, 측정, 잔존 이슈)을
착수한다. 계획과 진행 기준: `docs/_plan/site-ops-uplift-plan.md`.

진행(2026-07-18): 검색 전환 완료. DocSearch가 신청 승인 대기 방식이 아니라 셀프서브로 바뀌어
당일 완료했다. Algolia 계정 가입(사용자), 도메인 인증(메타 태그, 커밋 827f58b), 크롤러 생성과
전체 색인(레코드 13,749개, 에러 0), 주 1회(월요일) 크롤링 스케줄, 사이트 연동 배포까지 반영.
실사이트에서 한국어와 영어 검색 동작을 확인했다.

진행(2026-07-18, 이어서): GoatCounter 연동 완료(커밋 78bc5bf). 계정 가입(사용자,
trustedoss.goatcounter.com), 스크립트와 SPA 라우트 집계 클라이언트 모듈 추가, 죽어 있던
DocsRating을 GoatCounter 이벤트로 수리(번역 4키 추가, svg를 button으로 감싸 접근성 확보).
로컬 서빙에서 ko와 en 렌더, 클릭 후 감사 문구, count.js 로드를 확인하고 배포했다.
남은 것: GoatCounter 이메일 인증(사용자), 실집계 대시보드 확인, crawler 설정에 Docusaurus
facet 추가 후 contextualSearch 활성화(선택), Phase 1 웹폰트, Phase 2의 Lighthouse CI와
접근성 감사, Phase 0의 broken anchor 수정.

진행(2026-07-19): 사이트 운영 인프라 상향 계획의 나머지 전 단계 완료.

- Phase 0: en conformance broken anchor 3건 교정, `onBrokenAnchors: 'throw'`로 재발 방지
  (커밋 59c62cb)
- Phase 1: Pretendard Variable 셀프호스트(dynamic subset, 한글 폴백만 교체, Roboto 유지),
  POSITIONING §6에 중립 토큰 근거 기록 (커밋 f68306a)
- Phase 2: Lighthouse CI 워크플로우(대표 6페이지, warn 예산, 커밋 b975123),
  axe-core 접근성 감사에서 발견된 critical과 serious 위반 전량 수정 — 라이트와 다크
  모두 대표 6페이지 위반 0건 (커밋 73d1545), 월 1회 운영 점검 루틴과 접근성 스캔 절차를
  harness-guide §9에 기록
- contextualSearch 완료(2026-07-20): crawler 설정 v7에서 recordExtractor를 재작성해
  cheerio로 Docusaurus 메타 태그(docsearch:language, docsearch:docusaurus_tag 등)의
  content를 직접 읽어 레코드에 병합했다. 셀렉터 문자열 방식은 meta 태그에 텍스트가
  없어 빈 값이 나오므로 동작하지 않는다(URL Tester로 실검증). 재크롤링(14,140 레코드)
  후 실사이트에서 한국어 화면은 한국어 결과만, 영어 화면은 영어 결과만 나오는 것을
  확인했다. 사이트 쪽은 contextualSearch: true(커밋 3a4c1c5).

### 후속에서 완료한 것 (참고)

- #10 프로세스 템플릿 추적성 헤더, #11 정책 샘플 §10, #12 en 패리티(quirk 해소 포함), #13 ko-style 가운뎃점 정리.

### #19에서 완료한 것 (참고)

- 도구 큐레이션: onot(04-process 배포 전 고지문, SPDX 입력 OSS 고지문 생성, github.com/sktelecom/onot), SKT sbom-tools(05-tools/sbom-generation 보완, cdxgen·syft 파이프라인+Trivy, 메인은 syft 유지). FOSSLight/SW360/FOSSology는 기존 KWG tools 링크로 이미 연결됨.
- POSITIONING.md §7 "OpenChain KWG와의 관계(보완 레이어)" 신설 — KWG=무엇을·왜 / TrustedOSS=어떻게·자동으로, 차별점 5축 표.
- 랜딩 WhyKwg 섹션 신설(`website/src/components/Home/WhyKwg`, Showcase와 FinalCTA 사이). 중립 Infima 토큰(POSITIONING §5), en code.json 번역 추가. ko/en 홈에서 렌더 확인.
- 독립 검수(doc-qa): high 0. med 1건(03-policy 샘플 AGPL Strong→Network Copyleft) 즉시 수정.
- 최종: build ko/en SUCCESS, KO 0 broken, verify 12/12.

### #18에서 완료한 것 (참고)

- 단일 출처화: `reference/concepts/license-classification`, `reference/concepts/vulnerability-response` 정본 신설(사이드바 "개념 심화" 등록). 03-policy·04-process·05-tools/vulnerability 본문은 표 제거 후 정본 링크. 00-overview/index 비교표는 핵심 3행으로 축약 + checklist-mapping 정본 링크.
- 검색: `@easyops-cn/docusaurus-search-local` 테마 추가(language ko/en, docs와 devsecops, ai-coding, reference 인스턴스 인덱싱). ko/en search-index 생성과 navbar 검색창 렌더 확인.
- 매핑 정본: devsecops/ai-coding iso-mapping이 이미 checklist-mapping을 정본 참조 중(추가 작업 불필요).
- 정책 부록 A/B + 추적성 헤더를 output-sample/policy, reference/samples/policy에 반영.

## 핵심 결정 (drift 방지용 고정값)

- 미션: AI·도구로 OpenChain 2026(5230·18974) 관리를 쉽고 정확하게 + DevSecOps 자동화 + AI 코딩 거버넌스. 1차 대상=처음 맡은 담당자.
- 포지셔닝: KWG의 실행·자동화 레이어(경쟁 아님). CC BY 4.0 출처 표기, KWG 연계 명시.
- 상단 메뉴: 오픈소스 관리 / DevSecOps / AI 코딩 거버넌스 / 레퍼런스(유지) + 검색.
- 확정 라벨: 내게 맞는 시작 경로, 표준 요구사항 한눈에, (DevSecOps)표준 연계(18974), (AI)실전 적용.
- 디자인: 이미 구현된 Gemini 문서 look&feel 위에서. 신규 페이지/컴포넌트도 동일 시스템.
- 콘텐츠 패턴: 모든 주제 보기(무API키 데모/샘플) → 해보기(에이전트/도구 복붙) → 자동화(CI/Rules).
- 정적 데모 링크는 `pathname:///tools/<file>.html`(verify.sh가 pathname: 스킵하도록 수정됨).
- 정책/프로세스는 KWG 절 구조에 정렬 + 가치 항목은 확장으로 구분.
- 도구: 국제(syft/grype/trivy/cdxgen/OSV/Dependency-Track) + KWG생태계(FOSSLight/SW360/FOSSology) + 국내(onot 고지문, SKT sbom-tools).

## 핵심 발견·결정 로그

- #13: 산출물 세트 전체로는 KWG 거의 전 절 충족. 실제 갭 3개(용어 정의, 사내 공개 조건부, 추적성).
- #14: 정책 소스 템플릿에 부록 A(용어), 부록 B(사내 공개), 추적성 헤더 추가로 갭 해소(소스 기준).
- #15: 정적 데모는 `pathname://` 링크 + verify.sh가 이를 스킵하도록 수정. en i18n quirk 확인(ko 무관).
- #16: AI 에이전트 허브(`docs/00-overview/agents.md`) 신설.
- #17: `docs/05-tools/index.md` 신설(카테고리 link로 연결). 07-conformance에 "자동화로 확장" 분기, devsecops→AI코딩 상호 링크, checklist-mapping 라벨 "표준 요구사항 한눈에".
- #19: 도구 사실 확인(WebSearch/WebFetch) — onot은 github.com/sktelecom/onot(SPDX 입력으로 OSS 고지문 생성, Kakao와 SKT 공동), sbom-tools는 github.com/sktelecom/sbom-tools(내부 cdxgen과 syft 파이프라인에 Trivy, CycloneDX 1.6, 소스/Docker/바이너리/RootFS 분석, Apache-2.0). 계획의 "syft, cdxgen 래핑" 주장 사실 확인됨. FOSSLight, SW360, FOSSology는 이미 KWG tools 링크로 연결돼 추가 불필요. POSITIONING은 가이드 대 포털(SCA 제품) 축이라 KWG 차별화는 별도 §7로 신설. yarn과 corepack, playwright가 없어 락 immutable과 픽셀 캡처는 직접 검증 못 함(빌드 HTML로 UI 확인, yarn.lock은 정상 포맷으로 판단).
- #18: 단일 출처화 핵심 발견 — CVSS 대응 기한표가 04-process(KWG 기준선 Critical 1주)와 05-tools/vulnerability(운영 SLA Critical 24h)에서 값이 **달랐음**. 정본 페이지에서 "기준선 + 조직 SLA 강화안"으로 통합해 불일치 해소. 매핑 정본(#8)은 이미 두 iso-mapping이 checklist-mapping을 정본 참조 중이라 추가 작업 불필요였음. Diátaxis(#6)는 단일 출처용 reference 개념 페이지 신설로 부분 달성(개념=reference, 본문=링크).
