---
id: copilot
title: GitHub Copilot
sidebar_label: GitHub Copilot
sidebar_position: 3
---

# GitHub Copilot

GitHub Copilot은 GitHub과 OpenAI가 개발한 AI 페어 프로그래밍 도구입니다.
VS Code, JetBrains, Neovim 등 다양한 편집기에서 사용할 수 있습니다.

## 설치

VS Code 확장 마켓플레이스에서 "GitHub Copilot"을 검색하여 설치합니다.

## 오픈소스 컴플라이언스 설정

### .github/copilot-instructions.md 파일

저장소에 `.github/copilot-instructions.md` 파일을 생성합니다:

```markdown
# Copilot 지침

## 오픈소스 컴플라이언스

새로운 외부 라이브러리나 패키지를 제안할 때는 다음을 확인하세요:
1. 라이선스 호환성 (MIT, Apache-2.0, BSD 선호)
2. 알려진 보안 취약점 여부 (CVE 데이터베이스 확인)
3. 프로젝트 의존성 정책 준수

## SBOM 관리

- 새 의존성 추가 시 package.json/pom.xml/requirements.txt 업데이트
- SBOM은 `cdxgen` 또는 `syft`로 생성
```

### Copilot 필터링 설정

GitHub Copilot의 "공개 코드 제안 차단" 옵션을 활성화하여 라이선스 위험을 줄입니다:

1. GitHub 설정 → Copilot → Suggestions matching public code: **Block**

## 관련 링크

- [GitHub Copilot 공식 문서](https://docs.github.com/ko/copilot)
- [공통 Rules 템플릿](../rules-template)
