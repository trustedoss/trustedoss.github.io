# Tests

검증 스크립트는 `.claude/scripts/`에 위치합니다.

## 주요 스크립트

| 스크립트                  | 역할                                     | 실행 방법                                         |
| ------------------------- | ---------------------------------------- | ------------------------------------------------- |
| `verify.sh`               | 전체 검증 (11개 항목) — push 전 필수     | `bash .claude/scripts/verify.sh`                  |
| `validate-output.py`      | output/ 산출물 완전성 상세 확인          | `python3 .claude/scripts/validate-output.py`      |
| `test-coverage.py`        | ISO G항목 커버리지 정합성                | `python3 .claude/scripts/test-coverage.py`        |
| `test-agent-specs.py`     | Agent CLAUDE.md 스펙 구조 검증 (Layer 1) | `python3 .claude/scripts/test-agent-specs.py`     |
| `test-output-fixtures.py` | 골든 픽스처 회귀 테스트 (Layer 2)        | `python3 .claude/scripts/test-output-fixtures.py` |

## 일반 사용법

파일을 생성하거나 수정한 뒤:

```bash
bash .claude/scripts/verify.sh
```

모든 항목이 `PASS`여야 push할 수 있습니다. 상세 기준은 `CONTRIBUTING.md` 참조.

---

## 셀프스터디 Agent 자동화 테스트 (Layer 1 + 2)

### Layer 1: Agent 스펙 구조 검증

9개 셀프스터디 agent의 `CLAUDE.md`를 파싱하여 스펙이 올바르게 정의되어 있는지 검증합니다.

```bash
python3 .claude/scripts/test-agent-specs.py
```

**검증 항목:**

- 모든 agent에 `CLAUDE.md` 존재
- 각 `CLAUDE.md`에 `세션 시작 시 동작`, `## 입력 질문`, `## 출력 산출물` 선언
- 출력 산출물 선언이 `validate-output.py` 필수 파일 목록과 일치
- 참조된 `templates/` 파일 실제 존재 여부 (미존재 시 WARNING)

**판정 기준:**

- `FAIL`: 필수 구문 누락, 출력 파일 미선언
- `WARN`: 템플릿 파일 없음 (agent가 동적 생성할 수 있는 경우)

### Layer 2: 골든 픽스처 회귀 테스트

`output-sample/`을 임시 디렉토리에 복사하여 `validate-output.py`가 PASS하는지 검증합니다.

```bash
python3 .claude/scripts/test-output-fixtures.py
```

**동작 방식:**

1. `output-sample/` → 임시 디렉토리 복사
2. `.cdx.json` 픽스처 파일 자동 보완
3. `validate-output.py` 실행 (환경변수 `TRUSTEDOSS_OUTPUT_DIR` 활용)
4. 결과 PASS/FAIL 판정

**목적:**

- `output-sample/`이 실제로 유효한 골든 픽스처임을 보장
- 향후 agent 출력 스펙 변경 시 회귀 탐지
- `validate-output.py` 자체 정확성 검증

### verify.sh 통합

두 테스트 모두 `verify.sh`에 `[10/11]`, `[11/11]` 항목으로 통합되어 있습니다.

---

## Layer 3: LLM 기반 E2E 대화 테스트

Anthropic API를 사용해 각 agent의 실제 대화 흐름을 시뮬레이션하고
기대 파일 생성 여부 및 내용 패턴을 검증합니다.

### 사전 준비

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

### 실행 방법

```bash
# 단일 agent 테스트
python3 .claude/scripts/test-agent-e2e.py --agent 02-organization-designer

# 특정 fixture 파일로 테스트 (조건부 분기 등)
python3 .claude/scripts/test-agent-e2e.py --fixture tests/fixtures/04-process-designer-branch-A.json
python3 .claude/scripts/test-agent-e2e.py --fixture tests/fixtures/04-process-designer-branch-B.json

# 전체 fixture 실행
python3 .claude/scripts/test-agent-e2e.py --all

# 상세 출력 (도구 호출 흐름 확인)
python3 .claude/scripts/test-agent-e2e.py --agent 02-organization-designer --verbose
```

### 동작 방식

1. `tests/fixtures/*.json` 픽스처 로드
2. agent의 `CLAUDE.md` → system_prompt 설정
3. `prerequisite_files`를 `output-sample/`에서 임시 디렉토리로 복사
4. Anthropic API 멀티턴 대화 시작 (Write/Read/Edit/Bash mock 도구 제공)
5. LLM 질문 → fixture `inputs[i]` 자동 답변
6. LLM Write 도구 호출 → 임시 디렉토리에 파일 저장
7. `expected_files` 존재 / `expected_absent` 미존재 / `content_patterns` 내용 검증

### 픽스처 파일

| 파일                                | 설명                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| `02-organization-designer.json`     | 조직 산출물 생성 기본 케이스                                 |
| `03-policy-generator.json`          | 정책 문서 생성                                               |
| `04-process-designer-branch-A.json` | 프로세스 설계 — 기여+공개 둘 다 활성화                       |
| `04-process-designer-branch-B.json` | 프로세스 설계 — 기여+공개 둘 다 비활성화                     |
| `04-process-designer-openwave.json` | 프로세스 설계 — OpenWave: 기여만(Q5=예)·공개 없음(Q6=아니오) |
| `05-sbom-guide.json`                | SBOM 가이드 — Docker 없음, 샘플 SBOM 사용                    |
| `05-sbom-analyst.json`              | SBOM 라이선스 분석 (SaaS 배포)                               |
| `05-sbom-management.json`           | SBOM 관리 계획 — 납품처 있음(Q1=예), CycloneDX               |
| `05-sbom-management-openwave.json`  | SBOM 관리 계획 — OpenWave: 납품처 없음(Q1=아니오), SaaS      |
| `05-vulnerability-analyst.json`     | 취약점 분석 리포트                                           |
| `06-training-manager.json`          | 교육 커리큘럼 생성                                           |
| `07-conformance-preparer.json`      | 갭 분석 및 인증 선언문                                       |

**OpenWave 분기 fixture 의도**: `04-process-designer-openwave`·`05-sbom-management-openwave`는 정적 시뮬레이션(Phase 2 B안)에서 수정한 조건 분기 로직을 실제로 검증하기 위해 추가되었습니다.

### 주의 사항

- API 비용 발생 (Sonnet 4.6 기준, agent당 약 $0.10~0.30 예상)
- `verify.sh`에는 포함하지 않음 — 별도 실행 필요
- GitHub Actions: `agent-e2e-test.yml` 워크플로우로 수동 실행 또는 `agents/*/CLAUDE.md` 변경 시 자동 실행
- `ANTHROPIC_API_KEY` secret 필요 (GitHub Settings → Secrets)

---

## 어떤 Layer를 언제 실행해야 하나?

### Layer별 보장 범위

| 검증 항목                                 | Layer 1 | Layer 2 | Layer 3 |
| ----------------------------------------- | :-----: | :-----: | :-----: |
| CLAUDE.md 필수 구문 존재                  |   ✅    |    —    |    —    |
| 출력 파일 목록 선언 일치                  |   ✅    |    —    |    —    |
| `templates/` 파일 실존                    |   ✅    |    —    |    —    |
| `output-sample/` 파일 완전성              |    —    |   ✅    |    —    |
| `validate-output.py` 자체 정확성          |    —    |   ✅    |    —    |
| LLM이 실제로 올바른 질문을 하는가         |   ❌    |   ❌    |   ✅    |
| 조건부 분기 실제 동작 (Q5=예 → 파일 생성) |   ❌    |   ❌    |   ✅    |
| 사용자 답변이 파일 내용에 반영되는가      |   ❌    |   ❌    |   ✅    |
| Write 도구를 실제로 호출하는가            |   ❌    |   ❌    |   ✅    |

Layer 1·2는 **정적 분석(linting)** 에 해당합니다.
"문서가 올바르게 작성되어 있는가"는 보장하지만, "LLM이 실제로 올바르게 동작하는가"는 보장하지 못합니다.

### 상황별 실행 가이드

| 상황                                  | Layer 1+2 | Layer 3  |
| ------------------------------------- | :-------: | :------: |
| 일상적인 docs/ 수정, 링크·표현 교정   |  ✅ 필수  |  불필요  |
| `output-sample/` 내용 갱신            |  ✅ 필수  |  불필요  |
| `templates/` 파일 추가·수정           |  ✅ 필수  |  불필요  |
| agent `CLAUDE.md` 소폭 수정           |  ✅ 필수  |   권장   |
| agent `CLAUDE.md` 질문 순서·분기 변경 |  ✅ 필수  | **필수** |
| 새 agent 추가                         |  ✅ 필수  | **필수** |
| 릴리즈 전 최종 검증                   |  ✅ 필수  | **필수** |

### 권장 운영 방식

```
일상 push        →  bash .claude/scripts/verify.sh  (Layer 1+2 포함)
agents/ CLAUDE.md 수정  →  Layer 3 단일 agent 추가 실행
릴리즈 전        →  python3 .claude/scripts/test-agent-e2e.py --all
```

---

## 드라이런 — OpenWave 프로필 체인 테스트

OpenWave 스타트업 프로필(SaaS·Python/pip·GitHub Actions·2주 배포·기여 계획 있음)을 기준으로
agent 02~07 전체 체인을 테스트하는 전용 시스템입니다.

### 구성 파일

| 파일                                                    | 역할                           |
| ------------------------------------------------------- | ------------------------------ |
| `dry-run/run-dryrun.sh`                                 | 드라이런 오케스트레이터        |
| `.claude/scripts/validate-chain.py`                     | agent 체인 전제 조건 연결 검증 |
| `tests/fixtures/*-openwave.json` + `05-sbom-guide.json` | OpenWave 특화 fixture          |

### 사용법

```bash
# 1. 체인 연결 검증만 (API 불필요, 즉시 실행)
bash dry-run/run-dryrun.sh --chain-only

# 2. 전체 E2E 드라이런 (ANTHROPIC_API_KEY 필요)
export ANTHROPIC_API_KEY=sk-ant-...
bash dry-run/run-dryrun.sh

# 3. 특정 agent만
bash dry-run/run-dryrun.sh --agent 04-process-designer

# 4. 상세 출력
bash dry-run/run-dryrun.sh --chain-only -v

# 5. validate-chain.py 단독 실행
python3 .claude/scripts/validate-chain.py --dir output-sample
python3 .claude/scripts/validate-chain.py --dir output-sample --agent 05-sbom-analyst -v
```

### validate-chain.py 동작 방식

`output-sample/`(또는 지정 디렉토리)를 기준으로 9개 agent 각각의:

1. **전제 조건 파일** — 이전 agent가 생성해야 하는 파일이 존재하는가
2. **출력 파일** — 이 agent가 생성해야 하는 파일이 존재하는가
3. **조건부 출력** — 프로필에 따라 존재해야 하는 파일 (없으면 WARN, FAIL 아님)

```
[체인 연결 검증] 대상: output-sample/

  [PASS] 02-organization-designer: 3개 통과, 0개 실패
  [PASS] 03-policy-generator: 3개 통과, 0개 실패
    WARN 조건부 출력 없음: process/contribution-process.md (기여 계획 있음)
  [PASS] 04-process-designer: 7개 통과, 0개 실패 (경고 1개)
  ...
  PASS: 체인 연결 이상 없음 (경고 1개)
```

> **경고 1개 해설**: `output-sample/`이 "기여 없음" 프로필로 생성되어 `contribution-process.md`가 없습니다.
> OpenWave는 기여 계획이 있으므로, output-sample을 OpenWave 프로필로 재생성하면 경고가 사라집니다.

### Layer 3과의 관계

| 항목             | Layer 3 (test-agent-e2e.py) | 드라이런 (run-dryrun.sh)  |
| ---------------- | --------------------------- | ------------------------- |
| 실행 대상        | 개별 fixture (agent 단위)   | OpenWave 프로필 전체 체인 |
| 체인 연결 검증   | ❌ (격리 임시 디렉토리)     | ✅ (validate-chain.py)    |
| 조건부 분기 검증 | ✅ (expected_absent)        | ✅ (fixture 선택으로)     |
| API 없이 실행    | ❌                          | ✅ (--chain-only)         |

`--chain-only`는 API 없이 즉시 실행 가능하므로 agent CLAUDE.md 수정 후 빠른 회귀 검사에 유용합니다.
