---
id: cline-aider
title: Cline / Aider 설정
sidebar_label: Cline / Aider
sidebar_position: 5
---

# Cline / Aider 설정

## 개요

Cline은 `.clinerules` 파일(루트 단일 파일 또는 `.clinerules/` 폴더)을 프로젝트 지침으로 읽어 AI 동작에 반영합니다. Aider는 정책 문서(관례상 `CONVENTIONS.md`)를 `--read` 옵션이나 `.aider.conf.yml`의 `read` 항목으로 읽어 매 세션의 컨텍스트에 포함합니다. 두 도구 모두 프로젝트 단위로 규칙을 적용합니다.

Cline은 VS Code 확장으로 동작하는 에이전트형 AI 도구이며, Aider는 터미널 기반 CLI 도구입니다. 두 도구 모두 오픈소스이며 로컬 환경에서 실행되므로, 코드를 외부 서버에 전송하는 것을 꺼리는 팀에서 선호합니다. 오픈소스 정책을 각 설정 파일에 작성해 두면 AI가 패키지를 추가하거나 코드를 생성할 때 자동으로 정책을 고려합니다.

---

## Cline 설정

### 설정 파일 위치

- `.clinerules` (루트 단일 파일, 권장)
- `.clinerules/` (폴더, 여러 파일 분리 가능)

### 적용 방법

1. 프로젝트 루트에 `.clinerules` 파일을 생성합니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

### 설정 예시

```markdown
## 오픈소스 정책

### 라이선스 관리

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

<!-- 전체 규칙(보안, SBOM, 저작권 절 포함)은 공통 Rules 템플릿에서 복사 -->
```

전문은 [공통 Rules 템플릿](../rules-template)에서 복사하세요. 허용·금지 목록이 바뀌면 정본만 갱신하고 각 도구 파일에 다시 붙여넣으면 됩니다.

---

## Aider 설정

### 설정 파일 위치

- `CONVENTIONS.md` (루트, 파일명은 자유 — Aider 공식 문서의 관례)
- `.aider.conf.yml` 의 `read` 항목 (위 파일을 자동 로드하도록 등록)

### 적용 방법

1. 프로젝트 루트에 `CONVENTIONS.md` 파일을 생성합니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. `.aider.conf.yml`에 `read: CONVENTIONS.md`를 추가해 매 실행 시 자동으로 읽히게 합니다.
   (일회성으로는 `aider --read CONVENTIONS.md`)

### 설정 예시

**CONVENTIONS.md** — 공통 Rules 템플릿 내용을 담는 파일입니다. 아래는 발췌입니다.

```markdown
## 오픈소스 정책

### 라이선스 관리

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

<!-- 전체 규칙(보안, SBOM, 저작권 절 포함)은 공통 Rules 템플릿에서 복사 -->
```

전문은 [공통 Rules 템플릿](../rules-template)에서 복사하세요. 허용·금지 목록이 바뀌면 정본만 갱신하고 각 도구 파일에 다시 붙여넣으면 됩니다.

**.aider.conf.yml** — 정책 문서를 읽기 전용 컨텍스트로 항상 로드합니다.

```yaml
# 매 세션 시작 시 정책 문서를 읽기 전용으로 포함
read: CONVENTIONS.md
```

---

## 적용 확인

규칙이 적용됐는지 확인하려면 도구에 물어보세요.

"이 프로젝트에 GPL-3.0 라이선스 패키지를 추가해도 돼?"

규칙이 인식되면 금지 라이선스라는 답과 함께 대안을 제시합니다. 인식하지 못하면 설정 파일 위치와 적용 방법을 다시 확인하세요. 표준 항목과의 연계는 [ISO 표준 연계](../iso-mapping)를 참조하세요.

## 주의사항

:::info 알아두세요
Cline과 Aider 모두 규칙을 Hard Block이 아닌 소프트 가이드라인으로 처리합니다. 정책 위반 패키지를 완전히 차단하려면 CI/CD 파이프라인을 함께 구성해야 합니다. Aider는 CLI 기반으로 동작하므로, `.aider.conf.yml`이 없으면 매 실행 시 `aider --read CONVENTIONS.md`로 정책 문서를 직접 지정할 수도 있습니다. 자동화된 CI/CD 게이트 구성 방법은 [Quick CI/CD](../cicd-quick)를 참고하세요.
:::
