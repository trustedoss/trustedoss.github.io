# 프로젝트 진행 상황

## 로드맵

| Phase | 이름                                                  | 상태              |
| ----- | ----------------------------------------------------- | ----------------- |
| 0     | 플랫폼 기반 구축 (Docusaurus, CI/CD, 기본 구조)       | ✅ 완료           |
| 1     | 핵심 콘텐츠 작성 (docs 챕터 00~07, templates, agents) | ✅ 완료 (2026-03) |
| 2     | Agent 구축 (산출물 자동 생성 파이프라인)              | ⏳ 대기           |
| 3     | 검증 시스템 강화 (verify.sh, CI 통합)                 | ⏳ 대기           |
| 4     | 출시 및 배포 (퍼블리시, OpenChain 등록 안내)          | ⏳ 대기           |

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
