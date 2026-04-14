# trustedoss Claude Code 하네스 운영 가이드

> 이 문서는 프로젝트 기여자와 유지보수자를 위한 내부 운영 가이드입니다.  
> 콘텐츠 독자(셀프스터디 사용자)가 읽을 필요는 없습니다.

---

## 목차

1. [하네스 전체 구조](#1-하네스-전체-구조)
2. [슬래시 커맨드 레퍼런스](#2-슬래시-커맨드-레퍼런스)
3. [에이전트 레퍼런스](#3-에이전트-레퍼런스)
4. [스크립트 레퍼런스](#4-스크립트-레퍼런스)
5. [시나리오별 사용 예시](#5-시나리오별-사용-예시)
6. [KWG 원본 가이드 동기화](#6-kwg-원본-가이드-동기화)
7. [토큰 절약 원칙](#7-토큰-절약-원칙)
8. [트러블슈팅](#8-트러블슈팅)

---

## 1. 하네스 전체 구조

```
.claude/
├── CLAUDE.md                         # (루트) 프로젝트 전체 규칙
├── settings.json                     # 권한 + PostToolUse 훅 3개
├── progress.md                       # 작업 이력 (자동 추가)
├── progress-infra.md                 # 인프라 변경 이력 (자동 추가)
│
├── agents/                           # Claude Code 서브에이전트
│   ├── qa-reviewer.md   [탐지]       # 품질 이슈 6종 탐지
│   ├── doc-fixer.md     [수정]       # 자동 수정 가능 이슈 교정
│   ├── iso-verifier.md  [검증]       # output/ ISO 정합성 판정
│   └── content-auditor.md [감사]    # 챕터 완성도 10점 평가
│
├── skills/                           # 슬래시 커맨드 정의
│   ├── qa-loop/skill.md              # /qa  — QA 오케스트레이터
│   ├── diff-scope/skill.md           # /diff-scope — 변경 범위 계산
│   ├── create-doc.md                 # 문서 작성 표준 (직접 읽기용)
│   ├── validate-checklist.md         # 인증 체크리스트 검증
│   ├── generate-report.md            # 리포트 생성 표준
│   └── update-reference-samples/skill.md  # /update-reference-samples
│
├── scripts/
│   ├── verify.sh                     # 8가지 정적 검증 (항상 마지막에 실행)
│   ├── test-coverage.py              # ISO 커버리지 정합성 4종 테스트
│   ├── check-admonition.js           # PostToolUse 즉시 admonition 경고
│   ├── fix-style.py                  # 스타일 자동 수정
│   ├── sync-output-samples.sh        # output/ → output-sample/ 동기화
│   └── sync-kwg-reference.sh         # KWG 원본 md 파일 동기화
│
└── reference/
    ├── iso-5230.md                   # ISO/IEC 5230 전문
    ├── iso-18974.md                  # ISO/IEC 18974 전문
    └── kwg/                          # KWG 원본 가이드 (sync-kwg-reference.sh로 갱신)
        ├── README.md
        ├── content/ko/guide/
        │   ├── opensource_for_enterprise/  # 기업 오픈소스 관리 가이드
        │   │   ├── 0-openchain/
        │   │   ├── 1-teams/
        │   │   ├── 2-policy/
        │   │   ├── 3-process/
        │   │   ├── 4-tool/
        │   │   ├── 5-training/
        │   │   └── 6-conforming/
        │   ├── templates/              # KWG 정책·프로세스 템플릿
        │   │   ├── 1-policy/
        │   │   └── 2-process-template/
        │   └── tools/                  # SBOM·취약점 도구 가이드
        │       ├── 1-fossology/
        │       ├── 2-sw360/
        │       ├── 3-fosslight/
        │       ├── 4-osvscalibr/
        │       ├── 5-cdxgen/
        │       ├── 6-syft/
        │       └── 7-dependency-track/
        └── .sync-meta                  # 마지막 동기화 날짜 기록
```

### 역할 분리 원칙

| 계층          | 담당           | 설명                                  |
| ------------- | -------------- | ------------------------------------- |
| **skills**    | 오케스트레이션 | 여러 에이전트를 순서대로 조율         |
| **agents**    | 전문 처리      | 단일 책임 (탐지 / 수정 / 검증 / 감사) |
| **scripts**   | 정적 자동화    | Claude 없이 실행되는 쉘/파이썬 검사   |
| **hooks**     | 즉각 피드백    | 파일 저장 직후 자동 경고              |
| **reference** | 컨텍스트 제공  | ISO 스펙, KWG 원본 가이드             |

---

## 2. 슬래시 커맨드 레퍼런스

### `/qa` — QA 전체 파이프라인

```
/qa [대상]
```

| 대상                    | 동작                                         |
| ----------------------- | -------------------------------------------- |
| _(없음)_ 또는 `changed` | 미커밋 변경 파일만 검사 **(일상 사용 권장)** |
| `all`                   | docs/, agents/, templates/ 전체 스캔         |
| `03` ~ `08` (챕터 번호) | 해당 챕터 완성도 감사                        |
| `iso`                   | output/ ISO G항목 정합성 검증                |
| `iso changed`           | 변경된 output 파일만 ISO 검증                |
| 파일 경로               | 특정 파일 1개 검사                           |

**내부 실행 순서:**

```
[1] diff-scope   → 변경 파일 목록 계산
[2] qa-reviewer  → 6종 이슈 탐지
[3] doc-fixer    → 자동 수정 (이슈 있을 때만)
[4] verify.sh    → 8/8 정적 검증
[5] 보고         → 수동 처리 필요 항목 출력
```

**예시:**

```bash
/qa                    # 빠른 일상 검사
/qa all                # 전체 리팩토링 후 전체 검사
/qa docs/03-policy/index.md   # 특정 파일만
/qa 05                 # 05 도구 챕터 완성도 감사
/qa iso                # output/ 산출물 ISO 정합성 검증
```

---

### `/diff-scope` — 변경 범위 계산

`/qa` 내부에서 자동 호출. 직접 사용 시:

```
/diff-scope [staged | unstaged | last-commit | all]
```

변경된 파일 목록과 범위 요약을 출력한다.
`/qa` 전에 어떤 파일이 처리 대상인지 미리 확인하고 싶을 때 유용.

---

### `/update-reference-samples` — 샘플 페이지 재생성

output-sample/ 파일 변경 후 website/reference/samples/ 를 최신화할 때 사용.

```bash
# 전체 워크플로우
bash .claude/scripts/sync-output-samples.sh    # output/ → output-sample/ 동기화
/update-reference-samples                       # 샘플 페이지 재생성
bash .claude/scripts/verify.sh                 # 검증
```

---

## 3. 에이전트 레퍼런스

에이전트는 `/qa` 커맨드를 통해 자동 호출된다. 아래는 직접 호출이 필요한 특수 상황용 참조.

### `@qa-reviewer` — 품질 이슈 탐지

**직접 호출 예시:**

```
@qa-reviewer docs/03-policy/index.md
@qa-reviewer all
```

**탐지하는 이슈 유형:**

| 코드            | 이슈 유형                        | 예시                          |
| --------------- | -------------------------------- | ----------------------------- |
| `YAML_QUOTE`    | front matter 콜론 값 따옴표 없음 | `title: 정책: 관리`           |
| `ADMONITION`    | cd agents/ 직전 tip 블록 없음    | bash 블록 직전 누락           |
| `ISO18974_NUM`  | 18974 문서에 §3.x.x 사용         | §3.4.1 → §4.4.1               |
| `LOCAL_PATH`    | 사용자명 포함 경로 노출          | 사용자명 포함 절대경로        |
| `BROKEN_LINK`   | 내부 링크 대상 파일 없음         | `[링크](../없는파일.md)`      |
| `SECTION_ORDER` | 섹션 순서 위반                   | 완료확인이 다음단계 뒤에 위치 |

- **자동 수정 가능**: YAML_QUOTE, ADMONITION, ISO18974_NUM, LOCAL_PATH
- **수동 처리 필요**: BROKEN_LINK, SECTION_ORDER

---

### `@doc-fixer` — 자동 교정

보통 `/qa`를 통해 qa-reviewer 결과를 자동으로 전달받아 실행됨.

직접 호출 시 qa-reviewer 리포트를 붙여넣기:

```
@doc-fixer
[qa-reviewer 이슈 리포트 붙여넣기]
```

**주의**: BROKEN_LINK, SECTION_ORDER는 수정하지 않는다. 해당 항목은 사람이 판단해야 한다.

---

### `@iso-verifier` — ISO 정합성 검증

output/ 산출물이 ISO G항목을 실제로 충족하는지 판정.

```
@iso-verifier changed     # 변경된 output 파일만
@iso-verifier all         # output/ 전체
@iso-verifier G2.2        # 특정 G항목만
@iso-verifier output/process/vulnerability-response.md
```

**판정 기준:**

- ✅ 충족: 파일 존재 + 필수 섹션 + 핵심 내용 충족
- ⚠️ 부분충족: 파일 있으나 일부 누락
- ❌ 미충족: 파일 없음 또는 빈 파일

---

### `@content-auditor` — 챕터 완성도 감사

새 챕터 추가 후 또는 챕터 개정 후 실행.

```
@content-auditor 03       # 03-policy 챕터 감사
@content-auditor all      # 전체 챕터 순차 감사
```

**평가 기준 (10점 만점):**

- G항목 설명 충족: 3점
- 이유 설명 충족: 2점
- 입증자료 링크: 2점
- 구조 품질 6항목: 3점

---

## 4. 스크립트 레퍼런스

### `verify.sh` — 8가지 정적 검증

```bash
bash .claude/scripts/verify.sh
```

모든 파일 생성·수정 후 **반드시** 실행. 8/8 PASS 후에만 push 가능.

| #   | 항목              | 핵심                        |
| --- | ----------------- | --------------------------- |
| 1   | Docusaurus 빌드   | MDX 구문 오류 탐지          |
| 2   | 내부 링크         | 상대 경로 파일 존재 확인    |
| 3   | Front matter YAML | 콜론 포함 값 따옴표 확인    |
| 4   | 필수 파일 존재    | 13개 핵심 파일 확인         |
| 5   | 로컬 경로 노출    | `/Users/username` 탐지      |
| 6   | 18974 섹션 번호   | §3.x.x 혼용 탐지            |
| 7   | Admonition 누락   | cd agents/ 직전 :::tip 확인 |
| 8   | ISO 커버리지      | test-coverage.py 실행       |

---

### `test-coverage.py` — ISO 커버리지 정합성

```bash
python3 .claude/scripts/test-coverage.py
```

`verify.sh` [8/8] 항목이 내부적으로 실행. 독립 실행도 가능.

| 검사 | 내용                                          |
| ---- | --------------------------------------------- |
| A    | G항목 ↔ 담당 Agent 할당                       |
| B    | G항목 ↔ output 파일 할당                      |
| C    | checklist-mapping ↔ validate-checklist 일관성 |
| D    | agents CLAUDE.md → templates/ 파일 존재       |

---

### `sync-kwg-reference.sh` — KWG 원본 동기화

```bash
# 기본 실행 (rate limit: 60 req/hour)
bash .claude/scripts/sync-kwg-reference.sh

# 토큰 인증 실행 (rate limit: 5000 req/hour, 권장)
GITHUB_TOKEN=ghp_xxx bash .claude/scripts/sync-kwg-reference.sh
```

KWG GitHub 원본에서 `.md` 파일만 `.claude/reference/kwg/` 에 동기화한다.
동기화 주기: KWG 원본 업데이트 시 또는 분기별 1회 권장.

---

### `sync-output-samples.sh` — 산출물 샘플 동기화

```bash
bash .claude/scripts/sync-output-samples.sh
```

`output/` → `output-sample/` 단방향 동기화. `/update-reference-samples` 실행 전 선행.

---

### `check-admonition.js` — PostToolUse 즉시 경고

`settings.json` Hook으로 자동 실행. 직접 실행 불필요.

docs/ 파일 저장 시 `cd agents/` 블록 직전 `:::tip 실행 전 확인`이 없으면 즉시 경고 출력.

---

## 5. 시나리오별 사용 예시

### 시나리오 A — 일상적인 문서 수정 후 QA

```
상황: docs/03-policy/index.md 내용 수정 완료
```

```bash
# 세션 내에서 한 번 실행
/qa changed
```

예상 출력:

```
[1] 변경 파일: docs/03-policy/index.md (1개)
[2] qa-reviewer 실행 중...
    이슈 2건:
    - YAML_QUOTE: title 값 따옴표 없음 (3번 줄)
    - ADMONITION: cd agents/03 직전 누락 (87번 줄)
[3] doc-fixer 실행 중... 2건 자동 수정
[4] verify.sh: 8/8 PASS
✅ QA 완료 — 수동 처리 항목 없음
```

---

### 시나리오 B — 새 챕터 추가 후 완성도 확인

```
상황: docs/09-newchapter/ 신규 작성 완료
```

```bash
/qa 09            # 챕터 완성도 감사
/qa changed       # 품질 이슈 검사 및 자동 수정
bash .claude/scripts/verify.sh  # 최종 확인
```

예상 출력 (content-auditor):

```
## 챕터 완성도 감사 리포트
챕터: 09-newchapter
종합 점수: 7/10

개선 권고:
1. [중요] G항목 이유 설명 미흡 — 실제 사례 추가 필요
2. [선택] 입증자료 링크 누락 — /reference/samples/ 연결 필요
```

---

### 시나리오 C — output/ 산출물 생성 후 ISO 정합성 검증

```
상황: agents/04-process-designer 실행 → output/process/ 파일 생성
```

```bash
/qa iso changed   # 변경된 output 파일만 ISO 검증
```

예상 출력:

```
| G3L.1 | output/process/usage-approval.md | ✅ 충족 |
| G3L.5 | output/process/vulnerability-response.md | ⚠️ 부분충족 | CVD §8 없음 |
| G3L.6 | output/process/contribution-process.md | ✅ 충족 |

권고: G3L.5 부분충족 — vulnerability-response.md에 CVD §8 추가 필요
```

---

### 시나리오 D — 전체 리팩토링 후 점검

```
상황: templates/ 일괄 수정, 여러 docs/ 챕터 업데이트
```

```bash
/qa all                           # 전체 품질 이슈 검사
/qa iso                           # 전체 ISO 정합성 검증
bash .claude/scripts/verify.sh   # 8/8 최종 확인
```

> ⚠️ `/qa all`은 파일 수가 많아 토큰 소비가 크다. 개별 수정 후에는 `/qa changed` 사용 권장.

---

### 시나리오 E — 샘플 페이지 업데이트

```
상황: agents 실행으로 output/ 갱신 → website 샘플 최신화 필요
```

```bash
# 1. 산출물 동기화
bash .claude/scripts/sync-output-samples.sh

# 2. 샘플 페이지 재생성
/update-reference-samples

# 3. 검증
bash .claude/scripts/verify.sh
```

---

### 시나리오 F — KWG 원본 가이드 참조

```
상황: templates/ 갭 분석 시 KWG 원본과 비교 필요
```

```bash
# KWG 원본 최신화
bash .claude/scripts/sync-kwg-reference.sh
```

이후 Claude에게 참조 지시:

```
.claude/reference/kwg/content/ko/guide/templates/1-policy/_index.md 를 읽고
우리 templates/policy/oss-policy.md 와 비교해줘
```

---

### 시나리오 G — 세션 종료 전 체크리스트

```bash
# 1. QA 및 검증
/qa changed
bash .claude/scripts/verify.sh   # 8/8 PASS 확인

# 2. 진행 상황 업데이트
# .claude/progress.md 갱신 (작업 내용 요약 추가)

# 3. 커밋
git add -p
git commit -m "docs: ..."
```

---

## 6. KWG 원본 가이드 동기화

### 왜 필요한가

trustedoss의 templates/와 agents/는 KWG Working Group의 갭 분석 결과를 반영해 구현되었다.
KWG 원본이 업데이트될 때 우리 콘텐츠가 뒤처지지 않으려면 주기적으로 원본과 비교해야 한다.

### 동기화 주기

| 상황                   | 권장 주기  |
| ---------------------- | ---------- |
| KWG 공식 업데이트 알림 | 즉시       |
| 정기 유지보수          | 분기별 1회 |
| 갭 분석 작업 시        | 작업 직전  |

### 동기화 후 활용

```
# KWG 정책 템플릿과 우리 templates/ 비교
.claude/reference/kwg/content/ko/guide/templates/1-policy/_index.md 를 읽고
templates/policy/oss-policy.md 와 어떤 항목이 다른지 비교해줘

# KWG 도구 가이드 확인
.claude/reference/kwg/content/ko/guide/tools/3-fosslight/_index.md 를 읽고
docs/05-tools/index.md 에 반영이 필요한 내용이 있는지 확인해줘

# 기업 가이드 최신 변경사항 확인
.claude/reference/kwg/content/ko/guide/opensource_for_enterprise/3-process/_index.md
를 읽고 우리 04-process 챕터와 차이점을 정리해줘
```

### 동기화 대상 디렉토리

| KWG 원본 경로                   | 내용                           | 우리 매핑          |
| ------------------------------- | ------------------------------ | ------------------ |
| `opensource_for_enterprise/`    | 기업 오픈소스 관리 전체 가이드 | docs/ 챕터 전체    |
| `templates/1-policy/`           | 오픈소스 정책 문서 템플릿      | templates/policy/  |
| `templates/2-process-template/` | 프로세스 문서 템플릿           | templates/process/ |
| `tools/`                        | SBOM·취약점 도구 7종 가이드    | docs/05-tools/     |

---

## 7. 토큰 절약 원칙

### 기본 원칙

1. **증분 처리**: 변경된 파일만 처리 (`/qa changed` 기본값)
2. **단일 책임**: 에이전트 1개가 1가지 작업만 (qa-reviewer는 탐지만, doc-fixer는 수정만)
3. **최소 Read**: 파일 전체 대신 필요한 섹션만 읽음
4. **조기 종료**: 이슈 0건이면 doc-fixer·verify.sh 건너뜀

### 에이전트별 토큰 최적화

| 에이전트        | 최적화 방법                                       |
| --------------- | ------------------------------------------------- |
| qa-reviewer     | 파일 목록만 받아 처리 (전체 스캔 금지)            |
| doc-fixer       | 파일 1개 단위로 Read → Edit (한 번에 여러 파일 X) |
| iso-verifier    | `changed` 모드 기본, 변경 없는 G항목 재검증 안 함 |
| content-auditor | ISO 스펙에서 해당 챕터 섹션만 Read                |

### 상황별 커맨드 선택

| 상황             | 사용 커맨드       | 토큰               |
| ---------------- | ----------------- | ------------------ |
| 파일 1~3개 수정  | `/qa changed`     | 최소               |
| 챕터 완성도 확인 | `/qa 03`          | 중간               |
| ISO 정합성 확인  | `/qa iso changed` | 중간               |
| 전체 리팩토링    | `/qa all`         | 최대 (가급적 피함) |

---

## 8. 트러블슈팅

### verify.sh FAIL 항목별 대응

| FAIL 항목        | 즉각 대응                                                  |
| ---------------- | ---------------------------------------------------------- |
| [1] 빌드 실패    | MDX 구문 오류. `:::` admonition 괄호, `{` 중괄호 확인      |
| [2] 내부 링크    | 파일 경로 오타. 상대경로 기준 확인                         |
| [3] Front matter | 콜론 포함 값 따옴표 추가. `/qa changed`로 자동 수정        |
| [4] 필수 파일    | `.claude/scripts/verify.sh` L4 목록 확인 후 누락 파일 생성 |
| [5] 로컬 경로    | `/qa changed`로 LOCAL_PATH 자동 수정                       |
| [6] 18974 섹션   | `/qa changed`로 ISO18974_NUM 자동 수정                     |
| [7] Admonition   | `/qa changed`로 ADMONITION 자동 수정                       |
| [8] ISO 커버리지 | `python3 .claude/scripts/test-coverage.py` 상세 오류 확인  |

---

### PostToolUse 훅 경고 이해

파일 저장 직후 아래 경고가 나타나면:

```
⚠️  [check-admonition] docs/03-policy/index.md
   라인 87: cd agents/ 블록 직전에 :::tip 실행 전 확인 admonition 없음.
```

바로 `/qa docs/03-policy/index.md`를 실행하면 자동 수정된다.

---

### KWG 동기화 rate limit 오류

```
⚠️  API 오류: content/ko/guide/... (rate limit 또는 경로 오류)
```

대응:

1. 60분 대기 후 재시도
2. 또는 GitHub Personal Access Token 사용:
   ```bash
   GITHUB_TOKEN=ghp_xxx bash .claude/scripts/sync-kwg-reference.sh
   ```
   Token 생성: GitHub Settings → Developer settings → Personal access tokens (read:public 권한으로 충분)

---

### `/qa` 후 `수동 처리 필요` 항목 대응

| 유형                            | 대응 방법                                     |
| ------------------------------- | --------------------------------------------- |
| BROKEN_LINK                     | 링크 경로 직접 수정. 파일 이동 또는 링크 교정 |
| SECTION_ORDER                   | 해당 문서를 열어 섹션 순서 직접 재배치        |
| verify.sh FAIL (자동 수정 불가) | 항목별 위 표 참조                             |

---

_이 문서는 `.claude/harness-guide.md` 에 저장됩니다._  
_하네스 구조 변경 시 이 문서도 함께 업데이트하세요._
