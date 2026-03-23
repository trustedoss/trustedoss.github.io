---
리포트 유형: SBOM 라이선스 분석
생성일: 2026-03-23 07:11
대상 프로젝트: vulnerable-java-app
사용 도구: syft 1.42.3
---

# SBOM 라이선스 분석 리포트

## 1. 요약

- 분석 대상 SBOM: `java-vulnerable.cdx.json` (CycloneDX 1.6)
- 소프트웨어 컴포넌트 총 **3개** (파일 항목 제외)
- SBOM 내 라이선스 필드가 비어 있음 → 외부 정보 기반으로 라이선스 보완 분류
- Apache Log4j 2.14.1은 **Apache 2.0 (Permissive)** 으로 분류됨
- 내부 애플리케이션(`vulnerable-java-app`)은 라이선스 정보 없음 → **Unknown**
- Copyleft 컴포넌트 **0개** (즉시 컴플라이언스 조치 불필요)
- ⚠️ SBOM에 라이선스 정보가 누락되어 있어 도구 재실행 또는 수동 보완 권고

## 2. 컴포넌트별 라이선스 상세

| 컴포넌트 | 버전 | 그룹 | 라이선스 | 분류 | 출처 |
|---------|------|------|---------|------|------|
| log4j-api | 2.14.1 | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (보완) |
| log4j-core | 2.14.1 | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (보완) |
| vulnerable-java-app | 1.0.0 | com.example | Unknown | Unknown | SBOM 미기재 |

> **참고:** SBOM 생성 시 라이선스 정보가 포함되지 않았습니다.
> syft 재실행 시 `--source-name`, Maven Central 메타데이터 활성화 여부를 확인하거나
> `cdxgen` 도구를 병행 사용하여 라이선스 필드를 보완하는 것을 권장합니다.

## 3. 라이선스 분류 요약

| 분류 | 컴포넌트 수 | 컴포넌트 목록 |
|------|-----------|-------------|
| Permissive | 2 | log4j-api, log4j-core |
| Weak Copyleft | 0 | — |
| Strong Copyleft | 0 | — |
| Unknown | 1 | vulnerable-java-app |

## 4. 조치사항

### ⚪ Info — SBOM 라이선스 정보 보완

- **대상:** 전체 컴포넌트 (특히 `vulnerable-java-app`)
- **조치:** syft 또는 cdxgen 재실행 시 라이선스 메타데이터 활성화
  ```bash
  # syft: Maven POM 라이선스 정보 포함
  syft /path/to/project --output cyclonedx-json

  # cdxgen: 라이선스 정보 자동 수집
  cdxgen -t java /path/to/project -o sbom.cdx.json
  ```
- **예상 소요시간:** 30분

### ⚪ Info — 내부 애플리케이션 라이선스 명시

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

## 5. 컴플라이언스 의무 요약

| 라이선스 | 의무사항 |
|---------|---------|
| Apache-2.0 | 저작권 표시 유지, NOTICE 파일 포함, 라이선스 사본 배포 |
| Permissive 공통 | 2차 배포 시 원본 라이선스 텍스트 포함 |

> Apache-2.0은 소스코드 공개 의무가 없어 바이너리 배포에 친화적입니다.
> 배포 패키지에 `LICENSE`, `NOTICE` 파일이 포함되어 있는지 확인하십시오.

---

*이 리포트는 ISO/IEC 5230 §3.3.2(라이선스 식별) 및 §3.4.1(컴플라이언스 산출물) 요구사항을 충족하기 위해 생성되었습니다.*
