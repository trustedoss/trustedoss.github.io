# Skill: update-reference-samples

`output-sample/` 파일을 읽고 `website/reference/samples/` 페이지를 재생성한다.

## 트리거 조건

- `bash .claude/scripts/sync-output-samples.sh` 실행 후
- output-sample/ 파일이 변경되어 website 샘플 페이지를 최신화할 때

---

## 실행 절차

### 1단계: output-sample/ 파일 읽기

`output-sample/` 하위의 모든 `.md` 파일을 Read 도구로 읽는다.

### 2단계: 각 샘플 페이지 재생성

아래 **페이지별 매핑**을 참조하여 7개 파일을 순서대로 재생성한다.

### 3단계: verify.sh 실행

```bash
bash .claude/scripts/verify.sh
```

모든 항목 PASS 후 완료.

---

## 페이지별 매핑

### organization.md

| 섹션 헤더 (H2) | output-sample 파일 |
|----------------|-------------------|
| 오픈소스 역할 및 책임 정의 | organization/role-definition.md |
| 오픈소스 RACI 매트릭스 | organization/raci-matrix.md |

**특이사항**: `관련 표준` 코드블록 패턴 유지 (기존 파일 참조)

---

### policy.md

| 섹션 헤더 (H2) | output-sample 파일 |
|----------------|-------------------|
| oss-policy.md | policy/oss-policy.md |
| license-allowlist.md | policy/license-allowlist.md |

**특이사항**: `관련 표준` 코드블록 패턴 유지

---

### process.md

| 섹션 헤더 (H2) | output-sample 파일 |
|----------------|-------------------|
| usage-approval.md | process/usage-approval.md |
| distribution-checklist.md | process/distribution-checklist.md |
| vulnerability-response.md | process/vulnerability-response.md |
| process-diagram.md | process/process-diagram.md |

**특이사항**: `관련 표준` 코드블록 패턴 유지

---

### sbom.md

| 섹션 헤더 (H2) | output-sample 파일 |
|----------------|-------------------|
| license-report.md | sbom/license-report.md |
| copyleft-risk.md | sbom/copyleft-risk.md |
| sbom-management-plan.md | sbom/sbom-management-plan.md |
| sbom-sharing-template.md | sbom/sbom-sharing-template.md |

**특이사항**: `관련 표준` 블록 없음. YAML front matter → 평문 메타데이터만.

---

### vulnerability.md

| 섹션 헤더 (H2) | output-sample 파일 |
|----------------|-------------------|
| cve-report.md | vulnerability/cve-report.md |
| remediation-plan.md | vulnerability/remediation-plan.md |

**특이사항**: `관련 표준` 블록 없음.

---

### training.md

| 섹션 헤더 (H2) | output-sample 파일 |
|----------------|-------------------|
| curriculum.md | training/curriculum.md |
| completion-tracker.md | training/completion-tracker.md |
| resources.md | training/resources.md |

**특이사항**: `관련 표준` 코드블록 패턴 유지

---

### conformance.md

| 섹션 헤더 (H2) | output-sample 파일 |
|----------------|-------------------|
| gap-analysis.md | conformance/gap-analysis.md |
| declaration-draft.md | conformance/declaration-draft.md |
| submission-guide.md | conformance/submission-guide.md |

**특이사항**: `관련 표준` 블록 없음.

---

## 변환 규칙 (모든 페이지 공통)

### 1. Docusaurus frontmatter 유지

각 샘플 페이지의 기존 frontmatter(id, title, sidebar_label, sidebar_position)는 변경하지 않는다.
페이지 상단 안내문(`agent가 생성하는 N개 산출물의 완성 예시입니다.`)과
`> **레퍼런스 바로가기:**` callout도 유지한다.

### 2. 섹션 헤더 구조

각 output-sample 파일은 다음 구조로 임베드한다:

```
## {파일명}

> **생성 agent**: `{agent-name}` | **저장 경로**: `output/{폴더}/{파일명}`

---

{변환된 내용}

---
```

`생성 agent` 값은 기존 페이지의 callout을 그대로 유지한다.

### 3. YAML front matter 처리

output-sample 파일의 YAML front matter(`--- ... ---`)가 있으면 평문 메타데이터 블록으로 변환한다.

```
리포트 유형: {값}
생성일: {값}
대상 프로젝트: {값}
사용 도구: {값}
```

`---` 구분선으로 감싼다.

### 4. 헤딩 강등

output-sample 파일의 헤딩을 한 단계 강등한다:
- H1 (`#`) → 생략 (섹션 헤더인 H2가 대신함)
- H2 (`##`) → H3 (`###`)
- H3 (`###`) → H4 (`####`)

### 5. MDX 빌드 오류 방지

테이블 셀 또는 일반 문단에서 `{변수명}` 형식의 중괄호가 **코드블록 밖에** 있으면
`(변수명)`으로 교체한다. 코드블록(``` ``` ```) 내부는 변경하지 않는다.

### 6. 관련 표준 블록

organization/policy/process/training 계열 파일에는 HTML 주석(`<!-- 5230 §... -->`)이
있을 수 있다. 이를 다음 형식의 코드블록으로 변환한다:

````
```
관련 표준
- 5230 §3.x.x
- 18974 §4.x.x
```
````

섹션 번호 체계: ISO/IEC 5230은 `3.x.x`, ISO/IEC 18974는 `4.x.x`.

### 7. 타이포 수정

- `갭 分析` → `갭 분析` (한자 혼용 수정)

---

## 주의사항

- output-sample/에 없는 파일이 있으면 해당 섹션은 재생성하지 않고 기존 내용을 유지한다.
- 먼저 `bash .claude/scripts/sync-output-samples.sh`를 실행하여 output-sample/을 최신화한 후 이 스킬을 실행하는 것을 권장한다.
- 완료 후 반드시 `bash .claude/scripts/verify.sh`를 실행하여 7개 항목 PASS를 확인한다.
