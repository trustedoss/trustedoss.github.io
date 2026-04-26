---
id: copilot
title: GitHub Copilot
sidebar_label: GitHub Copilot
sidebar_position: 3
---

# GitHub Copilot

## 개요

GitHub Copilot은 `.github/copilot-instructions.md` 파일을 저장소 전체에 적용되는 커스텀 지침으로 읽습니다. VS Code, JetBrains, GitHub.com 등 Copilot이 활성화된 모든 환경에 동일하게 적용됩니다. 적용 범위는 저장소 단위입니다.

오픈소스 정책을 이 파일에 작성해 두면, 팀원들이 어떤 편집기를 사용하든 Copilot이 코드를 제안할 때 자동으로 라이선스와 보안 정책을 인지합니다. `.github/` 폴더는 이미 대부분의 저장소에 존재하므로 별도 디렉토리 생성 없이 바로 적용할 수 있다는 장점이 있습니다. 신규 저장소를 생성할 때마다 이 파일을 포함한 기본 템플릿을 함께 복사하는 것을 권장합니다.

## 설정 파일 위치

- `.github/copilot-instructions.md` (단일 파일, 저장소 전체 적용)

## 적용 방법

1. `.github/` 폴더가 없으면 생성 후 `copilot-instructions.md` 파일을 만듭니다.
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
조직(Organization) 단위의 공통 지침 설정은 별도로 지원되지 않으므로, 저장소마다 `.github/copilot-instructions.md` 파일을 직접 복사해야 합니다. 여러 저장소를 관리하는 경우 정책이 달라지지 않도록 파일을 공통 템플릿으로 관리하고, 변경 시 모든 저장소에 동기화하는 절차를 갖추는 것이 좋습니다. Copilot Chat과 코드 완성 모두에 적용되나, 설정 변경 후 반영까지 약간의 지연이 발생할 수 있습니다.
:::
