[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# 문서 스타일 가이드

trustedoss 문서 작성 시 따르는 규칙입니다.
이 가이드는 한국어 원본 문서(`docs/`, `website/`)와 영어 번역 파일(`website/i18n/en/`) 모두에 적용됩니다.

---

## 1. 문서 구조 원칙

모든 챕터 문서는 **what / why / how** 3단 구성을 따릅니다.

| 섹션      | 내용                                | 필수 여부 |
| --------- | ----------------------------------- | --------- |
| **what**  | 이 챕터에서 무엇을 하는가           | 필수      |
| **why**   | 왜 필요한가 (ISO 요구사항 연결)     | 필수      |
| **how**   | 어떻게 실행하는가 (Agent 실행 단계) | 필수      |
| 입증 자료 | ISO G항목 충족 근거 명시            | 권장      |

챕터 문서에는 해당 챕터가 충족하는 ISO/IEC 5230 및 18974 요구사항 항목을 front matter 또는 본문에 명시합니다.

---

## 2. 언어·용어 규칙

### 공식 용어

한국어 원본에서는 아래 용어를 일관되게 사용합니다.

| 용어              | 사용 | 사용 금지                         |
| ----------------- | ---- | --------------------------------- |
| 오픈소스 정책     | O    | 오픈소스 방침, OSS 정책           |
| 오픈소스 프로세스 | O    | 오픈소스 절차, OSS 프로세스       |
| 자체 인증         | O    | 자가 인증, 셀프 인증              |
| 산출물            | O    | 결과물, 아웃풋                    |
| 담당자            | O    | 책임자, 관리자 (문맥에 따라 구분) |
| 취약점            | O    | 보안 취약점 (중복 표현 주의)      |
| 고지문            | O    | 고지서, 노티스                    |

### 한/영 대응 용어표

영어 번역 파일 작성 시 아래 용어표를 기준으로 일관성을 유지합니다.

| 한국어             | English                  |
| ------------------ | ------------------------ |
| 오픈소스 정책      | Open Source Policy       |
| 오픈소스 프로세스  | Open Source Process      |
| 조직 구성          | Organizational Structure |
| 교육 체계          | Training Program         |
| 자체 인증          | Self-Certification       |
| 체계구축           | Build Your System        |
| 공급망 보안        | Supply Chain Security    |
| 취약점 분석        | Vulnerability Analysis   |
| 산출물             | Deliverables             |
| 담당자             | Program Manager          |
| 고지문             | Attribution Notice       |
| 거버넌스           | Governance               |
| 허용 라이선스 목록 | Approved License List    |
| 갭 분석            | Gap Analysis             |
| 인증 선언문        | Conformance Declaration  |

### 번역하지 않는 고유명사

다음은 번역 없이 원문 그대로 사용합니다.

`OpenChain`, `KWG`, `trustedoss`, `SBOM`, `CycloneDX`, `SPDX`, `Syft`, `Grype`, `Trivy`, `NTIA`, `OSS`, `DevSecOps`, `CLAUDE.md`, `Claude Code`, `Cursor`, `Copilot`

---

## 3. 코드 블록 규칙

- 셸 명령어, YAML, JSON 예시는 코드 블록(` ` ```)으로 감쌉니다.
- 코드 블록 내부는 번역 시 변경하지 않습니다.
- 코드 블록 내 주석(`#`)은 번역해도 됩니다.
- 언어 식별자를 명시합니다: ` ```bash `, ` ```yaml `, ` ```json `

```bash
# 올바른 예
cd agents/03-policy-generator && claude
```

---

## 4. 링크 규칙

### 내부 링크 (docs/ 내부)

같은 docs/ 디렉토리 내 문서 간 링크는 상대 경로를 사용합니다.

```markdown
<!-- 올바른 예 -->

[정책 가이드](../03-policy/index.md)

<!-- 금지 -->

[정책 가이드](/Users/사용자명/projects/trustedoss/docs/03-policy/index.md)
```

### docs/ → reference/ 크로스 링크

`docs/` 문서에서 `website/reference/` 페이지를 참조할 때는 Docusaurus 절대 경로를 사용합니다.

```markdown
<!-- 올바른 예 -->

[SBOM 샘플](/reference/samples/sbom)

<!-- 금지 -->

[SBOM 샘플](../../website/reference/samples/sbom.md)
```

### 로컬 경로 금지

사용자명이 포함된 절대 경로는 절대 사용하지 않습니다.

| 구분     | 형식                   | 예시                         |
| -------- | ---------------------- | ---------------------------- |
| **금지** | 사용자명 포함 절대경로 | `/Users/홍길동/projects/...` |
| **허용** | 상대 경로              | `./docs/...`                 |
| **허용** | 홈 디렉토리 약칭       | `~/projects/trustedoss`      |
| **허용** | 일반화 예시 경로       | `/path/to/trustedoss`        |

---

## 5. front matter 규칙

### 한국어 원본 문서 (docs/)

`docs/` 하위 문서는 아래 4개 필드를 포함해야 합니다. `verify.sh [3/11]` 항목이 이를 검사합니다.

```yaml
---
작성일: YYYY-MM-DD
버전: '1.0'
충족 체크리스트:
  - 'ISO/IEC 5230: [3.x.x, ...]'
  - 'ISO/IEC 18974: [4.x.x, ...]'
셀프스터디 소요시간: N시간
---
```

### 영어 번역 파일 (website/i18n/en/)

번역 파일에서 front matter 키는 영어로 변환합니다.

```yaml
---
date: YYYY-MM-DD
version: '1.0'
checklist:
  - 'ISO/IEC 5230: [3.x.x, ...]'
  - 'ISO/IEC 18974: [4.x.x, ...]'
self_study_time: N hour(s)
---
```

번역하지 않는 값: `id`, `slug`, `sidebar_position`, `tags`

---

## 6. ISO 표준 번호 표기 규칙

ISO/IEC 5230과 18974는 섹션 번호 체계가 다릅니다. 혼용하면 `verify.sh [6/11]`이 FAIL을 냅니다.

| 표준          | 섹션 번호 체계 | 올바른 예                 | 잘못된 예   |
| ------------- | -------------- | ------------------------- | ----------- |
| ISO/IEC 5230  | `3.x.x`        | `3.1.1`, `3.3.2`, `3.6.1` | —           |
| ISO/IEC 18974 | `4.x.x`        | `4.1.1`, `4.3.2`, `4.4.1` | ~~`3.1.1`~~ |

---

## 7. Admonition 규칙

Agent 실행 bash 코드블록 직전에는 세션 종료 안내 admonition을 반드시 추가합니다.
`verify.sh [7/11]` 항목이 이를 검사합니다.

````markdown
:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/03-policy-generator && claude
```
````

````

---

<a id="english"></a>

# Documentation Style Guide

These are the rules for writing trustedoss documentation.
This guide applies to both the Korean source documents (`docs/`, `website/`) and the English translation files (`website/i18n/en/`).

---

## 1. Document Structure

All chapter documents follow a **what / why / how** three-part structure.

| Section | Content | Required |
| ------- | ------- | -------- |
| **what** | What this chapter covers | Required |
| **why** | Why it matters (linked to ISO requirements) | Required |
| **how** | How to execute (agent run steps) | Required |
| Evidence | ISO requirement fulfillment notes | Recommended |

Each chapter document must identify the ISO/IEC 5230 and 18974 requirements it satisfies, either in front matter or in the body.

---

## 2. Language & Terminology

### Official Terms

English translation files must use the following terms consistently.

| Korean | English | Do Not Use |
| ------ | ------- | ---------- |
| 오픈소스 정책 | Open Source Policy | OSS Policy |
| 오픈소스 프로세스 | Open Source Process | OSS Process |
| 자체 인증 | Self-Certification | Self-Declaration, Self-Attestation |
| 산출물 | Deliverables | Outputs, Artifacts |
| 담당자 | Program Manager | Person in Charge |
| 체계구축 | Build Your System | System Building, Framework Setup |
| 고지문 | Attribution Notice | Notice, Notification |
| 갭 분석 | Gap Analysis | — |
| 인증 선언문 | Conformance Declaration | — |

### Korean/English Glossary

| Korean | English |
| ------ | ------- |
| 오픈소스 정책 | Open Source Policy |
| 오픈소스 프로세스 | Open Source Process |
| 조직 구성 | Organizational Structure |
| 교육 체계 | Training Program |
| 자체 인증 | Self-Certification |
| 체계구축 | Build Your System |
| 공급망 보안 | Supply Chain Security |
| 취약점 분석 | Vulnerability Analysis |
| 산출물 | Deliverables |
| 담당자 | Program Manager |
| 고지문 | Attribution Notice |
| 거버넌스 | Governance |
| 허용 라이선스 목록 | Approved License List |
| 갭 분석 | Gap Analysis |
| 인증 선언문 | Conformance Declaration |

### Proper Nouns — Do Not Translate

The following terms are always kept in their original form:

`OpenChain`, `KWG`, `trustedoss`, `SBOM`, `CycloneDX`, `SPDX`, `Syft`, `Grype`, `Trivy`, `NTIA`, `OSS`, `DevSecOps`, `CLAUDE.md`, `Claude Code`, `Cursor`, `Copilot`

---

## 3. Code Block Rules

- Wrap shell commands, YAML, and JSON examples in code blocks (` ``` `).
- Do not modify the contents of code blocks during translation.
- Comments inside code blocks (`#`) may be translated.
- Always specify a language identifier: ` ```bash `, ` ```yaml `, ` ```json `

```bash
# Correct example
cd agents/03-policy-generator && claude
````

---

## 4. Link Rules

### Internal Links (within docs/)

Use relative paths for links between documents in the same `docs/` directory.

```markdown
<!-- Correct -->

[Policy Guide](../03-policy/index.md)

<!-- Forbidden -->

[Policy Guide](/Users/username/projects/trustedoss/docs/03-policy/index.md)
```

### Cross-links from docs/ to reference/

When referencing `website/reference/` pages from `docs/`, use Docusaurus absolute paths.

```markdown
<!-- Correct -->

[SBOM Sample](/reference/samples/sbom)

<!-- Forbidden -->

[SBOM Sample](../../website/reference/samples/sbom.md)
```

### No Local Paths

Never use absolute paths containing usernames.

| Type          | Format                      | Example                    |
| ------------- | --------------------------- | -------------------------- |
| **Forbidden** | Absolute path with username | `/Users/john/projects/...` |
| **Allowed**   | Relative path               | `./docs/...`               |
| **Allowed**   | Home directory shorthand    | `~/projects/trustedoss`    |
| **Allowed**   | Generalized example path    | `/path/to/trustedoss`      |

---

## 5. Front Matter Rules

### Korean Source Documents (docs/)

Documents under `docs/` must include the following 4 fields. `verify.sh [3/11]` checks for these.

```yaml
---
작성일: YYYY-MM-DD
버전: '1.0'
충족 체크리스트:
  - 'ISO/IEC 5230: [3.x.x, ...]'
  - 'ISO/IEC 18974: [4.x.x, ...]'
셀프스터디 소요시간: N시간
---
```

### English Translation Files (website/i18n/en/)

In translation files, convert front matter keys to English.

```yaml
---
date: YYYY-MM-DD
version: '1.0'
checklist:
  - 'ISO/IEC 5230: [3.x.x, ...]'
  - 'ISO/IEC 18974: [4.x.x, ...]'
self_study_time: N hour(s)
---
```

Values that must not be translated: `id`, `slug`, `sidebar_position`, `tags`

---

## 6. ISO Standard Section Number Format

ISO/IEC 5230 and 18974 use different section numbering schemes. Mixing them causes `verify.sh [6/11]` to fail.

| Standard      | Numbering Scheme | Correct                   | Incorrect   |
| ------------- | ---------------- | ------------------------- | ----------- |
| ISO/IEC 5230  | `3.x.x`          | `3.1.1`, `3.3.2`, `3.6.1` | —           |
| ISO/IEC 18974 | `4.x.x`          | `4.1.1`, `4.3.2`, `4.4.1` | ~~`3.1.1`~~ |

---

## 7. Admonition Rules

A session-exit admonition must appear immediately before any agent execution bash code block.
`verify.sh [7/11]` checks for this.

````markdown
:::tip Before Running
First exit the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/03-policy-generator && claude
```
````

```

```
