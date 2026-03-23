# Skill: update-reference-samples

`output-sample/` 파일을 읽고 `website/reference/samples/` 페이지를 재생성한다.

## 트리거 조건

- `bash .claude/scripts/sync-output-samples.sh` 실행 후
- output-sample/ 파일이 변경되어 website 샘플 페이지를 최신화할 때

---

## 실행 절차 — 페이지 단위 순차 처리

**토큰 절약을 위해 파일을 한꺼번에 읽지 않는다.** 페이지별로 처리한다:

1. 해당 페이지에 필요한 output-sample 파일만 읽기 (2~4개)
2. 해당 페이지 재생성 (Write 도구)
3. 다음 페이지로 이동

7개 페이지 완료 후:

```bash
bash .claude/scripts/verify.sh
```

모든 항목 PASS 후 완료.

---

## 페이지별 매핑

### organization.md — Type A

| 섹션 이름 (H2) | 파일명 | output-sample 경로 |
|----------------|--------|-------------------|
| 오픈소스 역할 및 책임 정의 | role-definition.md | organization/role-definition.md |
| 오픈소스 RACI 매트릭스 | raci-matrix.md | organization/raci-matrix.md |

---

### policy.md — Type A

| 섹션 이름 (H2) | 파일명 | output-sample 경로 |
|----------------|--------|-------------------|
| 오픈소스 정책 | oss-policy.md | policy/oss-policy.md |
| 허용 라이선스 목록 | license-allowlist.md | policy/license-allowlist.md |

---

### process.md — Type A

| 섹션 이름 (H2) | 파일명 | output-sample 경로 |
|----------------|--------|-------------------|
| 오픈소스 사용 승인 절차 | usage-approval.md | process/usage-approval.md |
| 배포 전 라이선스 컴플라이언스 체크리스트 | distribution-checklist.md | process/distribution-checklist.md |
| 취약점 대응 절차 | vulnerability-response.md | process/vulnerability-response.md |
| 오픈소스 프로세스 흐름도 | process-diagram.md | process/process-diagram.md |

---

### sbom.md — Type B

| 섹션 헤더 (H2) | output-sample 경로 | 생성 agent |
|----------------|-------------------|-----------|
| license-report.md | sbom/license-report.md | `05-sbom-analyst` |
| copyleft-risk.md | sbom/copyleft-risk.md | `05-sbom-analyst` |
| sbom-management-plan.md | sbom/sbom-management-plan.md | `05-sbom-management` |
| sbom-sharing-template.md | sbom/sbom-sharing-template.md | `05-sbom-management` |

---

### vulnerability.md — Type B

| 섹션 헤더 (H2) | output-sample 경로 | 생성 agent |
|----------------|-------------------|-----------|
| cve-report.md | vulnerability/cve-report.md | `05-vulnerability-analyst` |
| remediation-plan.md | vulnerability/remediation-plan.md | `05-vulnerability-analyst` |

---

### training.md — Type A

| 섹션 이름 (H2) | 파일명 | output-sample 경로 |
|----------------|--------|-------------------|
| 오픈소스 교육 커리큘럼 | curriculum.md | training/curriculum.md |
| 교육 이수 추적 시트 | completion-tracker.md | training/completion-tracker.md |
| 무료 교육 리소스 목록 | resources.md | training/resources.md |

---

### conformance.md — Type B

| 섹션 헤더 (H2) | output-sample 경로 | 생성 agent |
|----------------|-------------------|-----------|
| gap-analysis.md | conformance/gap-analysis.md | `07-conformance-preparer` |
| declaration-draft.md | conformance/declaration-draft.md | `07-conformance-preparer` |
| submission-guide.md | conformance/submission-guide.md | `07-conformance-preparer` |

---

## 섹션 구조 — Type A vs Type B

### Type A: organization / policy / process / training

관련 표준 주석(HTML comment)이 있고, 메타데이터가 볼드 키-값 형식인 파일군.

```
## {섹션 이름}

문서: {파일명}

- **key1**: value1
- **key2**: value2

```
관련 표준
- 5230 §x.x.x
- 18974 §4.x.x
```

---

{변환된 내용}

---
```

**메타데이터 규칙**: output-sample의 `**key**: value` 줄을 `- **key**: value` (불릿 포함)으로 변환한다.
**관련 표준 위치**: 메타데이터 블록 바로 뒤, 첫 번째 `---` 앞에 배치한다.

### Type B: sbom / vulnerability / conformance

YAML front matter가 있고, 파일명을 섹션 헤더로 쓰는 파일군.

```
## {파일명}

> **생성 agent**: `{agent-name}` | **저장 경로**: `output/{폴더}/{파일명}`

---

{변환된 내용}

---
```

---

## 변환 규칙 (공통)

### 1. Docusaurus frontmatter 유지

각 샘플 페이지의 기존 frontmatter(id, title, sidebar_label, sidebar_position)는 변경하지 않는다.
페이지 상단 안내문과 `> **레퍼런스 바로가기:**` callout도 유지한다.

### 2. YAML front matter 처리 (Type B 전용)

output-sample 파일의 `--- ... ---` 블록을 평문으로 변환한다:

```
리포트 유형: {값}
생성일: {값}
대상 프로젝트: {값}
사용 도구: {값}
```

`---` 구분선으로 감싼다.

### 3. 헤딩 강등

- H1 (`#`) → 생략
- H2 (`##`) → H3 (`###`)
- H3 (`###`) → H4 (`####`)

### 4. MDX 빌드 오류 방지

코드블록 **밖의** `{변수명}` → `(변수명)` 교체. 코드블록 내부는 변경하지 않는다.

### 5. 관련 표준 블록 (Type A 전용)

HTML 주석 `<!-- 5230 §... -->` 을 코드블록으로 변환한다:

````
```
관련 표준
- 5230 §3.x.x
- 18974 §4.x.x
```
````

- 섹션 번호 체계: ISO/IEC 5230은 `3.x.x`, ISO/IEC 18974는 `4.x.x`
- 파일 최상단 주석은 메타데이터 바로 뒤에 배치
- 섹션별 주석은 해당 H3/H4 헤딩 바로 뒤에 배치

### 6. 타이포 수정

- `갭 分析` → `갭 분析`

---

## 주의사항

- output-sample/에 없는 파일이 있으면 해당 섹션은 재생성하지 않고 기존 내용을 유지한다.
- 먼저 `bash .claude/scripts/sync-output-samples.sh`를 실행하여 output-sample/을 최신화한 후 이 스킬을 실행하는 것을 권장한다.
- 완료 후 반드시 `bash .claude/scripts/verify.sh`를 실행하여 7개 항목 PASS를 확인한다.
