# 오픈소스 사용 승인 절차
<!-- 5230 §3.1.5.1 (라이선스 의무 검토), §3.3.1.1 (SBOM 관리), §3.3.2.1 -->

**회사명**: 테크유니콘
**작성일**: 2026-03-23
**담당자**: DevOps팀 오픈소스 담당자

---

## 1. 절차 개요

오픈소스 컴포넌트를 신규 도입하거나 기존 버전을 변경할 때 이 절차를 따른다.
<!-- 5230 §3.1.5.1: 라이선스 의무·제한·권리를 검토하고 기록하는 문서화된 절차 -->

### 리스크 기반 승인 단계

| 리스크 수준 | 조건 | 승인 단계 |
|-----------|------|---------|
| 낮음 | Permissive 라이선스 + Critical/High CVE 없음 | 담당자 단독 승인 |
| 중간 | Weak Copyleft 또는 Medium CVE 존재 | 팀장 승인 |
| 높음 | Strong/Network Copyleft, High/Critical CVE, 허용 목록 외 라이선스 | 위원회 승인 |

```
오픈소스 도입 요청 (Jira 티켓 생성)
    ↓
라이선스 확인 (허용 목록 대조)
    ↓
리스크 수준 판정
    ↓
[낮음] → 담당자 승인
[중간] → 팀장 승인
[높음] → 위원회 승인 (법무팀 포함)
    ↓
취약점 스캔 (CVE 확인)
    ↓
[Critical/High CVE?] → 대안 검색 또는 패치 확인
    ↓
승인 완료 → SBOM 업데이트
    ↓
배포 전 distribution-checklist.md 완료
```

---

## 2. CI/CD 자동화 통합

테크유니콘은 GitHub Actions, Jenkins, GitLab CI를 모두 사용한다. 각 파이프라인에서 오픈소스 사용 승인 절차를 아래와 같이 통합한다.

### GitHub Actions

```yaml
# .github/workflows/oss-scan.yml
name: OSS License & Vulnerability Scan
on:
  pull_request:
    branches: [main, develop]

jobs:
  oss-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: License Scan
        run: |
          # 라이선스 스캔 후 허용 목록 대조
          npx license-checker --summary --excludePrivatePackages
      - name: Vulnerability Scan
        run: |
          # CVE 스캔
          npm audit --audit-level=high
```

### Jenkins (Jenkinsfile)

```groovy
stage('OSS Compliance') {
    steps {
        sh 'license-checker --summary'
        sh 'osv-scanner --lockfile package-lock.json'
    }
    post {
        failure {
            // Jira 티켓 자동 생성
            jiraNewIssue site: 'SKT-JIRA',
                         projectKey: 'OSS',
                         summary: 'OSS 컴플라이언스 검사 실패'
        }
    }
}
```

### GitLab CI (.gitlab-ci.yml)

```yaml
oss-scan:
  stage: test
  script:
    - license-checker --summary
    - osv-scanner --lockfile package-lock.json
  only:
    - merge_requests
    - main
```

---

## 3. 사용 승인 요청 양식 (Jira 티켓)

Jira에서 프로젝트 **OSS** 유형 티켓을 생성하여 아래 항목을 기록한다.

| 항목 | 내용 |
|------|------|
| 요청자 | {이름/부서} |
| 요청일 | YYYY-MM-DD |
| 컴포넌트명 | {이름} |
| 버전 | {버전} |
| 라이선스 | {SPDX 식별자, 예: Apache-2.0} |
| 사용 목적 | {직접 사용 / 의존성 / 개발용} |
| 배포 포함 여부 | {배포 포함 / 내부용만} |
| 리스크 수준 | {낮음 / 중간 / 높음} |
| 대안 검토 여부 | {검토함 / 검토불필요 / 이유: } |

---

## 4. 라이선스 의무사항 검토
<!-- 5230 §3.1.5.1: 각 식별된 라이선스의 의무·제한·권리 검토 및 기록 -->

| 라이선스 유형 | 배포 방식 | 의무사항 | 이행 방법 | 승인 단계 |
|------------|---------|---------|---------|---------|
| MIT / Apache-2.0 / BSD | 모든 배포 | 저작권 표시, 라이선스 고지 | NOTICE 파일에 포함 | 담당자 단독 |
| LGPL | 임베디드/배포 | 소스코드 공개 또는 동적링크 보장 | 동적링크 유지 / 소스코드 공개 | 팀장 승인 |
| GPL-2.0 / GPL-3.0 | 임베디드/배포 | 전체 소스코드 공개 | 소스코드 공개 (배포 시) | 위원회 승인 |
| AGPL-3.0 | SaaS 포함 | 네트워크 서비스 포함 소스코드 공개 | 소스코드 공개 | 위원회 승인 |
| 허용 목록 외 | — | 사전 법무 검토 필수 | | 위원회 승인 |

---

## 5. 취약점 사전 확인
<!-- 18974 §4.1.5.1, §4.3.2 -->

신규 컴포넌트 도입 시:

- [ ] OSV API 또는 NVD에서 해당 버전의 CVE 조회
- [ ] Critical/High CVE 없음 확인
- [ ] Critical/High CVE 존재 시: 패치 버전으로 변경 또는 도입 재검토
- [ ] Jira 티켓에 스캔 결과 첨부

---

## 6. SBOM 업데이트 의무
<!-- 5230 §3.3.1.1: SBOM 식별·추적·검토·승인·보관 절차 -->

승인 후 반드시:
- `output/sbom/sbom-commands.sh`를 실행하여 SBOM 재생성
- 갱신된 `*.cdx.json` 파일을 지정 위치에 보관

---

## 7. 승인 기록

| 날짜 | 컴포넌트 | 버전 | 라이선스 | CVE 확인 | 리스크 | 승인자 | Jira 티켓 |
|------|---------|------|---------|---------|--------|--------|---------|
| YYYY-MM-DD | {이름} | {버전} | {라이선스} | ✅/⚠️ | 낮음/중간/높음 | {이름} | OSS-{번호} |

---

## 8. 허용 라이선스 목록 참조

허용·제한 라이선스의 전체 목록은 `output/policy/license-allowlist.md` 를 참조한다.
