# Cursor 작업 지시문 — README 이중 언어화 + 문서 완성도 점검

아래 작업을 순서대로 수행하세요.

---

## 작업 1 — README.md 이중 언어 변환 (Option B)

현재 `README.md`는 한국어 단일 언어입니다.
**파일 1개에 한/영 두 언어를 모두 담는 구조**로 변환합니다.

### 구조 규칙

```markdown
<!-- 상단 뱃지 3개 (현재 그대로 유지) -->

[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# Trusted OSS

... (현재 한국어 내용 그대로) ...

---

<a id="english"></a>

# Trusted OSS — English

... (한국어 내용을 영어로 번역) ...
```

### 번역 지침 (영어 섹션)

- 한국어 섹션의 모든 내용을 영어로 번역
- 테이블, 코드 블록 구조 동일하게 유지
- 코드 블록 내 셸 명령어는 번역하지 않음
- 단, 코드 블록 내 주석(`# "어디서 시작해야 해?" 입력`)은 영어로 번역
- URL과 뱃지는 그대로 유지 (단, 웹사이트 링크에 `/en` 경로 버전도 병기 가능)
- 브랜드명 변경 금지: `trustedoss`, `OpenChain`, `KWG`, `SBOM`, `Claude Code` 등

### 영어 섹션 번역 참고 용어

| 한국어           | English                     |
| ---------------- | --------------------------- |
| 체계구축         | Build Your System           |
| 빠른 시작        | Quick Start                 |
| 저장소 구조      | Repository Structure        |
| 최종 산출물 목록 | Deliverables                |
| 기여 방법        | Contributing                |
| 라이선스         | License                     |
| Agent 목록       | Agent List                  |
| 셀프스터디       | Self-study                  |
| 오픈소스 담당자  | Open Source Program Manager |
| 챕터 목록        | Chapter List                |

---

## 작업 2 — CONTRIBUTING.md 이중 언어 변환

현재 `CONTRIBUTING.md`는 한국어 단일 언어입니다.
README.md와 동일한 구조로 이중 언어화하세요.

```markdown
[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# 기여 가이드

... (현재 한국어 내용 그대로) ...

---

<a id="english"></a>

# Contributing Guide

... (한국어 내용을 영어로 번역) ...
```

번역 지침은 작업 1과 동일합니다.
코드 블록 내 셸 명령어와 경로는 변경하지 않습니다.

---

## 작업 3 — STYLEGUIDE.md 교체

현재 `STYLEGUIDE.md`는 **React Native 문서 스타일 가이드**가 잘못 들어있습니다.
이 프로젝트(`trustedoss`)에 맞는 문서 스타일 가이드로 완전히 교체하세요.

### 작성 내용

이 프로젝트는 ISO/IEC 5230 & 18974 오픈소스 컴플라이언스 가이드 사이트입니다.
아래 항목을 포함하는 **한/영 이중 언어** STYLEGUIDE.md를 작성하세요.

```markdown
[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# 문서 스타일 가이드

## 1. 문서 구조 원칙

## 2. 언어·용어 규칙

## 3. 코드 블록 규칙

## 4. 링크 규칙

## 5. front matter 규칙

## 6. ISO 표준 번호 표기 규칙

---

<a id="english"></a>

# Documentation Style Guide

(한국어 섹션의 영어 번역)
```

#### 포함해야 할 내용 상세

**1. 문서 구조 원칙**

- what(무엇을)/why(왜)/how(어떻게) 3단 구성
- 입증 자료(ISO G항목 참조) 명시 원칙

**2. 언어·용어 규칙**

- 한국어 원본 기준 공식 용어 (오픈소스 정책, 프로세스, 자체 인증 등)
- 영어 번역 대응 용어표 (아래 용어집 포함):

| 한국어            | English                          |
| ----------------- | -------------------------------- |
| 오픈소스 정책     | Open Source Policy               |
| 오픈소스 프로세스 | Open Source Process              |
| 조직 구성         | Organizational Structure         |
| 교육 체계         | Training Program                 |
| 자체 인증         | Self-Certification / Conformance |
| 산출물            | Deliverables                     |
| 고지문            | Attribution Notice               |
| 취약점 분석       | Vulnerability Analysis           |
| 컴플라이언스      | Compliance                       |

**3. 코드 블록 규칙**

- 번역 시 코드 블록 내부 변경 금지
- 코드 블록 내 주석은 번역 가능

**4. 링크 규칙**

- 절대 경로 vs 상대 경로 사용 기준
- docs → reference 크로스 링크 형식 (`/reference/samples/...`)
- 로컬 경로(사용자명 포함) 사용 금지

**5. front matter 규칙**

- 필수 키: `id`, `title`, `sidebar_label`, `sidebar_position`
- 영어 번역 파일에서 번역하는 값 / 유지하는 값 구분

**6. ISO 표준 번호 표기 규칙**

- ISO/IEC 5230: `3.x.x` 체계
- ISO/IEC 18974: `4.x.x` 체계
- 혼용 금지

---

## 작업 4 — 영어 번역 파일 완성도 점검

`website/i18n/en/` 하위 모든 파일을 대상으로 아래 체크리스트를 수행하세요.

### 체크 항목

#### A. 한국어 잔류 검색

아래 패턴을 검색하여 발견된 항목은 모두 영어로 수정하세요.

```bash
# 실행 명령 (참고용)
grep -rn "[가-힣]" website/i18n/en/ --include="*.md" --include="*.mdx" --include="*.json"
```

단, 아래 경우는 **수정하지 않습니다**:

- 코드 블록 안의 셸 명령어 주석 (`# 매주 월요일 오전 9시` 등 cron 관련)
- `# "어디서 시작해야 해?" 입력` — 실제 Claude에 입력해야 하는 한국어 명령어

위 2가지 예외를 제외한 모든 한국어 잔류 텍스트는 영어로 번역하세요.

#### B. Markdown 문법 이상 재확인

```bash
grep -rn "\* \*\|\] (" website/i18n/en/ --include="*.md" --include="*.mdx"
```

발견되면 수정 (bold 깨짐, 링크 깨짐).

#### C. 번역 일관성 검토

아래 용어가 파일 전반에서 일관되게 번역됐는지 확인하세요:

| 한국어 원문   | 올바른 영어        | 잘못된 예                          |
| ------------- | ------------------ | ---------------------------------- |
| 자체 인증     | Self-Certification | Self-Declaration, Self-Attestation |
| 체계구축      | Build Your System  | System Building, Framework Setup   |
| 산출물        | Deliverables       | Outputs, Artifacts                 |
| 오픈소스 정책 | Open Source Policy | OSS Policy                         |
| 담당자        | Program Manager    | Person in Charge, Manager          |

불일치 발견 시 올바른 번역으로 통일하세요.

#### D. 누락 번역 확인

`website/i18n/en/` 파일 목록과 원본(`docs/`, `website/ai-coding/`, `website/devsecops/`, `website/reference/`) 파일 목록을 대조하여 누락된 파일이 없는지 확인하세요.

---

## 완료 후 검증

```bash
cd website && npm run build
```

빌드 성공 확인 후 아래도 확인:

- `README.md`: 언어 전환 앵커 링크(`#한국어`, `#english`) 동작 확인
- `CONTRIBUTING.md`: 동일 확인
- `STYLEGUIDE.md`: trustedoss 관련 내용으로 교체됐는지 확인
- 영어 사이트(`npm run start -- --locale en`)에서 한국어 잔류 없는지 확인
