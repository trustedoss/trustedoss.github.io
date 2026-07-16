# 자체 인증 선언문

<!-- 5230 §3.6.1.1, 18974 §4.4.1.1 -->

---

## 선언

**회사명**: {회사명}
**담당자**: {이름}, {직책}
**선언일**: YYYY-MM-DD
**유효기간 만료일**: YYYY-MM-DD (선언일 + 18개월)
**재선언 예정일**: YYYY-MM-DD

---

## 인증 표준 선택

- [x] ISO/IEC 5230:2020 (OpenChain License Compliance)
- [x] ISO/IEC 18974:2023 (OpenChain Security Assurance)

_해당하는 항목에만 체크하세요._

---

## 적용 범위

<!-- §3.1.4, §4.1.4 -->

이 선언은 아래 소프트웨어/제품 범위에 적용됩니다:

- **대상 제품/소프트웨어**: {제품명 또는 서비스명}
- **버전 범위**: {버전 X 이상 / 전체}
- **배포 방식**: {SaaS / 앱스토어 / 임베디드 / 내부용}
- **적용 제외**: {없음 / 구체적 제외 항목}

---

## ISO/IEC 5230:2020 체크리스트 충족 확인

<!-- 표준별 입증자료 25개를 조항 ID 기준으로 확인한다. gap-analysis.md 와 같은 체계다.
     G항목(G1~G4) 지도는 docs/00-overview/checklist-mapping.md 가 정본이다. -->

아래 25개 입증자료의 충족 여부를 확인합니다. 부분충족(🔶)이 남아 있으면 충족 완료 후 선언하거나, 시간 기반 항목(18974 §4.1.2.5, §4.1.2.6, §4.1.4.3)만 계획 수립 상태로 선언합니다.

| 항목 ID | 내용                                  | 충족 여부 | 산출물                                                    |
| ------- | ------------------------------------- | :-------: | --------------------------------------------------------- |
| 3.1.1.1 | 문서화된 오픈소스 정책                |   ✅/🔶   | output/policy/oss-policy.md                               |
| 3.1.1.2 | 정책 전파 절차                        |   ✅/🔶   | oss-policy.md §7, training/curriculum.md                  |
| 3.1.2.1 | 역할과 책임 목록                      |   ✅/🔶   | organization/role-definition.md                           |
| 3.1.2.2 | 역할별 역량 기술 문서                 |   ✅/🔶   | role-definition.md §2                                     |
| 3.1.2.3 | 역량 평가 증거                        |   ✅/🔶   | training/completion-tracker.md                            |
| 3.1.3.1 | 참여자 인식 평가 증거                 |   ✅/🔶   | training/curriculum.md + completion-tracker.md            |
| 3.1.4.1 | 프로그램 적용 범위 문서               |   ✅/🔶   | oss-policy.md §1                                          |
| 3.1.5.1 | 라이선스 의무사항 검토 절차           |   ✅/🔶   | process/usage-approval.md §4, policy/license-allowlist.md |
| 3.2.1.1 | 외부 문의 공개 채널                   |   ✅/🔶   | role-definition.md §3                                     |
| 3.2.1.2 | 외부 문의 내부 대응 절차              |   ✅/🔶   | role-definition.md §3                                     |
| 3.2.2.1 | 역할 담당자 이름 문서                 |   ✅/🔶   | organization/raci-matrix.md (실명 기입 진행 중)           |
| 3.2.2.2 | 역할 배치 및 예산 확인                |   ✅/🔶   | raci-matrix.md §예산 배분 현황                            |
| 3.2.2.3 | 법률 자문 접근 방법                   |   ✅/🔶   | role-definition.md §4                                     |
| 3.2.2.4 | 내부 책임 할당 절차                   |   ✅/🔶   | raci-matrix.md §내부 책임 할당 절차                       |
| 3.2.2.5 | 미준수 사례 검토 및 수정 절차         |   ✅/🔶   | raci-matrix.md §미준수 사례 검토 절차                     |
| 3.3.1.1 | SBOM 관리 절차                        |   ✅/🔶   | sbom/sbom-management-plan.md                              |
| 3.3.1.2 | 컴포넌트 기록(SBOM 파일)              |   ✅/🔶   | sbom/[project].cdx.json                                   |
| 3.3.2.1 | 라이선스 사용 사례 처리 절차          |   ✅/🔶   | sbom/license-report.md, process/usage-approval.md         |
| 3.4.1.1 | 컴플라이언스 산출물 준비 및 배포 절차 |   ✅/🔶   | process/distribution-checklist.md                         |
| 3.4.1.2 | 컴플라이언스 산출물 보관 절차         |   ✅/🔶   | distribution-checklist.md §5                              |
| 3.5.1.1 | 오픈소스 기여 정책                    |   ✅/🔶   | oss-policy.md §5                                          |
| 3.5.1.2 | 오픈소스 기여 관리 절차               |   ✅/🔶   | oss-policy.md §5                                          |
| 3.5.1.3 | 기여 정책 인식 절차                   |   ✅/🔶   | oss-policy.md §7                                          |
| 3.6.1.1 | 모든 요구사항 충족 확인 문서          |   ✅/🔶   | conformance/gap-analysis.md                               |
| 3.6.2.1 | 18개월 이내 요구사항 충족 확인        |   ✅/🔶   | 본 문서(declaration-draft.md)                             |

---

## ISO/IEC 18974:2023 체크리스트 충족 확인

| 항목 ID | 내용                            | 충족 여부 | 산출물                                               |
| ------- | ------------------------------- | :-------: | ---------------------------------------------------- |
| 4.1.1.1 | 문서화된 보안 보증 정책         |   ✅/🔶   | oss-policy.md §4                                     |
| 4.1.1.2 | 정책 전파 절차                  |   ✅/🔶   | oss-policy.md §7, training/curriculum.md             |
| 4.1.2.1 | 역할과 책임 목록                |   ✅/🔶   | organization/role-definition.md §1                   |
| 4.1.2.2 | 역할별 역량 기술 문서           |   ✅/🔶   | role-definition.md §2                                |
| 4.1.2.3 | 참여자 목록 및 역할             |   ✅/🔶   | raci-matrix.md (실명 기입 진행 중)                   |
| 4.1.2.4 | 역량 평가 증거                  |   ✅/🔶   | training/completion-tracker.md                       |
| 4.1.2.5 | 주기적 검토 및 변경 증거        |   ✅/🔶   | oss-policy.md §9                                     |
| 4.1.2.6 | 내부 모범 사례 일치 검증 담당자 |   ✅/🔶   | role-definition.md §6                                |
| 4.1.3.1 | 참여자 인식 평가 증거           |   ✅/🔶   | training/curriculum.md + completion-tracker.md       |
| 4.1.4.1 | 프로그램 범위 문서              |   ✅/🔶   | oss-policy.md §1                                     |
| 4.1.4.2 | 성과 메트릭                     |   ✅/🔶   | oss-policy.md §3 (KPI 5개 항목)                      |
| 4.1.4.3 | 지속적 개선 증거(감사 이력)     |   ✅/🔶   | conformance/gap-analysis.md (1회차 감사 이력)        |
| 4.1.5.1 | 취약점 대응 표준 절차           |   ✅/🔶   | process/vulnerability-response.md                    |
| 4.2.1.1 | 외부 취약점 문의 공개 채널      |   ✅/🔶   | role-definition.md §3 (security@techunicorn.example) |
| 4.2.1.2 | 외부 문의 내부 대응 절차        |   ✅/🔶   | vulnerability-response.md §7                         |
| 4.2.2.1 | 역할 담당자 이름 문서           |   ✅/🔶   | raci-matrix.md (실명 기입 진행 중)                   |
| 4.2.2.2 | 역할 배치 및 예산 확인          |   ✅/🔶   | raci-matrix.md §예산 배분 현황                       |
| 4.2.2.3 | 취약점 해결 전문성 명시         |   ✅/🔶   | role-definition.md §5                                |
| 4.2.2.4 | 내부 책임 할당 절차             |   ✅/🔶   | raci-matrix.md §내부 책임 할당 절차                  |
| 4.3.1.1 | SBOM 수명주기 지속 기록 절차    |   ✅/🔶   | sbom/sbom-management-plan.md                         |
| 4.3.1.2 | 컴포넌트 기록(SBOM 파일)        |   ✅/🔶   | sbom/[project].cdx.json                              |
| 4.3.2.1 | 취약점 탐지 및 해결 절차        |   ✅/🔶   | vulnerability-response.md + remediation-plan.md      |
| 4.3.2.2 | 취약점 및 조치 기록             |   ✅/🔶   | vulnerability/cve-report.md + remediation-plan.md    |
| 4.4.1.1 | 모든 요구사항 충족 확인 문서    |   ✅/🔶   | conformance/gap-analysis.md                          |
| 4.4.2.1 | 18개월 이내 요구사항 충족 확인  |   ✅/🔶   | 본 문서(declaration-draft.md)                        |

---

## 서명

본 선언은 위 표준의 모든 요구사항을 충족함을 확인합니다.

- **선언자**: {이름}, {직책}
- **선언일**: YYYY-MM-DD
- **다음 재확인 예정일**: YYYY-MM-DD
