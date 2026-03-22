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

*해당하는 항목에만 체크하세요.*

---

## 적용 범위
<!-- §3.1.4, §4.1.4 -->

이 선언은 아래 소프트웨어/제품 범위에 적용됩니다:

- **대상 제품/소프트웨어**: {제품명 또는 서비스명}
- **버전 범위**: {버전 X 이상 / 전체}
- **배포 방식**: {SaaS / 앱스토어 / 임베디드 / 내부용}
- **적용 제외**: {없음 / 구체적 제외 항목}

---

## ISO/IEC 5230 체크리스트 충족 확인

| 항목ID | 요구사항 | 충족 여부 | 주요 산출물 |
|--------|---------|---------|-----------|
| G1.1 | 오픈소스 정책 수립 및 문서화 | ✅ | output/policy/oss-policy.md |
| G1.3 | 오픈소스 담당자 및 조직 지정 | ✅ | output/organization/ |
| G1.4 | 교육 프로그램 수립 | ✅ | output/training/curriculum.md |
| G1.5 | 프로그램 범위 정의 | ✅ | output/policy/oss-policy.md |
| G1.6 | 라이선스 의무사항 검토 절차 | ✅ | output/process/usage-approval.md |
| G1.7 | 참여자 인식 기록 | ✅ | output/training/completion-tracker.md |
| G2.1 | 역할과 책임 (RACI) 수립 | ✅ | output/organization/raci-matrix.md |
| G2.2 | 외부 문의 수신 채널 운영 | ✅ | output/organization/role-definition.md |
| G2.3 | 인식 제고 프로그램 운영 | ✅ | output/training/ |
| G3L.1 | 라이선스 식별 및 분류 | ✅ | output/sbom/license-report.md |
| G3L.2 | 라이선스 의무사항 이행 | ✅ | output/process/distribution-checklist.md |
| G3L.3 | 컴플라이언스 산출물 생성 | ✅ | output/sbom/license-report.md |
| G3L.4 | 오픈소스 기여 정책 수립 | ✅ | output/policy/oss-policy.md |
| G3L.5 | 라이선스 의무사항 충족 확인 | ✅ | output/process/distribution-checklist.md |
| G3L.6 | 오픈소스 기여 프로세스 운영 | ✅ | output/policy/oss-policy.md |
| G3B.1 | SBOM 생성 | ✅ | output/sbom/*.cdx.json |
| G3B.2 | SBOM 관리 및 유지보수 | ✅ | output/sbom/sbom-management-plan.md |
| G4.1 | ISO/IEC 5230 자체 인증 선언 | ✅ | 이 문서 |
| G4.3 | 인증 유효기간 관리 (18개월) | ✅ | output/conformance/submission-guide.md |
| G4.4 | 정기 갭 분析 및 정책 갱신 | ✅ | output/conformance/gap-analysis.md |

---

## ISO/IEC 18974 체크리스트 충족 확인

| 항목ID | 요구사항 | 충족 여부 | 주요 산출물 |
|--------|---------|---------|-----------|
| G1.1 | 오픈소스 정책 수립 및 문서화 | ✅ | output/policy/oss-policy.md |
| G1.2 | 보안 보증 정책 검토 프로세스 | ✅ | output/policy/oss-policy.md |
| G1.3 | 오픈소스 담당자 및 조직 지정 | ✅ | output/organization/ |
| G1.4 | 교육 프로그램 수립 | ✅ | output/training/curriculum.md |
| G1.5 | 프로그램 범위 정의 | ✅ | output/policy/oss-policy.md |
| G1.7 | 참여자 인식 기록 | ✅ | output/training/completion-tracker.md |
| G2.1 | 역할과 책임 (RACI) 수립 | ✅ | output/organization/raci-matrix.md |
| G2.2 | 외부 문의 수신 채널 운영 | ✅ | output/organization/role-definition.md |
| G2.3 | 인식 제고 프로그램 운영 | ✅ | output/training/ |
| G3S.1 | 알려진 취약점 식별 (CVE 스캔) | ✅ | output/vulnerability/cve-report.md |
| G3S.2 | 취약점 추적 및 상태 관리 | ✅ | output/vulnerability/cve-report.md |
| G3S.3 | CVE 위험 점수 평가 (CVSS) | ✅ | output/vulnerability/cve-report.md |
| G3S.4 | 취약점 대응 및 패치 절차 | ✅ | output/vulnerability/remediation-plan.md |
| G3S.5 | 보안 산출물 배포 프로세스 | ✅ | output/sbom/sbom-sharing-template.md |
| G3S.6 | 보안 의무사항 충족 확인 | ✅ | output/vulnerability/remediation-plan.md |
| G3B.1 | SBOM 생성 | ✅ | output/sbom/*.cdx.json |
| G3B.2 | SBOM 관리 및 유지보수 | ✅ | output/sbom/sbom-management-plan.md |
| G3B.3 | SBOM 공유 (공급망 파트너) | ✅ | output/sbom/sbom-sharing-template.md |
| G3B.4 | 공급망 취약점 지속 모니터링 | ✅ | output/sbom/sbom-management-plan.md |
| G4.2 | ISO/IEC 18974 자체 인증 선언 | ✅ | 이 문서 |
| G4.3 | 인증 유효기간 관리 (18개월) | ✅ | output/conformance/submission-guide.md |
| G4.4 | 정기 갭 분析 및 정책 갱신 | ✅ | output/conformance/gap-analysis.md |
| G4.5 | 배포 소프트웨어 알려진 취약점 없음 확인 | ✅ | output/vulnerability/cve-report.md |

---

## 서명

본 선언은 위 표준의 모든 요구사항을 충족함을 확인합니다.

- **선언자**: {이름}, {직책}
- **선언일**: YYYY-MM-DD
- **다음 재확인 예정일**: YYYY-MM-DD
