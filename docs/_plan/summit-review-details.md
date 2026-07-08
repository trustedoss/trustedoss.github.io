# Summit 검토 부속 자료 — 검토 원본 상세 (2026-07-09)

> summit-review-findings.md 의 근거 상세. 로컬 하네스 점검 1건과 독립 검토 에이전트 7개의 결과 원본이다.

---

# Phase 1 — 로컬 하네스 점검 결과 (2026-07-09)

## F1-1 [minor] verify.sh 항목 수 표기 불일치 (차원 6)

- 실측: `bash .claude/scripts/verify.sh` → **12/12 PASS** (12개 항목)
- CLAUDE.md "세션 종료 전 체크리스트": "11/11 모두 PASS 확인" — 낡음
- CLAUDE.md 검증 항목 설명도 9개만 나열 (12개와 불일치 가능)
- STATUS.md 는 12/12 로 정확

## F1-2 [major] KWG 원본 동기화가 2026-04-15에 멈춰 있음 (차원 11)

- `.claude/reference/kwg/.sync-meta`: sync_date 2026-04-15T02:45:35Z
- 원본 저장소 content/ko/guide 경로에 그 이후 **70 커밋** (GitHub API 실측)
- 로컬 drift 스크립트는 "싱크 OK" — 로컬 파일 vs 스냅샷만 비교하므로 상류 갱신을 감지하지 못함 (감지 도구 자체의 한계 finding)
- 이후 추가된 주요 상류 콘텐츠:
  - AI SBOM 컴플라이언스 가이드 신설 (2026-06-12~13, 조항 10개 + 도구 가이드 + cdxgen 실측)
  - 금융권 가이드 신설 (폐쇄망·망분리, 2026-06-09~10, 산출물 4종 포함)
  - SCANOSS·onot 도구 가이드 추가 (2026-04-20~21)
  - AI 코딩 도구 컴플라이언스 + SKT SBOM Scanner 가이드 (2026-04-21)
  - ISO 5230 입증자료 개수 24→25 정정, 18974 절 번호 §3.x→§4.x 오기 정정 (2026-05-12) — 우리 문서도 같은 수치를 쓰는지 대조 필요
  - cdxgen + Dependency-Track 자동화 환경 구성 가이드 (2026-04-19)
- 수정 단계 권고: `sync-kwg-reference.sh` 실행 후 `/kwg-check full` 로 의미론적 갭 분석

## F1-3 [major] 브라우저 도구 6종이 구형 모델 ID 하드코딩 (차원 7)

- `claude-sonnet-4-20250514` 하드코딩:
  - website/static/tools/iac-fixer.html:355
  - website/static/tools/sbom-analyzer.html:483
  - website/static/tools/workflow-generator.html:508
  - website/static/tools/secret-analyzer.html:335
  - website/static/tools/sast-analyzer.html:351
  - website/static/tools/rules-generator.html:566
- website/ai-coding/ai-security-review.md:159 — `claude-opus-4-7` 참조
- 2026-07 현재 최신은 Claude 5 계열 / Opus 4.8 / Haiku 4.5. deprecated 여부는 Phase 2 에이전트가 웹 확인 중. deprecated 확정 시 발표 데모 중 도구가 조용히 깨지는 최악 시나리오

## F1-4 [minor] ko-style 잔여 위반 — 사이트 노출 문서 기준 (차원 1)

- docs(사이트 노출분, \_plan 제외): 48건 (S2 2, S3 46)
- website/ai-coding: 14건 (S2 5, S3 9)
- website/devsecops: 22건 (S2 8, S3 14)
- website/reference: 29건 (S2 20, S3 9) — S2 중 장식 이모지(빨강/주황/노랑 원형 3종, samples/vulnerability.md:29)는
  이전 세션에서 "의미 기호라 보존" 판단했던 것과 구분 필요
- 합계 S2 35, S3 78. 재현: KO_STYLE_ROOT=<영역> 으로 ko-style lint --all 실행
- S3 화살표는 권고 수준이나 발표 전 정리 대상 후보. S2 는 훅 차단 수준이므로 우선 정리 권고

---

# Agent A — 도구 명령 최신성 검증 결과

## major

A1 anchore/scan-action@v3 → 현행 v7 (v7.4.0, 2026-03-20). v6부터 결과 파일이 outputs 참조 방식으로 변경.

- 위치: method4-cicd.md:67 (+ :72 output-format table vs :79 results.sarif 업로드 자체 모순), devsecops sca.mdx:72, pipeline-design.md:88, monitoring.md:159, ai-coding cicd-quick.mdx:69.

A2 semgrep/semgrep-action@v1 — 저장소 아카이브(2024-04) + deprecated 명시.

- 위치: sast.mdx:59, :37(서술), pipeline-design.md:75. GitLab 예시(sast.mdx:150-152)는 이미 semgrep ci 방식 — GH Actions 만 교정.

A3 cyclonedx/cdxgen Docker Hub 이미지 부재 (404 실측) — agents/05-sbom-guide/CLAUDE.md:65-66. 공식은 ghcr.io/cyclonedx/cdxgen (docker-cicd.md:44, sbom-generation/index.md:211 은 이미 올바름).

A4 Dependency-Track ALPINE_DATABASE_MODE=internal 은 유효하지 않은 값 (유효: server, embedded, external) — tools-setup.md:30. 권고: embedded 또는 줄 삭제(기본값).

A5 projectdiscovery/nuclei-action@main — v3 개편으로 severity, fail-on-severity input 제거(flags 로 전달). dast.md:136-141 예시는 현재 그대로 동작 안 함. 버전 고정 + flags 교정.

A6 Node20 구버전 액션 일괄 — 2026-09-16 GitHub 러너 Node20 제거 예정으로 이후 실패 예정.

- actions/checkout@v4 약 20곳(최신 v7.0.0), actions/upload-artifact@v4 약 10곳(최신 v7.0.1), gitleaks/gitleaks-action@v2 (secret-detection.mdx:61, pipeline-design.md:65, 최신 v3.0.0).
- 출처: github.blog changelog 2025-09-19.

A7 github/codeql-action@v3 → v4 (v3 은 2026-12 deprecated 예정) — sast.mdx:128, 135, 138, iac-security.mdx:81. autobuild 서브액션은 init 의 build-mode 로 대체 권장.

## minor

A8 gitleaks detect 는 v8.19.0부터 deprecated (gitleaks git / gitleaks dir 권장) — pipeline-design.md:176, secret-detection.mdx:75-77.
A9 zricethezav/gitleaks 이미지 → 공식 권장 ghcr.io/gitleaks/gitleaks — pipeline-design.md:174, secret-detection.mdx:73.
A10 syft/grype 설치 스크립트 — raw.githubusercontent 유효하나 공식 1차 권장은 get.anchore.io — sca.mdx:96-98, pipeline-design.md:192-194, cicd-quick.mdx:136, ai-security-review.md:71.
A11 .trivyignore.yaml 은 자동 로드 안 됨(--ignorefile 필요, plain text .trivyignore 만 자동) — pipeline-design.md:247.
A12 aquasecurity/trivy-action@master → 고정 태그 권장(최신 v0.36.0) — container-security.md:74, 83, 90, pipeline-design.md:129, monitoring.md:176.
A13 Trivy 공급망 침해 사고(2026-03-19~23, 악성 v0.69.4~6, 복구 완료) — latest 태그 대신 버전·다이제스트 고정 권고 각주 추가 가치 — container-security.md:110, pipeline-design.md:214.
A14 ZAP 액션 뒤처짐 — action-baseline@v0.12.0 → v0.15.0, action-api-scan@v0.7.0 → v0.10.0 — dast.md:64, 72, pipeline-design.md:145.
A15 tfsec 유지보수 종료 수순(Trivy 이관) — iac-security.mdx:29, 108, 128(tfsec-action@v1.0.0, 최신 v1.0.3). trivy config 중심 재서술 검토.
A16 Semgrep OSS → "Community Edition" 개칭(2024-12), 관리 룰셋은 별도 Semgrep Rules License — sast.mdx:26.
A17 GHAS 명칭 분리(2025-04: Code Security + Secret Protection) — sast.mdx:103.
A18 syft 버전 예시 v0.86.0 구식(1.x 시대) — sbom-101.md:65.
A19 docker-compose version:'3' 키 obsolete — tools-setup.md:21.
A20 cdxgen GitHub 조직 이전(cdxgen 독립 조직, 구 URL 리디렉션, 최신 v12) — 이미지 경로는 유효, 링크만 새 URL.

## 최신 상태 확인 항목

syft CLI 문법과 이미지, licenses JSON 경로 / grype 소스 스킴, fail-on, config / anchore/sbom-action@v0(최신 유지) / trivy CLI / OSV API v1 query, querybatch, Maven 표기 / Dependency-Track 배포 방식(v5 GA 됐으나 latest 는 v4 유지) / Checkov 명령과 이미지, skip 주석, checkov-action@master(upstream 관행 일치) / semgrep ci 명령 / CodeQL 12개 언어 서술 / actions/github-script@v9 / gitleaks pre-commit.

---

# Agent B — AI 코딩 도구 최신성 검증 결과 (2026-07 기준)

## Claude Code

F1 [major] hooks 예제가 실재하지 않는 환경변수 CLAUDE_TOOL_RESULT 의존 — method3-hooks.md:23. (정정: index.md:113~131 은 자리표시자 명령이라 직접 영향 없음 — 게이트 재판정 반영.) 현행은 stdin JSON(tool_name, tool_input, tool_response). 예제는 항상 빈 문자열 → 경고 절대 미출력. 출처: code.claude.com/docs/en/hooks.md. 권고: stdin 파싱 예제로 교체 + PreToolUse(exit 2) 결정적 차단 언급.
F2 [major] Skill 형식 구식 — method2-skill.md:12 등이 평면 파일 .claude/skills/oss-policy-check.md 안내. 현행은 .claude/skills/<name>/SKILL.md + YAML frontmatter 필수. 출처: code.claude.com/docs/en/skills.md.
F3 [minor] website/ai-coding/tools/claude-code.md:76 — "Hard Block 불가, CI/CD 병행 필수"만 서술, PreToolUse hook 로컬 차단 가능성 미언급 + 08 챕터 교차 링크 없음.

## Cursor

F4 [major] agent 산출물이 레거시 .cursorrules 생성 — agents/ai-coding-setup/CLAUDE.md:75, prompts/generate-rules.md:70-71. 웹사이트 가이드(tools/cursor.md:18)는 .cursor/rules/\*.mdc 권장 — 키트 내부 상충. best-practice-repo.md:31, strategy.md:15, rules-template.mdx:30 도 .cursorrules 표기. 출처: cursor.com/docs/context/rules.
F5 [minor] Cursor 의 AGENTS.md 지원 미언급 (tools/cursor.md).

## GitHub Copilot

F6 [major] copilot.md:66 "조직 단위 공통 지침 미지원" — 현행과 반대. 조직 Custom instructions 지원(Chat, code review, cloud agent). 출처: docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions.
F7 [major] path-scoped instructions(.github/instructions/\*.instructions.md, applyTo frontmatter)와 AGENTS.md 지원 누락 — copilot.md:18 은 단일 파일만 안내. 출처: docs.github.com .../add-repository-instructions.

## Windsurf

F8 [major] 소속 서술 구식 — intro.md:34 "Codeium의 AI 코딩 에이전트". 현행: 2025-07 Google 인력 영입 후 Cognition 이 인수, docs.windsurf.com → docs.devin.ai 리다이렉트, Devin Desktop 으로 통합 중. 출처: techcrunch.com 2025-07-14, cognition.com/blog/windsurf, docs.devin.ai.
F9 [major] windsurf.md:18-19 — .windsurfrules 단일 파일을 권장으로 안내. 현행은 .devin/rules/ 또는 .windsurf/rules/ 디렉토리(레거시 fallback 이 .windsurfrules), 글로벌은 ~/.codeium/windsurf/memories/global_rules.md(6,000자 제한). AGENTS.md 지원. agents/ai-coding-setup 산출물(CLAUDE.md:78, generate-rules.md:77-79)도 동일 갱신 필요.

## Cline / Aider

F10 [major] Aider 안내가 실재하지 않는 기능 근거 — cline-aider.md:12, 74-75, 110-119, 126 의 system_prompt 키, --system-prompt 플래그, AGENTS.md 자동 인식 모두 없음. 공식 패턴은 CONVENTIONS.md + --read 또는 .aider.conf.yml 의 read:. 현재 안내대로면 정책이 전혀 주입 안 됨. 출처: aider.chat/docs/usage/conventions.html.
F11 [minor] cline-aider.md:22 — .clinerules 단일 파일 "권장" 표기 뒤집힘. 현행 중심은 .clinerules/ 디렉토리 + AGENTS.md 공식 지원. 출처: docs.cline.bot/features/cline-rules.

## CI/CD 워크플로우

F12 [major] ai-security-review.md:54 — job 수준 if 에 secrets 컨텍스트 사용(secrets.ANTHROPIC_API_KEY != '') — jobs.<id>.if 에서 secrets 사용 불가, 워크플로우 그대로는 동작 안 함. best-practice-repo.md:54, 116 의 "등록 시 자동 활성화" 서술이 이 패턴 의존. 출처: docs.github.com/en/actions contexts. 권고: env 매핑 + step 수준 게이트.
F13 [minor] anchore/scan-action@v3 (cicd-quick.mdx:69, method4-cicd.md:67) — 현행 v7 (4개 메이저 뒤짐). method4-cicd.md:72 output-format table vs :79 results.sarif 업로드 모순도 발견.

## ISO/IEC 42001

F14 [major] iso42001.md:116-118 — §8.5, §8.6, §8.8 은 42001 에 존재하지 않는 조항. 8절은 8.1~8.4 뿐. 해당 주제는 부속서 A: A.6(생애주기), A.7(데이터), A.10(제3자). §5.2, §6.1.2, §7.5 매핑은 정확.
F15 [minor] iso42001.md:61-62 — GPT-J 는 MIT 아닌 Apache-2.0(huggingface.co/EleutherAI/gpt-j-6b). 대표 모델이 Llama 3 에 머묾 — Llama 4, Qwen(Apache-2.0), DeepSeek(MIT)가 시의성.

## 모델 ID

F16 [major] 웹 생성기 6종의 claude-sonnet-4-20250514 는 deprecated + 2026-06-15 은퇴 공지 — 검증일(2026-07-09) 기준 이미 경과, 호출 404 가능성 높음 → 생성기 전체 불능 위험. rules-template.mdx, cicd-quick.mdx 가 iframe 임베드. 권고: claude-sonnet-4-6 또는 claude-sonnet-5 로 교체(website/static 은 가드레일 절차).

- ai-security-review.md:159 의 claude-opus-4-7 은 유효(최신은 claude-opus-4-8, 교체 선택).

## 도구 지형

F17 [major] AGENTS.md 표준화 미반영 — Cursor, Copilot, Windsurf(Devin), Cline 모두 공식 지원. "도구별 6벌 복사" 대신 AGENTS.md 한 벌 + 도구별 보완이 2026 실무 표준. OpenAI Codex, Gemini CLI(GEMINI.md), Google Antigravity, AWS Kiro 등 부재. intro.md:27-38, rules-template.mdx:30.
F18 [minor] Dependabot, Renovate 단계 라벨 불일치 — strategy.md:18 은 5단계, best-practice-repo.md:37, 46 트리 주석은 4단계 (81~87행 표에서는 5단계).

## 최신 상태 확인 항목

- cursor.md 핵심 서술(.mdc 권장 + frontmatter + 우선순위), Claude Code 메모리 계층, hooks 설정 골격(형식), copilot-instructions.md 기본 서술, claude-opus-4-7, actions/github-script@v9(실존, 2026-04 v9.0.0), anchore/sbom-action@v0, actions/checkout@v4, syft/grype 설치 URL, 3~5단계 도구 선정(Gitleaks, Semgrep, CodeQL, syft, grype, Trivy, Checkov, Dependabot, Renovate, OWASP ZAP, OSS-Fuzz), ISO 42001 §5.2/§6.1.2/§7.5 매핑, Llama MAU 7억 조건, 프레임워크 라이선스 표, templates §5 AI 생성 코드 정책.

## 확인 불가

- windsurf.md:67 "Cascade 전용, Autocomplete 미적용" 구분.
- copilot.md:66 "코드 완성에도 적용" 주장 (미적용 가능성 높음).
- Aider 유지보수 활성도 둔화 정황.
- trustedoss/ai-coding-best-practice, trustedoss-agents 저장소 실존 여부 (범위 외).
- ISO 42001 개정(Amendment) 상태.

---

# Agent C — 표준·API·사례 최신성 검증 결과

[major] C1 — 브라우저 도구 6종 retired 모델 하드코딩. claude-sonnet-4-20250514 는 2026-04-14 deprecated 공지, 2026-06-15 retired ("Requests to retired models will fail"). 즉 현재 6개 도구 전부 404 로 불능 상태.

- 파일: sbom-analyzer.html:483, sast-analyzer.html:351, iac-fixer.html:355, secret-analyzer.html:335, workflow-generator.html:508, rules-generator.html:566 (website/static/tools/)
- iframe 삽입처: devsecops sca.mdx:214, sast.mdx, iac-security.mdx, secret-detection.mdx, ai-coding rules-template.mdx, cicd-quick.mdx
- 출처: platform.claude.com/docs/en/about-claude/model-deprecations. 공식 권장 대체: claude-sonnet-4-6 (claude-sonnet-5 도 가능).
- 권고: 6개 파일 교체 + 모델 ID 단일 관리 방안 검토.

[major] C2 — EO 14028 서술 낡음. supply-chain.md:117-132 "SBOM 제출 의무화" 현재형 서술 — 실제로는 EO 14306(2025-06)이 SBOM 산출물 요구 조항 삭제, OMB M-26-05(2026-02)가 M-22-18/M-23-16 폐지, 기관별 위험 기반 판단으로 전환. index.md:16 도 동일 서술.

- 출처: whitehouse.gov EO 14306, dwt.com 2026-02 OMB M-26-05 분석.
- 권고: "지시했으나 2025~2026 방침 변경으로 기관 재량 전환, 실질 동인은 EU CRA·조달 계약" 으로 갱신.

[major] C3 — KWG 동기화 2026-04-15 정지 (Phase 1 F1-2 와 동일 + 보강): 원본 최신 커밋 2026-07-07. 금융권 가이드 시리즈(약 20커밋), AI SBOM 컴플라이언스·도구 가이드 신설, 2026-06-02 80파일 문체 정리, 2026-06-29 conformance 페이지 수정. kwg-coverage-matrix.md 는 4월 동기화본 기준 — 신규 가이드 미반영.

[minor] C4 — "OpenChain 2026" 은 공식 용어 아님. quick-start.md:15(+en :14), STATUS.md:120, improvement-plan.md:20, 302. 공식 명명은 버전(2.1, 3.0 초안) 또는 ISO 표기. 출처는 KWG 가이드 제목 "2026 기업 오픈소스 관리 가이드"로 추정 — 스펙 명칭 아님.

- 권고: "OpenChain(ISO/IEC 5230, 18974)" 또는 "KWG 2026 가이드" 로 풀어 쓰기.

[minor] C5 — Artifex vs Hancom "1심에서 판결" 부정확 (03-policy/index.md:34). 실제는 2017-04 소각하 신청 기각(중간 결정) + 2017 말 합의 종결, 본안 판결 없음. 출처: justia, fsf.org.

- 권고: "구속력을 가질 수 있다고 판단(소각하 기각), 이후 합의 종결" 로 수정.

[minor] C6 — XZ Utils 과장 (supply-chain.md:104). "주요 배포판에 취약 버전 포함" — 실제는 개발·베타 버전만(Fedora 40 베타, Debian testing, Tumbleweed), 안정판 무영향, Ubuntu 는 proposed 에서 제거. 수정하면 105행 논리와 더 정합.

[minor] C7 — Log4Shell 수치 과장 (supply-chain.md:87). "72시간 내 수백만 건" — Check Point 기준 72시간 약 80만 건, 수백만은 수 주 누적.

[minor] C8 — 2025 npm 연쇄 공격(Shai-Hulud) 추가 권장. 사례 3종(SolarWinds, Log4Shell, XZ)은 유효하나 계정 탈취·자기 복제 웜 유형 부재. CISA 경보 2025-09-23(180+ 패키지), Shai-Hulud 2.0(2025-11, 796개).

[minor] C9 — EU CRA 보고 의무 2026-09-11 선행 적용 미언급 (supply-chain.md:146 은 "2027년 전면 시행"만). 전면 적용 2027-12-11. 발표 청중에게 임박 일정.

## 문제 없는 항목

- ISO/IEC 5230:2020, 18974:2023 이 최신판. Spec 3.0 은 초안만("ISO/IEC 5230:2024 (proposed)"). 저장소는 연도판 미표기라 낡을 위험 낮음.
- Conformance 절차 변경 없음(3.0 초안에 리뷰 주기 18→12개월 안 존재, 미확정).
- Anthropic API 엔드포인트(v1/messages), anthropic-version 2023-06-01, dangerous-direct-browser-access 헤더 — 유효.
- claude-opus-4-7(ai-security-review.md:159) active, retire 는 2027-04-16 이전 불가 공지.
- SolarWinds 18,000 조직 정확(2차 침투는 약 100 조직 보충 가능). CRA 벌금(1,500만 유로 또는 2.5%) 정확. 오픈소스 구성비(70~90% Census II / 70~80% OSSRA) 출처 차이로 오류 아님 — 출처 병기 권장. OSSRA 2026: 98% 포함, 취약점 107% 급증(발표용 최신 수치로 활용 가능).
- KWG 사이트 활발 갱신 중 — 참조 유효.

## 확인 불가

- ISO 5230:2020 systematic review(2026-03-05 마감) 최종 결과 — iso.org 차단. openchainproject.org/news 분기 확인 권장.

---

# Agent D1 — docs/ 메뉴·페이지 구성 검토 결과 (원문 보존)

검토 기준: website/sidebars.ts, docs/ 26페이지, .claude/skills/create-doc.md, improvement-plan §6 (보기/해보기/자동화 3계층).

전제 정정: "시작하기 7페이지 비대"는 현재 코드에서 이미 해소됨 — sidebars.ts:5-25 에서 시작하기(4페이지)와 배경 지식(3페이지)으로 분리돼 있음.

## 메뉴 구조 finding

- [major] docs/intro.md 가 고아 페이지이며 00-overview/index.md 와 대량 중복.
  sidebars.ts 에 intro 항목 없음, 어디서도 링크 안 됨. docs 루트 slug(/)는 00-overview/index.md:9 가 차지.
  중복 구간: intro.md:16-22 = index.md:24-27, intro.md:30-34 = index.md:31-35, intro.md:45-56 = index.md:39-49, intro.md:81-87 = index.md:144-149.
  권고: intro.md 삭제 후 index.md 로 단일화(또는 redirect).

- [major] docs/01-setup/method1-claude-md.md 가 고아 중복 파일.
  08-developer-guide/method1-claude-md.md 와 diff 2줄. 사이드바 미등재, 링크 0건(유일 참조는 08 쪽 파일). 01-setup 주제와 무관.
  권고: 삭제, 08 쪽만 유지.

- [minor] "시작하기" 카테고리 안 문서 제목이 "시작하기 전에"라 라벨 충돌.
  sidebars.ts:12 overview/index 에 sidebar_label 없음 → H1 "시작하기 전에"(index.md:12) 노출.
  권고: sidebar_label "개요: 두 표준과 전체 여정"(또는 "개요") 부여.

- [minor] 본편 챕터 1~7이 그룹 없이 평면 배치 — 계획의 "단계별 체계 구축" 카테고리 미구현 (sidebars.ts:26-68).
  권고: collapsed:false 카테고리로 묶기.

- [minor] "5. 도구" 카테고리에서 부속 페이지(docker-cicd, tools-setup)의 종속 관계가 라벨로 안 드러남 (sidebars.ts:51-57). 05-tools/index.md:21-23 "세 단계 흐름"과 어긋남.
  권고: 하위 category 화 또는 라벨 접두("5.1", "5.1a").

- [minor] "다음 단계: 자동화로 확장" 독립 페이지 없음 — 07-conformance/index.md:199-204 하위 섹션으로만 존재. 현 배치 자체는 나쁘지 않음.

## 페이지별 finding

### 00-overview

- [major] sbom-101.md:191-194 — 이동 안내가 실행 불가 bash 블록(`cd docs/01-setup`), docs/CLAUDE.md 규칙 위반. 188행 backtick 경로 표기도 링크 규칙 위반.
  권고: markdown 링크로 교체 + 다음 문서 2갈래 안내(checklist-mapping / 01-setup).
- [minor] index.md §1 빠른 시작 하위 섹션(29-35행)이 quick-start.md:39-42, intro.md:30-34 와 3중 중복. 권고: 링크 한 줄로 대체.
- [minor] index.md 존댓말/반말 혼용 (16, 18, 89, 94행).
- [minor] supply-chain.md 헤딩 건너뜀 H2→H4 (56→60행, 113→117행, H4 6개). 권고: H3 승격.
- [minor] checklist-mapping.md 단일 하위 헤딩 (16행 H2 아래 24행 H3 1개뿐). 604줄 분량은 정본 성격상 적정.

### 챕터 01~07

- [minor] 01-setup/index.md §8 셀프스터디가 §2~6 재요약이라 중복, 섹션 10개 과분화, 보기(See) 계층 없음.
- [minor] 02-organization/index.md — "배경 지식" 표준 섹션명 미준수, 산출물 목록 3중 서술(22-24, 188-192, 226~, 258-260행), 질문 번호 자기모순("질문 5/5" 뒤 155행 "질문 6/6", 131행 "6개 질문").
- [good] 03-policy/index.md — 표준 5섹션, 정본 참조, Artifex 사례. 가장 충실.
  - [minor] 자동화 다리 미구현: /ai-coding, /devsecops 링크 0건. 권고: Rules 내보내기 링크 1줄.
- [major] 04-process/index.md — 배경은 "핵심 프로세스 5가지"(58행)만 설명하는데 완료 기준은 inquiry-response.md 포함 7개 산출물 요구(255-265, 291-304행, 질문 184행). KWG 6대 프로세스 기준 누락.
  권고: "3-6. 외부 문의 대응" H4 추가 + "6가지"로 수정.
- [minor] 04-process — 하위 헤딩 번호 3-1~3-5가 §2 소속과 불일치, §3.5 설명 문단 위치 어색(60행), process-diagram 예시가 §4 체크리스트 하위(306행)로 부자연.
- [good] 05-tools/index.md — 41줄로 3계층 정확 구현, 모범 페이지.
- [minor] 05-tools/sbom-generation/index.md — 보기 계층 부재, 다음 단계 2갈래(269-293행)가 확정 순서(생성→관리→취약점)와 어긋남.
- [minor] 05-tools/vulnerability/index.md — 보기 계층 부재, 반말 혼용(14, 31, 122행). 구조 양호.
- [minor] 05-tools/sbom-management/index.md — 반말 혼용(14, 16, 24, 26행). 구조 준수.
- [minor] 06-training/index.md — admonition 닫힘 오류: 158행 :::tip 의 닫는 fence 가 174행 "> :::" 로 blockquote 안. 권고: blockquote 를 평문화, ::: 독립 행.
- [minor] 06-training — 산출물 서술 3중 중복(159-165, 195-201, 205-207행), §3~5가 표준 순서 이탈, §4 무료 리소스는 계획상 reference 이관 대상 + resources.md 산출물과 중복.
- [minor] 07-conformance/index.md — §3 셀프스터디가 §4~7 배경보다 앞서는 역순 구조, 199행 H3 단일, 문체 혼용(16, 18, 188행).

### 08-developer-guide

- [minor] index.md — 셀프스터디 admonition 이 §6 완료 확인 안에 배치(180-182행).
- [minor] index.md §5 "상세 구현 안내"가 "준비 중" 프로젝트만 가리키는 막다른 섹션(166-176행). 권고: 축약 후 §7로 이동.
- [minor] method3-hooks.md(40줄)·method4-cicd.md(94줄) H1 외 헤딩 없음. method4 는 H2 2개 유용.

## 3계층 적용 종합

- 해보기(Try): 전 챕터 일관 구현 — 가장 잘 됨.
- 보기(See): 샘플 링크는 02~07 전 챕터 존재. 인터랙티브 데모 링크는 quick-start·05-tools/index 2곳뿐 — 계획상 sbom-101, 01-setup, sbom-generation, vulnerability 연결 미구현.
- 자동화(Automate): 05-tools·07·08 연결됨. 03-policy(Rules 내보내기), 04-process(승인을 CI 게이트로) 다리 없음.

## 잘 구성된 부분

- 시작하기/배경 지식 분리로 선택 과부하 해소, 배치 순서도 안내 순서와 일치.
- quick-start, start-path, agents 허브는 계획 §6 설계를 충실 구현.
- "충족되는 표준 요구사항" info 블록이 02~07 동일 형식 — ISO 추적 용이.
- 정본 단일화 양호(checklist-mapping, reference/concepts).
- 05-tools 통합 인덱스 + Prerequisite 컴포넌트가 선후 관계 명시.

---

# Agent D2 — website 3개 영역(devsecops, ai-coding, reference) 구성 검토 결과

## navbar / 사이드바

[major] D2-1 devsecops mdx 4종 — 섹션 순서와 내부 참조 역전. sast.mdx:178 셀프 스터디 tip 이 "위 분석기는"이라 쓰지만 분석기 섹션은 199행(아래). sca.mdx:169, secret-detection.mdx:169, iac-security.mdx:184 동일. 계획 기준은 "복붙 설정, 바로 체험, ISO 연계" 순.
권고: 분석기를 설정 직후로 올리고 셀프 스터디를 뒤로. cicd-quick.mdx(196행 생성기, 215행 셀프 스터디)가 올바른 선례.

[minor] D2-2 navbar 순서 vs 권장 학습 순서 불일치 — devsecops/intro.md:23 은 "AI 코딩 전략, Quick CI/CD, DevSecOps 순 권장"인데 navbar 는 DevSecOps 가 앞(docusaurus.config.ts:221-240). 메뉴명 4개 자체는 무난.
[minor] D2-3 "AI 코딩 거버넌스" 3중 표기 — navbar vs intro front matter "AI 코딩 도구 소개" vs h1 "AI 코딩 도구와 오픈소스 컴플라이언스".
[minor] D2-4 cicd-quick 라벨 불일치 — 사이드바 "CI/CD 자동화" vs 링크 호칭 "(30분 완성) Quick CI/CD" (intro.md:36, devsecops/intro.md:22).
[minor] D2-5 단일 항목 카테고리 2건 — "표준 연계"에 iso-mapping 1개 (sidebarsDevSecOps.ts:27-31, sidebarsAiCoding.ts:31-35).
[minor] D2-6 front matter 죽은 메타데이터 — sidebar_position 이 실제 배치와 무관(ai-coding/iso-mapping.md:5 = 12 등), samples/sbom.md 와 vulnerability.md 만 id/title 부재.
[minor] D2-7 게이트 순서 3원 불일치 — 사이드바(SAST, SCA, 시크릿) vs devsecops/strategy.md:53-57(시크릿+SCA 먼저) vs ai-coding/strategy.md:62(시크릿, SAST, SCA).

## 페이지별

[major] D2-8 devsecops/iso-mapping.md:39-48 — 18974 섹션 번호·의미가 스펙과 대거 불일치. 표는 4.2.1=컴포넌트 식별, 4.2.2=취약점 확인, 4.2.3=취약점 대응, 4.3.1=컴플라이언스 보증, 4.3.2=자료 보존, 4.4.1=외부 문의로 기재. 스펙(.claude/reference/iso-18974.md)은 §4.2.1=접근성, §4.2.2=효과적 리소스, §4.3.1=SBOM, §4.3.2=보안 보증, §4.4.1=완전성이고 §4.2.3 은 존재하지 않음. ai-coding/iso-mapping.md:30-32(정확)와도 모순.
권고: checklist-mapping 정본 기준 재작성.

[major] D2-9 SLA·VEX 가 정본과 병존하는데 devsecops·ai-coding 에서 /reference/ 링크 0건 (grep 실측). sca.mdx:114-123 "권장 SLA"(Critical 24h) vs concepts/vulnerability-response.md:18-23 정본(KWG 기준선 Critical 1주). reference/intro.md:30 은 "도구 챕터는 여기 기준" 명시하나 실제 참조 없음.
권고: 조직 강화 SLA 임을 명시 + 정본 링크, VEX 상세는 정본 위임, 용어 첫 등장에 용어집 링크.

[major] D2-10 reference/intro.md:15 — 존재하지 않는 "규모별 3가지 프로필" 안내. 7개 샘플 전체에서 '스타트업', '프로필' 검색 0건. 모든 샘플은 단일 가상 회사(테크유니콘).
권고: 문장 삭제 또는 프로필 제공 후 복원.

[major] D2-11 sast.mdx:143-158 — "### GitLab CI"(semgrep 잡)가 "## CodeQL 설정"(101행) 하위에 잘못 소속.

[minor] D2-12 단계 번호 잔재 — devsecops/intro.md:23 "4단계 전략"(실제 5단계), cicd-quick.mdx:25 "3단계 전략([4단계 전략] 참고)" 문구 엉킴, best-practice-repo.md:37, 46 "4단계" 주석 vs 81-87행 표 5단계, devsecops/strategy.md:89-94 "2단계 — AI 규칙 내재화"가 어느 단계 체계인지 불명.
[minor] D2-13 Rules 템플릿 전문 6개 파일 중복 (E1-F4 와 동일 발견) — MDX partial import 단일화 권고.
[minor] D2-14 ai-coding 도구 페이지 5종 — 계획 공통 구조의 "적용 확인, 데모, ISO 연계" 뒷부분 부재.
[minor] D2-15 rules-template.mdx:10-24 — 생성기(API 키 필요)가 개요(28행)보다 앞. devsecops mdx 4종의 "키 없는 샘플 미리보기" 패턴 부재 (cicd-quick 생성기도 동일).
[minor] D2-16 체험 밀도 편차 — container-security, dast, pipeline-design 에는 셀프 스터디·데모 없음. ISO 연계 절은 게이트 6종 모두 없음.
[minor] D2-17 ai-coding/intro.md:27-38 표에 iso42001, iso-mapping 2페이지 누락 (devsecops/intro 표는 완전).
[minor] D2-18 샘플 7종 도입부 패턴 불일치 — 2가지 패턴 혼재, 에이전트 이름 번호 접두 유무 혼재.
[minor] D2-19 초장문 샘플에 상단 탐색 부재 — samples/process.md 831행 6문서, sbom.md 474행 4문서, 동일 헤딩 반복. 상단 수록 문서 표 권고.
[minor] D2-20 기타 — best-practice-repo.md:14 http:// 링크, glossary.md:73 내부 유지보수 규칙 노출, iso42001.md 단일 하위 h3. 헤딩 계층 건너뜀은 전 페이지 없음.

## 잘 구성된 부분

- 두 intro 의 "선택 단계" note + iso-mapping 2종의 정본 선언(중복 매핑 구조적 차단).
- devsecops 게이트 골격("X란, 도구 비교, GitHub/GitLab 설정, 주의, 다음 단계") 7페이지 일관.
- reference/concepts 2종은 정본 패턴 모범 (문제는 참조하는 쪽의 링크 부재).
- samples/sbom.md 의 키 없는 다운로드 + 분석기 연결 = 보기/해보기 모델 정확 구현.
- 사이드바 대계는 계획 사이트맵과 일치, samples 순서 = docs 2~7 진행 순서, 깊이 균형.
- devsecops/intro 의 "이 메뉴의 구성" 표 + 역할별 시작점 tip 우수 — ai-coding 이 따라갈 기준.

---

# Agent E1 — 페이지 가치·차별화 판정 결과

총 61페이지 중 53페이지 [고유 가치 명확]. docs/ 챕터는 배경 압축 + KWG 링크 위임 패턴이 일관돼 중복 통제 양호. 사각지대 3건(고아 사본 2 + 출처 없는 전재 1).

## Findings

[major] F1 — docs/intro.md: 고아 페이지, 00-overview/index.md 와 대부분 중복.

- intro.md:6 slug 주석 처리, 실제 / 슬러그는 00-overview/index.md:9. sidebars.ts 미등재, 인바운드 링크 0건.
- 중복: intro.md:30-34 = index.md:31-35(빠른 시작), intro.md:45-56 = index.md:39-49(챕터 표), "23개 산출물/40% 절약"(intro.md:20-21 = index.md:26-27), 관련 링크(intro.md:83-86 = index.md:146-149).
- 고유분은 "사용 경로" 표(60-77행)뿐 — start-path.md 와 역할 겹침.
- 권고: 삭제 + 소요 시간 비교만 start-path.md 에 흡수.

[major] F2 — docs/01-setup/method1-claude-md.md: 바이트 단위 중복 사본. diff 는 08쪽 말미 링크 2줄. sidebars 미등재, 인바운드 0건. 권고: 삭제, 정본은 08-developer-guide 쪽.

[major] F3 — website/ai-coding/iso42001.md: KWG 7-ai-compliance(\_index.md) 거의 전재.

- 다이어그램 :21-34 ≒ KWG :24-37, 프레임워크 표 :43-49 = KWG :50-56, 모델 라이선스 표 :58-64 = KWG :76-82, 데이터셋 표 :95-100 = KWG :121-126, AI SBOM YAML :79-85 ⊂ KWG :100-108, 조항 매핑 :111-118 = KWG :141-148.
- 고유 추가분은 :120-123 info 박스 한 단락. 원본 §5는 누락.
- CC BY 4.0 출처 표기 없음 — POSITIONING §7 "필수" 위반. samples/policy.md:33 은 표기 갖춤(대비).
- 권고: (a) 요약 + KWG 링크로 축약, 또는 (b) 존치 시 출처 표기 + /kwg-check 대상 포함. 현 상태(출처 없는 전재)가 최악.

[minor] F4 — website/ai-coding/tools/ 5개 페이지: 공통 Rules 템플릿 전문을 반복 수록(사이트 전체 7회 — rules-template.mdx:43-80 정본 + 도구 페이지 5개 + cline-aider 는 2회 :34-68, :88-121). 각 페이지 고유분은 위치·적용법·주의 25~30줄.

- 권고: 발췌 3~5줄 + 정본 링크로 교체. 허용/금지 목록 변경 시 7곳 동시 수정 드리프트 위험 해소.

[minor] F5 — docs/05-tools/sbom-generation/docker-cicd.md:14-19: 언어별 명령 표 4행이 전부 동일 명령, 아래 :21-34 에 같은 명령 재수록. 권고: "언어 무관 동일" 한 줄 + 코드블록 1개.

[minor] F6 — website/devsecops/iso-mapping.md: "ISO/IEC 18974란"(:19-32)과 "인증 등록 절차"(:80-85)는 docs 트랙 정본의 재서술. 핵심(매핑 표 :35-48, 증적 체크리스트 :52-77)은 고유. 권고: 두 절을 2~3문장 + 링크로 축약.

## 분류 요약

- 대부분 중복(통합·삭제 후보) 3: docs/intro.md, docs/01-setup/method1-claude-md.md, website/ai-coding/iso42001.md
- 부분 중복(축약 후보) 5: website/ai-coding/tools/ 5개 (claude-code, cursor, copilot, windsurf, cline-aider)
- 나머지 53페이지 고유 가치 명확. 특히 reference/samples 7종은 "KWG 빈 템플릿 vs 채워진 완성본" 차별점의 실물 증거.

---

# Agent E2 — 일관성·표기·노출 품질 검토 결과

## 1. 수치·표기 일관성

[major] verify.sh 항목 수 불일치 — 실제 12항목([1/12]~[12/12], verify.sh 12~275행).

- CLAUDE.md:25 "11/11", CLAUDE.md:196 "11/11"
- CONTRIBUTING.md:35 "# 11/11 PASS 확인", :179(영문), 섹션 헤더 [N/11] 한국어 6곳(60, 71, 82, 93, 104, 120행) + 영문판 6곳(204~264행)
- .claude/progress.md:123 "11/11" (현행 규칙 서술부)
- STATUS.md:9 는 12/12 로 정확
  권고: 11/11 및 [N/11] 헤더를 12/12 체계로 일괄 갱신.

[major] 셀프스터디 소요시간 README 표 vs front matter 5곳 불일치:

- 01-setup: README "30분" vs docs/01-setup/index.md:7 "30분~1시간"
- 04-process: README "1시간" vs index.md:7 "1~2시간"
- 05 sbom-generation: README "1시간" vs index.md:7 "1.5시간"
- 06-training: README "30분" vs index.md:7 "1시간"
- 07-conformance: README "30분" vs index.md:7 "2시간"
  front matter 합계 약 11.5~13.5시간 — "풀 코스 8~12시간"(README:63) 상한 초과 가능. docs/05-tools/CLAUDE.md:49 "3~4시간"은 front matter 기준과 일치.
  권고: front matter 를 기준으로 README 표와 합계 재산정.

[minor] 산출물 개수 3곳 상이 (23 / 18 / 19):

- docs/intro.md:20, docs/00-overview/index.md:26 "23개"
- README 최종 산출물 표 18행 (inquiry-response, sbom-sharing-template, contribution-process, completion-tracker, resources, submission-guide 누락)
- validate-output.py:24-57 필수 목록 = md 18 + cdx.json 1 = 19개. output-sample 은 24파일(픽스처 제외 23).
  권고: 정본 개수 확정 후 정렬.

[minor] 용어 편차: "허용 라이선스 목록" 27건 vs templates/policy/license-allowlist.md:1 "라이선스 허용 목록" 1건. 권고: 템플릿 제목 통일.

## 2. ISO 조항 인용 (표본 22건: OK 18, 불일치 4)

[major] docs/04-process/index.md:276 — §3.3.2 행에 §3.4.1 주제(컴플라이언스 산출물)를 오매핑. 원문 §3.3.2 는 "라이선스 사용 사례 처리 절차". 다음 행(277)이 §3.4.1 을 별도로 다뤄 이중 배치. 정본 checklist-mapping.md:253, 267 은 올바름 — 내부 불일치.
[minor] docs/05-tools/sbom-generation/index.md:232 — §3.3.2 를 "라이선스 식별 및 분류"로 서술 (식별은 §3.3.1 활동, §3.3.2 는 처리 절차).
[minor] docs/06-training/index.md:30, 35 — §3.1.2/§4.1.2(역량) 에 정책 전파(§3.1.1.2/§4.1.1.2) 문구 혼입. 같은 파일 183, 190행은 올바름.
존재하지 않는 조항 번호 인용 0건 (5230 인용 256건, 18974 인용 237건 전수).

## 3. CC BY 4.0 / KWG 출처 표기

[major] 표준 매핑 정본(docs/00-overview/checklist-mapping.md)에 KWG 원문 링크 0건, "KWG" 문자열 0건 — 링크 정책 항목 2 미적용 (정책 정의: improvement-plan.md:56-62).
[major] KWG 차용 챕터에 CC BY 4.0 고지 부재 — docs/02-organization/index.md:54, 03-policy/index.md:51, 04-process/index.md:33 은 KWG 링크는 있으나 라이선스 고지 없음 (POSITIONING.md:133 "필수" 규정 위반).
[minor] reference/samples 7개 중 CC BY 문구는 policy.md:33, process.md:12 2개뿐(클릭 가능 URL 아님). 소스 output-sample 단계부터 동일 패턴. 권고: output-sample 에 URL+고지 후 재생성.

## 4. 영문(en) 로케일

[major] sbom-101 **ISO13** 플레이스홀더 4건 확정 — i18n/en/.../00-overview/sbom-101.md 60행(log4j-core), 77행(lodash), 78행(requests), 79행(spring-core) — 전부 PURL 버전 자리. en 전역에서 이 패턴은 4건이 전부.
[major] en navbar 번역 키 스테일 — i18n/en/docusaurus-theme-classic/navbar.json 키가 "체계구축"(10행), "AI코딩"(18행)인데 현행 라벨은 "오픈소스 관리"(docusaurus.config.ts:224), "AI 코딩 거버넌스"(:234) → en 사이트에 한국어 메뉴 노출.
권고: write-translations 재실행 후 새 키 번역, 낡은 키 제거.
[minor] en intro.md 품질 저하 — 9행 제목 어순 붕괴, 18행 "New contacts" 오역, 33행 한국어 잔존, 볼드 공백 아티팩트 7건("**ISO/IEC 5230 **" 류) — 01-setup, 06-training, 05-tools 2종, 07-conformance, 08-developer-guide 에도 산발.
[minor] en 02-organization front matter title 소문자. Hero/index.tsx:13 '벤더중립' Translate 미적용 하드코딩 → en 랜딩에 한국어 노출.

## 5. 외부 노출 품질

[major] og:image 가 해석 불가 도메인 — docusaurus.config.ts:341, 346 이 https://trustedoss.dev/img/logo-share.png 참조. trustedoss.dev 는 DNS 미해석(ENOTFOUND) 실측. 실제 도메인은 trustedoss.github.io(:28), logo-share.png 는 website/static/img 에 존재. SNS 공유 미리보기 깨짐.
[minor] README 메뉴명 불일치 — README:23~28 "체계구축", "AI 코딩" vs navbar "오픈소스 관리", "AI 코딩 거버넌스". navbar 의 Portal(248행)은 README 에 없음.
[minor] README 챕터 목록에 08-developer-guide 누락 (사이트에는 sidebars.ts:73-78 로 노출).

## 문제 없는 항목

- STATUS.md 12/12 정확. "자체 인증" 용어 전 저장소 통일. 정본 매핑·templates 조항 주석 표본 정합.
- KWG 링크 정책 항목 1(챕터 페이지 링크): 02, 03, 04 모두 존재.
- en 코드펜스 정상, code.json 랜딩 번역 양호.
- docusaurus title/tagline/themeConfig.image 존재, sitemap 라이브 확인(약 103 URL).
- README 에이전트 목록(9+7) = agents/ 16개 일치.
- 랜딩 첫인상 5초 통과 (eyebrow → 헤드라인 → 서브타이틀 → 5분 시작 CTA).
