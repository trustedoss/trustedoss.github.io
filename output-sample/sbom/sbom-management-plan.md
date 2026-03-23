# SBOM 관리 계획

## 개요

본 문서는 ISO/IEC 18974 4.3.1 및 4.3.2 요구사항을 충족하기 위한 SBOM 관리 및 유지보수 계획을 정의한다.

| 항목 | 내용 |
|------|------|
| 외부 제공 여부 | 예 (고객/납품처 요청 시 제공) |
| 지원 포맷 | CycloneDX, SPDX (납품처 요구에 따라 선택 제공) |
| 갱신 주기 | 기능 완료 시 수시 (릴리즈 단위) |

---

## 1. SBOM 생성 원칙

### 1.1 생성 시점
- 기능 개발 완료 후 릴리즈 빌드 시점마다 SBOM 생성
- 의존성 변경(추가/삭제/버전 업데이트) 발생 시 즉시 재생성
- 정기 보안 점검(월 1회) 시 최신 SBOM 재생성 확인

### 1.2 생성 도구
| 빌드 환경 | 도구 | 생성 포맷 |
|-----------|------|-----------|
| Java/Maven | `cyclonedx-maven-plugin` | CycloneDX JSON |
| Java/Gradle | `cyclonedx-gradle-plugin` | CycloneDX JSON |
| Node.js | `@cyclonedx/cyclonedx-npm` | CycloneDX JSON |
| Python | `cyclonedx-bom` | CycloneDX JSON |
| 포맷 변환 | `cdxgen`, `spdx-tools` | CycloneDX ↔ SPDX |

### 1.3 포맷 변환

납품처가 SPDX를 요구하는 경우 CycloneDX → SPDX 변환을 수행한다.

```bash
# CycloneDX → SPDX 변환 (cdxgen 사용)
cdxgen -o sbom.cdx.json --format json .
# SPDX 변환은 별도 도구(spdx-tools) 또는 납품처 지정 도구 활용
```

---

## 2. SBOM 갱신 절차

### 2.1 릴리즈 단위 갱신 (주요 절차)

```
1. 기능 개발 완료 및 코드 프리즈
2. 의존성 목록 최종 확정 (package.json / pom.xml / requirements.txt 등)
3. SBOM 자동 생성 (CI/CD 파이프라인 연동)
4. 라이선스 검토 (copyleft 신규 포함 여부 확인)
5. 취약점 스캔 (OSV-Scanner / Grype)
6. SBOM 파일 버전 태깅 및 저장
7. 납품처 제출 필요 시 sbom-sharing-template.md 첨부하여 전달
```

### 2.2 긴급 갱신 (보안 취약점 발생 시)

Critical/High CVE 발생 시 릴리즈 주기와 무관하게 즉시 갱신:
1. 취약 컴포넌트 패치 또는 대체
2. SBOM 재생성
3. 납품처에 갱신 SBOM 재제출 (필요 시)

---

## 3. CI/CD 연동 자동화

### 3.1 파이프라인 구성 (예시: GitHub Actions)

```yaml
# .github/workflows/sbom.yml
name: SBOM 생성

on:
  push:
    branches: [main, release/*]
  workflow_dispatch:

jobs:
  generate-sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: SBOM 생성 (CycloneDX)
        run: |
          # 프로젝트 빌드 환경에 맞는 명령어로 교체
          npx @cyclonedx/cyclonedx-npm --output-file sbom.cdx.json

      - name: 취약점 스캔
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
          grype sbom:sbom.cdx.json

      - name: SBOM 저장
        uses: actions/upload-artifact@v4
        with:
          name: sbom-${{ github.sha }}
          path: sbom.cdx.json
```

### 3.2 로컬 저장 경로 규칙

```
output/sbom/
├── {프로젝트명}-{버전}.cdx.json    # CycloneDX 포맷
├── {프로젝트명}-{버전}.spdx.json   # SPDX 포맷 (변환 시)
├── sbom-management-plan.md
└── sbom-sharing-template.md
```

---

## 4. 공급망 모니터링 (ISO/IEC 18974 4.3.2)

### 4.1 정기 모니터링 항목

| 항목 | 주기 | 도구 |
|------|------|------|
| 신규 CVE 스캔 | 월 1회 (또는 릴리즈 시) | OSV-Scanner, Grype |
| 라이선스 변경 감지 | 릴리즈 시 | ort, scancode-toolkit |
| 의존성 업데이트 추적 | 지속 | Dependabot, Renovate |
| SBOM 유효성 검증 | 릴리즈 시 | cyclonedx-cli validate |

### 4.2 모니터링 자동화 설정

```bash
# GitHub Dependabot 활성화 (.github/dependabot.yml)
version: 2
updates:
  - package-ecosystem: "npm"   # 또는 maven, pip 등
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

### 4.3 취약점 대응 기준

| 심각도 | 대응 기한 | 조치 |
|--------|-----------|------|
| Critical | 즉시 (24시간 내) | 패치 또는 대체 컴포넌트 적용 |
| High | 7일 내 | 패치 계획 수립 및 적용 |
| Medium | 30일 내 | 다음 릴리즈 시 반영 |
| Low | 90일 내 또는 차기 계획 | 리스크 수용 여부 검토 |

---

## 5. 책임자 및 연락처

| 역할 | 담당 업무 |
|------|-----------|
| SBOM 담당자 | SBOM 생성·갱신·배포 총괄 |
| 보안 담당자 | 취약점 스캔 결과 검토 및 대응 |
| 법무/컴플라이언스 | 라이선스 검토 및 납품처 협의 |

> 담당자 정보는 `output/organization/` 산출물 참조

---

## 6. 준거 표준

| 표준 | 요구사항 |
|------|---------|
| ISO/IEC 18974 | 4.3.1 — SBOM 관리 및 유지보수 |
| ISO/IEC 18974 | 4.3.1 — SBOM 공유 (공급망 파트너) |
| ISO/IEC 18974 | 4.3.2 — 공급망 취약점 지속 모니터링 |
