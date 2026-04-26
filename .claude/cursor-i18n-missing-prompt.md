# Cursor 번역 수정 지시문 — 3차: 홈페이지 및 누락 페이지

영어로 전환 시 3가지 문제가 남아있습니다. 아래 순서대로 모두 수정하세요.

---

## 문제 A — 홈페이지 한국어 하드코딩

### 원인

`website/src/components/Home/` 컴포넌트들이 Docusaurus `<Translate>` 훅 없이 한국어 문자열을 하드코딩하고 있어서 언어 전환이 동작하지 않습니다.

### 수정 대상 파일

1. `website/src/components/Home/Hero/index.tsx`
2. `website/src/components/Home/CallToAction/index.tsx`
3. `website/src/pages/index.tsx`
4. `website/i18n/en/code.json` (영어 번역 추가)

---

### A-1: `Hero/index.tsx` 수정

파일 상단에 import 추가:

```tsx
import Translate, {translate} from '@docusaurus/Translate';
```

아래 한국어 문자열을 `<Translate>` 또는 `translate()` 로 감싸세요:

| 현재 (한국어 하드코딩)                                                       | 변경 후                                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `신뢰할 수 있는 오픈소스 공급망 관리`                                        | `<Translate id="homepage.hero.subtitle">신뢰할 수 있는 오픈소스 공급망 관리</Translate>` |
| `ISO/IEC 5230 &amp; 18974 기반<br/>기업 오픈소스 관리 체계 구축 실전 가이드` | `<Translate id="homepage.hero.description">...</Translate>`                              |
| `체계구축 시작하기` (버튼)                                                   | `translate({id: 'homepage.hero.cta.docs', message: '체계구축 시작하기'})`                |
| `AI코딩 가이드` (버튼)                                                       | `translate({id: 'homepage.hero.cta.aiCoding', message: 'AI코딩 가이드'})`                |

> 주의: `<Translate>`의 children은 기본값(한국어)으로 유지하세요. 영어는 `code.json`에서 지정합니다.

---

### A-2: `CallToAction/index.tsx` 수정

파일 상단에 import 추가:

```tsx
import Translate, {translate} from '@docusaurus/Translate';
```

`features` 배열의 각 항목과 하단 섹션의 문자열을 `translate()` 로 감싸세요:

```tsx
// 변경 전
const features = [
  {
    title: '체계구축',
    description: 'ISO/IEC 5230 & 18974 기반으로 ...',
    linkLabel: '가이드 시작하기',
  },
  ...
];

// 변경 후
const features = [
  {
    title: translate({id: 'homepage.cta.feature1.title', message: '체계구축'}),
    description: translate({id: 'homepage.cta.feature1.desc', message: 'ISO/IEC 5230 & 18974 기반으로 ...'}),
    linkLabel: translate({id: 'homepage.cta.feature1.link', message: '가이드 시작하기'}),
  },
  ...
];
```

하단 섹션도 동일하게:

```tsx
// 변경 전
<h2>오픈소스 관리, 지금 시작하세요</h2>
<p>OpenChain KWG 커뮤니티가 제공하는 무료 가이드로<br/>...</p>
<a ...>체계구축 시작하기</a>

// 변경 후
<h2><Translate id="homepage.cta.section.title">오픈소스 관리, 지금 시작하세요</Translate></h2>
<p><Translate id="homepage.cta.section.subtitle">...</Translate></p>
<a ...><Translate id="homepage.cta.section.cta">체계구축 시작하기</Translate></a>
```

---

### A-3: `website/src/pages/index.tsx` 수정

`<Head>` 태그 안의 한국어 문자열을 `translate()` 로 감싸세요:

```tsx
import {translate} from '@docusaurus/Translate';

// 변경 전
description="ISO/IEC 5230 & 18974 기반 기업 오픈소스 관리 체계 구축 실전 가이드"
<title>Trusted OSS · 신뢰할 수 있는 오픈소스 공급망 관리</title>
<meta content="Trusted OSS · 신뢰할 수 있는 오픈소스 공급망 관리" ... />

// 변경 후
description={translate({id: 'homepage.meta.description', message: 'ISO/IEC 5230 & 18974 기반 기업 오픈소스 관리 체계 구축 실전 가이드'})}
<title>{translate({id: 'homepage.meta.title', message: 'Trusted OSS · 신뢰할 수 있는 오픈소스 공급망 관리'})}</title>
```

---

### A-4: `website/i18n/en/code.json` — 영어 번역 추가

기존 JSON 끝 `}` 앞에 아래 항목들을 추가하세요:

```json
"homepage.hero.subtitle": {
  "message": "Trusted Open Source Supply Chain Management",
  "description": "Homepage hero subtitle"
},
"homepage.hero.description": {
  "message": "ISO/IEC 5230 & 18974 Based\nEnterprise Open Source Management System Guide",
  "description": "Homepage hero description"
},
"homepage.hero.cta.docs": {
  "message": "Get Started",
  "description": "Homepage hero primary CTA button"
},
"homepage.hero.cta.aiCoding": {
  "message": "AI Coding Guide",
  "description": "Homepage hero secondary CTA button"
},
"homepage.cta.feature1.title": {
  "message": "Build Your System",
  "description": "CTA feature card 1 title"
},
"homepage.cta.feature1.desc": {
  "message": "Build an enterprise open source management system from scratch to completion, based on ISO/IEC 5230 & 18974.",
  "description": "CTA feature card 1 description"
},
"homepage.cta.feature1.link": {
  "message": "Start the Guide",
  "description": "CTA feature card 1 link label"
},
"homepage.cta.feature2.title": {
  "message": "DevSecOps",
  "description": "CTA feature card 2 title"
},
"homepage.cta.feature2.desc": {
  "message": "Integrate security into your development pipeline. Covers SAST, SCA, container security, and CI/CD automation.",
  "description": "CTA feature card 2 description"
},
"homepage.cta.feature2.link": {
  "message": "DevSecOps Guide",
  "description": "CTA feature card 2 link label"
},
"homepage.cta.feature3.title": {
  "message": "AI Coding",
  "description": "CTA feature card 3 title"
},
"homepage.cta.feature3.desc": {
  "message": "Manage AI coding tools like Claude Code, Cursor, and Copilot alongside open source compliance.",
  "description": "CTA feature card 3 description"
},
"homepage.cta.feature3.link": {
  "message": "AI Coding Guide",
  "description": "CTA feature card 3 link label"
},
"homepage.cta.section.title": {
  "message": "Start Managing Open Source Today",
  "description": "CTA section heading"
},
"homepage.cta.section.subtitle": {
  "message": "Complete your ISO/IEC 5230 & 18974 self-certification with this free guide from the OpenChain KWG community.",
  "description": "CTA section subtitle"
},
"homepage.cta.section.cta": {
  "message": "Get Started",
  "description": "CTA section button"
},
"homepage.meta.title": {
  "message": "Trusted OSS · Trusted Open Source Supply Chain Management",
  "description": "Homepage meta title"
},
"homepage.meta.description": {
  "message": "A practical guide to building an enterprise open source management system based on ISO/IEC 5230 & 18974",
  "description": "Homepage meta description"
}
```

---

## 문제 B — AI Coding 사이드바 누락 페이지 (2개)

아래 파일들이 `website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/`에 없어서 영어 전환 시 페이지가 표시되지 않습니다. 원본을 번역해서 생성하세요.

### B-1: `cicd-quick.mdx` 생성

**원본**: `website/ai-coding/cicd-quick.mdx`
**생성 경로**: `website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/cicd-quick.mdx`

front matter:

```yaml
---
id: cicd-quick
title: CI/CD Automation
sidebar_label: CI/CD Automation
sidebar_position: 5
---
```

본문: 원본 전체를 영어로 번역 (번역 규칙은 기존 지시문 동일)

### B-2: `rules-template.mdx` 생성

**원본**: `website/ai-coding/rules-template.mdx`
**생성 경로**: `website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/rules-template.mdx`

front matter:

```yaml
---
id: rules-template
title: Common Rules Template
sidebar_label: Common Rules Template
sidebar_position: 3
---
```

본문: 원본 전체를 영어로 번역

---

## 문제 C — DevSecOps 사이드바 누락 페이지 (4개)

아래 파일들이 `website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/`에 없습니다.

### C-1: `sast.mdx` 생성

**원본**: `website/devsecops/sast.mdx`
**생성 경로**: `website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/sast.mdx`

front matter:

```yaml
---
id: sast
title: Static Analysis (SAST)
sidebar_label: SAST
sidebar_position: 3
---
```

### C-2: `sca.mdx` 생성

**원본**: `website/devsecops/sca.mdx`
**생성 경로**: `website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/sca.mdx`

front matter:

```yaml
---
id: sca
title: Software Composition Analysis (SCA)
sidebar_label: SCA
sidebar_position: 4
---
```

### C-3: `secret-detection.mdx` 생성

**원본**: `website/devsecops/secret-detection.mdx`
**생성 경로**: `website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/secret-detection.mdx`

front matter:

```yaml
---
id: secret-detection
title: Secret Detection
sidebar_label: Secret Detection
sidebar_position: 5
---
```

### C-4: `iac-security.mdx` 생성

**원본**: `website/devsecops/iac-security.mdx`
**생성 경로**: `website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/iac-security.mdx`

front matter:

```yaml
---
id: iac-security
title: IaC Security
sidebar_label: IaC Security
sidebar_position: 7
---
```

---

## 공통 번역 규칙

B, C 파일 번역 시 기존 규칙 동일 준수:

- 코드 블록 내부 변경 금지
- ISO 표준 번호/섹션 번호 변경 금지 (`ISO/IEC 5230`, `3.1.1` 등)
- 브랜드명 변경 금지 (`OpenChain`, `SBOM`, `trustedoss` 등)
- 내부 링크 경로 변경 금지, 링크 텍스트만 번역

---

## 완료 후 검증

```bash
cd website && npm run build
```

빌드 성공 + `npm run start -- --locale en` 으로 아래 확인:

- 홈페이지 영어 표시
- AI Coding 사이드바 `Common Rules Template`, `CI/CD Automation` 표시
- DevSecOps 사이드바 `SAST`, `SCA`, `Secret Detection`, `IaC Security` 표시
