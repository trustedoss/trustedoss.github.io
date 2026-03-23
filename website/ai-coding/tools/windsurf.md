---
id: windsurf
title: Windsurf
sidebar_label: Windsurf
sidebar_position: 4
---

# Windsurf

Windsurf(구 Codeium)는 AI 코딩 에이전트 기능을 제공하는 코드 편집기입니다.
"Flow"라는 에이전틱 AI 기능으로 복잡한 작업을 자율적으로 처리할 수 있습니다.

## 설치

[windsurf.ai](https://windsurf.ai)에서 다운로드합니다.

## 오픈소스 컴플라이언스 설정

### Global Rules 설정

Windsurf 설정에서 Global Rules를 추가합니다:

**Windsurf → Settings → AI → Global Rules:**

```
# 오픈소스 컴플라이언스 Rules

의존성 추가 시:
- 라이선스 명시 (MIT/Apache-2.0/BSD 선호, GPL 주의)
- 보안 취약점 여부 확인 권장
- SBOM 업데이트 필요성 안내

코드 생성 시:
- 저작권 헤더 유지
- 라이선스 호환성 고려
```

### .windsurfrules 파일

프로젝트별로 `.windsurfrules` 파일을 생성하여 프로젝트 특화 규칙을 정의할 수 있습니다.

## 관련 링크

- [Windsurf 공식 문서](https://docs.windsurf.ai)
- [공통 Rules 템플릿](../rules-template)
