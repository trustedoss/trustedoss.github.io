---
id: conformance
title: 인증 산출물 Best Practice
sidebar_label: 인증 산출물
---

# 인증 산출물 Best Practice

`conformance-preparer` agent가 생성하는 3개 산출물의 완성 예시입니다.
이 agent는 질문 없이 `output/` 폴더의 기존 산출물을 읽어 갭 분석과 선언문을 자동 생성합니다.

> **레퍼런스 바로가기:** [자체 인증 챕터 가이드](/docs/07-conformance)

---

## gap-analysis.md 완성 예시

모든 앞선 챕터를 완료한 상태의 갭 분석 리포트입니다. 항목별 충족 여부와 증거 파일을 확인하세요.

```markdown
# OpenChain 자체 인증 갭 분석

**회사명**: (주)테크스타트
**분석일**: 2026-03-20
**담당자**: 박서영

## ISO/IEC 5230 갭 분석

| 항목 ID | 섹션 | 요구사항 | 상태 | 증거 파일 |
|---------|------|---------|------|---------|
| G1.1 | 3.1.1 | 오픈소스 정책 문서화 | ✅ 충족 | output/policy/oss-policy.md |
| G1.3 | 3.1.2 | 담당자 및 역할 지정 | ✅ 충족 | output/organization/role-definition.md |
| G1.4 | 3.1.2 | 교육 프로그램 운영 | ✅ 충족 | output/training/curriculum.md |
| G1.5 | 3.1.4 | 프로그램 범위 정의 | ✅ 충족 | output/policy/oss-policy.md §1 |
| G1.6 | 3.1.5 | 라이선스 검토 절차 | ✅ 충족 | output/process/usage-approval.md |
| G2.1 | 3.2.2 | 역할·책임 RACI | ✅ 충족 | output/organization/raci-matrix.md |
| G2.2 | 3.2.1 | 외부 문의 수신 채널 | ✅ 충족 | output/organization/role-definition.md §3 |
| G2.3 | 3.1.3 | 인식 제고 프로그램 | ✅ 충족 | output/training/completion-tracker.md |
| G3L.1 | 3.3.1 | BOM 생성 | ✅ 충족 | output/sbom/[project].cdx.json |
| G3L.2 | 3.3.2 | 컴플라이언스 산출물 준비 | ✅ 충족 | output/process/distribution-checklist.md |
| G3L.3 | 3.4.1 | 컴플라이언스 산출물 관리 | ✅ 충족 | output/process/distribution-checklist.md |
| G3L.4 | 3.5.1 | 오픈소스 기여 정책 | ✅ 충족 | output/policy/oss-policy.md §5 |
| G4.1 | 3.6.1 | 자체 인증 선언 | 🔲 미충족 | 이 단계에서 생성 예정 |
| G4.2 | 3.6.2 | 인증 유지 절차 | ✅ 충족 | output/policy/oss-policy.md §5 |

## ISO/IEC 18974 갭 분석

| 항목 ID | 섹션 | 요구사항 | 상태 | 증거 파일 |
|---------|------|---------|------|---------|
| G1.1 | 4.1.1 | 보안 보증 정책 문서화 | ✅ 충족 | output/policy/oss-policy.md §4 |
| G1.3 | 4.1.2 | 보안 담당자 지정 | ✅ 충족 | output/organization/role-definition.md |
| G1.4 | 4.1.2 | 보안 교육 프로그램 | ✅ 충족 | output/training/curriculum.md |
| G3S.1 | 4.3.1 | CVE 식별 방법 | ✅ 충족 | output/vulnerability/cve-report.md |
| G3S.2 | 4.3.2 | CVE 추적 방법 | ✅ 충족 | output/vulnerability/cve-report.md |
| G3S.3 | 4.3.3 | CVE 대응 절차 | ✅ 충족 | output/process/vulnerability-response.md |
| G3S.4 | 4.3.4 | 취약점 공개 정책 | ✅ 충족 | output/process/vulnerability-response.md §공개 정책 |
| G3B.1 | 4.3.1 | SBOM 존재 | ✅ 충족 | output/sbom/[project].cdx.json |
| G3B.2 | 4.3.2 | SBOM 관리 계획 | ✅ 충족 | output/sbom/sbom-management-plan.md |
| G4.1 | 4.4.1 | 자체 인증 선언 | 🔲 미충족 | 이 단계에서 생성 예정 |

## 요약

| 구분 | 전체 항목 | 충족 | 미충족 | 충족률 |
|------|---------|------|--------|--------|
| ISO/IEC 5230 | 14항목 | 13 | 1 | 93% |
| ISO/IEC 18974 | 10항목 | 9 | 1 | 90% |

**미충족 항목 조치 계획:**
- G4.1: 아래 declaration-draft.md 작성 및 OpenChain 사이트 등록으로 충족
```

---

## declaration-draft.md 완성 예시

```markdown
# OpenChain 자체 인증 선언문

## ISO/IEC 5230 자체 인증 선언

**(주)테크스타트**는 2026년 3월 20일을 기준으로 ISO/IEC 5230:2023 (OpenChain License Compliance)의 모든 요구사항을 충족함을 선언합니다.

### 인증 범위

본 선언은 (주)테크스타트의 SaaS 플랫폼 및 모바일 애플리케이션 개발·운영에 사용되는 오픈소스 소프트웨어 관리 프로그램에 적용됩니다.

### 충족 근거

| 요구사항 | 충족 방법 | 증거 |
|---------|---------|------|
| 정책 문서화 | 오픈소스 정책 수립 및 전 임직원 공지 | output/policy/oss-policy.md |
| 담당자 지정 | 오픈소스 담당자(박서영) 공식 임명 | output/organization/appointment-template.md |
| 교육 프로그램 | 직군별 커리큘럼 및 이수 추적 | output/training/ |
| BOM 관리 | syft 기반 SBOM 생성 및 정기 갱신 | output/sbom/ |
| 컴플라이언스 절차 | 배포 전 체크리스트 운영 | output/process/ |

### 서명

- **선언자**: 박서영 (오픈소스 담당자)
- **승인자**: 김철민 (CTO)
- **선언일**: 2026-03-20
- **다음 검토일**: 2027-03-20

---

## ISO/IEC 18974 자체 인증 선언

**(주)테크스타트**는 2026년 3월 20일을 기준으로 ISO/IEC 18974:2023 (OpenChain Security Assurance)의 모든 요구사항을 충족함을 선언합니다.

### 인증 범위

ISO/IEC 5230 인증 범위와 동일. 보안 취약점 관리 프로세스 포함.

### 서명

- **선언자**: 박서영 (오픈소스 담당자), 정다은 (보안 담당)
- **승인자**: 김철민 (CTO)
- **선언일**: 2026-03-20
```

---

## submission-guide.md 완성 예시

```markdown
# OpenChain 자체 인증 등록 가이드

## 등록 방법

1. OpenChain 공식 사이트 접속: https://www.openchainproject.org/conformance
2. "Register Conformance" 버튼 클릭
3. 회사명, 담당자 정보, 인증 범위 입력
4. ISO/IEC 5230 및 18974 체크리스트 항목별 충족 여부 선택
5. 제출 완료 → 인증 로고 사용 자격 획득

## 등록 완료 후

- OpenChain 인증 기업 목록에 등재됩니다.
- 웹사이트·제품에 OpenChain 로고 사용 가능합니다.
- 공급망 파트너에게 컴플라이언스 수준을 공식으로 알릴 수 있습니다.

## 인증 유지 관리

- 인증은 만료일 없음 (자체 갱신 선언 방식)
- 정책/프로세스 중대 변경 시 재선언 권장
- 연 1회 갭 분석 재실시 권장
```
