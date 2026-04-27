# trustedoss-agents

ISO/IEC 5230 · 18974 자체 인증을 위한 AI Agent 키트.

## 시작

```bash
cd agents && claude
```

`agents/CLAUDE.md`가 현재 `output/` 상태를 진단하고 다음 실행 agent를 안내한다.

## 구조

| 경로                 | 역할                                 |
| -------------------- | ------------------------------------ |
| `agents/`            | 단계별 AI Agent (CLAUDE.md 포함)     |
| `templates/`         | 산출물 문서 템플릿                   |
| `.claude/skills/`    | Agent 공통 skill 정의                |
| `.claude/reference/` | ISO 5230 · 18974 스펙 참조           |
| `output/`            | 생성된 산출물 (로컬 생성, gitignore) |

## 단계별 전체 가이드

[trustedoss.github.io](https://trustedoss.github.io) 참조.

## 주의

이 저장소는 [trustedoss/trustedoss.github.io](https://github.com/trustedoss/trustedoss.github.io)에서 자동 동기화됩니다.
이슈 및 PR은 원본 저장소에서 열어주세요.
