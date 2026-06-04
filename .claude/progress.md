# 프로젝트 진행 상황

## 로드맵

| Phase | 이름                                                  | 상태              |
| ----- | ----------------------------------------------------- | ----------------- |
| 0     | 플랫폼 기반 구축 (Docusaurus, CI/CD, 기본 구조)       | ✅ 완료           |
| 1     | 핵심 콘텐츠 작성 (docs 챕터 00~07, templates, agents) | ✅ 완료 (2026-03) |
| 2     | Agent 구축 (산출물 자동 생성 파이프라인)              | 🔄 진행중         |
| 3     | 검증 시스템 강화 (verify.sh, CI 통합)                 | ⏳ 대기           |
| 4     | 출시 및 배포 (퍼블리시, OpenChain 등록 안내)          | ⏳ 대기           |

---

## 고도화 이니셔티브 (2026-06~)

POSITIONING.md 정체성에 맞춰 시스템·콘텐츠 고도화. 계획은 승인된 5단계 로드맵 참조.

| Phase | 이름                      | 상태                                     |
| ----- | ------------------------- | ---------------------------------------- |
| 0     | 거버넌스·품질 기반        | ✅ 완료                                  |
| 1     | 메뉴 구조 + 커버리지 재검 | ✅ 완료 (1A 커버리지 + 1B 메뉴)          |
| 2     | 용어집 + 콘텐츠 직접 개선 | ✅ 완료                                  |
| 3     | 실습환경                  | ✅ 완료                                  |
| 4     | 데모환경                  | ✅ 완료 (저위험 콘텐츠 + 컴포넌트 A·B·C) |

> 순서 변경(2026-06-04): IA·커버리지를 먼저 확정해야 콘텐츠·실습·데모 작업 방향이 잡히므로 '메뉴 구조+커버리지 재검'을 Phase 1로 올림.

**Phase 0 완료 내역 (2026-06-04):**

- `CLAUDE.md` 작업 범위 스코프 완화 — 고도화 목적 디자인/구조 변경 허용(4개 가드레일, POSITIONING §5 중립토큰 준수)
- `STYLEGUIDE.md` — 간결성 기준(결론 우선·한 문장 한 개념·200~350줄 밴드·반복 제거) + 쉬운 용어 규칙 + 약어·기술용어 풀이 표(~26개) 추가
- `.claude/skills/create-doc.md` — 쉬운 용어·간결성 필수 규칙 추가
- `.claude/gate.sh` 신설 — quality-gate 커밋 게이트(verify.sh 위임)
- `verify.sh` — STYLEGUIDE.md 로컬경로 오탐 제외(금지 패턴을 문서화하는 파일이므로). 검증 12/12 PASS
- 부트스트랩으로 `doc-qa`·`ko-style-lint`·`quality-gate` 플러그인 enable(다음 세션부터 `/qa` 자동 점검 반영)

**Phase 1 완료 내역 (2026-06-04):**

- 베이스라인 walkthrough(처음 담당자 시점)로 실제 마찰 발굴 → 클론 URL 불일치 10곳 통일(README+9파일)
- **1A 커버리지**: 중복 정리(ISO 매핑 정본화·SCA/SBOM/취약점 관계·08↔rules 역할) +
  갭 4개(공급망 위험평가·정책 변경운영 §11·AI코딩 ISO매핑 신규·예외/라이선스 분류학) +
  how 하이브리드 8파일(인라인 레시피 유지 + best-practice-repo 참조 프레이밍)
- **1B 메뉴(실속 보수안)**: navbar·footer Portal 출구 / 체계구축 사이드바 단계번호+시간 /
  DevSecOps·AI코딩 intro '선택·개발팀용' 배너 / Hero 처음 담당자 환영 신호
- 청크 단위(c1~c5b, 1B-a~d)로 각각 verify 12/12 통과 후 개별 커밋(품질 저하 방지)

**Phase 2 완료 내역 (2026-06-04):**

- Top-5 중 verbose 깊은 챕터 3개를 STYLEGUIDE 간결 기준으로 재작성
  - 04-process(386 → 342줄): 단계 번호 중복(6단계 2개) 수정, 결과물 표 3중 중복 제거, 질문 수 "4개 → 7개" 오기 수정, CVD 표기 통일, frontmatter 18974 4.3.2 제거(정본 정합)
  - 03-policy(364 → 337줄): 중복 Step 제거, 예상 결과 admonition 제거(완료 체크리스트와 중복), Step6 "5번 섹션" 오기 수정, footer 18974 4.1.4 누락 보정
  - 05-sbom-generation(287줄): Docker-없이 tip 단계 안내 오류(단계 5 → 단계 7) 수정, PURL 풀이 추가
- 공통: 반말 평서형 종결을 존댓말로 통일, 전문용어 첫 등장 풀이(Copyleft, CVD, PURL), 이모지 불릿을 :::note admonition으로 교체, 산문 화살표 제거
- ISO 번호 오표기(06 버그 유형) docs 전체 직접 스캔 → 잔존 없음(verify 검증6 PASS)
- 관찰: 08-developer-guide는 125줄로 길이 밴드 하한(200) 미달이나, verbose 간결화 스코프 밖이라 최소 변경 원칙상 보류
- 청크 단위로 각각 verify 12/12 통과 후 개별 커밋

**Phase 3 완료 내역 (2026-06-04):**

- samples 메타: 3개 README 상단에 학습 메타 표(목표, 예상 시간, 난이도, 선행 조건, 관련 챕터) 추가 + samples/README.md 인덱스 신설(비교 표, 공통 선행 조건, 사용 방법)
- 상태감지 정합 버그 수정: 루트 CLAUDE.md 독자 상태감지 테이블이 05-analyst→vulnerability→management 순서로 어긋나 있던 것을 정본(analyst→management→vulnerability→training)으로 정렬. 근거는 05-vulnerability-analyst 전제조건(sbom-management-plan.md)과 validate-chain.py
- agent 온보딩 메타: 9개 agent CLAUDE.md에 "예상 소요" 한 줄 추가(질문 수 + 검토 시간). 전제조건·다음명령은 기존 보유
- Docker 미설치 경로: docs/01-setup에 안내 추가(Docker는 05에서만 사용, 미설치 시 샘플 SBOM 경로). 05-sbom-guide·05-sbom-generation의 Docker-없이 경로는 기존 보유
- 온보딩 동선: docs/intro·README에 정직한 2경로(체계구축 agents vs 개발팀 도구 웹) + 빠른시작(1~2h)/풀코스(8~12h) 구분 추가. 무API키 웹 체험은 미구축이므로 약속하지 않고 Phase 4로 연기
- 04-process Q5·Q6 입력형식은 agent와 docs 모두 예/아니오로 이미 정합(수정 불필요 확인)
- 청크 7개로 분할(≤4파일/청크), 각각 verify 12/12 통과 후 커밋

**Phase 4 진행 내역 (2026-06-04) — 저위험 콘텐츠 완료:**

- 6개 브라우저 도구(rules-template, cicd-quick, sca, sast, secret-detection, iac-security) iframe 직전에 "Anthropic API 키 필요" :::info callout 추가. 6개 모두 키 필수(html 차단 확인), 브라우저에서 api.anthropic.com 직접 호출, 키는 trustedoss 서버 비경유, 키 발급 링크 포함
- rules-template "다음 단계" nav 보강(전략, CI/CD, Best Practice 저장소) — 도구 페이지 동선 표준화
- sca에 why→how 전환점 포털 cross-link 추가(일회성 분석기 → 상시 self-hosted SCA = TrustedOSS Portal). navbar·footer Portal은 Phase 1 완료
- 각 청크 build + verify 12/12 통과 후 커밋

**Phase 4 컴포넌트 A·C (2026-06-04, 설계 승인 후 구현):**

- 사전 조사: 포털 사이트는 살아있으나 호스팅된 공개 데모 인스턴스는 없음. live-demo URL(200)은 DEMO_READ_ONLY 모드를 직접 띄우는 법을 설명하는 docs 페이지 → "1클릭 라이브 데모" 약속 불가, 정직하게 포털 + 5분 배포/read-only 가이드로 연결
- 컴포넌트 A(무API키 샘플 체험): website/src/components/SampleDemo TSX 신설. 샘플 SBOM 입력 + canned 분석 결과(라이선스 요약·카피레프트 위험·실제 CVE 2건) 표시. sca.mdx에 임베드(미리보기 → API키 callout → 실제 도구 순). 중립 토큰만 사용. 성공 기준 ③ 충족
- 컴포넌트 C(포털 연결 CTA): sca 포털 tip 확장 — 포털 둘러보기 + read-only 데모 구성 가이드 링크 + 호스팅 데모 없음 명시
- build + verify 12/12 통과 후 청크별 커밋

**Phase 4 컴포넌트 B (2026-06-04) — 완료:**

- 복사는 Docusaurus 기본 제공 → 갭인 다운로드만 보강. MDX 컴포넌트 import는 eslint no-unused-vars 재발 위험이라 React 없이 정적 파일 + 일반 링크 방식 채택
- output-sample/sbom/fixture-sample.cdx.json을 website/static/samples/로 복사, reference/samples/sbom.md에 :::tip + 내려받기 링크 추가. 사용자가 받아 SCA 분석기·로컬 grype에 투입 가능(컴포넌트 A와 연결)
- 학습된 교훈: 이 레포 MDX에 React 컴포넌트 import 시 eslint-plugin-mdx가 본문 JSX 사용을 인식 못해 no-unused-vars 에러 발생. 임베드형 위젯은 static HTML + iframe, 단순 동작은 정적 파일/인라인 링크가 견고

**Phase 4 전체 완료**: 저위험 콘텐츠(API키 callout, nav 표준화, 포털 cross-link)와 컴포넌트 A(무API키 샘플 체험), B(샘플 다운로드), C(포털 연결 CTA)를 모두 반영. 호스팅된 공개 데모 인스턴스가 없다는 사실을 반영해 과장 없이 구성했다.

---

## 현재 단계 — 사용자 테스트 & 버그 리포트 대응

사용자가 가이드를 직접 따라가며 실습 동작을 검증하는 단계.
오류·개선 포인트 발견 시 알려주면 즉시 수정한다.

**수정 시 체크리스트:**

1. 파일 수정 후 `bash .claude/scripts/verify.sh` — 11/11 PASS 확인
2. `git commit`

---

## 완료된 주요 작업 이력 (요약)

- **Phase 0** (지시 A~D): Docusaurus + Yarn 4 플랫폼, CI/CD, self check 스크립트
- **Phase 1** (지시 E~O):
  - docs 챕터 00~07 콘텐츠 완성 (배경지식, 실습 블록, 완료 체크리스트)
  - agents/ 9개 CLAUDE.md 작성
  - templates/ 11개 산출물 템플릿 작성
  - validate-checklist skill (17항목), verify.sh 6항목 체크
  - 입증자료 50개 전체 checklist-mapping.md 매핑
  - 챕터별 :::info 충족되는 표준 요구사항 블록 추가 (03-policy 기준)
  - README.md 저장소 구조 안내 추가
  - docs 챕터 02/03/04/06 셀프스터디 경로에 `:::details` Agent 대화 예시 블록 추가
  - website/reference/samples/ 산출물 Best Practice 5종 생성 (organization, policy, process, training, conformance) — 규모별 3 프로필 (스타트업/중소기업/대기업)
  - website/reference/intro.md 및 sidebarsReference.ts 업데이트
  - docs/intro.md 챕터 05 테이블 3행 → 1행("05 도구") 병합
  - 전체 챕터 "셀프스터디 경로" 섹션 제목 → "셀프 스터디"로 통일 (11개 파일)
  - docs/06-training: `시작` 입력 안내를 bash block 직후로 이동
  - docs/05-tools/vulnerability + agents/05-vulnerability-analyst: 다음 단계 `시작` 안내 추가
  - website/reference/samples/sbom.md, vulnerability.md 신규 생성 (Best Practice, 렌더링 마크다운)
  - sidebarsReference.ts에 sbom, vulnerability 항목 추가
  - 전체 챕터(00~07) 완료 확인 섹션 및 산출물 테이블에 /reference/samples/\* 링크 추가
  - verify.sh: 절대경로 링크(/로 시작) 및 settings.local.json 예외 처리 추가
- **KWG 동등성 갭 해소** (2026-03-29, Phase 0~7):
  - Phase 0: agents/ 실행 순서 수정 (sbom-analyst→sbom-management→vulnerability)
  - Phase 1: templates 신규 4종 (contribution-process, inquiry-response, project-publication-process, appointment-template)
  - Phase 2: templates 기존 6개 수정 (3년 보관 조항, CVD §8, RACI 기여·공개·문의 행, role-definition §6 검토이력)
  - Phase 3: verify.sh 필수파일 5개 추가, validate-checklist.md 18항목화, settings.json hook 확장
  - Phase 4: agents/ 8개 CLAUDE.md 수정 (입력질문 신설·보강, 산출물 목록 확장, 연결고리 수정)
  - Phase 5: docs/ 4개 수정 (02-organization, 03-policy, 04-process, 07-conformance)
  - Phase 6: update-reference-samples.md process.md 매핑 3종 추가, website/reference/samples/process.md 3섹션 추가
  - Phase 7: verify.sh 7/7 PASS, 갭 해소 확인 완료
- **ISO 커버리지 테스트 추가** (2026-03-30):
  - `.claude/scripts/test-coverage.py` 신규 작성 — 4가지 정적 검증 (G-항목 Agent할당, output 파일 할당, mapping↔checklist 일관성, templates 파일 존재)
  - `docs/00-overview/checklist-mapping.md` G2.2·G3L.6 테이블 보완 (inquiry-response.md, contribution-process.md 누락 추가)
  - `verify.sh` 8번 항목 추가 (ISO 커버리지 정합성), 번호 표기 [1/8]~[8/8] 통일
  - 8/8 PASS 확인
- **QA 자동화 하네스 구축** (2026-04-14):
  - `.claude/agents/` 4종 신규: qa-reviewer, doc-fixer, iso-verifier, content-auditor
  - `.claude/skills/qa-loop/skill.md` 신규 — `/qa` 슬래시 커맨드 오케스트레이터
  - `.claude/skills/diff-scope/skill.md` 신규 — git 변경 범위 계산 (토큰 절약)
  - `.claude/scripts/check-admonition.js` 신규 — PostToolUse 즉시 admonition 경고
  - `settings.json` 훅 추가 (check-admonition)
  - `CLAUDE.md` Skills + Agents 트리거 테이블 추가
  - 8/8 PASS 확인
- **KWG 원본 동기화 + 하네스 가이드** (2026-04-14):
  - `.claude/scripts/sync-kwg-reference.sh` 신규 — KWG GitHub에서 md 파일 20개 다운로드
  - `.claude/reference/kwg/` 신규 — opensource_for_enterprise, templates, tools 원본
  - `.claude/harness-guide.md` 신규 — 하네스 전체 사용법·시나리오 가이드
- **KWG 템플릿 정렬** (2026-04-21):
  - 조직: output-sample·templates·agents/02 — `role-definition.md`에 OSRB·OSPO 선택 섹션 추가 (5인 이상 조건부)
  - 정책: CVE KPI Critical 24h→1주·High 1주→4주 (KWG 기준선), 유연성 노트 추가, 프로그램 효과성 측정 서브섹션 추가 — output-sample·templates·agents/03·docs/03 반영
  - 프로세스: `vulnerability-response.md` CVSS 테이블 동기화 (Critical 1주·High 4주), `distribution-checklist.md` 고지문 생성 절차(3-1/3-2) + 배포 후 최종 확인 섹션 추가 — output-sample·templates·agents/04·docs/04 반영
  - website/reference/samples/ 3페이지 재생성 (organization, policy, process)
  - 총 16개 파일 수정, 10/11 PASS (Docusaurus 빌드 FAIL은 기존 이슈)
- **KWG 싱크 드리프트 탐지 시스템 구축** (2026-04-14):
  - `.claude/reference/kwg-mapping.yaml` 신규 — 4개 차원 KWG↔우리파일 매핑 (guide 7개, template 3개, tools 7종, iso_section 12개)
  - `.claude/scripts/check-kwg-drift.py` 신규 — 구조적 변경 감지 + 스냅샷 관리 (4개 차원)
  - `.claude/agents/kwg-drift-checker.md` 신규 — 의미론적 갭 분석 에이전트
  - `.claude/skills/kwg-check/skill.md` 신규 — `/kwg-check` 슬래시 커맨드
  - `sync-kwg-reference.sh` 수정 — sync 완료 후 check-kwg-drift.py 자동 실행
  - `.claude/kwg-human-tasks.md` 신규 — 사람이 해야 할 일 상세 가이드
  - 초기 스냅샷 생성 및 차원 4 미매핑 섹션 보완 완료
  - "싱크 OK" 확인
- **AI 코딩 가이드 개선** (2026-04-25):
  - `website/ai-coding/strategy.md`: 3단계 핵심 수단을 SCA → DevSecOps 6개 영역(시크릿 탐지·SAST·SCA·IaC·컨테이너·AI 리뷰)으로 확대, 4단계에 AI 퍼징 추가
  - `website/ai-coding/cicd-quick.mdx`: SCA 중심 최소 시작점 포지셔닝 명확화, 다음 단계 링크 7개로 확장
  - `website/ai-coding/ai-security-review.md` 신규: AI 활용 의미론적 취약점 탐지 (역할 분담 테이블 + GitHub Actions 예시)
  - `website/ai-coding/best-practice-repo.md` 신규: 1~4단계 구현 참조 저장소 안내
  - `website/ai-coding/intro.md`: 새 페이지 2개 목록 추가, cicd-quick 설명 갱신
  - `website/devsecops/intro.md`: AI 코딩 가이드 진입 경로 개선 (4단계 전략 → Quick CI/CD → DevSecOps)
  - `github.com/trustedoss/ai-coding-best-practice` 신규 저장소 구성:
    - 3단계 전체 (Gitleaks·Semgrep·CodeQL·syft+grype·Checkov·Trivy)
    - 4단계 전체 (Dependabot·Renovate·OWASP ZAP·AI 퍼징)
    - 정책 파일(.gitleaks.toml·.grype.yaml·.semgrep.yml), 샘플 앱(Flask), K8s 매니페스트
  - `.claude/plan-ai-coding-improvement.md` 신규: 세션 연속성 보장용 작업 계획 문서
  - 11/11 PASS 확인
- **AI 코딩 전략 5단계 개편** (2026-04-25):
  - strategy.md: 4단계 → 5단계 (3: CI/CD / 4: AI 방어 레이어 / 5: 모니터링)
  - 4단계 AI 방어: findings-driven AI 리뷰(4a) + AI 퍼징(4b) 독립 단계화
  - ai-security-review.md: 전체 diff 방식 → Semgrep·grype findings 기반으로 전면 재작성
  - best-practice-repo.md·intro.md: 5단계 구조 반영
  - ai-coding-best-practice: ai-review.yml findings-driven으로 재작성 + README 5단계 반영
  - 11/11 PASS 확인
- **Phase 2 — Agent 체인 검증 1차** (2026-04-25):
  - `validate-output.py` sbom 챕터 3개 파일 누락 수정 (license-report.md·copyleft-risk.md·sbom-sharing-template.md)
  - `fixture-sample.cdx.json` 현실화: 2개→5개 컴포넌트, GPL-2.0 Copyleft + CVE 취약점 포함
  - `05-sbom-guide` Docker 없이 진행하는 경우 fallback 추가
  - `05-sbom-analyst`·`05-vulnerability-analyst` 샘플 SBOM 경로 힌트 추가
  - `docs/sbom-generation` Docker 없이 진행 tip 블록 추가
  - 11/11 PASS 확인
- **Phase 2 — Agent 드라이런 인프라 구축 (C안)** (2026-04-25):
  - `dry-run/run-dryrun.sh` 신규: OpenWave 프로필 오케스트레이터 (--chain-only / --agent 지원)
  - `.claude/scripts/validate-chain.py` 신규: agent 체인 전제 조건 연결 검증
  - `tests/fixtures/05-sbom-guide.json` 신규: Docker 없이 샘플 SBOM 케이스 (기존 누락)
  - `tests/fixtures/04-process-designer-openwave.json` 신규: Q5=예·Q6=아니오 분기 (기여만, 공개 없음)
  - `tests/fixtures/05-sbom-management-openwave.json` 신규: Q1=아니오 분기 (SaaS 납품처 없음)
  - `test-agent-e2e.py`: Bash mock에 cp·chmod 지원 추가 (05-sbom-guide E2E 가능)
  - 드라이런 실행: `bash dry-run/run-dryrun.sh --chain-only` (PASS) / 전체 E2E는 ANTHROPIC_API_KEY 필요
  - 11/11 PASS 확인
- **Phase 2 — Agent 지시문 정적 검토 (B안)** (2026-04-25):
  - OpenWave 스타트업 프로필(12명·SaaS·Python/pip·GitHub Actions·2주 배포) 기준 02~07 전체 정적 시뮬레이션
  - 탐지 이슈 6건 수정:
    - 02: Q4 법무 선택지 "활용 예정" 추가
    - 03: Q4(납품 여부) 처리 방식 분기 누락 보완
    - 04: Q2 배포 주기 "격주(2주 1회)" 선택지 추가
    - 05-sbom-management: Q1 "아니오/미정" 시 Q2 건너뛰기 분기 추가
    - 05-vulnerability-analyst: 완료 확인 `ls` 추가 (일관성)
    - 06-training-manager: Q1 직군 예시 추가 (스타트업 모호성 해소)
  - 11/11 PASS 확인
