---
id: windsurf
title: Windsurf
sidebar_label: Windsurf
sidebar_position: 4
---

# Windsurf

## 개요

Windsurf는 프로젝트 루트의 `.windsurfrules` 파일을 읽어 Cascade AI 에이전트의 동작 지침으로 활용합니다. 글로벌 규칙은 Windsurf 앱 설정(UI)에서 별도로 지정할 수 있습니다. 적용 범위는 프로젝트 단위이며, 글로벌 설정과 프로젝트 설정을 병행 사용할 수 있습니다.

글로벌 Rules에는 조직 공통 정책을 작성하고, 워크스페이스 규칙(`.windsurf/rules/`)에는 프로젝트 특화 예외 사항이나 추가 규칙을 작성하는 방식으로 계층적으로 관리하면 효율적입니다. 규칙 디렉토리를 저장소에 커밋하면 팀 전체에 동일한 정책이 적용됩니다. 글로벌 규칙과 프로젝트 규칙이 충돌할 경우 프로젝트 규칙이 우선합니다.

## 설정 파일 위치

- 프로젝트: `.windsurf/rules/` 디렉토리 (권장 — 파일당 12,000자 제한. 레거시 `.windsurfrules` 단일 파일도 인식). `AGENTS.md` 도 지원
- 글로벌: `~/.codeium/windsurf/memories/global_rules.md` (6,000자 제한)

## 적용 방법

1. 프로젝트에 `.windsurf/rules/oss-policy.md` 파일을 생성합니다.
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
Windsurf 는 2025년 Cognition(Devin 개발사) 인수 후 Devin Desktop 으로 통합이 진행 중이며, 공식 문서도 docs.devin.ai 로 이전됐습니다. 신규 문서에서는 `.devin/rules/` 디렉토리를 우선 안내하므로 도구 업데이트 시 규칙 경로 변화를 확인하세요. 규칙 파일이 클수록 응답 지연이 발생할 수 있으므로(파일당 12,000자 제한), 전체 템플릿 중 팀에 꼭 필요한 핵심 정책만 간결하게 유지하는 것을 권장합니다.
:::
