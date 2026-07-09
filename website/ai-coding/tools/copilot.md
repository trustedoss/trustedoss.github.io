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

- `.github/copilot-instructions.md` — 단일 파일, 저장소 전체 적용
- `.github/instructions/*.instructions.md` — frontmatter 의 `applyTo` 패턴으로 경로 한정 적용 (언어·폴더별 규칙 분리에 적합)
- `AGENTS.md` — 루트 공통 규칙 파일 (가장 가까운 파일 우선)

## 적용 방법

1. `.github/` 폴더가 없으면 생성 후 `copilot-instructions.md` 파일을 만듭니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
## 오픈소스 정책

### 라이선스 관리

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

<!-- 전체 규칙(보안, SBOM, 저작권 절 포함)은 공통 Rules 템플릿에서 복사 -->
```

전문은 [공통 Rules 템플릿](../rules-template)에서 복사하세요. 허용·금지 목록이 바뀌면 정본만 갱신하고 각 도구 파일에 다시 붙여넣으면 됩니다.

## 적용 확인

규칙이 적용됐는지 확인하려면 도구에 물어보세요.

"이 프로젝트에 GPL-3.0 라이선스 패키지를 추가해도 돼?"

규칙이 인식되면 금지 라이선스라는 답과 함께 대안을 제시합니다. 인식하지 못하면 설정 파일 위치와 적용 방법을 다시 확인하세요. 표준 항목과의 연계는 [ISO 표준 연계](../iso-mapping)를 참조하세요.

## 주의사항

:::info 알아두세요
조직(Organization) 설정에서 조직 전체 공통 지침(Custom instructions)을 지원합니다. 다만 적용 범위가 GitHub.com 의 Copilot Chat, 코드 리뷰, 코딩 에이전트에 한정되므로, IDE 전반에 일관 적용하려면 저장소별 지침 파일을 공통 템플릿으로 함께 관리하는 것이 좋습니다. 커스텀 지침은 Chat, 코드 리뷰, 코딩 에이전트에 적용되며 인라인 코드 완성에의 적용은 보장되지 않습니다. 설정 변경 후 반영까지 약간의 지연이 발생할 수 있습니다.
:::
