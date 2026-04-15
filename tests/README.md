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

| 파일                                | 설명                               |
| ----------------------------------- | ---------------------------------- |
| `02-organization-designer.json`     | 조직 산출물 생성 기본 케이스       |
| `03-policy-generator.json`          | 정책 문서 생성                     |
| `04-process-designer-branch-A.json` | 프로세스 설계 (기여+공개 활성화)   |
| `04-process-designer-branch-B.json` | 프로세스 설계 (기여+공개 비활성화) |
| `05-sbom-analyst.json`              | SBOM 라이선스 분석                 |
| `05-sbom-management.json`           | SBOM 관리 계획                     |
| `05-vulnerability-analyst.json`     | 취약점 분석 리포트                 |
| `06-training-manager.json`          | 교육 커리큘럼 생성                 |
| `07-conformance-preparer.json`      | 갭 분석 및 인증 선언문             |

### 주의 사항

- API 비용 발생 (Sonnet 4.6 기준, agent당 약 $0.10~0.30 예상)
- `verify.sh`에는 포함하지 않음 — 별도 실행 필요
- GitHub Actions: `agent-e2e-test.yml` 워크플로우로 수동 실행 또는 `agents/*/CLAUDE.md` 변경 시 자동 실행
- `ANTHROPIC_API_KEY` secret 필요 (GitHub Settings → Secrets)
