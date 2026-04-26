---
sidebar_position: 2
sidebar_label: '방법 1: CLAUDE.md 정책'
---

# 방법 1: CLAUDE.md에 정책 추가하기

:::info 셀프스터디 모드 (약 15분)
프로젝트 루트 CLAUDE.md에 정책을 추가하면 Claude Code가 즉시 인식합니다.
:::

프로젝트 루트의 `CLAUDE.md`에 아래 섹션을 추가합니다.

```markdown
## 오픈소스 정책 (자동 준수)

### 허용 라이선스

아래 라이선스만 신규 패키지에 사용 가능하다:

- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- 전체 목록: output/policy/license-allowlist.md 참조

### 금지 라이선스

아래 라이선스는 사전 승인 없이 추가 금지:

- GPL-2.0, GPL-3.0, AGPL-3.0 (Copyleft - 소스코드 공개 의무)
- LGPL-2.0, LGPL-2.1, LGPL-3.0 (Weak Copyleft - 동적 링킹 검토 필요)
- CC-BY-SA (소프트웨어에 부적합)
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

---
