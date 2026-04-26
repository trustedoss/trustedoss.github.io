# Cursor 번역 지시문 — trustedoss 영어 i18n

## 배경

이 프로젝트는 ISO/IEC 5230 및 18974 오픈소스 컴플라이언스 가이드 사이트입니다.
Docusaurus 기반이며, `website/i18n/en/` 디렉토리에 영어 번역 파일을 추가합니다.
이미 디렉토리 구조와 한국어 원본이 복사되어 있습니다. **당신이 할 일은 번역뿐입니다.**

---

## 작업 범위

### 1. JSON 파일 번역 (UI 문자열)

아래 JSON 파일들의 각 항목에서 `"message"` 값을 영어로 번역하세요.
`"description"` 값은 수정하지 않습니다.

번역할 JSON 파일:

- `website/i18n/en/code.json`
- `website/i18n/en/docusaurus-theme-classic/navbar.json`
- `website/i18n/en/docusaurus-theme-classic/footer.json`
- `website/i18n/en/docusaurus-plugin-content-docs/current.json`
- `website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current.json`
- `website/i18n/en/docusaurus-plugin-content-docs-devsecops/current.json`
- `website/i18n/en/docusaurus-plugin-content-docs-reference/current.json`

**JSON 번역 예시:**

```json
// 변경 전
{
  "sidebar.docs.category.시작하기": {
    "message": "시작하기",
    "description": "The label for category 시작하기 in sidebar docs"
  }
}

// 변경 후
{
  "sidebar.docs.category.시작하기": {
    "message": "Getting Started",
    "description": "The label for category 시작하기 in sidebar docs"
  }
}
```

---

### 2. Markdown 파일 번역

`website/i18n/en/` 하위의 모든 `.md` 파일을 영어로 번역하세요.

번역 대상 디렉토리:

- `website/i18n/en/docusaurus-plugin-content-docs/current/` (22개 파일)
- `website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/` (10개 파일)
- `website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/` (7개 파일)
- `website/i18n/en/docusaurus-plugin-content-docs-reference/current/` (8개 파일)
- `website/i18n/en/docusaurus-plugin-content-pages/about.md` (1개 파일)

---

## 번역 규칙 (반드시 준수)

### 1. front matter 처리

front matter의 키(key)와 구조는 그대로 유지합니다.
번역하는 값: `title`, `description`, `sidebar_label`
**번역하지 않는 값**: `id`, `slug`, `sidebar_position`, `tags`, 날짜/버전 필드

```yaml
# 변경 전
---
id: intro
title: trustedoss 소개
sidebar_label: 소개
sidebar_position: 1
slug: /
---
# 변경 후
---
id: intro
title: Introduction to trustedoss
sidebar_label: Introduction
sidebar_position: 1
slug: /
---
```

### 2. ISO 표준 번호 및 섹션 번호 — 변경 금지

```
ISO/IEC 5230, ISO/IEC 18974
3.1.1, 3.3.2, 4.1.1, 4.4.1  ← 그대로 유지
```

### 3. 코드 블록 내부 — 변경 금지

코드 블록(` ``` `) 안의 내용은 번역하지 않습니다.
shell 명령어, YAML, JSON 예시, 파일 경로 모두 원본 유지.

### 4. 내부 링크 — 경로는 유지, 링크 텍스트만 번역

```markdown
# 변경 전

자세한 내용은 [정책 가이드](./03-policy/index.md)를 참조하세요.

# 변경 후

For details, see the [Policy Guide](./03-policy/index.md).
```

경로 부분(`./03-policy/index.md`)은 절대 변경하지 않습니다.

### 5. 브랜드명/고유명사 — 변경 금지

다음 단어들은 번역하지 않습니다:
`OpenChain`, `KWG`, `trustedoss`, `SBOM`, `CycloneDX`, `SPDX`, `Syft`, `Grype`, `Trivy`, `NTIA`, `OSS`, `DevSecOps`, `CLAUDE.md`

### 6. Admonition 블록 — 레이블만 번역

```markdown
# 변경 전

:::tip 핵심 포인트
내용입니다.
:::

# 변경 후

:::tip Key Point
Content here.
:::
```

`:::tip`, `:::info`, `:::warning`, `:::danger` 키워드 자체는 유지.

### 7. 번역 톤 & 스타일

- 독자: 기업 오픈소스 컴플라이언스 담당자 (중급 수준 영어)
- 격식체 사용 (technical documentation style)
- 한국어 존댓말 어미(`~합니다`, `~하세요`)는 일반 기술 문서 어투로 변환
- 예: "살펴보겠습니다" → "This section covers..."

---

## 번역 참고 용어집

| 한국어            | English                           |
| ----------------- | --------------------------------- |
| 오픈소스 정책     | Open Source Policy                |
| 오픈소스 프로세스 | Open Source Process               |
| 조직 구성         | Organizational Structure          |
| 교육 체계         | Training Program                  |
| 자체 인증         | Self-Certification / Conformance  |
| 체계구축          | Build Your System                 |
| 공급망 보안       | Supply Chain Security             |
| 취약점 분석       | Vulnerability Analysis            |
| 컴플라이언스      | Compliance                        |
| 체크리스트        | Checklist                         |
| 개발자 가이드     | Developer Guide                   |
| 산출물            | Deliverables / Output             |
| 소프트웨어 부품표 | Software Bill of Materials (SBOM) |
| 라이선스          | License                           |
| 고지문            | Attribution Notice                |
| 거버넌스          | Governance                        |
| 검토              | Review                            |
| 승인              | Approval                          |
| 레퍼런스          | Reference                         |

---

## 작업 순서 (권장)

1. JSON 파일 먼저 번역 (전체 분량 적음, 용어 기준 확립)
2. `docs/` 계열 (.md) 번역 — 챕터 순서대로 (00 → 08)
3. `ai-coding/`, `devsecops/`, `reference/` 번역
4. `about.md` 번역

---

## 완료 확인

번역 완료 후 프로젝트 루트에서 아래 명령으로 빌드 확인:

```bash
cd website && npm run build

```

빌드 성공 후 영문 사이트 확인:

```bash
cd website && npm run start -- --locale en
# → http://localhost:3000/en/
```
