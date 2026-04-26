---
sidebar_label: SBOM 산출물
sidebar_position: 4
---

# SBOM 산출물 Best Practice

[05 도구 챕터](/docs/tools/sbom-generation)에서 생성하는 SBOM 관련 산출물 예시입니다.
샘플 프로젝트(`java-vulnerable`, Log4Shell CVE-2021-44228 포함)를 기준으로 작성된 실제 출력 예시를 확인할 수 있습니다.

---

## SBOM 라이선스 분석 리포트

> **생성 agent**: `05-sbom-analyst` | **저장 경로**: `output/sbom/license-report.md`

---

리포트 유형: SBOM 라이선스 분석
생성일: 2026-03-23 07:11
대상 프로젝트: vulnerable-java-app
사용 도구: syft 1.42.3

---

### 1. 요약

- 분석 대상 SBOM: `java-vulnerable.cdx.json` (CycloneDX 1.6)
- 소프트웨어 컴포넌트 총 **3개** (파일 항목 제외)
- SBOM 내 라이선스 필드가 비어 있음 → 외부 정보 기반으로 라이선스 보완 분류
- Apache Log4j 2.14.1은 **Apache 2.0 (Permissive)** 으로 분류됨
- 내부 애플리케이션(`vulnerable-java-app`)은 라이선스 정보 없음 → **Unknown**
- Copyleft 컴포넌트 **0개** (즉시 컴플라이언스 조치 불필요)
- ⚠️ SBOM에 라이선스 정보가 누락되어 있어 도구 재실행 또는 수동 보완 권고

### 2. 컴포넌트별 라이선스 상세

| 컴포넌트            | 버전   | 그룹                     | 라이선스   | 분류       | 출처                 |
| ------------------- | ------ | ------------------------ | ---------- | ---------- | -------------------- |
| log4j-api           | 2.14.1 | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (보완) |
| log4j-core          | 2.14.1 | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (보완) |
| vulnerable-java-app | 1.0.0  | com.example              | Unknown    | Unknown    | SBOM 미기재          |

> **참고:** SBOM 생성 시 라이선스 정보가 포함되지 않았습니다.
> syft 재실행 시 `--source-name`, Maven Central 메타데이터 활성화 여부를 확인하거나
> `cdxgen` 도구를 병행 사용하여 라이선스 필드를 보완하는 것을 권장합니다.

### 3. 라이선스 분류 요약

| 분류            | 컴포넌트 수 | 컴포넌트 목록         |
| --------------- | ----------- | --------------------- |
| Permissive      | 2           | log4j-api, log4j-core |
| Weak Copyleft   | 0           | —                     |
| Strong Copyleft | 0           | —                     |
| Unknown         | 1           | vulnerable-java-app   |

### 4. 조치사항

#### ⚪ Info — SBOM 라이선스 정보 보완

- **대상:** 전체 컴포넌트 (특히 `vulnerable-java-app`)
- **조치:** syft 또는 cdxgen 재실행 시 라이선스 메타데이터 활성화

  ```bash
  # syft: Maven POM 라이선스 정보 포함
  syft /path/to/project --output cyclonedx-json

  # cdxgen: 라이선스 정보 자동 수집
  cdxgen -t java /path/to/project -o sbom.cdx.json
  ```

- **예상 소요시간:** 30분

#### ⚪ Info — 내부 애플리케이션 라이선스 명시

- **대상:** `vulnerable-java-app@1.0.0`
- **조치:** `pom.xml`의 `<licenses>` 섹션에 내부 라이선스 또는 Proprietary 명시
  ```xml
  <licenses>
    <license>
      <name>Proprietary</name>
      <url>https://example.com/license</url>
    </license>
  </licenses>
  ```
- **예상 소요시간:** 15분

### 5. 컴플라이언스 의무 요약

| 라이선스        | 의무사항                                               |
| --------------- | ------------------------------------------------------ |
| Apache-2.0      | 저작권 표시 유지, NOTICE 파일 포함, 라이선스 사본 배포 |
| Permissive 공통 | 2차 배포 시 원본 라이선스 텍스트 포함                  |

> Apache-2.0은 소스코드 공개 의무가 없어 바이너리 배포에 친화적입니다.
> 배포 패키지에 `LICENSE`, `NOTICE` 파일이 포함되어 있는지 확인하십시오.

---

_이 리포트는 ISO/IEC 5230 §3.3.2(라이선스 식별) 및 §3.4.1(컴플라이언스 산출물) 요구사항을 충족하기 위해 생성되었습니다._

---

## Copyleft 위험도 리포트

> **생성 agent**: `05-sbom-analyst` | **저장 경로**: `output/sbom/copyleft-risk.md`

---

리포트 유형: Copyleft 위험도 분석
생성일: 2026-03-23 07:11
대상 프로젝트: vulnerable-java-app
사용 도구: syft 1.42.3

---

### 1. 요약

- 분석 대상: `java-vulnerable.cdx.json` (CycloneDX 1.6, 컴포넌트 3개)
- **Strong Copyleft (GPL/AGPL) 컴포넌트: 0개**
- **Weak Copyleft (LGPL/MPL) 컴포넌트: 0개**
- 식별된 컴포넌트 2개는 모두 **Apache-2.0 (Permissive)** 으로 Copyleft 위험 없음
- 1개 컴포넌트는 라이선스 **Unknown** — 별도 확인 필요
- ⚠️ SBOM 내 라이선스 메타데이터 누락으로 잠재적 미확인 Copyleft 위험 존재 가능

### 2. Copyleft 위험 컴포넌트 목록

| 컴포넌트            | 버전   | 라이선스   | Copyleft 등급 | 위험도    | 조치               |
| ------------------- | ------ | ---------- | ------------- | --------- | ------------------ |
| log4j-api           | 2.14.1 | Apache-2.0 | 없음          | 🟢 Low    | 불필요             |
| log4j-core          | 2.14.1 | Apache-2.0 | 없음          | 🟢 Low    | 불필요             |
| vulnerable-java-app | 1.0.0  | Unknown    | 미확인        | 🟡 Medium | 라이선스 확인 필요 |

### 3. Copyleft 등급 기준

| 등급            | 해당 라이선스               | 배포 시 의무                            |
| --------------- | --------------------------- | --------------------------------------- |
| Strong Copyleft | GPL-2.0, GPL-3.0, AGPL-3.0  | 전체 소스코드 공개 의무                 |
| Weak Copyleft   | LGPL-2.1, LGPL-3.0, MPL-2.0 | 해당 컴포넌트 수정본 소스코드 공개      |
| Permissive      | Apache-2.0, MIT, BSD        | 저작권 표시만 유지                      |
| Unknown         | —                           | 확인 전까지 Copyleft로 보수적 처리 권고 |

### 4. 위험도 평가

#### 현재 배포 방식 기준

| 배포 방식                     | Copyleft 위험                       |
| ----------------------------- | ----------------------------------- |
| 소스코드 비공개 바이너리 배포 | 🟢 위험 없음 (Apache-2.0만 사용 시) |
| SaaS / 네트워크 서비스        | 🟢 위험 없음 (AGPL 컴포넌트 없음)   |
| 오픈소스 재배포               | 🟢 위험 없음 (Strong Copyleft 없음) |

> **결론:** 현재 식별된 오픈소스 컴포넌트(log4j-api, log4j-core)는 모두 Apache-2.0으로
> 어떤 배포 방식에서도 소스코드 공개 의무가 발생하지 않습니다.

### 5. 조치사항

#### 🟡 Medium — Unknown 라이선스 컴포넌트 확인

- **대상:** `vulnerable-java-app@1.0.0` (내부 개발 애플리케이션)
- **위험:** 라이선스 미명시 상태에서 외부 배포 시 컴플라이언스 불명확
- **조치:** `pom.xml`에 라이선스 정보 명시 또는 내부 IP 정책 문서화
- **예상 소요시간:** 15분

#### ⚪ Info — SBOM 라이선스 정보 보완

- **대상:** 전체 컴포넌트
- **위험:** 라이선스 필드 공백으로 추가 의존성 추가 시 Copyleft 누락 가능
- **조치:** SBOM 생성 도구에서 라이선스 메타데이터 활성화 후 재생성
- **예상 소요시간:** 30분

### 6. 향후 모니터링 권고

- 새 의존성 추가 시 SBOM 재생성 및 이 리포트 업데이트
- GPL/AGPL 컴포넌트 도입 시 법무팀 검토 필수
- 분기별 SBOM 라이선스 현황 점검 일정 수립

---

_이 리포트는 ISO/IEC 5230 §3.3.2(라이선스 식별) 요구사항을 충족하기 위해 생성되었습니다._

---

## SBOM 관리 계획

> **생성 agent**: `05-sbom-management` | **저장 경로**: `output/sbom/sbom-management-plan.md`

---

본 문서는 ISO/IEC 18974 4.3.1 및 4.3.2 요구사항을 충족하기 위한 SBOM 관리 및 유지보수 계획을 정의한다.

| 항목           | 내용                                           |
| -------------- | ---------------------------------------------- |
| 외부 제공 여부 | 예 (고객/납품처 요청 시 제공)                  |
| 지원 포맷      | CycloneDX, SPDX (납품처 요구에 따라 선택 제공) |
| 갱신 주기      | 기능 완료 시 수시 (릴리즈 단위)                |

---

### 1. SBOM 생성 원칙

#### 1.1 생성 시점

- 기능 개발 완료 후 릴리즈 빌드 시점마다 SBOM 생성
- 의존성 변경(추가/삭제/버전 업데이트) 발생 시 즉시 재생성
- 정기 보안 점검(월 1회) 시 최신 SBOM 재생성 확인

#### 1.2 생성 도구

| 빌드 환경   | 도구                       | 생성 포맷        |
| ----------- | -------------------------- | ---------------- |
| Java/Maven  | `cyclonedx-maven-plugin`   | CycloneDX JSON   |
| Java/Gradle | `cyclonedx-gradle-plugin`  | CycloneDX JSON   |
| Node.js     | `@cyclonedx/cyclonedx-npm` | CycloneDX JSON   |
| Python      | `cyclonedx-bom`            | CycloneDX JSON   |
| 포맷 변환   | `cdxgen`, `spdx-tools`     | CycloneDX ↔ SPDX |

#### 1.3 포맷 변환

납품처가 SPDX를 요구하는 경우 CycloneDX → SPDX 변환을 수행한다.

```bash
# CycloneDX → SPDX 변환 (cdxgen 사용)
cdxgen -o sbom.cdx.json --format json .
# SPDX 변환은 별도 도구(spdx-tools) 또는 납품처 지정 도구 활용
```

---

### 2. SBOM 갱신 절차

#### 2.1 릴리즈 단위 갱신 (주요 절차)

```
1. 기능 개발 완료 및 코드 프리즈
2. 의존성 목록 최종 확정 (package.json / pom.xml / requirements.txt 등)
3. SBOM 자동 생성 (CI/CD 파이프라인 연동)
4. 라이선스 검토 (copyleft 신규 포함 여부 확인)
5. 취약점 스캔 (OSV-Scanner / Grype)
6. SBOM 파일 버전 태깅 및 저장
7. 납품처 제출 필요 시 sbom-sharing-template.md 첨부하여 전달
```

#### 2.2 긴급 갱신 (보안 취약점 발생 시)

Critical/High CVE 발생 시 릴리즈 주기와 무관하게 즉시 갱신:

1. 취약 컴포넌트 패치 또는 대체
2. SBOM 재생성
3. 납품처에 갱신 SBOM 재제출 (필요 시)

---

### 3. CI/CD 연동 자동화

#### 3.1 파이프라인 구성 (예시: GitHub Actions)

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

#### 3.2 로컬 저장 경로 규칙

```
output/sbom/
├── {프로젝트명}-{버전}.cdx.json    # CycloneDX 포맷
├── {프로젝트명}-{버전}.spdx.json   # SPDX 포맷 (변환 시)
├── sbom-management-plan.md
└── sbom-sharing-template.md
```

---

### 4. 공급망 모니터링 (ISO/IEC 18974 4.3.2)

#### 4.1 정기 모니터링 항목

| 항목                 | 주기                    | 도구                   |
| -------------------- | ----------------------- | ---------------------- |
| 신규 CVE 스캔        | 월 1회 (또는 릴리즈 시) | OSV-Scanner, Grype     |
| 라이선스 변경 감지   | 릴리즈 시               | ort, scancode-toolkit  |
| 의존성 업데이트 추적 | 지속                    | Dependabot, Renovate   |
| SBOM 유효성 검증     | 릴리즈 시               | cyclonedx-cli validate |

#### 4.2 모니터링 자동화 설정

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

#### 4.3 취약점 대응 기준

| 심각도   | 대응 기한              | 조치                         |
| -------- | ---------------------- | ---------------------------- |
| Critical | 즉시 (24시간 내)       | 패치 또는 대체 컴포넌트 적용 |
| High     | 7일 내                 | 패치 계획 수립 및 적용       |
| Medium   | 30일 내                | 다음 릴리즈 시 반영          |
| Low      | 90일 내 또는 차기 계획 | 리스크 수용 여부 검토        |

---

### 5. 책임자 및 연락처

| 역할              | 담당 업무                     |
| ----------------- | ----------------------------- |
| SBOM 담당자       | SBOM 생성·갱신·배포 총괄      |
| 보안 담당자       | 취약점 스캔 결과 검토 및 대응 |
| 법무/컴플라이언스 | 라이선스 검토 및 납품처 협의  |

> 담당자 정보는 `output/organization/` 산출물 참조

---

### 6. 준거 표준

| 표준          | 요구사항                            |
| ------------- | ----------------------------------- |
| ISO/IEC 18974 | 4.3.1 — SBOM 관리 및 유지보수       |
| ISO/IEC 18974 | 4.3.1 — SBOM 공유 (공급망 파트너)   |
| ISO/IEC 18974 | 4.3.2 — 공급망 취약점 지속 모니터링 |

---

## SBOM 제출 안내문 (납품처 제출용 템플릿)

> **생성 agent**: `05-sbom-management` | **저장 경로**: `output/sbom/sbom-sharing-template.md`

---

> **사용 방법**: 이 문서를 SBOM 파일과 함께 납품처/고객에게 전달한다.
> `[ ]` 항목은 실제 정보로 채워서 제출한다.

---

수신: [ 납품처/고객명 ]
발신: [ 귀사 회사명 ]
문서 제목: SBOM (Software Bill of Materials) 제출 안내
작성일: [ YYYY-MM-DD ]

---

### 1. 제출 파일 정보

| 항목         | 내용                                   |
| ------------ | -------------------------------------- |
| 제품명       | [ 제품명 또는 소프트웨어명 ]           |
| 버전         | [ v0.0.0 ]                             |
| 빌드 일시    | [ YYYY-MM-DD HH:MM ]                   |
| SBOM 포맷    | [ CycloneDX 1.5 JSON / SPDX 2.3 JSON ] |
| 파일명       | [ 예: myproduct-v1.0.0.cdx.json ]      |
| SHA-256 해시 | [ 파일 해시값 ]                        |

---

### 2. SBOM 포맷 안내

#### CycloneDX 포맷 제출 시

- 표준: CycloneDX Specification 1.5
- 인코딩: JSON
- 생성 도구: [ 사용한 도구명 및 버전 ]
- 검증: `cyclonedx-cli validate --input-file <파일명>`

#### SPDX 포맷 제출 시

- 표준: SPDX 2.3
- 인코딩: JSON
- 생성 도구: [ 사용한 도구명 및 버전 ]
- 검증: `pyspdxtools validate <파일명>`

---

### 3. 포함 범위

| 항목          | 내용                                               |
| ------------- | -------------------------------------------------- |
| 포함 컴포넌트 | 직접 의존성 및 전이 의존성 전체                    |
| 포함 정보     | 컴포넌트명, 버전, 라이선스, PURL, 해시             |
| 제외 항목     | 빌드 전용 도구 (devDependencies 등, 런타임 미포함) |
| 분석 범위     | [ 예: 백엔드 서비스 / 프론트엔드 앱 / 전체 ]       |

---

### 4. 라이선스 의무사항 이행 현황

| 라이선스 유형        | 포함 여부       | 이행 조치                              |
| -------------------- | --------------- | -------------------------------------- |
| MIT, Apache-2.0, BSD | 포함            | 저작권 고지 포함 완료                  |
| LGPL-2.1, LGPL-3.0   | [ 포함/미포함 ] | 동적 링크 방식 사용, 소스 제공 준비    |
| GPL-2.0, GPL-3.0     | [ 포함/미포함 ] | 소스코드 공개 또는 제공 의무 검토 완료 |
| 기타 독점 라이선스   | [ 포함/미포함 ] | 개별 라이선스 계약 확인 완료           |

> 라이선스 상세 분석 결과는 `output/sbom/license-report.md` 참조

---

### 5. 갱신 정책

| 항목      | 내용                                            |
| --------- | ----------------------------------------------- |
| 갱신 주기 | 기능 완료 시 수시 (릴리즈 단위)                 |
| 긴급 갱신 | Critical/High CVE 발생 시 즉시 재생성 및 재제출 |
| 버전 관리 | 각 릴리즈 버전별 SBOM 아카이브 유지             |
| 제공 방식 | [ 이메일 / 보안 포털 / 납품처 지정 방식 ]       |

---

### 6. 연락처

SBOM 관련 문의 또는 추가 요청 시 아래로 연락한다.

| 역할              | 담당자   | 연락처     |
| ----------------- | -------- | ---------- |
| SBOM 담당자       | [ 이름 ] | [ 이메일 ] |
| 보안 담당자       | [ 이름 ] | [ 이메일 ] |
| 법무/컴플라이언스 | [ 이름 ] | [ 이메일 ] |

---

### 7. 추가 제공 가능 자료

요청 시 아래 자료를 추가 제공할 수 있다:

- [ ] 오픈소스 고지문 (NOTICES.txt / ATTRIBUTION.md)
- [ ] 취약점 분석 리포트
- [ ] 라이선스 상세 분석 리포트
- [ ] 소스코드 (LGPL/GPL 컴포넌트 해당분)

---

_본 문서는 ISO/IEC 18974 4.3.1 요구사항에 따라 작성되었습니다._
