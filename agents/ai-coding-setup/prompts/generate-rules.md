# generate-rules 프롬프트

## 목적

사용자 답변과 프로젝트 분석 결과를 바탕으로
AI 코딩 도구별 오픈소스 정책 Rules 파일을 생성한다.

## 입력 변수

아래 변수들이 CLAUDE.md의 질의응답을 통해 수집된다.

- PROJECT_PATH: 분석할 프로젝트 경로
- TOOLS: 선택한 AI 코딩 도구 목록
- LICENSE_LEVEL: 엄격 / 표준 / 유연
- VULN_THRESHOLD: critical / high / medium
- OPTIONS: 추가 규칙 목록 (sbom / copyright / cicd)
- DETECTED_LANGS: 감지된 언어 목록 (자동)
- DETECTED_PKGS: 감지된 패키지 목록 (자동)
- RISK_PKGS: 금지 라이선스 패키지 목록 (자동)

## 라이선스 정책 매핑

LICENSE_LEVEL에 따라 아래 내용을 Rules에 포함한다.

엄격:
  허용: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
  금지: LGPL, MPL, GPL, AGPL, SSPL, Commons Clause

표준:
  허용: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
  주의(법무 검토 필요): LGPL, MPL
  금지: GPL, AGPL, SSPL, Commons Clause

유연:
  허용: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, LGPL, MPL
  주의(법무 검토 필요): GPL, AGPL
  금지: SSPL, Commons Clause

## 취약점 정책 매핑

VULN_THRESHOLD에 따라 아래 내용을 포함한다.

critical: Critical CVE만 즉시 차단. High 이하는 경고.
high:     High·Critical CVE 발견 시 차단. Medium 이하는 경고.
medium:   Medium·High·Critical CVE 발견 시 차단.

## 언어별 audit 명령어

DETECTED_LANGS에 포함된 언어만 Rules에 추가한다.

javascript / typescript: npm audit 또는 yarn audit
python:  pip-audit
java:    dependency-check
go:      govulncheck ./...
rust:    cargo audit
ruby:    bundle audit

## 도구별 파일 생성 규칙

TOOLS에 포함된 도구별로 아래 파일을 생성한다.
출력 경로는 모두 output/ai-coding/ 하위.

Claude Code:
  파일: CLAUDE.md
  형식: ## 섹션 헤더 기반 지시문
  특이사항: 기존 파일이 PROJECT_PATH에 있으면
            ## 오픈소스 정책 섹션만 추가 (기존 내용 보존)

Cursor:
  파일: .cursorrules
  형식: 간결한 규칙 목록

GitHub Copilot:
  파일: .github/copilot-instructions.md
  형식: 마크다운 지침

Windsurf:
  파일: .windsurfrules
  형식: 간결한 규칙 목록

Cline / Aider:
  파일: .clinerules
  형식: 프로젝트 지침 목록

## LICENSE-RISK-REPORT.md 생성 규칙

RISK_PKGS가 있을 때만 생성한다.
없으면 생략.

포함 내용:
- 발견된 금지/주의 라이선스 패키지 목록
- 각 패키지의 라이선스 유형
- 권장 대체 패키지 (있는 경우)
- 법무 검토 권고 여부

## SETUP-SUMMARY.md 생성 규칙

항상 생성한다.

포함 내용:
- 생성된 파일 목록과 각 파일의 적용 위치
- 프로젝트 경로별 복사 명령어 예시
- 발견된 라이선스 위험 요약 (있는 경우)
- 다음 단계 안내 (devsecops-setup agent)

## 실행 순서

1. PROJECT_PATH 의존성 파일 읽기
   → 언어·패키지 자동 감지
   → 금지 라이선스 패키지 검색

2. RISK_PKGS 발견 시 사용자에게 보고 후 계속 여부 확인

3. 모든 질문 수집 완료 후 파일 생성 시작
   → TOOLS 목록 순서대로 도구별 파일 생성
   → LICENSE-RISK-REPORT.md (RISK_PKGS 있을 때)
   → SETUP-SUMMARY.md

4. 생성 완료 후 CLAUDE.md의 "완료 후 안내" 출력

## 주의사항

- output/ai-coding/ 외부에 파일을 쓰지 않는다
- PROJECT_PATH의 기존 파일은 읽기만 하고 수정하지 않는다
- 로컬 절대경로를 산출물에 노출하지 않는다
  (SETUP-SUMMARY.md의 경로 예시는 ./프로젝트명 형식 사용)
- 생성하는 모든 파일은 한국어로 작성한다
