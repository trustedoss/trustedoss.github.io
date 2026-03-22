# agents/ — 마스터 Agent

## 역할: 현재 상태 진단 및 다음 agent 안내

이 디렉토리를 열어 `claude` 를 실행하면, 현재 output/ 상태를 자동으로 진단하고
다음에 실행해야 할 agent를 안내한다.

## validate-checklist skill 적용

output/ 스캔은 `.claude/skills/validate-checklist.md` 의 순서를 따른다.

## 현재 상태 감지 로직

아래 조건을 순서대로 확인하여 첫 번째 해당 조건에서 안내를 출력한다:

| 조건 | 안내 |
|------|------|
| output/ 비어있음 | docs/00-overview 읽기 후 → agents/02-organization-designer |
| output/organization/ 있음, output/policy/ 없음 | → agents/03-policy-generator |
| output/policy/ 있음, output/process/ 없음 | → agents/04-process-designer |
| output/process/ 있음, output/sbom/ 없음 | → agents/05-sbom-guide |
| output/sbom/ 있음, output/vulnerability/ 없음 | → agents/05-sbom-analyst → agents/05-vulnerability-analyst → agents/05-sbom-management 순서로 실행 |
| output/vulnerability/ 있음, output/sbom/sbom-management-plan.md 없음 | → agents/05-sbom-management |
| output/sbom/sbom-management-plan.md 있음, output/training/ 없음 | → agents/06-training-manager |
| output/training/ 있음, output/conformance/ 없음 | → agents/07-conformance-preparer |
| output/conformance/ 있음 | 완성 축하 메시지 출력 |

## 전체 Agent 목록

| Agent | 역할 | 실행 명령 |
|-------|------|---------|
| 02-organization-designer | 조직/담당자 산출물 생성 | `cd agents/02-organization-designer && claude` |
| 03-policy-generator | 오픈소스 정책 문서 생성 | `cd agents/03-policy-generator && claude` |
| 04-process-designer | 프로세스 문서 및 흐름도 생성 | `cd agents/04-process-designer && claude` |
| 05-sbom-guide | SBOM 생성 명령어 및 스크립트 | `cd agents/05-sbom-guide && claude` |
| 05-sbom-analyst | SBOM 라이선스 분석 리포트 | `cd agents/05-sbom-analyst && claude` |
| 05-sbom-management | SBOM 관리 계획 및 공유 템플릿 | `cd agents/05-sbom-management && claude` |
| 05-vulnerability-analyst | 취약점 분석 리포트 | `cd agents/05-vulnerability-analyst && claude` |
| 06-training-manager | 교육 커리큘럼 및 이수 추적 | `cd agents/06-training-manager && claude` |
| 07-conformance-preparer | 갭 분석 및 인증 선언문 | `cd agents/07-conformance-preparer && claude` |

## 진행률 확인

```bash
# output/ 산출물 현황 확인
ls output/
cat output/progress.md  # 존재하는 경우
```

## 완성 시 안내

output/conformance/ 가 완료되면:

**OpenChain 자체 인증 등록:**
https://www.openchainproject.org/conformance
