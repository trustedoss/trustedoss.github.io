---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: [4.3.1, 4.3.2]'
self_study_time: 1 hour
---

# SBOM Management:Creating is not the end; management is the beginning.

## 1. What we do in this chapter

Creating SBOM once is not enough. Software is constantly changing and,New vulnerabilities are disclosed every day. In this chapter, the created SBOM is updated according to the release cycle.,Stored by version,Establish a process to systematically share with external customers or suppliers.

`agents/05-sbom-management` Running the agent produces two outputs::`output/sbom/sbom-management-plan.md`, which defines the renewal cycle and responsible person, and `output/sbom/sbom-sharing-template.md`, a cover document for providing the supplier. Once these two documents are completed, the basis for the SBOM management system is established.

---

## 2. Background knowledge

### SBOM is not something you make once and that’s it.

Whenever the software changes, SBOM must also change. An old, unmaintained SBOM can be more dangerous than nothing at all. Trusting SBOM that is not up to date creates security blind spots due to inconsistencies between actual components and documentation.

**Real life examples:** Trusted SBOM created 6 months ago,There may be cases where vulnerable libraries added in the meantime are not found. Even after the CVE was disclosed in that library, the organization was unaware that it was affected.,The customer discovered the problem first and lost trust.

---

### SBOM Update trigger

SBOM must be updated whenever the event below occurs.

| Event                             | When to renew                 | Remarks                          |
| --------------------------------- | ----------------------------- | -------------------------------- |
| Add new open source components    | immediately(When merging PRs) | CI/CD automation recommended     |
| Change existing component version | immediately(When merging PRs) | Especially when security patches |
| Software Release                  | Just before release           | Release SBOM stored separately   |
| Security vulnerability patch      | Upon completion of patch      | Purpose of proof of response     |

The most important of these is **right before software release**. SBOM at the time of release is the official documentation of the components for that version, so,They should be kept separately and clearly tagged with versions.

---

### SBOM Version management strategy

File naming convention for Git-based SBOM versioning:

```
output/sbom/[project]-[version]-[date].cdx.json
```

example:

```
output/sbom/myapp-v1.2.0-20260320.cdx.json
output/sbom/myapp-v1.1.0-20260101.cdx.json
output/sbom/myapp-latest.cdx.json  ← 항상 최신본 링크
```

`myapp-latest.cdx.json` always keeps pointing to the most recently created SBOM,Files for each release are managed in separate directories or tags according to the storage policy.

**Why you should keep release-specific SBOM:**

- Components can be proven at a specific point in time when responding to regulations
- When a vulnerability is discovered, the scope of affected versions can be quickly determined.
- EU CRA,Can respond to the requirements of emerging regulations such as EO 14028

Recommended storage period:Maintenance period of the software release + 1 year or more

---

### Provide SBOM to suppliers/customers

**When to provide SBOM:**

- When the supplier explicitly requests
- When the contract contains a clause providing SBOM
- EO 14028 applies to(When delivered to the U.S. federal government)
- EU CRA applies(Scheduled for launch in EU market,Implementation in 2027)
- When participating in a large enterprise supply chain management program(samsung,Increasing trend, including Hyundai Motors)

**Pros and cons of each delivery method:**

| method                                 | suitable situation                            | Precautions                                                 |
| -------------------------------------- | --------------------------------------------- | ----------------------------------------------------------- |
| Email Attachment                       | small scale,Occasional offer                  | Version management is difficult and there is a risk of loss |
| Secure file sharing(Google Drive, Box) | medium scale,Regular offer                    | Access rights management required                           |
| API provided                           | large scale,Automation needed                 | Initial development cost required                           |
| Portal/Web                             | Simultaneously provided to multiple customers | Infrastructure construction and maintenance costs required  |

**SBOM Information to include when providing**(Included in `sbom-sharing-template.md`):

- SBOM file body(CycloneDX JSON or SPDX format)
- SBOM Generation tool name and version
- Creation date and time(ISO 8601 format recommended)
- Applied software version
- Contact name and contact information

---

### After deployment(Post-Release)Continuous monitoring of vulnerabilities

ISO/IEC 18974 §4.3.2 requires pre-deployment vulnerability scanning as well as the ability to continuously monitor and respond to new vulnerabilities **post-deployment**. This is because after deployment, versions affected by a publicly disclosed CVE may still be in production for customers.

**Processing flow when new CVE is discovered after distribution:**

1. monitoring tools(Dependency Track, etc.)Receive notifications from
2. `output/process/vulnerability-response.md` Severity assessment according to procedure
3. Critical/High:Immediately schedule patch releases + decide whether to notify customers
4. When Customer Notification Is Required:List of affected versions,Temporary Mitigation Measures,Share expected patch date
5. Maintain records of SBOM updates and responses after patch deployment

Make sure your SBOM is always up to date to immediately know if your software is affected when a new CVE is released. If SBOM is outdated, the monitoring tool will not generate the correct notification.

**Monitoring method:**

- **Dependency Track Notification:** Vulnerability Threshold(CVSS score, etc.)Notify by email or webhook when exceeded
- **GitHub Dependabot:** Automatic PR notification of dependency vulnerabilities in GitHub-based projects
- **Subscribe to OSV.dev:** Subscribe to notifications from the open source vulnerability database operated by Google

**CI/CD automatic monitoring example(weekly scan):**

```yaml
# .github/workflows/vuln-scan.yml
name: Weekly Vulnerability Scan
on:
  schedule:
    - cron: '0 9 * * 1' # 매주 월요일 오전 9시
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate fresh SBOM
        run: |
          syft . -o cyclonedx-json > output/sbom/myapp-latest.cdx.json
      - name: Check SBOM for new CVEs
        run: |
          # Dependency Track API 또는 grype 등으로 스캔
          grype sbom:output/sbom/myapp-latest.cdx.json --fail-on high
```

This workflow automatically scans for vulnerabilities based on the latest SBOM every week.,If a high-severity vulnerability is discovered, the CI build can be failed and the team can be notified.

---

## 3. Self-study

:::info Self-study mode(About 45 minutes)
Interact with the agent to create SBOM management plans and ship-to sharing templates. The agent asks three questions in order,A document is automatically created based on the answers.
:::

**Advance preparation — If you understand the three things below in advance, it will proceed quickly.:**

1. SBOM external(Customer/Supplier)Whether it must be provided to
2. SBOM format required by the supplier(CycloneDX / SPDX / irrelevant)
3. Software release cycle(yes:Once a month,Once a quarter,irregular)

**Step-by-step practice:**

**Step 1.** Briefly note your situation regarding the three questions above.

**Step 2.** Run the agent.

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-management
claude
```

**Step 3.** Answer the three questions asked by the agent in order.

| Question                               | Sample Answer                                                   |
| -------------------------------------- | --------------------------------------------------------------- |
| Should SBOM be provided externally?    | "yes,Supplier A requests it” or “No.,"Internal management only" |
| What format does the supplier require? | "CycloneDX JSON" or "irrelevant"                                |
| What is the release cycle?             | “Once a Quarter” or “Irregularly as Function Completes”         |

**Step 4.** Review the generated document.

```bash
cat output/sbom/sbom-management-plan.md
```

**Step 5.** Fill in the shared template with actual company information.

```bash
# 텍스트 에디터로 열어 [회사명], [담당자명] 등 플레이스홀더 교체
open output/sbom/sbom-sharing-template.md
```

**Step 6.** Apply the SBOM file naming convention to existing files.

```bash
# 예: 기존 파일 이름 변경
mv output/sbom/myapp.cdx.json output/sbom/myapp-v1.0.0-20260320.cdx.json
cp output/sbom/myapp-v1.0.0-20260320.cdx.json output/sbom/myapp-latest.cdx.json
```

**When stuck:** If there is no supplier or the requirements are unclear, the answer is “No external provision.” The agent creates an internal management-oriented plan.

**Expected results:**

- `output/sbom/sbom-management-plan.md`:renewal trigger,renewal cycle,responsible person,Storage Policy,Includes monitoring plan
- `output/sbom/sbom-sharing-template.md`:Cover document provided to delivery address(Includes company information placeholder)

:::info Standard requirements met
Completing this lab will meet the requirements below:

**ISO/IEC 18974**

| Item ID | Requirements                        | Self-certification checklist                                                                          |
| ------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 4.3.1   | SBOM Management and Updates         | Do you have a process for maintaining and updating the SBOM when supply software changes?             |
| 4.3.2   | SBOM-based vulnerability monitoring | Do you have a process for continuously monitoring supply software components for new vulnerabilities? |

:::

---

## 4. Completion Confirmation Checklist

Check all of the items below to complete this chapter.

- [ ] `output/sbom/sbom-management-plan.md` file created
- [ ] `output/sbom/sbom-sharing-template.md` file created
- [ ] SBOM List of update triggers specified in management-plan
- [ ] SBOM The update cycle is defined in conjunction with the release cycle.
- [ ] Name and contact information of person in charge are specified in management-plan
- [ ] Documented external delivery procedures(If there is no delivery destination, indicate “not applicable”)
- [ ] File naming convention(`[project]-[version]-[date].cdx.json`)is defined
- [ ] Retention period policy defined

**sbom-management-plan.md example main sections:**

```markdown
# SBOM 관리 계획

## 1. SBOM 생성 및 갱신 정책

- **갱신 트리거 목록:** 신규 컴포넌트 추가, 버전 변경, 릴리즈, 보안 패치
- **갱신 담당자:** [이름], [역할]
- **갱신 절차:** PR 병합 시 CI/CD 자동 생성 → 담당자 검토 → 보관

## 2. 버전 관리 전략

- **파일 명명 규칙:** `[project]-[version]-[date].cdx.json`
- **보관 위치:** `output/sbom/` (Git 관리)
- **보관 기간:** 릴리즈 유지 기간 + 1년

## 3. 외부 공유 절차

- **공유 대상 및 조건:** [납품처명], 계약서 제X조 요건
- **제공 포맷:** CycloneDX JSON
- **제공 채널:** 보안 파일 공유 링크 (Box)
- **제공 주기:** 릴리즈 시마다, 납품처 요청 시

## 4. 모니터링 계획

- **신규 CVE 알림:** Dependency Track, CVSS 7.0 이상 즉시 알림
- **정기 검토 주기:** 월 1회 담당자 검토
- **자동 스캔:** 매주 월요일 GitHub Actions 실행
```

> This step is ISO/IEC 18974 4.3.1,Meets 4.3.2 requirements.

> 📋 **Example of output**: [SBOM Output Best Practice](/reference/samples/sbom)You can check the actual format of the generated file at .

---

## 5. Next steps

SBOM If a management system is in place,Go to the vulnerability analysis step. Based on SBOM, we analyze the CVEs affected by the current software and,This is the stage of establishing a response plan.

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/05-vulnerability-analyst
claude
```

or [Vulnerability Analysis:Find out the known risks of open source](../vulnerability/index.md)You can read the guide first by going to .

In the vulnerability analysis stage, the previously created `output/sbom/[project].cdx.json` is used as input.,We recommend that you check one more time to ensure that the SBOM file is up to date before proceeding.
