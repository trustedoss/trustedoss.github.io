# Agent: 05-sbom-guide

## 역할

프로젝트 SBOM 생성 안내 및 실행 스크립트를 제공하는 agent다.
3개 질문에 답변하면 언어에 맞는 명령어와 실행 스크립트를 생성한다.

## 충족 체크리스트

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G3B.1 | SBOM 생성 (CycloneDX/SPDX) | 3.3.1 | 4.3.1 |

## 전제 조건

- Docker Desktop 실행 중 (`docker ps` 오류 없이 실행되어야 함)
- 분석할 프로젝트 존재 (없으면 `samples/` 중 선택)

## 입력 질문 (순서대로)

1. **분석할 프로젝트 경로**를 알려주세요.
   (없으면 samples/ 중에서 선택 안내)
2. **주요 개발 언어**는?
   (Java / Python / Node.js / Go / 기타)
3. **패키지 매니저**는?
   (Maven / Gradle / pip / poetry / npm / yarn / 기타)

## 처리 방식

언어/패키지매니저에 맞는 명령어 생성:

| 언어 | 도구 | Docker 명령어 패턴 |
|------|------|-----------------|
| Java/Maven | cdxgen | `docker run --rm -v $(pwd):/app cyclonedx/cdxgen` |
| Java/Gradle | cdxgen | `docker run --rm -v $(pwd):/app cyclonedx/cdxgen` |
| Python | syft | `docker run --rm -v $(pwd):/src anchore/syft` |
| Node.js | syft | `docker run --rm -v $(pwd):/src anchore/syft` |

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
