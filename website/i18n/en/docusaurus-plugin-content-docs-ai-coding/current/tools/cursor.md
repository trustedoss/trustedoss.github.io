---
id: cursor
title: Cursor
sidebar_label: Cursor
sidebar_position: 2
---

# Cursor

## 개요

Cursor는 `.cursor/rules/` 폴더 내 `.mdc` 파일을 규칙으로 인식해 AI 동작에 반영합니다. 파일별로 적용 범위(glob 패턴)를 지정할 수 있어 언어·폴더별로 규칙을 분리 관리할 수 있습니다. 적용 범위는 프로젝트 단위입니다.

오픈소스 정책 규칙 파일을 `.cursor/rules/oss-policy.mdc`로 별도 분리해 두면, 다른 개발 가이드라인과 독립적으로 관리하고 필요 시 쉽게 비활성화할 수 있습니다. `globs` 패턴으로 적용 대상 파일을 한정하면 불필요한 컨텍스트 소비를 줄일 수 있습니다. 저장소에 커밋해 두면 팀 전체에 동일한 정책이 자동으로 적용됩니다. 규칙 파일이 여러 개인 경우 목적별로 파일명을 명확히 구분해 관리하면 유지보수가 쉬워집니다.

## 설정 파일 위치

- `.cursor/rules/oss-policy.mdc` (권장)
- `.cursorrules` (루트 단일 파일, 레거시)

## 적용 방법

1. `.cursor/rules/oss-policy.mdc` 파일을 생성합니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
---
description: 오픈소스 라이선스 및 보안 정책
globs: ['**/*.{js,ts,py,go,java}']
alwaysApply: true
---

## 오픈소스 정책

### 라이선스 관리

새로운 외부 패키지·라이브러리 추가 시 반드시 라이선스를 확인하고 명시할 것.

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

### 보안 관리

- 알려진 CVE 취약점이 있는 패키지 버전 사용 금지
- 의존성 추가 후 아래 명령어 중 하나를 실행할 것:
  - npm: `npm audit`
  - Python: `pip-audit`
  - 컨테이너·범용: `trivy fs .`
- 패키지 버전은 가능한 최신 안정 버전(Latest Stable) 사용

### SBOM 관리

- 의존성 변경 시 SBOM 업데이트 필요
- 생성 도구: cdxgen, syft, trivy
- 권장 포맷: CycloneDX (차선: SPDX)

### 저작권

- 기존 코드의 저작권 헤더 유지
- 새 파일 생성 시 프로젝트 라이선스 헤더 포함
- 타 프로젝트 코드 복사 시 출처 및 라이선스 명시
```

## 주의사항

:::info 알아두세요
`alwaysApply: true`로 설정하면 모든 파일에 규칙이 적용되어 토큰 사용량이 증가할 수 있습니다. 정책 규칙처럼 항상 적용이 필요한 경우에는 `alwaysApply: true`를, 특정 언어나 폴더에만 필요한 규칙은 `globs` 패턴으로 범위를 한정하는 것이 효율적입니다. `.cursorrules`(레거시)와 `.cursor/rules/`를 동시에 사용하는 경우 `.cursor/rules/`가 우선 적용되므로, 신규 프로젝트에서는 `.cursor/rules/` 방식을 권장합니다.
:::
