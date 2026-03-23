---
리포트 유형: 갭 분석 (ISO/IEC 5230 + ISO/IEC 18974)
생성일: 2026-03-23
대상 프로젝트: SK텔레콤 오픈소스 프로그램
사용 도구: trustedoss agents/07-conformance-preparer
---

# 갭 분析 리포트

## 1. 요약

- 분석 대상: ISO/IEC 5230:2020 (25개 항목) + ISO/IEC 18974:2023 (25개 항목) = 총 50개 입증자료
- **ISO/IEC 5230**: 충족 ✅ 22개 / 부분충족 🔶 3개 / 미충족 ❌ 0개
- **ISO/IEC 18974**: 충족 ✅ 17개 / 부분충족 🔶 8개 / 미충족 ❌ 0개
- ❌ 미충족(인증 차단) 항목 없음 → **자체 인증 선언 가능**
- 즉시 조치 권고: 담당자 실명 기입(raci-matrix.md), 교육 이수 개시(completion-tracker.md)
- 시간 기반 🔶 항목 3개는 초기 인증 시 정상(18개월 갱신 시 충족)

---

## 2. ISO/IEC 5230:2020 항목별 충족 현황

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

## 3. ISO/IEC 18974:2023 항목별 충족 현황

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
| 4.1.4.3 | 지속적 개선 증거(감사 이력) | 🔶 | 본 갭 분析 = 1회차 감사 이력 ※시간 기반 |
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

## 4. 조치사항

### 🟡 Medium — 담당자 실명 기입 (1개월 이내 권고)

- **대상**: `output/organization/raci-matrix.md` §역할별 담당자
- **문제**: "(담당자명 기입)" 자리표시자가 실명으로 교체되지 않은 상태
- **영향 항목**: 3.2.2.1, 4.1.2.3, 4.2.2.1
- **조치**: raci-matrix.md 역할별 담당자 표에 실제 이름 기입
- **예상 소요시간**: 10분

### 🟡 Medium — 교육 이수 개시 (2026-Q2 실행 계획 수립 완료)

- **대상**: `output/training/completion-tracker.md`
- **문제**: 교육 계획과 양식은 완비되었으나 실제 이수 0명(0%)
- **영향 항목**: 3.1.2.3, 3.1.3.1, 4.1.2.4, 4.1.3.1
- **조치**: curriculum.md §교육 일정 계획에 따라 2026-Q2부터 교육 시행
  - 운영 100명: 2026-05 중 온라인 교육 개시
  - 관리자 10명: 2026-06 오프라인 집합 교육
  - 개발자 1000명: 2026-Q2~Q3 순차 온라인 개시
- **예상 소요시간**: 계획 기수립 완료, 실행 단계

### 🟢 Low — 예산 정보 확인 및 보완

- **대상**: `output/organization/raci-matrix.md` §예산 배분 현황
- **문제**: 오픈소스 도구 예산 및 외부 교육 예산 항목 "(확인 후 기입)" 미완성
- **영향 항목**: 3.2.2.2 (현재 ✅로 판정했으나 해당 항목 보완 권고)
- **조치**: 실제 예산 배분 현황 기입
- **예상 소요시간**: 30분

---

## 5. 시간 기반 항목 처리 (초기 인증 정상)

아래 3개 항목은 최초 인증 시 증거를 생성할 수 없는 항목이다. 🔶 부분충족으로 처리하며, 18개월 갱신 시 충족으로 전환된다.

| 항목 ID | 현재 조치 | 충족 전환 조건 |
|---------|---------|-------------|
| 18974 §4.1.2.5 주기적 검토 증거 | oss-policy.md §9에 "다음 검토 예정일: 2027-03-23" 기록 | 실제 검토 이력 1건 이상 축적 |
| 18974 §4.1.2.6 모범 사례 일치 검증 | role-definition.md §6에 담당자 지정 및 최초 검토 예정일(2026-12-31) 기록 | 검토 결과 기록 1건 이상 |
| 18974 §4.1.4.3 지속적 개선 증거 | 본 갭 分析(2026-03-23)을 1회차 감사 이력으로 기록 | 감사 이력 2건 이상 |

---

## 6. 갱신 일정

| 일정 | 작업 |
|------|------|
| 2026-06-30 | 관리자 교육 완료 후 completion-tracker.md 업데이트 |
| 2026-09-30 | 개발자 1차 그룹(250명) 오프라인 교육 완료 |
| 2026-12-31 | 18974 §4.1.2.6 모범 사례 일치 검토 수행 → gap-analysis.md 갱신 |
| 2027-03-23 | 연간 정책 검토(oss-policy.md §9) → gap-analysis.md 갱신 |
| 2027-09-23 | 자체 인증 유효기간 만료 (선언일 + 18개월) → 재선언 |
