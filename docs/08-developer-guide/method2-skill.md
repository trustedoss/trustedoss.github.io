---
sidebar_position: 3
sidebar_label: "방법 2: Skill 정의"
---

# 방법 2: Skill 정의하기

:::info 셀프스터디 모드 (약 20분)
한 번 정의하면 모든 프로젝트에서 `/oss-policy-check`으로 즉시 호출할 수 있습니다.
:::

`.claude/skills/oss-policy-check.md` 파일을 생성합니다.

```markdown
# Skill: OSS 정책 준수 검사 (oss-policy-check)

## 트리거
개발자가 `/oss-policy-check` 또는 "오픈소스 정책 확인" 요청 시 실행

## 실행 절차

### 1단계: 라이선스 확인

Node.js 프로젝트:
```bash
npx license-checker --summary --excludePrivatePackages
```

Python 프로젝트:
```bash
pip-licenses --format=markdown --with-urls
```

Java/Maven 프로젝트:
```bash
mvn license:aggregate-third-party-report
```

### 2단계: 허용 목록 대조
output/policy/license-allowlist.md 의 허용 라이선스와 비교한다.
목록에 없는 라이선스가 발견되면 즉시 경고한다.

### 3단계: 취약점 조회 (OSV API)
발견된 패키지에 대해 OSV API로 취약점을 조회한다:

```bash
# grype 사용 (권장)
grype dir:. --fail-on high

# 또는 OSV-Scanner 사용
osv-scanner --recursive .
```

### 4단계: 결과 보고 형식

검사 결과를 아래 형식으로 보고한다:

---
## OSS 정책 검사 결과

**검사 일시:** YYYY-MM-DD
**대상 프로젝트:** [프로젝트명]

### 라이선스 현황
| 라이선스 | 패키지 수 | 상태 |
|---------|---------|------|
| MIT | 45 | ✅ 허용 |
| Apache-2.0 | 12 | ✅ 허용 |
| GPL-3.0 | 1 | ❌ 위반 |

### 취약점 현황
| CVE | CVSS | 패키지 | 상태 |
|-----|------|--------|------|
| CVE-2024-XXXX | 9.1 | lodash@4.17.15 | ❌ 긴급 패치 필요 |

### 권고사항
- [ ] GPL-3.0 패키지 대체 또는 사용 승인 요청
- [ ] lodash 4.17.21 이상으로 업그레이드
---
```

**효과:** 팀원 누구나 `/oss-policy-check` 명령으로 즉시 현황을 파악할 수 있습니다.

---

→ 다음: [방법 3: Hooks 설정하기](./method3-hooks.md)
