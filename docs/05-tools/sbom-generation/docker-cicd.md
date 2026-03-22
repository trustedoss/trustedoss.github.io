---
sidebar_position: 2
sidebar_label: "Docker·CI/CD 실행 가이드"
---

# SBOM 생성: Docker 실행 가이드 및 CI/CD 자동화

이 문서는 syft·cdxgen의 실제 Docker 실행 명령어, GitHub Actions 자동화 설정, 샘플 프로젝트 실습, 트러블슈팅을 담고 있다.

---

## Docker로 syft 실행 — 언어/패키지매니저별 명령어

| 언어 | 패키지매니저 | 명령어 |
|------|------------|--------|
| Java | Maven/Gradle | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Python | pip | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Node.js | npm | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Go | go mod | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |

전체 명령어 (각 언어 동일, 디렉토리만 조정):

```bash
# output/sbom 폴더 생성
mkdir -p output/sbom

# syft로 SBOM 생성
docker run --rm \
  -v $(pwd):/project \
  anchore/syft:latest \
  /project \
  --output cyclonedx-json \
  > output/sbom/sbom.cdx.json
```

---

## Docker로 cdxgen 실행 (더 정밀한 분석 필요 시)

```bash
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  ghcr.io/cyclonedx/cdxgen:latest \
  -r /app \
  -o /app/output/sbom/sbom-cdxgen.cdx.json
```

Java Maven 프로젝트에 권장한다. syft보다 의존성 추적이 더 정밀하며, 전이 의존성(transitive dependencies)까지 더 완전하게 수집한다.

---

## GitHub Actions 자동화

SBOM 생성을 CI/CD 파이프라인에 통합하면 모든 릴리스마다 최신 SBOM이 자동으로 생성된다.

```yaml
# .github/workflows/sbom.yml
name: Generate SBOM

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate SBOM with syft
        run: |
          docker run --rm \
            -v ${{ github.workspace }}:/project \
            anchore/syft:latest \
            /project --output cyclonedx-json \
            > sbom.cdx.json
      - name: Upload SBOM as artifact
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.cdx.json
```

---

## samples/ 프로젝트로 실습

실습용 샘플 프로젝트가 두 가지 제공된다:

- `samples/java-vulnerable/`: log4j-core 2.14.1 포함 → CVE-2021-44228 탐지 예상
- `samples/python-mixed-license/`: GPL 혼재 → 라이선스 충돌 탐지 예상

```bash
# java-vulnerable 샘플로 실습
docker run --rm \
  -v $(pwd)/samples/java-vulnerable:/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > output/sbom/java-vulnerable.cdx.json
```

---

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|---------|
| SBOM이 비어있음 (`components: []`) | lock 파일 없음 | `package-lock.json`, `requirements.txt`, `pom.xml` 등 확인 |
| Docker 볼륨 마운트 오류 | 경로 문제 | 절대 경로로 변경: `-v /full/path:/project` |
| Permission denied | 권한 문제 | `sudo` 또는 Docker 그룹 추가 |
| 이미지 풀링 오래 걸림 | 네트워크 | 최초 실행 시 정상, 이후 캐시 사용 |
