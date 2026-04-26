# 다국어(영어) 지원 구현 계획

## 개요

Docusaurus 공식 i18n 기능을 사용해 영어(`en`) 로케일을 추가한다.
번역 파일은 `website/i18n/en/` 하위에 관리되며, 한국어 원본(`ko`)은 변경하지 않는다.

---

## 작업 분담

| 단계 | 작업자     | 내용                                                                     |
| ---- | ---------- | ------------------------------------------------------------------------ |
| 1    | **Claude** | `website/i18n/en/` 디렉토리 구조 생성 + 원본 .md 복사 (번역 placeholder) |
| 2    | **사용자** | `docusaurus.config.ts` 로케일 추가 (아래 참조)                           |
| 3    | **사용자** | `write-translations` 명령 실행 → UI 문자열 JSON 자동 생성                |
| 4    | **Cursor** | 생성된 JSON + 복사된 .md 전체 번역                                       |
| 5    | **사용자** | 로컬 영문 빌드 검증                                                      |

---

## 단계별 상세

### 단계 1 — 구조 설정 (Claude 완료)

`website/i18n/en/` 아래 다음 구조를 생성한다.

```
website/i18n/en/
├── docusaurus-plugin-content-docs/
│   └── current/               ← docs/ 전체 .md 복사 (CLAUDE.md 제외)
├── docusaurus-plugin-content-docs-ai-coding/
│   └── current/               ← website/ai-coding/ 전체 .md 복사
├── docusaurus-plugin-content-docs-devsecops/
│   └── current/               ← website/devsecops/ 전체 .md 복사
├── docusaurus-plugin-content-docs-reference/
│   └── current/               ← website/reference/ 전체 .md 복사
└── docusaurus-plugin-content-pages/
    └── about.md               ← website/src/pages/about.md 복사
```

JSON 파일(UI 문자열, 사이드바 레이블, navbar/footer)은 단계 3에서 자동 생성된다.

---

### 단계 2 — `docusaurus.config.ts` 수정 (사용자 직접)

> ⚠️ 이 파일은 CLAUDE.md 수정 금지 대상이므로 사용자가 직접 수정한다.

**변경 위치**: `website/docusaurus.config.ts` 약 42번째 줄

```ts
// 변경 전
i18n: {
  defaultLocale: 'ko',
  locales: ['ko'],
},

// 변경 후
i18n: {
  defaultLocale: 'ko',
  locales: ['ko', 'en'],
  localeConfigs: {
    ko: { label: '한국어' },
    en: { label: 'English' },
  },
},
```

---

### 단계 3 — `write-translations` 실행 (사용자 직접)

```bash
cd website
npx docusaurus write-translations --locale en
```

이 명령이 아래 JSON 파일을 자동 생성한다:

- `i18n/en/code.json` — 공통 UI 문자열
- `i18n/en/docusaurus-theme-classic/navbar.json` — navbar 레이블
- `i18n/en/docusaurus-theme-classic/footer.json` — footer 레이블
- `i18n/en/docusaurus-plugin-content-docs/current.json` — 메인 사이드바 카테고리
- `i18n/en/docusaurus-plugin-content-docs-ai-coding/current.json`
- `i18n/en/docusaurus-plugin-content-docs-devsecops/current.json`
- `i18n/en/docusaurus-plugin-content-docs-reference/current.json`

> ✅ 단계 1에서 복사한 .md 파일은 유지된다. 명령 실행 후 JSON만 추가됨.

---

### 단계 4 — Cursor 번역 (`.claude/cursor-i18n-prompt.md` 참조)

번역 대상:

- `website/i18n/en/` 하위 모든 `.md` 파일 (약 55개)
- `write-translations`로 생성된 `.json` 파일의 `"message"` 값 (약 50개 항목)

---

### 단계 5 — 로컬 검증

```bash
# 영문 로케일만 실행
cd website && npm run start -- --locale en

# 또는 전체 빌드
cd website && npm run build
```

URL 패턴:

- 한국어: `https://trustedoss.github.io/` (기본값)
- 영어: `https://trustedoss.github.io/en/`

---

## 번역 대상 파일 목록

### docs/ → `i18n/en/docusaurus-plugin-content-docs/current/` (19개)

| 원본 경로                                      | i18n 경로                                         |
| ---------------------------------------------- | ------------------------------------------------- |
| `docs/intro.md`                                | `current/intro.md`                                |
| `docs/00-overview/index.md`                    | `current/00-overview/index.md`                    |
| `docs/00-overview/checklist-mapping.md`        | `current/00-overview/checklist-mapping.md`        |
| `docs/00-overview/supply-chain.md`             | `current/00-overview/supply-chain.md`             |
| `docs/00-overview/sbom-101.md`                 | `current/00-overview/sbom-101.md`                 |
| `docs/01-setup/index.md`                       | `current/01-setup/index.md`                       |
| `docs/01-setup/method1-claude-md.md`           | `current/01-setup/method1-claude-md.md`           |
| `docs/02-organization/index.md`                | `current/02-organization/index.md`                |
| `docs/03-policy/index.md`                      | `current/03-policy/index.md`                      |
| `docs/04-process/index.md`                     | `current/04-process/index.md`                     |
| `docs/05-tools/sbom-generation/index.md`       | `current/05-tools/sbom-generation/index.md`       |
| `docs/05-tools/sbom-generation/docker-cicd.md` | `current/05-tools/sbom-generation/docker-cicd.md` |
| `docs/05-tools/sbom-management/index.md`       | `current/05-tools/sbom-management/index.md`       |
| `docs/05-tools/vulnerability/index.md`         | `current/05-tools/vulnerability/index.md`         |
| `docs/05-tools/vulnerability/tools-setup.md`   | `current/05-tools/vulnerability/tools-setup.md`   |
| `docs/06-training/index.md`                    | `current/06-training/index.md`                    |
| `docs/07-conformance/index.md`                 | `current/07-conformance/index.md`                 |
| `docs/08-developer-guide/index.md`             | `current/08-developer-guide/index.md`             |
| `docs/08-developer-guide/method1-claude-md.md` | `current/08-developer-guide/method1-claude-md.md` |
| `docs/08-developer-guide/method2-skill.md`     | `current/08-developer-guide/method2-skill.md`     |
| `docs/08-developer-guide/method3-hooks.md`     | `current/08-developer-guide/method3-hooks.md`     |
| `docs/08-developer-guide/method4-cicd.md`      | `current/08-developer-guide/method4-cicd.md`      |

### website/ai-coding/ → `i18n/en/docusaurus-plugin-content-docs-ai-coding/current/` (10개)

| 원본 경로                                 | i18n 경로                       |
| ----------------------------------------- | ------------------------------- |
| `website/ai-coding/intro.md`              | `current/intro.md`              |
| `website/ai-coding/strategy.md`           | `current/strategy.md`           |
| `website/ai-coding/iso42001.md`           | `current/iso42001.md`           |
| `website/ai-coding/best-practice-repo.md` | `current/best-practice-repo.md` |
| `website/ai-coding/ai-security-review.md` | `current/ai-security-review.md` |
| `website/ai-coding/tools/claude-code.md`  | `current/tools/claude-code.md`  |
| `website/ai-coding/tools/cursor.md`       | `current/tools/cursor.md`       |
| `website/ai-coding/tools/copilot.md`      | `current/tools/copilot.md`      |
| `website/ai-coding/tools/windsurf.md`     | `current/tools/windsurf.md`     |
| `website/ai-coding/tools/cline-aider.md`  | `current/tools/cline-aider.md`  |

### website/devsecops/ → `i18n/en/docusaurus-plugin-content-docs-devsecops/current/` (7개)

| 원본 경로                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------- |
| `intro.md`, `strategy.md`, `pipeline-design.md`, `container-security.md`, `dast.md`, `monitoring.md`, `iso-mapping.md` |

### website/reference/ → `i18n/en/docusaurus-plugin-content-docs-reference/current/` (8개)

| 원본 경로                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `intro.md`, `samples/conformance.md`, `samples/organization.md`, `samples/policy.md`, `samples/process.md`, `samples/sbom.md`, `samples/training.md`, `samples/vulnerability.md` |

### 기타 (1개)

| 원본 경로                    | i18n 경로                                          |
| ---------------------------- | -------------------------------------------------- |
| `website/src/pages/about.md` | `i18n/en/docusaurus-plugin-content-pages/about.md` |

---

## 번역 시 주의사항

1. **front matter는 유지** — `id`, `slug`, `sidebar_position`, `sidebar_label` 키는 그대로. `title`과 `description` 값만 번역.
2. **ISO 표준 번호/섹션 번호 변경 금지** — `ISO/IEC 5230`, `3.1.1`, `4.2.1` 등은 번역하지 않음.
3. **코드 블록 내부 번역 금지** — shell 명령어, YAML 예시, JSON 샘플은 그대로 유지.
4. **내부 링크 경로 변경 금지** — `[텍스트](./relative-path)` 에서 경로 부분은 유지, 링크 텍스트만 번역.
5. **브랜드명/고유명사 변경 금지** — `OpenChain`, `KWG`, `trustedoss`, `SBOM`, `CycloneDX`, `SPDX` 등.
