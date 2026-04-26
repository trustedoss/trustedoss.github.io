# Cursor 번역 수정 지시문 — 2차 패스

1차 번역에서 발생한 아래 6가지 문제를 수정합니다.
**대상 디렉토리: `website/i18n/en/` 전체**

---

## 문제 1 — `__ TERMx __` / `__ CODEx __` placeholder 미복원 (36개)

번역 과정에서 일부 용어가 placeholder 형태로 남아있습니다. 아래 규칙대로 원래 값으로 복원하세요.

| placeholder    | 복원할 값    | 비고                                            |
| -------------- | ------------ | ----------------------------------------------- |
| `__ TERM0 __`  | `trustedoss` | 브랜드명                                        |
| `__ TERM1 __`  | `OpenChain`  | 브랜드명                                        |
| `__ TERM7 __`  | `SBOM`       | 고유명사                                        |
| `__ CODE13 __` | `` `시작` `` | Claude에 입력하는 명령어 (코드이므로 백틱 유지) |

나머지 `__ TERMx __` / `__ CODEx __` 패턴이 있다면 동일하게 **원본 한국어 파일에서 해당 위치의 원문을 확인해 복원**하세요.

**찾는 방법:**

```bash
grep -rn "__ TERM\|__ CODE" website/i18n/en/ --include="*.md"
```

---

## 문제 2 — `* * text * *` Markdown bold 문법 깨짐 (17개)

`**텍스트**`가 `* * text * *`(공백 삽입)으로 변환되어 굵게 렌더링되지 않습니다.

**수정 규칙:** `* * ` → `**`, ` * *` → `**`

```markdown
# 잘못된 형태

- - ISO/IEC 5230 \* _ (License Compliance)
    Agent will automatically create _ _ 23 deliverables _ \*

# 올바른 형태

**ISO/IEC 5230** (License Compliance)
Agent will automatically create **23 deliverables**
```

**찾는 방법:**

```bash
grep -rn "\* \*" website/i18n/en/ --include="*.md"
```

---

## 문제 3 — `] (url)` Markdown 링크 문법 깨짐 (11개)

`[텍스트](경로)` 형식에서 `]`와 `(` 사이에 공백이 삽입되어 링크가 동작하지 않습니다.

**수정 규칙:** `] (` → `](`

```markdown
# 잘못된 형태

[Overview] (./00-overview/index.md)
[Supply Chain Security] (./00-overview/supply-chain.md)

# 올바른 형태

[Overview](./00-overview/index.md)
[Supply Chain Security](./00-overview/supply-chain.md)
```

**찾는 방법:**

```bash
grep -rn "\] (" website/i18n/en/ --include="*.md"
```

---

## 문제 4 — 코드 블록 내 `관련 표준` 한국어 잔류

`reference/samples/` 하위 파일들에서 아래 패턴이 번역되지 않고 남아있습니다.
이 항목은 코드 블록이지만 **사람이 읽는 레이블**이므로 번역해야 합니다.

대상 파일:

- `website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/process.md`
- `website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/training.md`
- `website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/organization.md`
- `website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/policy.md`
- (같은 패턴이 있는 다른 samples 파일 포함)

**수정 규칙:**

```
# 잘못된 형태
```

관련 표준

- 5230 §3.1.5.1·§3.3.1.1

```

# 올바른 형태
```

Related Standards

- 5230 §3.1.5.1·§3.3.1.1

```

```

**찾는 방법:**

```bash
grep -rn "관련 표준" website/i18n/en/ --include="*.md"
```

---

## 문제 5 — front matter 커스텀 필드 한국어 잔류 (56개)

docs 파일들의 front matter에 한국어 키/값이 그대로 남아있습니다.

대상: `website/i18n/en/docusaurus-plugin-content-docs/current/` 하위 파일들

**수정 규칙 (키와 값 모두 영어로):**

```yaml
# 잘못된 형태
---
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: [3.1.1, 3.2.1]'
셀프스터디 소요시간: 1시간
---
# 올바른 형태
---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: [3.1.1, 3.2.1]'
self_study_time: 1 hour
---
```

**찾는 방법:**

```bash
grep -rn "^작성일:\|^버전:\|^셀프스터디\|^충족 체크리스트" website/i18n/en/ --include="*.md"
```

---

## 문제 6 — `blog/options.json` 미번역

아래 파일의 `sidebar.title` 값이 한국어로 남아있습니다.

파일: `website/i18n/en/docusaurus-plugin-content-blog/options.json`

```json
// 잘못된 형태
"sidebar.title": {
  "message": "전체 블로그 포스트",
  "description": "The label for the left sidebar"
}

// 올바른 형태
"sidebar.title": {
  "message": "All Blog Posts",
  "description": "The label for the left sidebar"
}
```

---

## 완료 후 검증

```bash
cd website && npm run build
```

빌드 성공 + broken anchors 경고 없음을 확인하세요.
