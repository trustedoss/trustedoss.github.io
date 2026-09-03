# Skill: update-reference-samples

`output-sample/` 파일을 읽고 `website/reference/samples/` 페이지를 재생성한다.

## 트리거 조건

- `output-sample/` 파일이 변경되어 website 샘플 페이지를 최신화할 때

:::danger sync-output-samples.sh 를 먼저 돌리지 말 것
`sync-output-samples.sh` 는 `output/` → `output-sample/` 방향이다. `output/` 은 gitignore
대상이라 세션마다 내용이 다르므로, 돌리면 골든 픽스처를 덮어써 `verify.sh` [11/13] 이 깨진다.
그 스크립트는 agent 를 실제로 실행해 `output/` 을 새로 만든 뒤 픽스처를 갱신할 때만 쓴다.
샘플 페이지 재생성만 하려면 이 스킬만 실행한다.
:::

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

| 섹션 이름 (H2)             | 파일명                  | output-sample 경로                   |
| -------------------------- | ----------------------- | ------------------------------------ |
| 오픈소스 역할 및 책임 정의 | role-definition.md      | organization/role-definition.md      |
| 오픈소스 RACI 매트릭스     | raci-matrix.md          | organization/raci-matrix.md          |
| 오픈소스 담당자 임명장     | appointment-template.md | organization/appointment-template.md |

---

### policy.md — Type A

| 섹션 이름 (H2)     | 파일명               | output-sample 경로          |
| ------------------ | -------------------- | --------------------------- |
| 오픈소스 정책      | oss-policy.md        | policy/oss-policy.md        |
| 허용 라이선스 목록 | license-allowlist.md | policy/license-allowlist.md |

---

### process.md — Type A

| 섹션 이름 (H2)                           | 파일명                         | output-sample 경로                     | 조건                         |
| ---------------------------------------- | ------------------------------ | -------------------------------------- | ---------------------------- |
| 오픈소스 사용 승인 절차                  | usage-approval.md              | process/usage-approval.md              | 상시                         |
| 배포 전 라이선스 컴플라이언스 체크리스트 | distribution-checklist.md      | process/distribution-checklist.md      | 상시                         |
| 취약점 대응 절차                         | vulnerability-response.md      | process/vulnerability-response.md      | 상시                         |
| 외부 문의 대응 절차                      | inquiry-response.md            | process/inquiry-response.md            | 상시                         |
| 오픈소스 프로세스 흐름도                 | process-diagram.md             | process/process-diagram.md             | 상시                         |
| 오픈소스 기여 절차                       | contribution-process.md        | process/contribution-process.md        | 조건부 (기여 계획 있을 경우) |
| 사내 프로젝트 공개 절차                  | project-publication-process.md | process/project-publication-process.md | 조건부 (공개 계획 있을 경우) |

> **조건부 처리**: output-sample/process/ 에 해당 파일이 없으면 해당 섹션을 재생성하지 않고 기존 내용을 유지한다.

---

### sbom.md — Type B

| 섹션 헤더 (H2)           | output-sample 경로            | 생성 agent           |
| ------------------------ | ----------------------------- | -------------------- |
| license-report.md        | sbom/license-report.md        | `05-sbom-analyst`    |
| copyleft-risk.md         | sbom/copyleft-risk.md         | `05-sbom-analyst`    |
| sbom-management-plan.md  | sbom/sbom-management-plan.md  | `05-sbom-management` |
| sbom-sharing-template.md | sbom/sbom-sharing-template.md | `05-sbom-management` |

---

### vulnerability.md — Type B

| 섹션 헤더 (H2)      | output-sample 경로                | 생성 agent                 |
| ------------------- | --------------------------------- | -------------------------- |
| cve-report.md       | vulnerability/cve-report.md       | `05-vulnerability-analyst` |
| remediation-plan.md | vulnerability/remediation-plan.md | `05-vulnerability-analyst` |

---

### training.md — Type A

| 섹션 이름 (H2)         | 파일명                | output-sample 경로             |
| ---------------------- | --------------------- | ------------------------------ |
| 오픈소스 교육 커리큘럼 | curriculum.md         | training/curriculum.md         |
| 교육 이수 추적 시트    | completion-tracker.md | training/completion-tracker.md |
| 무료 교육 리소스 목록  | resources.md          | training/resources.md          |

---

### conformance.md — Type B

| 섹션 헤더 (H2)       | output-sample 경로               | 생성 agent                |
| -------------------- | -------------------------------- | ------------------------- |
| gap-analysis.md      | conformance/gap-analysis.md      | `07-conformance-preparer` |
| declaration-draft.md | conformance/declaration-draft.md | `07-conformance-preparer` |
| submission-guide.md  | conformance/submission-guide.md  | `07-conformance-preparer` |

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

:::info
**생성 agent**: `{agent-name}` | **저장 경로**: `output/{폴더}/{파일명}`
:::

---

{변환된 내용}

---
```

(기존 페이지가 `> **생성 agent**...` 인용 표기를 쓰고 있으면 admonition 형식으로 교체한다 — 인용(>) 금지 규칙)

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

- `갭 分析` → `갭 분석`

### 7. 코드블록 언어 태그

output-sample 의 펜스 언어를 그대로 옮긴다. 언어가 내용과 어긋나면 생성물이 아니라
`output-sample/` 원본을 고치고 재생성한다. 생성물만 고치면 다음 재생성에서 원복된다.

### 8. 페이지 목차 (필수)

각 페이지는 첫 H2 바로 앞에 수록 산출물 목차를 둔다. 페이지 하나가 산출물 2~7개를 이어
붙인 형태라, 독자는 자기 `output/` 파일과 비교할 하나만 필요하다.

- 목차 제목: ko `**이 페이지에 수록된 산출물**`, en `**Deliverables on this page**`
- 각 항목은 앵커 링크로 만든다: `- [{H2 제목}](#{앵커 id})`
- 각 H2 에 명시적 앵커를 붙인다: `## {제목} {#{앵커 id}}`
- 앵커 id 는 위 "페이지별 매핑" 표의 output-sample 파일명에서 확장자를 뺀 값을 쓴다.
  예: `role-definition.md` → `{#role-definition}`. ko 와 en 이 같은 id 를 쓰므로
  언어를 바꿔도 같은 앵커가 유지된다.
- 헤딩 제목에서 자동 생성되는 슬러그에 의존하지 않는다. 제목이 바뀌어도 앵커가 살아 있어야
  한다. 빌드가 `onBrokenAnchors: 'throw'` 이므로 끊긴 앵커는 빌드에서 잡힌다.

`conformance.md` 의 갭 분석 표는 다른 샘플 페이지의 섹션을 앵커로 참조한다
(`/reference/samples/policy#license-allowlist` 형태). 이 링크도 위 앵커 id 를 쓴다.
제목에서 자동 생성된 슬러그를 쓰면 제목이 바뀔 때 조용히 끊긴다. 재생성 후
`grep -rho "samples/[a-z]*#[^)]*" website/reference/samples` 로 참조된 앵커가 전부
파일명 기반 id 인지 확인한다.

---

## 주의사항

- output-sample/에 없는 파일이 있으면 해당 섹션은 재생성하지 않고 기존 내용을 유지한다.
- `sync-output-samples.sh` 를 이 스킬의 사전 단계로 돌리지 않는다(위 트리거 조건의 경고 참조).
- 이 스킬은 한국어 페이지(`website/reference/samples/`)만 생성한다. 영문
  (`website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/`)은 대응하는
  output-sample 영문 원본이 없어 사람이 옮긴 번역본이다. 한국어를 재생성했으면 영문도 같은
  변경을 손으로 반영해야 `verify.sh` [13/13] 패리티와 내용 일치가 유지된다.
- 완료 후 반드시 `bash .claude/scripts/verify.sh`를 실행하여 13개 항목 PASS를 확인한다.
