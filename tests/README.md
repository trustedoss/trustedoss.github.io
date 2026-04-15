# Tests

검증 스크립트는 `.claude/scripts/`에 위치합니다.

## 주요 스크립트

| 스크립트             | 역할                                | 실행 방법                                    |
| -------------------- | ----------------------------------- | -------------------------------------------- |
| `verify.sh`          | 전체 검증 (9개 항목) — push 전 필수 | `bash .claude/scripts/verify.sh`             |
| `validate-output.py` | output/ 산출물 완전성 상세 확인     | `python3 .claude/scripts/validate-output.py` |
| `test-coverage.py`   | ISO G항목 커버리지 정합성           | `python3 .claude/scripts/test-coverage.py`   |

## 일반 사용법

파일을 생성하거나 수정한 뒤:

```bash
bash .claude/scripts/verify.sh
```

모든 항목이 `PASS`여야 push할 수 있습니다. 상세 기준은 `CONTRIBUTING.md` 참조.
