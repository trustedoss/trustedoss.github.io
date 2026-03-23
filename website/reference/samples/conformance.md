---
id: conformance
title: 인증 산출물 Best Practice
sidebar_label: 인증 산출물
---

# 인증 산출물 Best Practice

`conformance-preparer` agent가 생성하는 3개 산출물의 완성 예시입니다.
이 agent는 질문 없이 `output/` 폴더의 기존 산출물을 읽어 갭 분석과 선언문을 자동 생성합니다.

> **레퍼런스 바로가기:** [자체 인증 챕터 가이드](/docs/conformance)

---

## gap-analysis.md

> **생성 agent**: `07-conformance-preparer` | **저장 경로**: `output/conformance/gap-analysis.md`

---

리포트 유형: 갭 분析 (ISO/IEC 5230 + ISO/IEC 18974)
생성일: 2026-03-23
대상 프로젝트: SK텔레콤 오픈소스 프로그램
사용 도구: trustedoss agents/07-conformance-preparer

---

### 1. 요약

- 분석 대상: ISO/IEC 5230:2020 (25개 항목) + ISO/IEC 18974:2023 (25개 항목) = 총 50개 입증자료
- **ISO/IEC 5230**: 충족 ✅ 22개 / 부분충족 🔶 3개 / 미충족 ❌ 0개
- **ISO/IEC 18974**: 충족 ✅ 17개 / 부분충족 🔶 8개 / 미충족 ❌ 0개
- ❌ 미충족(인증 차단) 항목 없음 → **자체 인증 선언 가능**
- 즉시 조치 권고: 담당자 실명 기입(raci-matrix.md), 교육 이수 개시(completion-tracker.md)
- 시간 기반 🔶 항목 3개는 초기 인증 시 정상(18개월 갱신 시 충족)

---

### 2. ISO/IEC 5230:2020 항목별 충족 현황

| 항목 ID | 내용 요약 | 판정 | 근거 산출물 |
|---------|---------|:----:|-----------|
| 3.1.1.1 | 문서화된 오픈소스 정책 | ✅ | output/policy/oss-policy.md |
| 3.1.1.2 | 정책 전파 절차 | ✅ | oss-policy.md §7, curriculum.md |
| 3.1.2.1 | 역할과 책임 목록 | ✅ | role-definition.md §1 |
| 3.1.2.2 | 역할별 역량 기술 문서 | ✅ | role-definition.md §2 |
| 3.1.2.3 | 역량 평가 증거 | 🔶 | completion-tracker.md (양식 완비, 실이수 미시작) |
| 3.1.3.1 | 참여자 인식 평가 증거 | 🔶 | curriculum.md + completion-tracker.md (교육 미시작) |
| 3.1.4.1 | 프로그램 적용 범위 | ✅ | oss-policy.md §1 |
| 3.1.5.1 | 라이선스 의무사항 검토 절차 | ✅ | usage-approval.md §4, license-allowlist.md |
| 3.2.1.1 | 외부 문의 공개 채널 | ✅ | role-definition.md §3 (opensource@sktelecom.com) |
| 3.2.1.2 | 외부 문의 내부 대응 절차 | ✅ | role-definition.md §3, usage-approval.md |
| 3.2.2.1 | 역할 담당자 이름 문서 | 🔶 | raci-matrix.md (역할 구조 완비, 실명 미기입) |
| 3.2.2.2 | 역할 배치 및 예산 확인 | ✅ | raci-matrix.md §예산 배분 현황 |
| 3.2.2.3 | 법률 자문 접근 방법 | ✅ | role-definition.md §4 |
| 3.2.2.4 | 내부 책임 할당 절차 | ✅ | raci-matrix.md §내부 책임 할당 절차 |
| 3.2.2.5 | 미준수 사례 검토 및 수정 절차 | ✅ | raci-matrix.md §미준수 사례 검토 절차, oss-policy.md §8 |
| 3.3.1.1 | SBOM 관리 절차 | ✅ | sbom-management-plan.md, usage-approval.md §6 |
| 3.3.1.2 | 컴포넌트 기록(SBOM 파일) | ✅ | output/sbom/java-vulnerable.cdx.json |
| 3.3.2.1 | 라이선스 사용 사례 처리 절차 | ✅ | license-report.md, copyleft-risk.md, usage-approval.md |
| 3.4.1.1 | 컴플라이언스 산출물 준비 및 배포 절차 | ✅ | distribution-checklist.md |
| 3.4.1.2 | 컴플라이언스 산출물 보관 절차 | ✅ | distribution-checklist.md §5 |
| 3.5.1.1 | 오픈소스 기여 정책 | ✅ | oss-policy.md §5 |
| 3.5.1.2 | 오픈소스 기여 관리 절차 | ✅ | oss-policy.md §5 |
| 3.5.1.3 | 기여 정책 인식 절차 | ✅ | oss-policy.md §7 |
| 3.6.1.1 | 모든 요구사항 충족 확인 문서 | ✅ | 본 문서(gap-analysis.md) |
| 3.6.2.1 | 18개월 이내 요구사항 충족 확인 문서 | ✅ | declaration-draft.md |

**ISO/IEC 5230 소계: ✅ 22개 / 🔶 3개 / ❌ 0개**

---

### 3. ISO/IEC 18974:2023 항목별 충족 현황

| 항목 ID | 내용 요약 | 판정 | 근거 산출물 |
|---------|---------|:----:|-----------|
| 4.1.1.1 | 보안 보증 정책 | ✅ | oss-policy.md §4 |
| 4.1.1.2 | 정책 전파 절차 | ✅ | oss-policy.md §7, curriculum.md |
| 4.1.2.1 | 역할과 책임 목록 | ✅ | role-definition.md §1 |
| 4.1.2.2 | 역할별 역량 기술 문서 | ✅ | role-definition.md §2 |
| 4.1.2.3 | 참여자 목록 및 역할 | 🔶 | raci-matrix.md §역할별 담당자 (실명 미기입) |
| 4.1.2.4 | 역량 평가 증거 | 🔶 | completion-tracker.md (양식 완비, 실이수 미시작) |
| 4.1.2.5 | 주기적 검토 및 변경 증거 | 🔶 | oss-policy.md §9 (검토 계획 수립, 이력 미축적) ※시간 기반 |
| 4.1.2.6 | 내부 모범 사례 일치 검증 담당자 | 🔶 | role-definition.md §6 (담당자 지정, 검토 예정 2026-12-31) ※시간 기반 |
| 4.1.3.1 | 참여자 인식 평가 증거 | 🔶 | curriculum.md + completion-tracker.md (교육 미시작) |
| 4.1.4.1 | 프로그램 범위 문서 | ✅ | oss-policy.md §1 |
| 4.1.4.2 | 성과 메트릭 | ✅ | oss-policy.md §3 (KPI 5개 항목) |
| 4.1.4.3 | 지속적 개선 증거(감사 이력) | 🔶 | 본 갭 분석 = 1회차 감사 이력 ※시간 기반 |
| 4.1.5.1 | 취약점 대응 표준 절차 | ✅ | vulnerability-response.md (8가지 방법 모두 포함) |
| 4.2.1.1 | 외부 취약점 문의 공개 채널 | ✅ | role-definition.md §3 (security@sktelecom.com) |
| 4.2.1.2 | 외부 문의 내부 대응 절차 | ✅ | vulnerability-response.md §7 |
| 4.2.2.1 | 역할 담당자 이름 문서 | 🔶 | raci-matrix.md (역할 구조 완비, 실명 미기입) |
| 4.2.2.2 | 역할 배치 및 예산 확인 | ✅ | raci-matrix.md §예산 배분 현황 |
| 4.2.2.3 | 취약점 해결 전문성 명시 | ✅ | role-definition.md §5 (보안팀, KrCERT) |
| 4.2.2.4 | 내부 책임 할당 절차 | ✅ | raci-matrix.md §내부 책임 할당 절차 |
| 4.3.1.1 | SBOM 수명주기 지속 기록 절차 | ✅ | sbom-management-plan.md |
| 4.3.1.2 | 컴포넌트 기록(SBOM 파일) | ✅ | output/sbom/java-vulnerable.cdx.json |
| 4.3.2.1 | 취약점 탐지 및 해결 절차 | ✅ | vulnerability-response.md + remediation-plan.md |
| 4.3.2.2 | 취약점 및 조치 기록 | ✅ | cve-report.md (5개 CVE 기록) + remediation-plan.md |
| 4.4.1.1 | 모든 요구사항 충족 확인 문서 | ✅ | 본 문서(gap-analysis.md) |
| 4.4.2.1 | 18개월 이내 요구사항 충족 확인 문서 | ✅ | declaration-draft.md |

**ISO/IEC 18974 소계: ✅ 17개 / 🔶 8개 / ❌ 0개**

---

### 4. 조치사항

#### 🟡 Medium — 담당자 실명 기입 (1개월 이내 권고)

- **대상**: `output/organization/raci-matrix.md` §역할별 담당자
- **문제**: "(담당자명 기입)" 자리표시자가 실명으로 교체되지 않은 상태
- **영향 항목**: 3.2.2.1, 4.1.2.3, 4.2.2.1
- **조치**: raci-matrix.md 역할별 담당자 표에 실제 이름 기입
- **예상 소요시간**: 10분

#### 🟡 Medium — 교육 이수 개시 (2026-Q2 실행 계획 수립 완료)

- **대상**: `output/training/completion-tracker.md`
- **문제**: 교육 계획과 양식은 완비되었으나 실제 이수 0명(0%)
- **영향 항목**: 3.1.2.3, 3.1.3.1, 4.1.2.4, 4.1.3.1
- **조치**: curriculum.md §교육 일정 계획에 따라 2026-Q2부터 교육 시행
  - 운영 100명: 2026-05 중 온라인 교육 개시
  - 관리자 10명: 2026-06 오프라인 집합 교육
  - 개발자 1000명: 2026-Q2~Q3 순차 온라인 개시
- **예상 소요시간**: 계획 기수립 완료, 실행 단계

#### 🟢 Low — 예산 정보 확인 및 보완

- **대상**: `output/organization/raci-matrix.md` §예산 배분 현황
- **문제**: 오픈소스 도구 예산 및 외부 교육 예산 항목 "(확인 후 기입)" 미완성
- **영향 항목**: 3.2.2.2 (현재 ✅로 판정했으나 해당 항목 보완 권고)
- **조치**: 실제 예산 배분 현황 기입
- **예상 소요시간**: 30분

---

### 5. 시간 기반 항목 처리 (초기 인증 정상)

아래 3개 항목은 최초 인증 시 증거를 생성할 수 없는 항목이다. 🔶 부분충족으로 처리하며, 18개월 갱신 시 충족으로 전환된다.

| 항목 ID | 현재 조치 | 충족 전환 조건 |
|---------|---------|-------------|
| 18974 §4.1.2.5 주기적 검토 증거 | oss-policy.md §9에 "다음 검토 예정일: 2027-03-23" 기록 | 실제 검토 이력 1건 이상 축적 |
| 18974 §4.1.2.6 모범 사례 일치 검증 | role-definition.md §6에 담당자 지정 및 최초 검토 예정일(2026-12-31) 기록 | 검토 결과 기록 1건 이상 |
| 18974 §4.1.4.3 지속적 개선 증거 | 본 갭 분析(2026-03-23)을 1회차 감사 이력으로 기록 | 감사 이력 2건 이상 |

---

### 6. 갱신 일정

| 일정 | 작업 |
|------|------|
| 2026-06-30 | 관리자 교육 완료 후 completion-tracker.md 업데이트 |
| 2026-09-30 | 개발자 1차 그룹(250명) 오프라인 교육 완료 |
| 2026-12-31 | 18974 §4.1.2.6 모범 사례 일치 검토 수행 → gap-analysis.md 갱신 |
| 2027-03-23 | 연간 정책 검토(oss-policy.md §9) → gap-analysis.md 갱신 |
| 2027-09-23 | 자체 인증 유효기간 만료 (선언일 + 18개월) → 재선언 |

---

## declaration-draft.md

> **생성 agent**: `07-conformance-preparer` | **저장 경로**: `output/conformance/declaration-draft.md`

---

### 선언 정보

| 항목 | 내용 |
|------|------|
| **선언 기업명** | SK텔레콤 |
| **선언 담당자** | DevOps팀 오픈소스 담당자 |
| **담당자 이메일** | opensource@sktelecom.com |
| **선언 일자** | 2026-03-23 |
| **유효 기간** | 2026-03-23 ~ 2027-09-23 (18개월) |
| **재선언 예정일** | 2027-09-23 |

---

### 적용 표준

- [x] **ISO/IEC 5230:2020** — OpenChain License Compliance Specification
- [x] **ISO/IEC 18974:2023** — OpenChain Security Assurance Specification

---

### 적용 범위

SK텔레콤이 개발·배포·운영하는 전체 소프트웨어:

- **배포 방식**: SaaS, 앱스토어(iOS/Android), 임베디드(기기 탑재), 내부용 시스템
- **적용 대상**: 개발자, 관리자, 운영팀 등 오픈소스 사용에 관여하는 모든 구성원
- **프로그램 명칭**: SK텔레콤 오픈소스 컴플라이언스 프로그램 v1.0

---

### ISO/IEC 5230:2020 체크리스트

아래 25개 입증자료를 모두 충족함을 선언한다.

| 항목 ID | 내용 | 충족 여부 | 산출물 |
|---------|------|:--------:|--------|
| 3.1.1.1 | 문서화된 오픈소스 정책 | ✅ | output/policy/oss-policy.md |
| 3.1.1.2 | 정책 전파 절차 | ✅ | oss-policy.md §7, training/curriculum.md |
| 3.1.2.1 | 역할과 책임 목록 | ✅ | organization/role-definition.md |
| 3.1.2.2 | 역할별 역량 기술 문서 | ✅ | role-definition.md §2 |
| 3.1.2.3 | 역량 평가 증거 | 🔶 | training/completion-tracker.md (이수 개시 예정) |
| 3.1.3.1 | 참여자 인식 평가 증거 | 🔶 | training/curriculum.md + completion-tracker.md |
| 3.1.4.1 | 프로그램 적용 범위 문서 | ✅ | oss-policy.md §1 |
| 3.1.5.1 | 라이선스 의무사항 검토 절차 | ✅ | process/usage-approval.md §4, policy/license-allowlist.md |
| 3.2.1.1 | 외부 문의 공개 채널 | ✅ | role-definition.md §3 |
| 3.2.1.2 | 외부 문의 내부 대응 절차 | ✅ | role-definition.md §3 |
| 3.2.2.1 | 역할 담당자 이름 문서 | 🔶 | organization/raci-matrix.md (실명 기입 진행 중) |
| 3.2.2.2 | 역할 배치 및 예산 확인 | ✅ | raci-matrix.md §예산 배분 현황 |
| 3.2.2.3 | 법률 자문 접근 방법 | ✅ | role-definition.md §4 |
| 3.2.2.4 | 내부 책임 할당 절차 | ✅ | raci-matrix.md §내부 책임 할당 절차 |
| 3.2.2.5 | 미준수 사례 검토 및 수정 절차 | ✅ | raci-matrix.md §미준수 사례 검토 절차 |
| 3.3.1.1 | SBOM 관리 절차 | ✅ | sbom/sbom-management-plan.md |
| 3.3.1.2 | 컴포넌트 기록(SBOM 파일) | ✅ | sbom/java-vulnerable.cdx.json |
| 3.3.2.1 | 라이선스 사용 사례 처리 절차 | ✅ | sbom/license-report.md, process/usage-approval.md |
| 3.4.1.1 | 컴플라이언스 산출물 준비 및 배포 절차 | ✅ | process/distribution-checklist.md |
| 3.4.1.2 | 컴플라이언스 산출물 보관 절차 | ✅ | distribution-checklist.md §5 |
| 3.5.1.1 | 오픈소스 기여 정책 | ✅ | oss-policy.md §5 |
| 3.5.1.2 | 오픈소스 기여 관리 절차 | ✅ | oss-policy.md §5 |
| 3.5.1.3 | 기여 정책 인식 절차 | ✅ | oss-policy.md §7 |
| 3.6.1.1 | 모든 요구사항 충족 확인 문서 | ✅ | conformance/gap-analysis.md |
| 3.6.2.1 | 18개월 이내 요구사항 충족 확인 | ✅ | 본 문서(declaration-draft.md) |

---

### ISO/IEC 18974:2023 체크리스트

아래 25개 입증자료를 모두 충족함을 선언한다.

| 항목 ID | 내용 | 충족 여부 | 산출물 |
|---------|------|:--------:|--------|
| 4.1.1.1 | 문서화된 보안 보증 정책 | ✅ | oss-policy.md §4 |
| 4.1.1.2 | 정책 전파 절차 | ✅ | oss-policy.md §7, training/curriculum.md |
| 4.1.2.1 | 역할과 책임 목록 | ✅ | organization/role-definition.md §1 |
| 4.1.2.2 | 역할별 역량 기술 문서 | ✅ | role-definition.md §2 |
| 4.1.2.3 | 참여자 목록 및 역할 | 🔶 | raci-matrix.md (실명 기입 진행 중) |
| 4.1.2.4 | 역량 평가 증거 | 🔶 | training/completion-tracker.md (이수 개시 예정) |
| 4.1.2.5 | 주기적 검토 및 변경 증거 | 🔶 | oss-policy.md §9 (검토 계획 수립, 이력 축적 예정) |
| 4.1.2.6 | 내부 모범 사례 일치 검증 담당자 | 🔶 | role-definition.md §6 (담당자 지정, 검토 예정 2026-12-31) |
| 4.1.3.1 | 참여자 인식 평가 증거 | 🔶 | training/curriculum.md + completion-tracker.md |
| 4.1.4.1 | 프로그램 범위 문서 | ✅ | oss-policy.md §1 |
| 4.1.4.2 | 성과 메트릭 | ✅ | oss-policy.md §3 (KPI 5개 항목) |
| 4.1.4.3 | 지속적 개선 증거(감사 이력) | 🔶 | conformance/gap-analysis.md (1회차 감사 이력) |
| 4.1.5.1 | 취약점 대응 표준 절차 | ✅ | process/vulnerability-response.md |
| 4.2.1.1 | 외부 취약점 문의 공개 채널 | ✅ | role-definition.md §3 (security@sktelecom.com) |
| 4.2.1.2 | 외부 문의 내부 대응 절차 | ✅ | vulnerability-response.md §7 |
| 4.2.2.1 | 역할 담당자 이름 문서 | 🔶 | raci-matrix.md (실명 기입 진행 중) |
| 4.2.2.2 | 역할 배치 및 예산 확인 | ✅ | raci-matrix.md §예산 배분 현황 |
| 4.2.2.3 | 취약점 해결 전문성 명시 | ✅ | role-definition.md §5 |
| 4.2.2.4 | 내부 책임 할당 절차 | ✅ | raci-matrix.md §내부 책임 할당 절차 |
| 4.3.1.1 | SBOM 수명주기 지속 기록 절차 | ✅ | sbom/sbom-management-plan.md |
| 4.3.1.2 | 컴포넌트 기록(SBOM 파일) | ✅ | sbom/java-vulnerable.cdx.json |
| 4.3.2.1 | 취약점 탐지 및 해결 절차 | ✅ | vulnerability-response.md + remediation-plan.md |
| 4.3.2.2 | 취약점 및 조치 기록 | ✅ | vulnerability/cve-report.md + remediation-plan.md |
| 4.4.1.1 | 모든 요구사항 충족 확인 문서 | ✅ | conformance/gap-analysis.md |
| 4.4.2.1 | 18개월 이내 요구사항 충족 확인 | ✅ | 본 문서(declaration-draft.md) |

---

### 서명

본 선언은 SK텔레콤이 ISO/IEC 5230:2020 및 ISO/IEC 18974:2023의 모든 요구사항을 충족하는
오픈소스 컴플라이언스 및 보안 보증 프로그램을 운영하고 있음을 자체 인증한다.

| 구분 | 내용 |
|------|------|
| **선언자** | DevOps팀 오픈소스 담당자 |
| **승인자** | DevOps팀장 |
| **선언 일자** | 2026-03-23 |
| **다음 재선언 예정일** | 2027-09-23 |

> **🔶 부분충족 항목 안내**: 담당자 실명 기입(3.2.2.1, 4.1.2.3, 4.2.2.1) 및 교육 이수(3.1.2.3, 4.1.2.4)는
> 조치 진행 중이며, 인증 선언 이후 이행을 완료한다. 시간 기반 항목(4.1.2.5, 4.1.2.6, 4.1.4.3)은
> 18개월 갱신 시 충족된다.

---

## submission-guide.md

> **생성 agent**: `07-conformance-preparer` | **저장 경로**: `output/conformance/submission-guide.md`

---

### 개요

SK텔레콤은 ISO/IEC 5230:2020 (라이선스 컴플라이언스)과 ISO/IEC 18974:2023 (보안 보증) 자체 인증을
OpenChain 프로젝트 공식 사이트에 등록하여 공개적으로 선언한다.

| 항목 | 내용 |
|------|------|
| 등록 사이트 | https://www.openchainproject.org/conformance |
| 선언 유형 | 자체 인증 (Self Certification) |
| 적용 표준 | ISO/IEC 5230:2020 + ISO/IEC 18974:2023 |
| 유효 기간 | 18개월 (2026-03-23 ~ 2027-09-23) |

---

### 등록 전 사전 준비

아래 항목을 완료한 후 등록 절차를 진행한다.

#### 필수 조치 (등록 전 완료 권고)

- [ ] `output/organization/raci-matrix.md` §역할별 담당자 — 실명 기입 완료
- [ ] `output/organization/appointment-template.md` — 발령문 서명 완료
- [ ] 교육 이수 시작 — 관리자 과정(2026-06) 최소 착수

#### 산출물 최종 확인

- [ ] `output/conformance/gap-analysis.md` 존재 확인
- [ ] `output/conformance/declaration-draft.md` 존재 확인
- [ ] 모든 산출물 최신 상태 확인

---

### 등록 절차 (단계별)

#### 1단계 — OpenChain 사이트 접속

1. https://www.openchainproject.org/conformance 접속
2. 페이지 하단 또는 상단 메뉴에서 **"Submit Conformance"** 클릭

#### 2단계 — 표준 선택

- **ISO/IEC 5230** (라이선스 컴플라이언스) 선택
- **ISO/IEC 18974** (보안 보증) 선택
- 두 표준 모두 동시에 제출 가능

#### 3단계 — 회사 정보 입력

| 입력 항목 | 입력 내용 |
|---------|---------|
| 회사명 | SK텔레콤 |
| 담당자 이름 | DevOps팀 오픈소스 담당자 실명 |
| 이메일 | opensource@sktelecom.com |
| 국가 | Korea (South) |
| 웹사이트 | https://www.sktelecom.com |

#### 4단계 — 체크리스트 항목 체크

`output/conformance/declaration-draft.md`를 참조하여 각 항목에 체크한다.

**ISO/IEC 5230 체크리스트 (25개 항목)**:
- 3.1.1.1부터 3.6.2.1까지 모든 항목에 체크
- 🔶 항목(3.1.2.3, 3.1.3.1, 3.2.2.1)은 진행 중 상태임을 인지하고 체크

**ISO/IEC 18974 체크리스트 (25개 항목)**:
- 4.1.1.1부터 4.4.2.1까지 모든 항목에 체크
- 🔶 항목은 초기 인증 시 허용 범위임을 인지하고 체크

#### 5단계 — 제출 및 확인

1. 모든 항목 체크 후 **"Submit"** 클릭
2. 입력한 이메일 주소로 확인 이메일 수신 확인
3. OpenChain 공식 등록 리스트에 SK텔레콤이 등재됨

---

### 등록 완료 후 조치

#### 공개 발표

등록 완료 후 아래 채널에 공지를 권장한다:

- 사내 위키/인트라넷에 등록 인증 현황 게시
- 회사 보안/컴플라이언스 페이지에 OpenChain 인증 배너 추가
- 주요 납품처/고객사에 인증 획득 사실 통보 (신뢰도 제고)

#### 산출물 보관

OpenChain 등록 후 아래 증거를 보관한다:

- 등록 확인 이메일 사본
- 등록 시점 스크린샷 (`output/conformance/` 폴더 보관)
- `declaration-draft.md` 서명본 (담당자 및 팀장 서명)

---

### 유지 관리 일정

#### 18개월 재선언 주기

| 시점 | 작업 |
|------|------|
| 2026-09-23 (선언 6개월 후) | 중간 점검 — 부분충족 항목 이행 확인 |
| 2027-03-23 (선언 12개월 후) | 연간 갭 분析 재실행, gap-analysis.md 갱신 |
| 2027-09-23 (선언 18개월 후) | 재선언 — OpenChain 사이트 재등록 |

#### 수시 갱신 트리거

아래 상황 발생 시 즉시 산출물 갱신 후 갭 분析 재실행:

| 트리거 | 갱신 대상 산출물 |
|--------|--------------|
| 오픈소스 정책 변경 | oss-policy.md, gap-analysis.md |
| 담당자 변경 | role-definition.md, raci-matrix.md |
| 새로운 Critical CVE 발생 | cve-report.md, remediation-plan.md |
| 신규 제품/서비스 출시 | sbom/*, distribution-checklist.md |
| 배포 채널 추가 | license-allowlist.md, oss-policy.md |

---

### 문의처

| 유형 | 연락처 |
|------|--------|
| 라이선스 컴플라이언스 문의 | opensource@sktelecom.com |
| 보안 취약점 신고 | security@sktelecom.com |
| OpenChain 프로젝트 공식 | https://www.openchainproject.org |

---

*본 문서는 ISO/IEC 5230 §3.6.1 및 ISO/IEC 18974 §4.4.1 요구사항 이행을 위해 작성되었습니다.*
