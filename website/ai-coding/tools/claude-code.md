---
id: claude-code
title: Claude Code
sidebar_label: Claude Code
sidebar_position: 1
---

# Claude Code

## 개요

Claude Code는 프로젝트 루트의 `CLAUDE.md`를 세션 시작 시 자동으로 읽어 모든 작업에 컨텍스트로 활용합니다. 하위 폴더에도 `CLAUDE.md`를 둘 수 있으며, 해당 폴더에서 작업할 때 추가로 로드됩니다. 적용 범위는 프로젝트 단위이며, `~/.claude/CLAUDE.md`를 통해 글로벌 설정도 가능합니다.

오픈소스 정책을 `CLAUDE.md`에 작성해 두면, 개발자가 명시적으로 요청하지 않아도 Claude Code가 새 패키지를 추가하거나 코드를 생성할 때 라이선스·보안 정책을 자동으로 고려합니다. 팀 전체가 동일한 저장소를 사용하는 경우 `CLAUDE.md`를 커밋해 두면 모든 팀원에게 일관된 정책이 적용됩니다.

## 설정 파일 위치

- 프로젝트 루트: `CLAUDE.md` (권장)
- 하위 폴더별: `{폴더명}/CLAUDE.md` (보조)
- 글로벌: `~/.claude/CLAUDE.md` (모든 프로젝트 공통)

## 적용 방법

1. 프로젝트 루트에 `CLAUDE.md` 파일을 생성하거나 기존 파일을 엽니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
# 프로젝트 가이드

(기존 프로젝트 지침 내용)

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
---
```

## 주의사항

:::warning AI 규칙의 한계
`CLAUDE.md`는 프롬프트 토큰으로 소비되므로 내용이 너무 길면 컨텍스트 효율이 저하됩니다. 또한 Claude Code는 규칙을 "권장사항"으로 처리할 뿐, 정책 위반 코드를 Hard Block하지는 않습니다. 실질적인 차단이 필요하다면 CI/CD 파이프라인과 반드시 병행해야 합니다. 실제 게이트키퍼 역할은 파이프라인이 담당하고, `CLAUDE.md`는 AI가 올바른 방향으로 코드를 생성하도록 돕는 보조 수단으로 활용하세요.
:::
