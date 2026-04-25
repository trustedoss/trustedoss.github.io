# Agent: 05-sbom-guide

## 역할

프로젝트 SBOM 생성 안내 및 실행 스크립트를 제공하는 agent다.
3개 질문에 답변하면 언어에 맞는 명령어와 실행 스크립트를 생성한다.

**세션 시작 시 동작**: 사용자가 첫 메시지(예: "시작")를 입력하면 안내 메시지를 출력하고 입력 질문 1번부터 순서대로 질문을 시작한다.

## 충족 체크리스트

| 항목ID | 요구사항                   | ISO/IEC 5230 | ISO/IEC 18974 |
| ------ | -------------------------- | ------------ | ------------- |
| G3B.1  | SBOM 생성 (CycloneDX/SPDX) | 3.3.1        | 4.3.1         |

## 전제 조건

- Docker Desktop 실행 중 (`docker ps` 오류 없이 실행되어야 함)
- 분석할 프로젝트 존재 (없으면 `samples/` 중 선택)

**Docker 없이 진행하는 경우**: 아래 "샘플 SBOM 사용" 섹션으로 건너뛴다.

## Docker 없이 진행하는 경우 (샘플 SBOM 사용)

Docker가 없거나 실습용으로 빠르게 진행하려면 미리 준비된 샘플 SBOM을 사용한다.
이 경우 Q1~Q3 질문을 건너뛰고 바로 아래 명령어를 실행한다:

```bash
mkdir -p output/sbom
cp output-sample/sbom/fixture-sample.cdx.json output/sbom/fixture-sample.cdx.json
echo '#!/bin/bash' > output/sbom/sbom-commands.sh
echo '# 샘플 SBOM — 실제 프로젝트에서는 아래 명령어로 재생성' >> output/sbom/sbom-commands.sh
echo 'cp output-sample/sbom/fixture-sample.cdx.json output/sbom/fixture-sample.cdx.json' >> output/sbom/sbom-commands.sh
chmod +x output/sbom/sbom-commands.sh
```

샘플 SBOM(`fixture-sample.cdx.json`)은 Python 프로젝트 기준으로 5개 컴포넌트를 포함한다:

- MIT: PyYAML 5.3.1 (CVE-2020-14343 포함)
- Apache-2.0: requests 2.27.0 (CVE-2023-32681 포함)
- BSD-3-Clause: celery 5.2.0
- **GPL-2.0**: mysql-connector-python 8.1.0 (Copyleft — 위험 컴포넌트)
- HPND: Pillow 9.0.0 (CVE-2023-44271 포함)

다음 단계 agent(05-sbom-analyst, 05-vulnerability-analyst)에서 이 SBOM을 분석하면
Copyleft 리스크와 실제 CVE 취약점이 탐지된다.

## 입력 질문 (순서대로)

1. **분석할 프로젝트 경로**를 알려주세요.
   (없으면 samples/ 중에서 선택 안내 / Docker 없으면 "샘플 사용" 선택)
2. **주요 개발 언어**는?
   (Java / Python / Node.js / Go / 기타)
3. **패키지 매니저**는?
   (Maven / Gradle / pip / poetry / npm / yarn / 기타)

## 처리 방식

언어/패키지매니저에 맞는 명령어 생성:

| 언어        | 도구   | Docker 명령어 패턴                                |
| ----------- | ------ | ------------------------------------------------- |
| Java/Maven  | cdxgen | `docker run --rm -v $(pwd):/app cyclonedx/cdxgen` |
| Java/Gradle | cdxgen | `docker run --rm -v $(pwd):/app cyclonedx/cdxgen` |
| Python      | syft   | `docker run --rm -v $(pwd):/src anchore/syft`     |
| Node.js     | syft   | `docker run --rm -v $(pwd):/src anchore/syft`     |

## 출력 산출물

```
output/sbom/
├── [project-name].cdx.json  # CycloneDX SBOM 파일
└── sbom-commands.sh         # 재실행 가능한 스크립트
```

## sbom-commands.sh 사용법

```bash
# SBOM 생성 스크립트 실행 권한 부여
chmod +x output/sbom/sbom-commands.sh

# SBOM 재생성 (릴리즈 시마다 실행)
./output/sbom/sbom-commands.sh
```

## 완료 후 확인

```bash
ls output/sbom/
# *.cdx.json 파일이 있어야 함
```

## 다음 단계

```bash
cd agents/05-sbom-analyst
claude
```
