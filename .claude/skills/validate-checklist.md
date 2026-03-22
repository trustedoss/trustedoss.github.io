# Skill: 체크리스트 검증 (validate-checklist)

## 적용 대상
agents/07-conformance-preparer
agents/CLAUDE.md (마스터 agent)

## output/ 스캔 방법
아래 순서로 output/ 하위 폴더와 파일을 확인한다.

### 조직 (G1.3, G2.1, G2.2)
1. output/organization/role-definition.md — 역할·책임·외부 문의 채널 (5230 §3.1.2.1, 18974 §4.1.2.1)
2. output/organization/raci-matrix.md — RACI 매트릭스 (5230 §3.2.2.1, 18974 §4.2.2.1)

### 정책 (G1.1, G1.2, G1.5, G3L.4)
3. output/policy/oss-policy.md — 오픈소스 정책 (5230 §3.1.1.1, 18974 §4.1.1.1)
4. output/policy/license-allowlist.md — 허용 라이선스 목록 (5230 §3.1.5.1)

### 프로세스 (G1.6, G3L.2, G3L.5)
5. output/process/usage-approval.md — 오픈소스 사용 승인·라이선스 의무 검토 절차 (5230 §3.1.5.1, §3.3.1.1)
6. output/process/distribution-checklist.md — 배포 전 체크리스트·컴플라이언스 산출물 절차 (5230 §3.4.1.1, §3.4.1.2)
7. output/process/vulnerability-response.md — 취약점 대응 절차·외부 문의 대응 (18974 §4.1.5.1, §4.2.1.2)

### SBOM (G3B.1, G3B.2, G3L.1, G3L.3)
8. output/sbom/*.cdx.json — SBOM 파일 (5230 §3.3.1.2, 18974 §4.3.1.2)
9. output/sbom/license-report.md — 라이선스 분석·컴플라이언스 산출물 (5230 §3.4.1.1, §3.3.2.1)
10. output/sbom/copyleft-risk.md — Copyleft 위험 분석 (5230 §3.3.2.1)
11. output/sbom/sbom-management-plan.md — SBOM 관리·모니터링 계획 (5230 §3.3.1.1, 18974 §4.3.1.1)
12. output/sbom/sbom-sharing-template.md — 공급망 SBOM 공유 절차 (18974 §4.3.1.1)

### 취약점 (G3S.1~G3S.4)
13. output/vulnerability/cve-report.md — 취약점 분석 리포트 (18974 §4.3.2.1, §4.3.2.2)
14. output/vulnerability/remediation-plan.md — 취약점 대응·패치 계획 (18974 §4.1.5.1, §4.3.2.1)

### 교육 (G1.4, G1.7, G2.3)
15. output/training/curriculum.md — 교육 커리큘럼 (5230 §3.1.1.2, 18974 §4.1.1.2)
16. output/training/completion-tracker.md — 이수 추적·역량 평가 증거 (5230 §3.1.2.3, 18974 §4.1.2.4)

### 인증 (G4.1~G4.5)
17. output/conformance/gap-analysis.md — 갭 분석 리포트 (5230 §3.6.2.1, 18974 §4.4.2.1)

## 충족 판정 기준
- 충족: 파일 존재 + 필수 섹션 포함
- 부분충족: 파일 존재 + 일부 섹션 누락
- 미충족: 파일 없음

## 미충족 시 안내 메시지 형식
> [미충족] {항목명}
> 이동: docs/{챕터명} 또는 agents/{agent명}
> 예상 소요시간: {시간}

## 시간 기반 항목 처리 (초기 인증 시 부분충족 허용)

아래 3개 항목은 처음 인증 시점에 증거를 생성할 수 없다. 부분충족(🔶)으로 처리하고 18개월 후 갱신 시 충족한다.

| 입증자료 ID | 내용 | 처리 방법 |
|-----------|------|---------|
| 18974 §4.1.2.5 | 주기적 검토 및 프로세스 변경 증거 | 검토 주기 계획을 gap-analysis.md에 기록 → 갱신 시 이력으로 충족 |
| 18974 §4.1.2.6 | 내부 모범 사례 일치 검증 담당자 지정 증거 | 담당자를 role-definition.md에 명시 → 갱신 시 검토 이력으로 충족 |
| 18974 §4.1.4.3 | 지속적 개선을 입증하는 감사 증거 | 초기 갭 분석 자체를 1회 감사 이력으로 기록 → 갱신 시 2회 이상으로 충족 |

## 전체 진행률 계산
완료 항목 수 / 전체 항목 수(17) * 100 = 진행률(%)
