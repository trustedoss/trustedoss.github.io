---
id: claude-code
title: Claude Code
sidebar_label: Claude Code
sidebar_position: 1
---

# Claude Code

Claude Code는 Anthropic이 개발한 CLI 기반 AI 코딩 에이전트입니다.
터미널에서 직접 실행하며, 코드베이스 전체를 이해하고 복잡한 작업을 자율적으로 수행합니다.

## 설치

```bash
npm install -g @anthropic-ai/claude-code
```

## 오픈소스 컴플라이언스 설정

### CLAUDE.md 파일 활용

프로젝트 루트에 `CLAUDE.md` 파일을 생성하여 오픈소스 컴플라이언스 지침을 추가합니다:

```markdown
## 오픈소스 컴플라이언스 지침

- 새로운 의존성 추가 시 라이선스를 확인하세요 (MIT, Apache-2.0, BSD 권장)
- GPL/AGPL 라이선스 패키지 추가 전 반드시 승인을 받으세요
- 코드 생성 시 저작권 헤더를 유지하세요
- 패키지 추가 후 `syft` 또는 `cdxgen`으로 SBOM을 업데이트하세요
```

### trustedoss 연동

Claude Code를 trustedoss와 함께 사용하면 오픈소스 관리 체계 구축 작업을 자동화할 수 있습니다.

```bash
git clone https://github.com/haksungjang/trustedoss.git
cd trustedoss
claude
# "어디서 시작해야 해?" 입력
```

## 관련 링크

- [Claude Code 공식 문서](https://docs.anthropic.com/ko/docs/claude-code)
- [CLAUDE.md 작성 가이드](https://docs.anthropic.com/ko/docs/claude-code/memory)
