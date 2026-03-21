# Skill: 체크리스트 검증 (validate-checklist)

## 적용 대상
agents/07-conformance-preparer
agents/CLAUDE.md (마스터 agent)

## output/ 스캔 방법
아래 순서로 output/ 하위 폴더와 파일을 확인한다.

1. output/organization/role-definition.md 존재 여부
2. output/organization/raci-matrix.md 존재 여부
3. output/policy/oss-policy.md 존재 여부
4. output/policy/license-allowlist.md 존재 여부
5. output/process/usage-approval.md 존재 여부
6. output/process/vulnerability-response.md 존재 여부
7. output/sbom/*.cdx.json 존재 여부
8. output/sbom/license-report.md 존재 여부
9. output/sbom/sbom-management-plan.md 존재 여부
10. output/vulnerability/cve-report.md 존재 여부
11. output/training/curriculum.md 존재 여부
12. output/training/completion-tracker.md 존재 여부
13. output/conformance/gap-analysis.md 존재 여부

## 충족 판정 기준
- 충족: 파일 존재 + 필수 섹션 포함
- 부분충족: 파일 존재 + 일부 섹션 누락
- 미충족: 파일 없음

## 미충족 시 안내 메시지 형식
> [미충족] {항목명}
> 이동: docs/{챕터명} 또는 agents/{agent명}
> 예상 소요시간: {시간}

## 전체 진행률 계산
완료 항목 수 / 전체 항목 수 * 100 = 진행률(%)
