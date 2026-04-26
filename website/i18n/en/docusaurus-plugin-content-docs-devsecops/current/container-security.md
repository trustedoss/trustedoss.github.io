---
id: container-security
title: 컨테이너·이미지 보안
sidebar_label: 컨테이너 보안
sidebar_position: 6
---

# 컨테이너·이미지 보안

## 컨테이너 보안이란

컨테이너 이미지에 포함된 OS 패키지·애플리케이션 의존성의 취약점, Dockerfile 설정 오류, 시크릿 노출을 배포 전에 탐지하는 보안 검사입니다. 이미지가 한 번 배포되면 전체 인스턴스에 동일한 취약점이 퍼지므로 빌드 단계 차단이 특히 중요합니다.

---

## 도구 비교

| 도구   | 특징                       | 탐지 범위                    | 라이선스   |
| ------ | -------------------------- | ---------------------------- | ---------- |
| Trivy  | 올인원·빠른 속도·설정 단순 | 이미지·파일시스템·IaC·시크릿 | Apache-2.0 |
| Grype  | SBOM 연동 최적화           | 이미지·파일시스템            | Apache-2.0 |
| Dockle | Dockerfile 모범 사례 검사  | 이미지 설정                  | Apache-2.0 |

컨테이너 보안 단일 도구로는 Trivy를 권장하며, SCA 파이프라인에서 이미 grype를 사용 중이라면 이미지 스캔도 grype로 통일 가능합니다.

---

## Trivy 설정

### 기본 사용법

```bash
# 로컬 이미지 스캔
trivy image myapp:latest

# 파일시스템 스캔 (빌드 전)
trivy fs .

# SBOM 생성
trivy image --format cyclonedx myapp:latest \
  -o sbom.cdx.json

# 심각도 필터
trivy image --severity HIGH,CRITICAL myapp:latest
```

### GitHub Actions

```yaml
# .github/workflows/container-security.yml

name: Container Security — Trivy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan image — vulnerability
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: table
          exit-code: 1
          severity: HIGH,CRITICAL
          ignore-unfixed: true

      - name: Scan image — secret
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          scanners: secret
          exit-code: 1

      - name: Upload SBOM
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: cyclonedx
          output: sbom.cdx.json

      - uses: actions/upload-artifact@v4
        with:
          name: container-sbom-${{ github.sha }}
          path: sbom.cdx.json
          retention-days: 90
```

### GitLab CI

```yaml
# .gitlab-ci.yml (container-security 잡 부분)

container-security:
  stage: test
  image: aquasec/trivy:latest
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2376
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script:
    - docker build -t $IMAGE_TAG .
    # 취약점 스캔
    - trivy image
      --severity HIGH,CRITICAL
      --exit-code 1
      --ignore-unfixed
      $IMAGE_TAG
    # 시크릿 스캔
    - trivy image
      --scanners secret
      --exit-code 1
      $IMAGE_TAG
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## Trivy 정책 파일

:::info ignore-unfixed 옵션으로 수정 불가 취약점을 제외하세요
upstream에서 아직 패치가 없는 취약점은 개발팀이 수정할 수 없으므로 제외하면 실행 가능한 알림에 집중할 수 있습니다.
:::

```yaml
# .trivyignore.yaml

vulnerabilities:
  - id: CVE-2023-XXXXX
    paths:
      - usr/lib/some-lib
    statement: '해당 경로 컨테이너 내 미사용 — 보안팀 승인 2024-02-01'

secrets:
  - id: aws-access-key-id
    paths:
      - test/fixtures/dummy.env
```

---

## Dockerfile 보안 모범 사례

1. **최소 베이스 이미지 사용:** `ubuntu` 대신 `alpine`·`distroless`를 선택합니다. 패키지 수가 적을수록 취약점 노출 면적이 줄어듭니다.
2. **루트 실행 금지:** `USER` 명령어로 비루트 사용자를 지정합니다. 루트 실행은 컨테이너 탈출 시 피해를 확대합니다.
3. **멀티 스테이지 빌드:** 빌드 도구·소스코드를 최종 이미지에서 제외합니다. 이미지 크기 축소와 공격 면적 감소를 동시에 달성합니다.
4. **시크릿 ARG·ENV 금지:** 빌드 인수나 환경변수로 시크릿을 전달하지 않습니다. 이미지 레이어에 평문으로 남습니다.
5. **버전 고정:** `FROM ubuntu:22.04`처럼 태그를 명시합니다. `latest` 사용 시 예상치 못한 취약점이 유입될 수 있습니다.

---

## 다음 단계

- 인프라 코드 보안: [IaC 보안](./iac-security)
- 전체 파이프라인 통합: [파이프라인 설계](./pipeline-design)
- 배포 후 이미지 지속 모니터링: [모니터링·자동 교정](./monitoring)
