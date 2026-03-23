---
sidebar_label: SBOM 산출물
sidebar_position: 4
---

# SBOM 산출물 Best Practice

[05 도구 챕터](/docs/05-tools/sbom-generation/index.md)에서 생성하는 SBOM 관련 산출물 예시입니다.
샘플 프로젝트(`java-vulnerable`)를 기준으로 작성된 실제 출력 예시를 확인할 수 있습니다.

---

## license-report.md

> **생성 agent**: `05-sbom-analyst` | **저장 경로**: `output/sbom/license-report.md`

---

리포트 유형: SBOM 라이선스 분석
생성일: YYYY-MM-DD
대상 프로젝트: your-project
사용 도구: syft

---

### 1. 요약

- 분석 대상 SBOM: `your-project.cdx.json` (CycloneDX 1.6)
- 소프트웨어 컴포넌트 총 **3개**
- Apache Log4j 2.14.1은 **Apache 2.0 (Permissive)** 으로 분류됨
- Copyleft 컴포넌트 **0개** (즉시 컴플라이언스 조치 불필요)

### 2. 컴포넌트별 라이선스 상세

| 컴포넌트 | 버전 | 그룹 | 라이선스 | 분류 |
|---------|------|------|---------|------|
| log4j-api | 2.14.1 | org.apache.logging.log4j | Apache-2.0 | Permissive |
| log4j-core | 2.14.1 | org.apache.logging.log4j | Apache-2.0 | Permissive |
| your-app | 1.0.0 | com.example | Proprietary | N/A |

### 3. 라이선스 분류 요약

| 분류 | 컴포넌트 수 |
|------|-----------|
| Permissive | 2 |
| Weak Copyleft | 0 |
| Strong Copyleft | 0 |
| Unknown | 0 |

### 4. 컴플라이언스 의무 요약

| 라이선스 | 의무사항 |
|---------|---------|
| Apache-2.0 | 저작권 표시 유지, NOTICE 파일 포함, 라이선스 사본 배포 |

*이 리포트는 ISO/IEC 5230 §3.3.2(라이선스 식별) 및 §3.4.1(컴플라이언스 산출물) 요구사항을 충족하기 위해 생성되었습니다.*

---

## copyleft-risk.md

> **생성 agent**: `05-sbom-analyst` | **저장 경로**: `output/sbom/copyleft-risk.md`

---

리포트 유형: Copyleft 위험도 분석
생성일: YYYY-MM-DD
대상 프로젝트: your-project

---

### 1. 요약

- **Strong Copyleft (GPL/AGPL) 컴포넌트: 0개**
- **Weak Copyleft (LGPL/MPL) 컴포넌트: 0개**
- 식별된 컴포넌트는 모두 **Apache-2.0 (Permissive)** 으로 Copyleft 위험 없음

### 2. Copyleft 위험 컴포넌트 목록

| 컴포넌트 | 버전 | 라이선스 | Copyleft 등급 | 위험도 | 조치 |
|---------|------|---------|-------------|------|------|
| log4j-api | 2.14.1 | Apache-2.0 | 없음 | 🟢 Low | 불필요 |
| log4j-core | 2.14.1 | Apache-2.0 | 없음 | 🟢 Low | 불필요 |

### 3. Copyleft 등급 기준

| 등급 | 해당 라이선스 | 배포 시 의무 |
|------|------------|-----------|
| Strong Copyleft | GPL-2.0, GPL-3.0, AGPL-3.0 | 전체 소스코드 공개 의무 |
| Weak Copyleft | LGPL-2.1, LGPL-3.0, MPL-2.0 | 해당 컴포넌트 수정본 소스코드 공개 |
| Permissive | Apache-2.0, MIT, BSD | 저작권 표시만 유지 |

*이 리포트는 ISO/IEC 5230 §3.3.2(라이선스 식별) 요구사항을 충족하기 위해 생성되었습니다.*

---

## sbom-management-plan.md

> **생성 agent**: `05-sbom-management` | **저장 경로**: `output/sbom/sbom-management-plan.md`

---

### 1. SBOM 생성 원칙

#### 생성 시점

- 기능 개발 완료 후 릴리즈 빌드 시점마다 SBOM 생성
- 의존성 변경(추가/삭제/버전 업데이트) 발생 시 즉시 재생성
- 정기 보안 점검(월 1회) 시 최신 SBOM 재생성 확인

#### 생성 도구

| 빌드 환경 | 도구 | 생성 포맷 |
|-----------|------|-----------|
| Java/Maven | `cyclonedx-maven-plugin` | CycloneDX JSON |
| Node.js | `@cyclonedx/cyclonedx-npm` | CycloneDX JSON |
| Python | `cyclonedx-bom` | CycloneDX JSON |

### 2. SBOM 갱신 절차

```
1. 기능 개발 완료 및 코드 프리즈
2. 의존성 목록 최종 확정
3. SBOM 자동 생성 (CI/CD 파이프라인)
4. 라이선스 검토 (copyleft 신규 포함 여부 확인)
5. 취약점 스캔
6. SBOM 파일 버전 태깅 및 저장
7. 납품처 제출 필요 시 sbom-sharing-template.md 첨부하여 전달
```

### 3. 공급망 모니터링

| 항목 | 주기 | 도구 |
|------|------|------|
| 신규 CVE 스캔 | 월 1회 (또는 릴리즈 시) | OSV-Scanner, Grype |
| 라이선스 변경 감지 | 릴리즈 시 | ort, scancode-toolkit |
| 의존성 업데이트 추적 | 지속 | Dependabot, Renovate |

### 4. 취약점 대응 기준

| 심각도 | 대응 기한 | 조치 |
|--------|-----------|------|
| Critical | 즉시 (24시간 내) | 패치 또는 대체 컴포넌트 적용 |
| High | 7일 내 | 패치 계획 수립 및 적용 |
| Medium | 30일 내 | 다음 릴리즈 시 반영 |
| Low | 90일 내 또는 차기 계획 | 리스크 수용 여부 검토 |

*ISO/IEC 18974 4.3.1(SBOM 관리), 4.3.2(공급망 취약점 모니터링) 준거*

---

## sbom-sharing-template.md

> **생성 agent**: `05-sbom-management` | **저장 경로**: `output/sbom/sbom-sharing-template.md`

---

수신: [ 납품처/고객명 ]
발신: [ 귀사 회사명 ]
문서 제목: SBOM (Software Bill of Materials) 제출 안내
작성일: [ YYYY-MM-DD ]

---

### 1. 제출 파일 정보

| 항목 | 내용 |
|------|------|
| 제품명 | [ 제품명 또는 소프트웨어명 ] |
| 버전 | [ v0.0.0 ] |
| SBOM 포맷 | CycloneDX 1.5 JSON |
| 파일명 | [ 예: myproduct-v1.0.0.cdx.json ] |

### 2. 포함 범위

| 항목 | 내용 |
|------|------|
| 포함 컴포넌트 | 직접 의존성 및 전이 의존성 전체 |
| 포함 정보 | 컴포넌트명, 버전, 라이선스, PURL |
| 제외 항목 | 빌드 전용 도구 (devDependencies 등) |

### 3. 라이선스 의무사항 이행 현황

| 라이선스 유형 | 포함 여부 | 이행 조치 |
|--------------|-----------|-----------|
| MIT, Apache-2.0, BSD | 포함 | 저작권 고지 포함 완료 |
| LGPL-2.1, LGPL-3.0 | [ 포함/미포함 ] | 동적 링크 방식 사용, 소스 제공 준비 |
| GPL-2.0, GPL-3.0 | [ 포함/미포함 ] | 소스코드 공개 의무 검토 완료 |

### 4. 연락처

| 역할 | 담당자 | 연락처 |
|------|--------|--------|
| SBOM 담당자 | [ 이름 ] | [ 이메일 ] |
| 보안 담당자 | [ 이름 ] | [ 이메일 ] |

*본 문서는 ISO/IEC 18974 4.3.1 요구사항에 따라 작성되었습니다.*
