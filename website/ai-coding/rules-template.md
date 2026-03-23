---
id: rules-template
title: 공통 Rules 템플릿
sidebar_label: 공통 Rules 템플릿
sidebar_position: 3
---

# 오픈소스 컴플라이언스 공통 Rules 템플릿

AI 코딩 도구에 공통으로 적용할 수 있는 오픈소스 컴플라이언스 Rules 템플릿입니다.
각 도구의 설정 방식에 맞게 적용하세요.

## 기본 템플릿

```markdown
# 오픈소스 컴플라이언스 지침

## 라이선스 관리

새로운 외부 패키지/라이브러리 추가 시:
1. 반드시 라이선스를 확인하고 명시할 것
2. 허용 라이선스: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
3. 주의 라이선스 (법무 검토 필요): LGPL, MPL
4. 금지 라이선스 (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

## 보안 관리

- 알려진 CVE 취약점이 있는 패키지 버전 사용 금지
- 의존성 추가 후 `npm audit` / `pip-audit` / `trivy` 실행 권장
- 패키지 버전은 가능한 최신 안정 버전 사용

## SBOM 관리

- 의존성 변경 시 SBOM 업데이트 필요
- SBOM 생성 도구: cdxgen, syft, trivy
- SBOM 포맷: CycloneDX (권장) 또는 SPDX

## 저작권

- 기존 코드의 저작권 헤더 유지
- 새 파일 생성 시 프로젝트 라이선스 헤더 포함
- 타 프로젝트 코드 복사 시 출처 및 라이선스 명시
```

## 도구별 적용 방법

| 도구 | 파일/설정 위치 |
|------|--------------|
| Claude Code | `CLAUDE.md` (프로젝트 루트) |
| Cursor | `.cursorrules` (프로젝트 루트) |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` (프로젝트 루트) 또는 Global Rules |

## 자동화 연동

CI/CD 파이프라인에서 자동으로 컴플라이언스를 검증하는 방법은 [CI/CD 자동화](./cicd-quick)를 참고하세요.
