# generate-pipeline 프롬프트

## 목적

사용자 답변과 프로젝트 분석 결과를 바탕으로
DevSecOps CI/CD 파이프라인 파일과 정책 파일을 생성한다.

## 입력 변수

- PROJECT_PATH: 분석할 프로젝트 경로
- PLATFORM: github / gitlab / both
- DOMAINS: 선택된 보안 영역 목록
- VULN_THRESHOLD: critical / high / medium
- IAC_TOOLS: terraform / kubernetes / cloudformation
- SCHEDULE: daily / weekly / none
- DETECTED_LANGS: 감지된 언어 목록 (자동)
- HAS_DOCKERFILE: true / false (자동)
- HAS_IAC: true / false (자동)
- HAS_EXISTING_WORKFLOW: true / false (자동)

## 파이프라인 설계 원칙

1. 병렬 실행: 독립적인 검사는 같은 stage에 배치
2. 단계별 게이트: 시크릿 탐지 → 코드 분석 → 빌드 분석 순서
3. 실패 정책:
   - 시크릿·SAST·SCA·IaC: Hard Fail (PR 차단)
   - DAST: 초기 도입 시 Soft Fail (fail_action: false)
4. 아티팩트 보관: SBOM은 90일, 리포트는 30일

## GitHub Actions 생성 규칙

devsecops-pr.yml:
- on: pull_request (branches: [main, develop])
- jobs 병렬 구성:
  - secret-detection (항상 먼저, needs 없음)
  - sast (needs: secret-detection, SAST 선택 시)
  - sca (needs: secret-detection, SCA 선택 시)
  - iac (needs: secret-detection, IaC 선택 시)
- 각 job: runs-on ubuntu-latest
- checkout: fetch-depth: 0 (시크릿 탐지 전체 히스토리)
- SBOM 아티팩트: retention-days: 90

devsecops-merge.yml (컨테이너·DAST 선택 시):
- on: push (branches: [main])
- jobs 순서:
  - container-security (Trivy, 컨테이너 선택 시)
  - dast (needs: container-security, DAST 선택 시)
- DAST: fail_action: false (초기 Soft Fail)

devsecops-schedule.yml (스케줄 선택 시):
- on: schedule (cron 설정) + workflow_dispatch
- jobs: sca-scan + container-scan (선택 영역만)
- 아티팩트: retention-days: 365 (연간 보관)

## GitLab CI 생성 규칙

stages: [secret-scan, code-scan, build-scan, dast]
각 domain을 해당 stage에 배치:
- secret-detection → secret-scan stage
- sast·sca·iac → code-scan stage (병렬)
- container → build-scan stage
- dast → dast stage
rules: merge_request_event (PR 단계 job)
       CI_COMMIT_BRANCH == "main" (merge 단계 job)

## 정책 파일 생성 규칙

.grype.yaml (SCA 선택 시):
- fail-on-severity: VULN_THRESHOLD 값
- ignore 예시 1개 포함 (주석으로 사용법 설명)

.gitleaks.toml (시크릿 탐지 선택 시):
- useDefault: true
- allowlists: 테스트 파일 경로 예외
- PROJECT_PATH의 테스트 폴더 자동 감지해서 경로 포함

.trivyignore.yaml (컨테이너 선택 시):
- 예시 무시 규칙 1개 포함

## PIPELINE-SUMMARY.md 생성 규칙

항상 생성. 포함 내용:
- 선택된 보안 영역과 사용 도구 표
- 파이프라인 실행 흐름 (단계별)
- 예상 소요 시간 (영역별)
- 생성된 파일 목록

## APPLY-GUIDE.md 생성 규칙

항상 생성. 포함 내용:
- 파일별 복사 위치
- 기존 워크플로우 충돌 방지 방법
  (HAS_EXISTING_WORKFLOW: true일 때 강조)
- 첫 실행 후 확인 사항
- 단계적 강화 로드맵
  (처음엔 Soft Fail → 안정화 후 Hard Fail로 전환)

## 주의사항

- output/devsecops/ 외부에 파일을 쓰지 않는다
- PROJECT_PATH의 기존 파일은 읽기만 하고 수정하지 않는다
- 로컬 절대경로를 산출물에 노출하지 않는다
- 생성하는 모든 파일은 한국어 주석 포함
