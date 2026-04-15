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

## Layer 3 (향후 추가 예정)

Anthropic API를 사용한 실제 대화 흐름 + 파일 생성 E2E 테스트.
각 agent에 mock 입력(tests/fixtures/)을 제공하고 생성된 output 파일을 검증합니다.
API 비용이 발생하므로 verify.sh에는 포함하지 않고 별도 실행합니다.

모델: `claude-sonnet-4-6`
