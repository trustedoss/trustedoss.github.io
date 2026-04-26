---
sidebar_position: 3
sidebar_label: 'Method 2:Skill definition'
---

# Method 2:Define Skill

:::info Self-study mode(About 20 minutes)
Define it once and you can immediately call it as `/oss-policy-check` from any project.
:::

Create a `.claude/skills/oss-policy-check.md` file.

````markdown
# Skill: OSS 정책 준수 검사 (oss-policy-check)

## 트리거

개발자가 `/oss-policy-check` 또는 "오픈소스 정책 확인" 요청 시 실행

## 실행 절차

### 1단계: 라이선스 확인

Node.js 프로젝트:

```bash
npx license-checker --summary --excludePrivatePackages
```
````

Python project:

```bash
pip-licenses --format=markdown --with-urls
```

Java/Maven project:

```bash
mvn license:aggregate-third-party-report
```

### Step 2:Whitelist matching

Compare with the allowed license in output/policy/license-allowlist.md.
If a license that is not in the list is found, an immediate alert is issued.

### Step 3:Vulnerability inquiry(OSV API)

Search for vulnerabilities in discovered packages using OSV API:

```bash
# grype 사용 (권장)
grype dir:. --fail-on high

# 또는 OSV-Scanner 사용
osv-scanner --recursive .
```

### Step 4:Results reporting format

Report the test results in the format below.:

---

## OSS Policy check result

**Inspection date and time:** YYYY-MM-DD
**Target project:** [Project Name]

### License Status

| License    | number of packages | status       |
| ---------- | ------------------ | ------------ |
| MIT        | 45                 | ✅ Allowed   |
| Apache-2.0 | 12                 | ✅ Allowed   |
| GPL-3.0    | 1                  | ❌ Violation |

### Vulnerability Status

| CVE           | CVSS | package        | status                 |
| ------------- | ---- | -------------- | ---------------------- |
| CVE-2024-XXXX | 9.1  | lodash@4.17.15 | ❌ Urgent patch needed |

### Recommendation

- [ ] Request for approval to replace or use GPL-3.0 package
- [ ] Upgrade to lodash 4.17.21 or higher

---

```

**효과:** 팀원 누구나 `/oss-policy-check` 명령으로 즉시 현황을 파악할 수 있습니다.

---

→ 다음: [방법 3: Hooks 설정하기](./method3-hooks.md)
```
