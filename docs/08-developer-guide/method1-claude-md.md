---
sidebar_position: 1
sidebar_label: '방법 1: CLAUDE.md 정책'
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
셀프스터디 소요시간: 15분
---

# 방법 1: CLAUDE.md에 정책 추가하기

:::info 셀프스터디 모드 (약 15분)
프로젝트 루트 CLAUDE.md에 정책을 추가하면 Claude Code가 즉시 인식합니다.
:::

프로젝트 루트의 `CLAUDE.md`에 아래 섹션을 추가합니다. 등급 구분은
[라이선스 분류](/reference/concepts/license-classification) 기준을 따릅니다. 실제 회사
정책의 허용 목록은 03 정책 챕터에서 생성한 `output/policy/license-allowlist.md`이므로,
아래 예시를 붙여넣은 뒤 그 파일 내용에 맞게 조정하세요.

```markdown
## 오픈소스 정책 (자동 준수)

### 허용 라이선스

아래 라이선스는 별도 승인 없이 신규 패키지에 사용 가능하다:

- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- 전체 목록: output/policy/license-allowlist.md 참조

### 조건부 허용 라이선스

아래 라이선스는 담당자 사전 검토와 승인 후 사용 가능하다:

- LGPL, MPL (Weak Copyleft - 사용 방식에 따라 소스 공개 의무 발생, 법무 검토 필요)
- CC-BY-SA (콘텐츠용 라이선스라 소프트웨어 적용 시 별도 검토 필요)
- 조건과 예외는 output/policy/license-allowlist.md 참조

### 금지 라이선스

아래 라이선스는 사전 승인 없이 추가 금지:

- GPL, AGPL (Copyleft - 배포 시 소스코드 공개 의무)
- SSPL, Commons Clause (오픈소스 정의를 충족하지 않는 사용 제한 조항)
- 상업적 사용 금지 조항이 있는 모든 라이선스

### 취약점 정책

- CVSS 7.0 이상(High/Critical) 취약점이 있는 패키지 사용 금지
- 알려진 취약점이 있는 버전은 패치 버전으로 업그레이드

### 패키지 추가 시 확인 절차

새 패키지를 추가할 때는 반드시 아래 순서로 확인한다:

1. 라이선스 확인: `license-checker` 또는 `/oss-policy-check` skill 실행
2. 취약점 확인: OSV API 또는 `grype` 실행
3. 허용 목록 비교: output/policy/license-allowlist.md 대조
4. 위반 시: 담당자에게 사용 승인 요청 (output/process/usage-approval.md 참조)
```

**효과:** Claude Code가 패키지 추가를 도울 때 이 정책을 자동으로 참조하여 경고합니다.

**한계:** 개발자가 직접 터미널에서 `npm install`을 실행하면 Claude Code가 개입하지 못합니다.

:::note 등급 기준의 정본
허용·조건부·금지 세 등급의 판단 기준은 [라이선스 분류](/reference/concepts/license-classification)가
정본입니다. 위 예시는 그 기준을 CLAUDE.md 형식으로 옮긴 것이므로, 등급이 바뀌면 정본을 먼저
확인하세요. AI 코딩 도구별 설정 파일에 넣을 규칙 전문은
[공통 Rules 템플릿](/ai-coding/rules-template)에 있습니다.
:::

---

→ 다음: [방법 2: Skill 정의하기](./method2-skill.md)
