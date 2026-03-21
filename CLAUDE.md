# trustedoss

소프트웨어 공급망 보안과 오픈소스 관리 체계를
처음부터 완성까지 구축하는 실전 키트.

ISO/IEC 5230 (라이선스 컴플라이언스)과
ISO/IEC 18974 (보안 보증) 자체 인증을 목표로 한다.

## 프로젝트 구조
- docs/: 챕터별 가이드 문서
- agents/: 산출물 자동 생성 agent
- templates/: 문서 템플릿
- samples/: 실습용 샘플 프로젝트
- workshop/: 강의 키트
- output/: 생성된 산출물 (gitignore)
- .claude/skills/: 재사용 skill 정의

## 독자 상태 감지 및 안내
독자가 "어디서 시작해야 해?" 또는
"다음에 뭘 해야 해?" 라고 물으면
output/ 폴더를 스캔하여 현재 상태를 파악하고
아래 로직에 따라 다음 단계를 안내한다.

output/ 비어있음
→ docs/00-overview 와 docs/00b-supply-chain 읽기 권장
→ cd agents/02-organization-designer 후 claude 실행 안내

output/organization/ 있음, output/policy/ 없음
→ cd agents/03-policy-generator 후 claude 실행 안내

output/policy/ 있음, output/process/ 없음
→ cd agents/04-process-designer 후 claude 실행 안내

output/process/ 있음, output/sbom/ 없음
→ cd agents/05-sbom-guide 후 claude 실행 안내

output/sbom/ 있음, output/vulnerability/ 없음
→ cd agents/05-sbom-analyst 실행 후
→ cd agents/05-vulnerability-analyst 실행 안내

output/vulnerability/ 있음, output/training/ 없음
→ cd agents/05-sbom-management 실행 후
→ cd agents/06-training-manager 실행 안내

output/training/ 있음, output/conformance/ 없음
→ cd agents/07-conformance-preparer 후 claude 실행 안내

output/conformance/ 있음
→ 완성 축하 메시지 출력
→ OpenChain 자체 인증 등록 안내:
   https://www.openchainproject.org/conformance

## 두 가지 사용 경로
셀프스터디: docs/ 챕터를 00부터 순서대로 진행
워크숍: workshop/student-handout.md 를 따라 진행

## 전체 챕터 목록
- 00-overview: 두 표준 개요 및 체크리스트 매핑
- 00b-supply-chain: 소프트웨어 공급망 보안 + SBOM 개념
- 01-setup: 환경 준비
- 02-organization: 조직 구성 및 담당자 지정
- 03-policy: 오픈소스 정책 수립
- 04-process: 오픈소스 프로세스 설계
- 05-tools/sbom-generation: SBOM 생성
- 05-tools/sbom-management: SBOM 관리 및 공유
- 05-tools/vulnerability: 취약점 분석 및 대응
- 06-training: 교육 체계 구축
- 07-conformance: 자체 인증 선언

## 전체 Agent 목록
- agents/02-organization-designer: 조직/담당자 산출물 생성
- agents/03-policy-generator: 오픈소스 정책 문서 생성
- agents/04-process-designer: 프로세스 문서 및 흐름도 생성
- agents/05-sbom-guide: SBOM 생성 명령어 및 스크립트
- agents/05-sbom-analyst: SBOM 라이선스 분석 리포트
- agents/05-sbom-management: SBOM 관리 계획 및 공유 템플릿
- agents/05-vulnerability-analyst: 취약점 분석 리포트
- agents/06-training-manager: 교육 커리큘럼 및 이수 추적
- agents/07-conformance-preparer: 갭 분석 및 인증 선언문

## 최종 산출물 목록
output/organization/role-definition.md
output/organization/raci-matrix.md
output/organization/appointment-template.md
output/policy/oss-policy.md
output/policy/license-allowlist.md
output/process/usage-approval.md
output/process/distribution-checklist.md
output/process/vulnerability-response.md
output/process/process-diagram.md
output/sbom/[project].cdx.json
output/sbom/sbom-commands.sh
output/sbom/license-report.md
output/sbom/copyleft-risk.md
output/sbom/sbom-management-plan.md
output/sbom/sbom-sharing-template.md
output/vulnerability/cve-report.md
output/vulnerability/remediation-plan.md
output/training/curriculum.md
output/training/completion-tracker.md
output/training/resources.md
output/conformance/gap-analysis.md
output/conformance/declaration-draft.md
output/conformance/submission-guide.md

## 진행 상황 확인
output/progress.md 파일 참조

## Skills
- .claude/skills/create-doc.md: 문서 작성 표준
- .claude/skills/validate-checklist.md: 체크리스트 검증
- .claude/skills/generate-report.md: 리포트 생성 표준

## 작업 완료 후 필수 규칙

### 자체 검증 실행
파일을 생성하거나 수정한 후
반드시 아래 명령어를 실행하라.

```bash
bash .claude/scripts/verify.sh
```

모든 항목이 PASS 되어야 푸시할 수 있다.
FAIL 항목이 있으면 수정 후 재실행하라.

### 검증 항목
1. Docusaurus 빌드 성공 여부
2. 내부 링크 유효성
3. Front matter YAML 형식
4. 필수 파일 존재 여부
5. 로컬 경로 노출 여부

### 로컬 경로 금지 규칙
코드, 문서, 스크립트 어디에도
로컬 PC의 절대 경로를 포함하지 말 것.

금지 패턴 (아래 형태의 절대 경로 사용 금지):
- 맥/리눅스 홈: `~username/...` 형태의 절대 경로
- 윈도우 홈: `C:\Users\사용자명\...` 형태의 절대 경로

대신 아래를 사용하라:
- 프로젝트 루트 기준 상대 경로: `./docs/...`
- 홈 디렉토리: `~/`
- 예시 경로: `/path/to/trustedoss`

경로가 포함될 수 있는 상황:
- 명령어 예시 작성 시
- 스크립트 작성 시
- 에러 메시지 인용 시
- README 설치 가이드 작성 시

위 상황에서는 반드시 일반화된 경로를 사용하라.

### settings 파일 규칙
- settings.json: 프로젝트 공통 설정만 포함
  로컬 경로 절대 포함 금지
- settings.local.json: 로컬 전용 설정
  .gitignore 처리되어 있으므로 로컬 경로 사용 가능
  GitHub에 절대 커밋하지 말 것

로컬에서만 필요한 설정은 반드시
settings.local.json 에 작성하라.

### 푸시 전 체크리스트
- [ ] `bash .claude/scripts/verify.sh` 실행
- [ ] 모든 항목 PASS 확인
- [ ] 커밋 메시지 작성
- [ ] `git push origin main`

## 막혔을 때
해당 docs/ 챕터 폴더로 이동하면
그 폴더의 CLAUDE.md 가 맥락을 제공한다.
