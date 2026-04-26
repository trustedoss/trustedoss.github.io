---
sidebar_position: 2
sidebar_label: 'Method 1:CLAUDE.md policy'
---

# Method 1:Adding policy to CLAUDE.md

:::info Self-study mode(About 15 minutes)
If you add a policy to your project root CLAUDE.md, Claude Code will recognize it immediately.
:::

Add the section below to `CLAUDE.md` in the project root.

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

**effect:** When Claude Code helps you add packages, it automatically references this policy to alert you.

**margin:** If the developer directly executes `npm install` in the terminal, Claude Code will not be able to intervene.

---

→ next: [Method 2:Define Skill](./method2-skill.md)
