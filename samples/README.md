# 실습 샘플 프로젝트

trustedoss 가이드 [챕터 05 — 도구 실습](../docs/05-tools/sbom-generation/index.md)에서 분석 대상으로 사용하는 샘플 3개입니다. 각 샘플에는 학습을 위한 결함(취약점·라이선스 리스크)을 의도적으로 심어 두었습니다. SBOM 생성과 라이선스·취약점 분석 실습의 입력이 됩니다.

| 샘플                                            | 언어          | 학습 포인트                                    | 난이도 | 예상 시간 |
| ----------------------------------------------- | ------------- | ---------------------------------------------- | ------ | --------- |
| [java-vulnerable](./java-vulnerable/)           | Java (Maven)  | Log4Shell(CVE-2021-44228) Critical 취약점 탐지 | 입문   | 약 20분   |
| [python-mixed-license](./python-mixed-license/) | Python (pip)  | GPL + Permissive 혼재 Copyleft 리스크          | 입문   | 약 20분   |
| [nodejs-unlicensed](./nodejs-unlicensed/)       | Node.js (npm) | 라이선스 미명시(NOASSERTION) 패키지 처리       | 중급   | 약 25분   |

## 공통 선행 조건

- **Docker Desktop 실행** (`docker ps`가 오류 없이 동작). 설치하지 않았다면 [챕터 05](../docs/05-tools/sbom-generation/index.md)의 "Docker 없이 진행하는 경우" 경로로 미리 만든 샘플 SBOM을 사용할 수 있습니다.
- 처음이라면 **java-vulnerable**부터 권장합니다. 취약점 탐지 결과가 가장 직관적입니다.
- nodejs-unlicensed는 SBOM 생성 전 `npm install`이 필요합니다.

## 사용 방법

1. [챕터 05 — SBOM 생성](../docs/05-tools/sbom-generation/index.md)을 진행하며 분석 대상으로 샘플 경로를 선택합니다.
2. 각 샘플 README의 "SBOM 생성 명령어"를 실행해 `output/sbom/`에 SBOM을 만듭니다.
3. 라이선스·취약점 분석 agent로 결과(Copyleft 리스크, CVE)를 확인합니다.

각 샘플의 상세한 학습 목표·예상 결과·실제 조치 방법은 해당 폴더의 README를 참고하세요.
