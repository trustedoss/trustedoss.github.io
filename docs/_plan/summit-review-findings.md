# 사이트 개선 검토 보고서 — Open Source Summit Korea 대비 (2026-07-09)

> 목적: Linux Foundation Open Source Summit Korea 발표를 앞두고 사이트 자체의 개선점을 전수 검토.
> 방법: 로컬 하네스 점검 1회 + 독립 검토 에이전트 7개 병렬 실행(도구 명령 최신성, AI 코딩 도구 최신성,
> 표준과 사례 최신성, docs 구조, website 3영역 구조, 페이지 가치와 차별화, 일관성과 노출 품질).
> 모든 최신성 주장은 1차 출처(공식 문서, 릴리스 노트) 기준. 수정은 이 보고서 승인 후 별도 진행.

## 요약

| 구분                                     | 건수                             |
| ---------------------------------------- | -------------------------------- |
| P0 — 발표 전 필수 (동작 불능, 신뢰 훼손) | 표제 6묶음 (하위 세부 포함 14건) |
| P1 — major (정확성, 구조, 표기)          | 17건                             |
| P2 — minor (개선 권고)                   | 40여 건                          |

근거 상세와 검토 원본은 `docs/_plan/summit-review-details.md` 참조.

가치 판정 대상 61페이지 중 53페이지가 "고유 가치 명확" — 예외 8페이지(삭제·통합 후보 3 + 축약 후보 5)의
목록은 summit-review-details.md 의 Agent E1 절 참조. 포지셔닝(에이전트 동선, 복붙 자산, 채워진 완성본)이
콘텐츠에 실제 반영돼 있고, KWG 중복은 잘 통제되고 있다. 문제는 (1) 시간 경과로 낡아 동작하지 않게 된
코드·설정 예시, (2) 표준 매핑 오류 1곳, (3) 고아 중복 페이지와 출처 미표기 등 사각지대다.

## P0 — 발표 전 필수

### P0-1. 브라우저 도구 6종이 은퇴한 모델을 호출 — 현재 전부 불능 추정 [최신성]

`claude-sonnet-4-20250514` 는 2026-04-14 deprecated 공지 후 **2026-06-15 은퇴 완료**
(출처: platform.claude.com/docs/en/about-claude/model-deprecations — "Requests to retired models will fail").
즉 아래 6개 도구는 현재 API 호출이 404로 실패한다. 발표에서 데모하면 그대로 깨진다.

| 파일                                         | 라인 |
| -------------------------------------------- | ---- |
| website/static/tools/sbom-analyzer.html      | 483  |
| website/static/tools/sast-analyzer.html      | 351  |
| website/static/tools/iac-fixer.html          | 355  |
| website/static/tools/secret-analyzer.html    | 335  |
| website/static/tools/workflow-generator.html | 508  |
| website/static/tools/rules-generator.html    | 566  |

- 삽입처: devsecops sca.mdx:214 외 mdx 5종이 iframe 으로 노출.
- 권고: 공식 권장 대체 `claude-sonnet-4-6`(또는 `claude-sonnet-5`)으로 교체 후 재빌드.
  재발 방지로 모델 ID를 한 곳에서 관리하는 구조 검토. website/static 은 가드레일 절차 적용 대상.
- 참고: ai-coding/ai-security-review.md:159 의 `claude-opus-4-7` 은 유효(은퇴는 2027-04-16 이전 불가 공지).

### P0-2. devsecops/iso-mapping.md 의 18974 매핑이 스펙과 대거 불일치 [사실 정확성]

devsecops/iso-mapping.md:39-48 표: 4.2.1=컴포넌트 식별, 4.2.2=취약점 확인, 4.2.3=취약점 대응,
4.3.1=컴플라이언스 보증, 4.3.2=자료 보존, 4.4.1=외부 문의.
스펙(.claude/reference/iso-18974.md): §4.2.1=접근성, §4.2.2=효과적 리소스, §4.3.1=SBOM,
§4.3.2=보안 보증, §4.4.1=완전성. **§4.2.3 은 존재하지 않는 조항**.
같은 사이트의 ai-coding/iso-mapping.md:30-32(정확)와도 모순. 표준 정합성이 이 사이트의 핵심
신뢰 자산이므로 발표 전 교정 필수. 권고: checklist-mapping 정본 기준으로 표 재작성.

### P0-3. "따라 하면 동작하지 않는" 코드·설정 안내 7건 [최신성]

| #   | 위치                                                           | 문제                                                                                                                                                                                                          | 근거 출처                                 |
| --- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| a   | docs/08-developer-guide/method3-hooks.md:23                    | hooks 예제가 실재하지 않는 환경변수 CLAUDE_TOOL_RESULT 의존 — 항상 빈 문자열, 경고 미출력. 현행은 stdin JSON. index.md:113-131 의 방법 3 예제는 자리표시자 명령이라 직접 영향은 없으나 수정 시 함께 정합 확인 | code.claude.com/docs/en/hooks.md          |
| b   | docs/08-developer-guide/method2-skill.md:12 (+index.md:187)    | Skill 을 평면 파일 .claude/skills/name.md 로 안내 — 현행은 skills/name/SKILL.md + frontmatter 필수                                                                                                            | code.claude.com/docs/en/skills.md         |
| c   | website/ai-coding/tools/cline-aider.md:12, 74-75, 110-119, 126 | Aider 의 system_prompt 키, --system-prompt 플래그, AGENTS.md 자동 인식 전부 실재하지 않음. 공식은 CONVENTIONS.md + read 설정                                                                                  | aider.chat/docs/usage/conventions.html    |
| d   | website/devsecops/sast.mdx:59 (+pipeline-design.md:75)         | semgrep/semgrep-action@v1 은 2024-04 아카이브 + deprecated 명시. semgrep ci 직접 실행으로 교체(GitLab 예시는 이미 올바름)                                                                                     | github.com/semgrep/semgrep-action         |
| e   | website/devsecops/dast.md:136-141                              | nuclei-action v3 에서 severity, fail-on-severity input 제거 — 현 예시 그대로는 동작 안 함                                                                                                                     | github.com/projectdiscovery/nuclei-action |
| f   | website/ai-coding/ai-security-review.md:54                     | job 수준 if 에 secrets 컨텍스트 사용 — GitHub Actions 에서 유효하지 않음. env 매핑 + step 게이트로 교체                                                                                                       | docs.github.com contexts 문서             |
| g   | agents/05-sbom-guide/CLAUDE.md:65-66                           | cyclonedx/cdxgen Docker Hub 이미지 부재(404 실측). ghcr.io/cyclonedx/cdxgen 으로 교체                                                                                                                         | hub.docker.com API 404                    |

추가 동작 결함: docs/05-tools/vulnerability/tools-setup.md:30 의 `ALPINE_DATABASE_MODE=internal` 은
Dependency-Track 유효 값(server, embedded, external)이 아님. method4-cicd.md:72 는 output-format
table 인데 79행에서 results.sarif 를 업로드하는 자체 모순.

### P0-4. og:image 가 해석 불가 도메인을 가리킴 — SNS 공유 미리보기 깨짐 [외부 노출]

docusaurus.config.ts:341, 346 이 `https://trustedoss.dev/img/logo-share.png` 참조.
trustedoss.dev 는 DNS 미해석(ENOTFOUND 실측). 실제 도메인은 trustedoss.github.io(:28),
이미지 파일은 website/static/img 에 존재. 발표 후 링크 공유가 몰릴 때 미리보기가 깨진다.
수정 난이도 극소(도메인 문자열 2곳).

### P0-5. en 사이트 navbar 에 한국어 메뉴 노출 [영문 품질]

i18n/en/docusaurus-theme-classic/navbar.json 의 키가 "체계구축"(10행), "AI코딩"(18행)으로
현행 라벨 "오픈소스 관리"(docusaurus.config.ts:224), "AI 코딩 거버넌스"(:234)와 어긋나
en 로케일에서 두 메뉴가 한국어로 노출된다. 국제 행사 특성상 발표 전 수정 필수.
권고: write-translations 재실행 후 새 키에 영어 번역, 낡은 키 제거.
같은 계열: en sbom-101 의 `__ISO13__` 플레이스홀더 4건(60, 77, 78, 79행 — PURL 버전 자리 유실),
Hero/index.tsx:13 '벤더중립' Translate 미적용.

### P0-6. KWG 원본 동기화가 2026-04-15에 멈춰 있음 — 이후 70커밋 미반영 [KWG drift]

.claude/reference/kwg/.sync-meta 기준 마지막 동기화 2026-04-15. 원본 content/ko/guide 경로에
이후 70커밋(GitHub API 실측, 최신 2026-07-07). 미반영 주요 콘텐츠:

- AI SBOM 컴플라이언스 가이드 신설(2026-06-12~13, 조항 10개 + 도구 가이드) — 발표 주제와 직결
- 금융권 폐쇄망·망분리 가이드 시리즈(2026-06-09~10, 약 20커밋)
- SCANOSS, onot 도구 가이드, AI 코딩 도구 컴플라이언스, SKT SBOM Scanner(2026-04-20~21)
- ISO 5230 입증자료 개수 24에서 25로 정정, 18974 절 번호 오기 정정(2026-05-12) — 우리 문서 대조 필요

kwg-coverage-matrix.md 는 4월 동기화본 기준이라 신규 가이드 미반영. 부수 발견: check-kwg-drift.py 는
로컬 파일 vs 스냅샷만 비교해 상류 갱신을 감지하지 못함(도구 한계).
권고: sync-kwg-reference.sh 실행 후 /kwg-check full 로 갭 분석, 커버리지 매트릭스 갱신.

## P1 — major

### 최신성 (AI 코딩 도구 지형)

1. **Cursor**: agent 산출물이 레거시 .cursorrules 생성(agents/ai-coding-setup/CLAUDE.md:75,
   prompts/generate-rules.md:70-71) — 웹사이트 가이드(tools/cursor.md:18, .cursor/rules/\*.mdc 권장)와
   키트 내부 상충. 출처: cursor.com/docs/context/rules.
2. **GitHub Copilot**: "조직 단위 공통 지침 미지원"(tools/copilot.md:66)은 현행과 반대 —
   조직 Custom instructions 지원됨. path-scoped instructions 와 AGENTS.md 지원도 누락(:18).
   출처: docs.github.com copilot custom-instructions 문서.
3. **Windsurf**: "Codeium 의 도구"(intro.md:34) — 현행은 Cognition 인수 후 Devin Desktop 통합 중.
   .windsurfrules 단일 파일 권장(windsurf.md:18-19)도 레거시(현행은 디렉토리 방식).
   agents/ai-coding-setup 산출물도 동일 갱신 필요.
   출처: techcrunch.com(2025-07-14 Cognition 인수), cognition.com/blog/windsurf, docs.devin.ai.
4. **AGENTS.md 표준화 미반영**: Cursor, Copilot, Windsurf, Cline 모두 AGENTS.md 공식 지원 —
   "도구별 규칙 파일 여러 벌" 대신 AGENTS.md 한 벌 + 도구별 보완이 2026 실무 표준.
   OpenAI Codex, Gemini CLI 등 신흥 도구도 부재(intro.md:27-38, rules-template.mdx:30).
   출처: cursor.com/docs/context/rules, docs.github.com copilot repository-instructions,
   docs.cline.bot/features/cline-rules, docs.devin.ai/desktop/cascade/memories.
5. **ISO 42001 조항 오류**: iso42001.md:116-118 의 §8.5, §8.6, §8.8 은 존재하지 않는 조항
   (8절은 8.1~8.4). 해당 주제는 부속서 A(A.6, A.7, A.10). GPT-J 라이선스도 MIT 가 아닌 Apache-2.0(:61).

### 최신성 (규제·사례)

6. **EO 14028 서술 낡음**: supply-chain.md:117-132 "SBOM 제출 의무화" 현재형 — EO 14306(2025-06)과
   OMB M-26-05(2026-02)로 기관 재량의 위험 기반 접근으로 전환됨. index.md:16 도 동일.
   EU CRA 보고 의무의 2026-09-11 선행 적용(supply-chain.md:146 미언급)도 발표 청중에게 임박 일정.

### 최신성 (CI/CD 액션 버전)

7. **Node20 지원 종료 대비**: 2026-09-16 GitHub 러너에서 Node20 제거 예정 —
   actions/checkout@v4(약 20곳, 대표: method4-cicd.md:34, 64, docker-cicd.md:71),
   actions/upload-artifact@v4(약 10곳, 대표: docker-cicd.md:80, method4-cicd.md:76),
   gitleaks-action@v2(secret-detection.mdx:61, pipeline-design.md:65)는 이후 실패 예정.
   codeql-action@v3 도 2026-12 deprecated 예정(sast.mdx:128, 135, 138, iac-security.mdx:81).
   anchore/scan-action@v3 은 4개 메이저 뒤짐(현행 v7, 결과 파일 참조 방식 변경됨).
   위치 전체 집계는 summit-review-details.md 의 Agent A 절(A1, A6, A7).
   출처: github.blog changelog 2025-09-19 (Node20 deprecation).

### 사실 정확성

8. **ISO 5230 인용 오매핑**: docs/04-process/index.md:276 이 §3.3.2 행에 §3.4.1 주제(컴플라이언스
   산출물)를 기재 — 원문 §3.3.2 는 라이선스 사용 사례 처리. 정본 checklist-mapping 은 올바름(내부 불일치).
   표본 22건 대조 결과 이 외 §3.3.2 주제 드리프트 1건(sbom-generation/index.md:232),
   교육 조항 문구 혼입 1건(06-training/index.md:30, 35). 존재하지 않는 조항 번호 인용은 0건.
9. **법적 사례 서술 부정확**: Artifex vs Hancom "1심에서 판결"(03-policy/index.md:34) — 실제는
   소각하 신청 기각(중간 결정) 후 합의 종결, 본안 판결 없음. XZ Utils "주요 배포판에 포함"
   (supply-chain.md:104)은 개발·베타 버전 한정이 정확. Log4Shell "72시간 내 수백만 건"(:87)은
   약 80만 건이 1차 출처 수치.

### 구조 (고아·중복·전재)

10. **고아 중복 페이지 2건**: docs/intro.md(사이드바 미등재, 인바운드 0건, 00-overview/index.md 와
    4개 구간 동일)와 docs/01-setup/method1-claude-md.md(08 쪽과 diff 2줄, 인바운드 0건).
    권고: 삭제(intro 의 소요 시간 비교만 start-path.md 흡수).
11. **iso42001.md 는 KWG 7-ai-compliance 사실상 전재 + 출처 미표기**: 표 5종과 다이어그램이
    KWG 원본과 동일 대응 확인. CC BY 4.0 표기 없음 — POSITIONING §7 "필수" 위반.
    권고: 요약 + 링크로 축약하거나, 존치 시 출처 표기 + /kwg-check 관리 대상 포함.

### 구조 (배치·정본 참조)

12. **devsecops mdx 4종 섹션 순서 역전**: 셀프 스터디 tip 이 "위 분석기"라 쓰는데 분석기가 아래에
    배치(sast.mdx:178 vs 199 등 4곳). 계획 기준(설정, 체험, ISO 연계 순)과도 어긋남.
13. **SLA·VEX 정본 미참조**: devsecops·ai-coding 전체에서 /reference/ 링크 0건(grep 실측).
    sca.mdx:114-123 의 SLA(Critical 24시간)와 정본(KWG 기준선 1주)이 관계 설명 없이 병존.
14. **reference/intro.md:15 허위 안내**: "규모별 3가지 프로필 제공" — 샘플 7종 어디에도 없음(전부 단일 가상 회사).
15. **docs 배경 챕터 결함**: sbom-101.md:191-194 이동 안내가 실행 불가 bash 블록(cd docs/...) —
    docs/CLAUDE.md 규칙 위반. 04-process 는 배경에서 5개 프로세스만 설명하는데 완료 기준은
    외부 문의 대응 포함 7개 산출물 요구(58행 vs 255-265행) — KWG 6대 프로세스 기준 누락.

### 일관성·표기

16. **수치 불일치 일괄**: verify.sh 실측 12항목 vs CLAUDE.md:25, 196 "11/11", CONTRIBUTING.md 의
    "11/11" 표기와 [N/11] 헤더 한국어 6곳 + 영문 6곳, progress.md:123. 셀프스터디 소요시간 README 표 vs front matter 5챕터 불일치
    (합계 9.5시간 vs 11.5~13.5시간 — "풀 코스 8~12시간" 상한 초과 가능). 산출물 개수 3곳 상이(23/18/19).
17. **CC BY 4.0 / KWG 링크 정책 미완**: 매핑 정본 checklist-mapping 에 KWG 링크 0건(정책 항목 2 위반),
    KWG 차용 챕터 3곳(02, 03, 04)에 CC BY 고지 부재, reference/samples 는 7종 중 2종만 표기.

## P2 — minor (주제별)

### 도구 명령 소소한 낡음 (전체 목록: summit-review-details.md 의 Agent A 절)

- gitleaks detect 는 deprecated(gitleaks git / dir 권장), 이미지도 ghcr.io 권장.
- trivy-action@master 는 고정 태그 권장 — 특히 2026-03 Trivy 공급망 침해 사고(악성 v0.69.4~6, 복구 완료)
  이력을 고려하면 버전·다이제스트 고정 각주가 정합적. .trivyignore.yaml 은 자동 로드 안 됨.
- ZAP 액션 2종 버전 뒤짐, tfsec 는 Trivy 로 유지보수 이관(단서 필요), Semgrep OSS 는 "Community
  Edition" 개칭 + 룰 라이선스 분리, GHAS 는 2025-04 두 제품으로 분리, syft 예시 버전 v0.86.0 구식,
  docker-compose version 키 obsolete, syft/grype 설치 스크립트는 get.anchore.io 가 1차 권장.
- 공급망 사례에 2025 npm 자기 복제 웜(Shai-Hulud, CISA 경보) 추가 가치 — 기존 3종이 못 다루는
  계정 탈취 유형.

### docs 구조 다듬기 (상세: summit-review-details.md 의 Agent D1 절)

- 사이드바: overview/index 에 sidebar_label 부여("개요"), 챕터 1~7을 "단계별 체계 구축" 카테고리로
  묶기, 05-tools 부속 페이지 종속 표현.
- 페이지: supply-chain H2 다음 H4 건너뜀 6곳, 02-organization 질문 번호 자기모순(5/5 뒤 6/6),
  06-training admonition 닫힘 오류(174행)와 산출물 3중 서술, 07-conformance 역순 구조,
  08 developer-guide "준비 중" 막다른 §5, 01-setup §8 재요약 중복.
- 3계층 패턴: 보기(See) 데모 링크가 quick-start 와 05-tools/index 2곳뿐 — 계획상 4곳 미구현.
  자동화 다리: 03-policy 와 04-process 에서 ai-coding/devsecops 링크 0건.
- 문체: 존댓말/반말 혼용이 index, 05-tools 3종, 07 등에 산재. ko-style 잔여 위반(사이트 노출분)
  S2 35건 + S3 78건 — 영역별 집계와 재현 방법은 summit-review-details.md 의 Phase 1 절.

### website 구조 다듬기 (상세: summit-review-details.md 의 Agent D2 절)

- navbar 순서 vs 권장 학습 순서 불일치, "AI 코딩 거버넌스" 3중 표기, cicd-quick 라벨 불일치,
  단일 항목 카테고리 2건, 게이트 도입 순서 3원 불일치, 단계 번호 잔재 4건("4단계 전략" 등).
- Rules 템플릿 전문이 사이트에 7회 중복(정본 1 + 도구 페이지 5 + cline-aider 2회) — 정책 개정 시
  7곳 동시 수정 위험. 발췌 + 정본 링크(또는 MDX partial)로 단일화.
- ai-coding 도구 페이지 5종에 "적용 확인, 데모, ISO 연계" 절 부재. rules-template 생성기가
  개요보다 앞 + 키 없는 미리보기 부재. container-security, dast, pipeline-design 은 체험 요소 전무.
- ai-coding/intro 표에 2페이지 누락, 샘플 7종 도입부 패턴 불일치, 초장문 샘플 상단 탐색 부재,
  best-practice-repo http 링크, glossary 말미 내부 규칙 노출.

### 영문·표기 다듬기

- en intro.md 재번역(제목 어순, "New contacts" 오역, 한국어 잔존), 볼드 공백 아티팩트 7건+,
  en 02-organization title 소문자.
- "OpenChain 2026" 은 공식 용어 아님(quick-start.md:15 + en) — "OpenChain(ISO/IEC 5230, 18974)"
  또는 "KWG 2026 가이드"로 풀어 쓰기.
- 용어 편차 1건: templates/policy/license-allowlist.md:1 "라이선스 허용 목록"(정본 표기는
  "허용 라이선스 목록" 27건).
- README: 메뉴명이 현행 navbar 와 불일치, 08-developer-guide 챕터 누락.

## 확인 결과 문제 없는 항목 (재검토 불필요)

- ISO/IEC 5230:2020, 18974:2023 이 현행 최신판. Spec 3.0 은 초안만 존재. conformance 절차 변경 없음.
- Anthropic API 엔드포인트와 헤더(v1/messages, anthropic-version 2023-06-01, 브라우저 직접 접근 헤더) 유효.
- syft, grype, trivy, OSV API, Dependency-Track 배포 방식, Checkov, semgrep ci 명령 — 문서 명령 유효.
- SolarWinds 18,000 조직, CRA 벌금 규정, 오픈소스 구성비 수치 — 1차 출처와 부합.
- 랜딩 첫인상(5초 내 사이트 성격 전달), README 에이전트 목록(16개 일치), "자체 인증" 용어 통일,
  존재하지 않는 ISO 조항 인용 0건, en 코드펜스 무결, sitemap 라이브 확인.
- verify.sh 12/12 PASS(2026-07-09 실측).

## 권고 실행 순서

1. **즉시(발표 전, 소규모)**: P0-1 모델 ID 교체, P0-4 og:image 도메인, P0-5 en navbar 키,
   P0-2 18974 매핑 표 재작성, en `__ISO13__` 4건.
2. **발표 전(반나절)**: P0-3 동작 불능 안내 7건 교정, P1-16 수치 불일치 일괄(verify.sh 표기 포함).
3. **발표 전후(하루)**: P0-6 KWG 재동기화 + 갭 분석(AI SBOM 신규 가이드 대응 방향 결정),
   P1 AI 코딩 도구 지형 갱신(1~5), P1 규제 서술(6), 고아 페이지 정리(10), 출처 표기(11, 17).
4. **후속**: P1 나머지, P2 주제별 일괄(액션 버전 상향은 한 브랜치로, Rules 템플릿 단일화,
   docs/website 구조 다듬기, en 품질).

각 수정은 CLAUDE.md 가드레일(최소 변경, verify.sh 12/12, website 빌드, 대규모 변경 사전 확인) 적용.
