---
id: windsurf
title: Devin Desktop (구 Windsurf)
sidebar_label: Devin Desktop
sidebar_position: 4
---

# Devin Desktop (구 Windsurf)

## 개요

Windsurf 는 2026-06-02 에 Devin Desktop 으로 이름이 바뀌었습니다. IDE와 기능은 그대로이고 브랜드가 Devin 으로 통합됐습니다. 코딩 에이전트도 Cascade 에서 Devin Local 로 교체됐습니다(Cascade 는 2026-07 까지만 제공).

규칙 파일은 프로젝트 단위로 두고, 글로벌 규칙은 앱 설정(UI)에서 별도로 지정합니다. 글로벌 Rules 에는 조직 공통 정책을, 프로젝트 규칙 디렉토리에는 프로젝트 특화 예외나 추가 규칙을 두는 계층 관리가 효율적입니다. 규칙 디렉토리를 저장소에 커밋하면 팀 전체에 동일한 정책이 적용됩니다. 글로벌 규칙과 프로젝트 규칙이 충돌하면 프로젝트 규칙이 우선합니다.

## 설정 파일 위치

- 프로젝트(권장): `.devin/rules/` 디렉토리 — 신규 표준 경로이며 다른 경로보다 우선합니다
- 프로젝트(하위 호환): `.windsurf/rules/` 디렉토리, 레거시 `.windsurfrules` 단일 파일. 기존 설정을 그대로 두어도 계속 동작합니다
- 공통 규격: `AGENTS.md` 지원. `.cursor/rules` 가져오기도 가능합니다
- 글로벌: 앱 설정의 글로벌 Rules

파일당 12,000자 제한이 있습니다.

## 적용 방법

1. 프로젝트에 `.devin/rules/oss-policy.md` 파일을 생성합니다.
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
Windsurf 는 2025년 Cognition(Devin 개발사) 인수를 거쳐 2026-06-02 에 Devin Desktop 으로 리브랜딩이 완료됐고, 공식 문서도 docs.devin.ai 로 이전됐습니다. 기존 `.windsurf/rules/` 와 `.windsurfrules` 는 계속 인식되므로 당장 옮길 필요는 없지만, 새로 만든다면 `.devin/rules/` 를 쓰세요. 규칙 파일이 클수록 응답 지연이 발생할 수 있으므로(파일당 12,000자 제한), 전체 템플릿 중 팀에 꼭 필요한 핵심 정책만 간결하게 유지하는 것을 권장합니다.
:::
