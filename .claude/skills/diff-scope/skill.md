# Skill: 변경 범위 계산 (diff-scope)

## 역할

git 상태를 기반으로 처리 대상 파일 목록을 계산한다.
전체 파일 스캔 대신 **변경된 파일만** 에이전트에 전달하여 토큰을 절약한다.

## 호출 방법

qa-loop 오케스트레이터 내부에서 자동 호출된다.
직접 호출 시:

```
/diff-scope [모드]
```

| 모드           | 의미                         |
| -------------- | ---------------------------- |
| `staged`       | git add된 파일               |
| `unstaged`     | 수정되었으나 미스테이징 파일 |
| `last-commit`  | 마지막 커밋 변경 파일        |
| `all` (기본값) | staged + unstaged 합산       |

## 실행 명령

```bash
# 미커밋 변경 전체 (staged + unstaged)
git diff --name-only HEAD

# 마지막 커밋 변경
git diff --name-only HEAD~1 HEAD 2>/dev/null

# Untracked 신규 파일 포함
git status --short | grep '?' | awk '{print $2}'
```

## 출력 형식

```
## 변경 범위 계산 결과
계산 기준: unstaged + staged (git diff HEAD)
계산 시각: YYYY-MM-DD HH:MM

변경 파일 목록:
- docs/03-policy/index.md         [docs]
- templates/process/vulnerability-response.md  [templates]
- agents/04-process-designer/CLAUDE.md         [agents]

범위 요약:
- 총 파일 수: 3
- docs/: 1개
- templates/: 1개
- agents/: 1개
- 기타 (website/, scripts/ 등): 0개

QA 대상: docs 1개, agents 1개, templates 1개 (기타 제외)
```

## 필터링 규칙

아래 파일은 QA 대상에서 제외한다:

| 제외 패턴                  | 이유                              |
| -------------------------- | --------------------------------- |
| `website/src/**`           | 코드 파일, 콘텐츠 QA 불필요       |
| `*.json`, `*.ts`, `*.tsx`  | 설정/코드 파일                    |
| `*.sh`, `*.py`, `*.js`     | 스크립트 파일                     |
| `output/`                  | 산출물 (iso-verifier가 별도 처리) |
| `output-sample/`           | 샘플, QA 대상 아님                |
| `.claude/scripts/`         | 스크립트                          |
| `MEMORY.md`, `progress.md` | 내부 추적 파일                    |

## 토큰 절약 효과

| 상황                | 기존 방식                 | diff-scope 방식  |
| ------------------- | ------------------------- | ---------------- |
| 파일 3개 수정 후 QA | docs/ 전체 20개 파일 스캔 | 3개 파일만 처리  |
| 챕터 1개 수정       | 전체 챕터 순회            | 해당 챕터만 처리 |
| 템플릿 1개 수정     | templates/ 전체 스캔      | 해당 파일만 처리 |

## 변경 파일이 없는 경우

```
변경 파일 없음 — QA 건너뜀.
(힌트: 커밋 후 변경사항이 없거나, 모든 수정이 이미 QA를 통과했습니다)
```
