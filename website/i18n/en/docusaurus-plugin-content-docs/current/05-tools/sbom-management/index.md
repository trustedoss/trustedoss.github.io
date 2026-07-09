---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: [4.3.1, 4.3.2]'
self_study_time: 1 hour
---

# SBOM management: creating it is not the end; managing it is the beginning

## 1. What we do in this chapter

Creating an SBOM once is not enough. Software changes constantly, and new vulnerabilities are disclosed every day. In this chapter, you establish a process to update the SBOM in step with your release cycle, store it by version, and share it systematically with external customers or suppliers.

Running the `agents/05-sbom-management` agent produces two outputs: `output/sbom/sbom-management-plan.md`, which defines the update cycle and the responsible owner, and `output/sbom/sbom-sharing-template.md`, a cover document for delivering the SBOM to a supplier. Once these two documents are complete, the foundation for your SBOM management system is in place.

---

## 2. Background knowledge

### An SBOM is not something you make once and forget

Whenever the software changes, the SBOM must change with it. A stale, unmaintained SBOM can be more dangerous than none at all. Trusting an out-of-date SBOM creates security blind spots, because the actual components and the documentation no longer match.

**Real-world example:** an organization trusted an SBOM created six months earlier and failed to notice the vulnerable libraries added since then. Even after a CVE was disclosed in one of those libraries, the organization did not realize it was affected — the customer discovered the problem first, and trust was lost.

---

### SBOM update triggers

The SBOM must be updated whenever one of the events below occurs.

| Event                                | When to update             | Notes                           |
| ------------------------------------ | -------------------------- | ------------------------------- |
| Add a new open source component      | Immediately (on PR merge)  | CI/CD automation recommended    |
| Change an existing component version | Immediately (on PR merge)  | Especially for security patches |
| Software release                     | Just before release        | Release SBOM stored separately  |
| Security vulnerability patch         | When the patch is complete | Serves as proof of response     |

The most important of these is **right before a software release**. The SBOM at release time is the official record of that version's components, so it should be stored separately and clearly tagged with the version.

---

### SBOM version management strategy

A file naming convention for Git-based SBOM versioning:

```
output/sbom/[project]-[version]-[date].cdx.json
```

Example:

```
output/sbom/myapp-v1.2.0-20260320.cdx.json
output/sbom/myapp-v1.1.0-20260101.cdx.json
output/sbom/myapp-latest.cdx.json  ← always points to the latest
```

`myapp-latest.cdx.json` always points to the most recently created SBOM, while the per-release files are kept in separate directories or tags according to your storage policy.

**Why you should keep release-specific SBOMs:**

- You can prove a version's components at a specific point in time when responding to regulations
- When a vulnerability is found, you can quickly determine the range of affected versions
- You can meet the requirements of emerging regulations such as the EU CRA and EO 14028

Recommended retention period: the software release's maintenance period plus at least one year.

---

### Providing the SBOM to suppliers and customers

**When to provide an SBOM:**

- When the supplier explicitly requests one
- When the contract includes a clause requiring SBOM delivery
- When EO 14028 applies (delivery to the U.S. federal government)
- When the EU CRA applies (entering the EU market; enforcement in 2027)
- When participating in a large enterprise supply chain management program (an increasing trend, including Samsung and Hyundai Motor)

**Pros and cons of each delivery method:**

| Method                                  | Best suited for                  | Cautions                                      |
| --------------------------------------- | -------------------------------- | --------------------------------------------- |
| Email attachment                        | Small scale, occasional delivery | Hard to version, risk of loss                 |
| Secure file sharing (Google Drive, Box) | Medium scale, regular delivery   | Requires access control                       |
| API                                     | Large scale, automation needed   | Requires initial development effort           |
| Portal / web                            | Serving many customers at once   | Requires infrastructure setup and maintenance |

**Information to include when providing an SBOM** (covered by `sbom-sharing-template.md`):

- The SBOM file itself (CycloneDX JSON or SPDX format)
- The SBOM generation tool name and version
- The creation date and time (ISO 8601 format recommended)
- The applicable software version
- A contact name and contact details

---

### Continuous vulnerability monitoring after deployment (post-release)

ISO/IEC 18974 §4.3.2 requires not only pre-deployment vulnerability scanning but also the ability to continuously monitor and respond to new vulnerabilities **after deployment**. This is because, once shipped, versions affected by a newly disclosed CVE may still be running in customer production environments.

**Workflow when a new CVE is discovered after release:**

1. Receive an alert from a monitoring tool (Dependency Track, etc.)
2. Assess severity following the `output/process/vulnerability-response.md` procedure
3. Critical/High: schedule a patch release immediately and decide whether to notify customers
4. When customer notification is required: share the list of affected versions, temporary mitigations, and the expected patch date
5. Keep records of the SBOM update and the response after the patch is deployed

Keep your SBOM up to date so you can immediately tell whether your software is affected when a new CVE is disclosed. If the SBOM is stale, the monitoring tool will not raise the correct alert.

**Monitoring methods:**

- **Dependency Track alerts:** notify by email or webhook when a vulnerability exceeds a threshold (CVSS score, etc.)
- **GitHub Dependabot:** automatic PR alerts for dependency vulnerabilities in GitHub-based projects
- **OSV.dev subscription:** subscribe to alerts from the open source vulnerability database operated by Google

**CI/CD automated monitoring example (weekly scan):**

```yaml
# .github/workflows/vuln-scan.yml
name: Weekly vulnerability Scan
on:
  schedule:
    - cron: '0 9 * * 1' # every Monday at 9 AM
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - name: Generate fresh SBOM
        run: |
          syft . -o cyclonedx-json > output/sbom/myapp-latest.cdx.json
      - name: Check SBOM for new CVEs
        run: |
          # Scan with Dependency-Track API or grype
          grype sbom:output/sbom/myapp-latest.cdx.json --fail-on high
```

This workflow automatically scans for vulnerabilities against the latest SBOM every week. If a high-severity vulnerability is found, the CI build can be failed and the team notified.

---

## 3. Self-study

:::info Self-study mode (about 45 minutes)
Work with the agent to create an SBOM management plan and a sharing template for recipients. The agent asks three questions in order and generates a document automatically from your answers.
:::

**Preparation — knowing the three things below in advance makes this go faster:**

1. Whether the SBOM must be provided externally (to customers/suppliers)
2. The SBOM format the supplier requires (CycloneDX / SPDX / no preference)
3. Your software release cycle (e.g. monthly, quarterly, irregular)

**Step-by-step practice:**

**Step 1.** Briefly note your situation for the three questions above.

**Step 2.** Run the agent.

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-management
claude
```

**Step 3.** Answer the agent's three questions in order.

| Question                                | Sample answer                                            |
| --------------------------------------- | -------------------------------------------------------- |
| Should the SBOM be provided externally? | "Yes, Supplier A requests it" or "No, internal use only" |
| What format does the supplier require?  | "CycloneDX JSON" or "No preference"                      |
| What is your release cycle?             | "Quarterly" or "Irregular, as features are completed"    |

**Step 4.** Review the generated document.

```bash
cat output/sbom/sbom-management-plan.md
```

**Step 5.** Fill in the shared template with actual company information.

```bash
# Open with a text editor and replace placeholders such as [Company Name], [Program Manager Name]
open output/sbom/sbom-sharing-template.md
```

**Step 6.** Apply the SBOM file naming convention to existing files.

```bash
# Example: rename existing file
mv output/sbom/myapp.cdx.json output/sbom/myapp-v1.0.0-20260320.cdx.json
cp output/sbom/myapp-v1.0.0-20260320.cdx.json output/sbom/myapp-latest.cdx.json
```

**When stuck:** if there is no supplier or the requirements are unclear, answer "No external provision." The agent will create an internally-focused plan.

**Expected results:**

- `output/sbom/sbom-management-plan.md`: includes update triggers, update cycle, responsible owner, storage policy, and monitoring plan
- `output/sbom/sbom-sharing-template.md`: cover document for the recipient (includes company information placeholders)

:::info Standard requirements met
Completing this lab will meet the requirements below:

**ISO/IEC 18974**

| Item ID | Requirements                        | Self-certification checklist                                                                          |
| ------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 4.3.1   | SBOM Management and Updates         | Do you have a process for maintaining and updating the SBOM when supply software changes?             |
| 4.3.2   | SBOM-based vulnerability monitoring | Do you have a process for continuously monitoring supply software components for new vulnerabilities? |

:::

---

## 4. Completion checklist

Check all of the items below to complete this chapter.

- [ ] `output/sbom/sbom-management-plan.md` file created
- [ ] `output/sbom/sbom-sharing-template.md` file created
- [ ] The list of SBOM update triggers is specified in the management plan
- [ ] The SBOM update cycle is defined in relation to the release cycle
- [ ] The name and contact details of the responsible owner are specified in the management plan
- [ ] The external delivery procedure is documented (if there is no recipient, mark it "not applicable")
- [ ] The file naming convention (`[project]-[version]-[date].cdx.json`) is defined
- [ ] The retention period policy is defined

**Main sections of an example sbom-management-plan.md:**

```markdown
# SBOM Management Plan

## 1. SBOM Generation and Update Policy

- **Update trigger list:** new Component addition, Version changed, release, security patches
- **update owner:** [Name], [Role]
- **update procedure:** On PR merge: auto-generate in CI/CD -> Program Manager review -> archive

## 2. versioning strategy

- **file naming convention:** `[project]-[version]-[date].cdx.json`
- **storage location:** `output/sbom/` (Git managed)
- **retention period:** release retention period + 1 year

## 3. external sharing procedure

- **sharing recipients and conditions:** [customer name], contract Clause X requirements
- **delivery format:** CycloneDX JSON
- **delivery channel:** secure file-sharing link (Box)
- **delivery frequency:** for each release and upon customer request

## 4. monitoring plan

- **new CVE alerts:** Dependency Track, CVSS 7.0 or later Immediate alerts
- **regular review cycle:** monthly Program Manager review
- **automated scan:** Run GitHub Actions every Monday
```

> This step meets ISO/IEC 18974 4.3.1 and 4.3.2 requirements.

> 📋 **Example output**: see the actual format of the generated file at [SBOM output best practice](/reference/samples/sbom).

---

## 5. Next steps

Once your SBOM management system is in place, move on to the vulnerability analysis step. There, you use the SBOM to analyze which CVEs affect your current software and establish a response plan.

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/05-vulnerability-analyst
claude
```

Or read the guide first at [Vulnerability analysis: uncover the known risks in open source](../vulnerability/index.md).

The vulnerability analysis stage uses the `output/sbom/[project].cdx.json` you created earlier as its input, so we recommend double-checking that the SBOM file is up to date before you proceed.
