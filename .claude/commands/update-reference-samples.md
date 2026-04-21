output-sample/ 파일을 읽고 website/reference/samples/ 페이지를 재생성한다.
자세한 변환 규칙은 .claude/skills/update-reference-samples.md 참조.

## 실행 절차

### 1단계: output-sample/ 파일 읽기

output-sample/ 하위의 모든 .md 파일을 Read 도구로 읽는다.

### 2단계: 각 샘플 페이지 재생성

아래 페이지별 매핑을 참조하여 7개 파일을 순서대로 재생성한다.

### 3단계: verify.sh 실행

```bash
bash .claude/scripts/verify.sh
```

모든 항목 PASS 후 완료.

---

## 페이지별 매핑

| 샘플 페이지                                | output-sample 파일들                                                                                                        |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| website/reference/samples/organization.md  | organization/role-definition.md, organization/raci-matrix.md                                                                |
| website/reference/samples/policy.md        | policy/oss-policy.md, policy/license-allowlist.md                                                                           |
| website/reference/samples/process.md       | process/usage-approval.md, process/distribution-checklist.md, process/vulnerability-response.md, process/process-diagram.md |
| website/reference/samples/sbom.md          | sbom/license-report.md, sbom/copyleft-risk.md, sbom/sbom-management-plan.md, sbom/sbom-sharing-template.md                  |
| website/reference/samples/vulnerability.md | vulnerability/cve-report.md, vulnerability/remediation-plan.md                                                              |
| website/reference/samples/training.md      | training/curriculum.md, training/completion-tracker.md, training/resources.md                                               |
| website/reference/samples/conformance.md   | conformance/gap-analysis.md, conformance/declaration-draft.md, conformance/submission-guide.md                              |

---

## 변환 규칙 (공통)

1. **Docusaurus frontmatter 유지** — id, title, sidebar_label, sidebar_position 및 상단 안내문 변경 없음
2. **YAML front matter → 평문** — output-sample 파일의 `--- ... ---` 블록을 평문 메타데이터로 변환
3. **헤딩 강등** — H1 생략, H2→H3, H3→H4
4. **MDX 빌드 오류 방지** — 코드블록 밖의 `{변수명}` → `(변수명)` 교체
5. **관련 표준 블록** — organization/policy/process/training 파일의 HTML 주석(`<!-- 5230 §... -->`)을 코드블록으로 변환
6. **타이포 수정** — `갭 分析` → `갭 분석`

각 섹션은 다음 구조로 임베드:

```
## {파일명}

> **생성 agent**: `{agent-name}` | **저장 경로**: `output/{폴더}/{파일명}`

---

{변환된 내용}

---
```
