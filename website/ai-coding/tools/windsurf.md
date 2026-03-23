---
id: windsurf
title: Windsurf
sidebar_label: Windsurf
sidebar_position: 4
---

# Windsurf

## 개요

Windsurf는 프로젝트 루트의 `.windsurfrules` 파일을 읽어 Cascade AI 에이전트의 동작 지침으로 활용합니다. 글로벌 규칙은 Windsurf 앱 설정(UI)에서 별도로 지정할 수 있습니다. 적용 범위는 프로젝트 단위이며, 글로벌 설정과 프로젝트 설정을 병행 사용할 수 있습니다.

글로벌 Rules에는 조직 공통 정책을 작성하고, `.windsurfrules`에는 프로젝트 특화 예외 사항이나 추가 규칙을 작성하는 방식으로 계층적으로 관리하면 효율적입니다. `.windsurfrules`를 저장소에 커밋하면 팀 전체에 동일한 정책이 적용됩니다. 글로벌 규칙과 프로젝트 규칙이 충돌할 경우 프로젝트 규칙이 우선합니다.

## 설정 파일 위치

- 프로젝트: `.windsurfrules` (루트, 권장)
- 글로벌: Windsurf 앱 설정 > Global Rules

## 적용 방법

1. 프로젝트 루트에 `.windsurfrules` 파일을 생성합니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
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
`.windsurfrules`는 Cascade 에이전트 전용이며, 일반 코드 완성(Autocomplete) 기능에는 적용되지 않습니다. 에이전트 작업(파일 생성·수정·패키지 추가 등)에만 정책이 적용된다는 점을 인지하고 단순 코드 완성 사용 시에는 별도 주의가 필요합니다. 파일 크기가 클수록 응답 지연이 발생할 수 있으므로, 전체 템플릿 중 팀에 꼭 필요한 핵심 정책만 간결하게 유지하는 것을 권장합니다.
:::
