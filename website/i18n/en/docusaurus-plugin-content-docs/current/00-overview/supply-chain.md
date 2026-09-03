---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 1 hour
sidebar_position: 4
sidebar_label: Supply chain security
---

# Software Supply Chain Security: Why It Matters Now

## 1. What this chapter covers

This is a background chapter — read it, no hands-on work required. Through real-world incidents, you will see what software supply chain security looks like in practice, why an SBOM (Software Bill of Materials) has become an essential tool, and how international regulations now require it.

After reading this chapter, you will have a clear answer to the question "Why do I need this kit?" Everything you do in later chapters — writing policy, designing processes, creating an SBOM, analyzing vulnerabilities — makes more sense in the context laid out here.

---

## 2. What is the software supply chain?

### How open source enters a product

Software is never built in isolation. Developers pull open source libraries from package registries such as npm, PyPI, and Maven, and each of those libraries depends on still other libraries. This entire chain is the **software supply chain**.

```mermaid
flowchart LR
    A[Open source community] -->|Source code/packages| B[Package registries\nnpm/PyPI/Maven]
    B -->|Install dependencies| C[Developers\nInternal codebase]
    C -->|Build/Release| D[Software product]
    D -->|Delivery/Distribution| E[Customers/Recipients]

    style A fill:#e8f5e9
    style E fill:#e3f2fd
```

Modern software is **70-80% open source components**. In other words, far more code comes from outside than your team writes itself. This speeds up development, but it is also a conduit through which external threats can flow inward.

Supply chain security is the discipline of identifying and managing the risks that can arise anywhere along this path — vulnerabilities, malware, and license violations.

---

## 3. Real-world supply chain attacks

The cases below show that supply chain security is anything but an abstract concept. The first three targeted source code and maintainer trust, the pattern of the early years. The last two show where attacks moved from 2025 onward: stolen credentials and hijacked build pipelines.

### SolarWinds (2020)

**What happened**
Attackers inserted malware (Sunburst) into SolarWinds' internal build pipeline. Because it was bundled into a legitimate software update (the Orion Platform) and distributed that way, existing security tools had an extremely hard time detecting it.

**Scope of impact**
More than 18,000 organizations worldwide — including federal agencies such as the U.S. Treasury and the Department of State — installed the malicious update. Attackers had undetected access to internal networks for months.

**Lesson**
The build pipeline that produces the software can itself be a target. You need a system that verifies where every component in the product comes from and that the build process is safe.

---

### Log4Shell (2021, CVE-2021-44228)

**What happened**
An injection vulnerability was found in Apache Log4j 2, a logging library used almost universally across Java applications. It abused JNDI (Java Naming and Directory Interface), letting an attacker achieve remote code execution (RCE) with a single specially crafted string.

**Scope of impact**
Hundreds of millions of systems worldwide were affected, covering the services of virtually every major technology company — Apple, Amazon, Tesla, Twitter, and more. About 800,000 exploit attempts were detected within 72 hours of disclosure, and millions over the following weeks.

**Lesson**
You cannot even patch what you cannot find. With an SBOM, every system using Log4j could have been identified and remediated immediately.

---

### XZ Utils (2024, CVE-2024-3094)

**What happened**
Over two years, an attacker using the pseudonym "Jia Tan" contributed to the XZ Utils open source project, posing as a trustworthy maintainer. After building credibility through steady contributions, they committed malicious code that planted a backdoor in sshd (the SSH daemon). A widespread compromise was averted only because a developer noticed anomalies just before the release shipped.

**Scope of impact**
Development and beta channels of major distributions — Fedora beta, Debian testing, openSUSE Tumbleweed — had pulled in the vulnerable versions, and the discovery came just before stable releases. Had discovery been delayed by even a few days, backdoors would have landed on millions of servers.

**Lesson**
The identity and long-term behavior of open source contributors deserve scrutiny. The health of the open source projects you depend on, meaning their governance and maintainer activity, is also part of supply chain security.

---

### tj-actions/changed-files (2025-03, CVE-2025-30066)

**What happened**
Several version tags of `tj-actions/changed-files`, a widely used GitHub Action, were retargeted to point at a single malicious commit. Tags including `v1.0.0`, `v35.7.7-sec`, and `v44.5.1` all moved to that commit, whose script dumped secrets out of the Runner Worker process memory and printed them into the workflow logs.

**Scope of impact**
More than 23,000 repositories used the action. In repositories with public logs, API keys, cloud credentials, and SSH keys were exposed in plain text. Not a single line of application code changed. The attack was active on 2025-03-14 and 15, and was fixed in 46.0.1 (CVSS 8.6).

**Lesson**
Your dependency inventory includes not only libraries but also the actions and tools your build runs. A movable tag such as `@v45` can point at a different commit at any time, so pinning to a 40-character commit SHA is what actually fixes the code that runs.

---

### The Shai-Hulud lineage and ChainDrop (2025-2026)

**What happened**
The Shai-Hulud worm, first observed on npm in 2025-09, used each victim's stolen npm token to reinfect the packages they maintained and spread to more than 500 packages. It was followed by Shai-Hulud 2.0 in 2025-11, several variants through the first half of 2026, and then ChainDrop on 2026-08-04. ChainDrop did not steal npm tokens: it compromised a maintainer's GitHub account and triggered the legitimate release workflows. As a result, the malicious versions were published with valid SLSA provenance attestations.

**Scope of impact**
Starting from `keyv`, `flat-cache`, and `file-entry-cache`, packages with over 100 million weekly downloads each, 444 packages and 2,212 versions were poisoned in under four hours. The payload harvested secrets from CI runner memory along with AWS, Kubernetes, and Vault credentials.

**Lesson**
The persistence mechanism is the part worth studying. ChainDrop's payload planted a `SessionStart` hook in the Claude Code settings file (`.claude/settings.json`) and a folder-open task in VS Code's `.vscode/tasks.json` inside the repositories it compromised. Simply opening that repository runs the payload again. Configuration files for AI coding tools are execution paths, so a configuration file that arrives from a repository deserves the same review as source code. Provenance attestations alone also do not guarantee safety: a compromised pipeline issues valid attestations through the normal process, and the consumer cannot tell the difference.

---

### Where the attacks moved

In the first three cases, attackers went after source code or maintainer trust. In the cases from 2025 onward, they go after the accounts that hold publishing rights and the build pipelines themselves. Hijacking a single release workflow lets an attacker ship a malicious version that is indistinguishable from a legitimate release, without touching library source at all. Managing an inventory of open source components is therefore no longer enough: the pipeline that pulls those components in and builds them has to be under control as well. For the practical measures, see [Pipeline Security and Build Provenance](/devsecops/pipeline-security).

---

## 4. International regulatory trends

Supply chain security is moving beyond voluntary best practice and becoming a legal requirement.

### U.S. Executive Order EO 14028 (2021)

**Background**
In response to a series of large-scale supply chain attacks such as SolarWinds and Microsoft Exchange, the Biden administration signed this cybersecurity executive order in May 2021.

**Key content and what changed since**

- It directed agencies to establish SBOM guidance for software delivered to the federal government,
  and the **SBOM minimum elements** defined by the NTIA (National Telecommunications and Information
  Administration) date from this effort.
- The administration's course has since changed: EO 14306 (2025-06) removed the SBOM artifact
  requirements, and OMB M-26-05 (2026-02) rescinded the blanket attestation mandates, moving to a
  **risk-based, per-agency approach**.

- The minimum elements themselves were updated in 2026-07. The **2026 Minimum Elements for a SBOM**,
  published by CISA, the NSA, the FBI, and international partner agencies including Korea, replaces
  the NTIA 2021 baseline and makes component hashes and licenses required fields.

**Impact on Korean companies**
The blanket SBOM mandate for U.S. federal procurement has been relaxed, but the minimum-elements
baseline continues through the CISA 2026 edition and still functions as the de facto standard. The
practical SBOM demands now come from the EU CRA and customer procurement contracts. Companies active
in the U.S. market should prepare for contract-level requirements.

---

### EU Cyber Resilience Act — CRA (2024)

**Background**
An EU-wide regulation adopted in 2024 to strengthen the cybersecurity of digital products placed on the EU Digital Single Market.

**Key requirements**

- Apply security requirements to digital products placed on the EU market (software included)
- Mandatory management of the open source component list and remediation of vulnerabilities
- **Reporting duties for actively exploited vulnerabilities and severe incidents apply first, from
  2026-09-11**; the essential requirements apply in full from 2027-12-11.

**Penalties**
For non-compliance, up to **EUR 15 million** or **2.5% of annual global turnover**, whichever is greater.

**Impact on Korean companies**
This applies to **any business** that sells software products or services in the EU. All products with digital elements — cloud services, mobile apps, IoT devices — are in scope.

---

### Trends in Korea

Korean policy started with advisory guidelines and has moved on to a roadmap with a phased schedule.

**SW Supply Chain Security Guideline 1.0 (2024-05-13)**
Published jointly by the Ministry of Science and ICT (MSIT), the National Intelligence Service (NIS), and the Presidential Committee on Digital Platform Government, and distributed by KISA. Its stated purpose is to help government bodies, public institutions, and companies build their own capability to manage software supply chain security, with the SBOM submission requirements emerging in the United States and Europe as background. It comes in a full version and a summary, and English and Spanish summaries were added on 2024-09-12.

**Phased implementation plan for SW supply chain security (2026-06-24)**
MSIT released this under the title "Government announces a phased implementation plan (roadmap) for software supply chain security," with the NIS and KISA taking part. Its stated goal is "securing cyber resilience through a transition to a safe and responsible supply chain security system," and it sets out the three strategies below.

| Strategy                                | Content                                                              |
| --------------------------------------- | -------------------------------------------------------------------- |
| Strengthen threat prevention capability | Build management capability upstream, before threats enter the chain |
| Establish rapid detection and response  | Put detection and response procedures in place for compromises       |
| Build the policy and institutional base | Prepare the institutional and support framework                      |

:::info Check the source document for the detailed tasks
The detailed tasks under each strategy and the year-by-year schedule are in the attached documents. Check the source directly for when and to what scope public procurement will require an SBOM. Both documents can be downloaded from the [KISA guideline library](https://www.kisa.or.kr/2060204).
:::

**Impact on Korean companies**
This is not yet a legal obligation with penalties attached, unlike the EU CRA. That said, public procurement requirements and large-enterprise supplier requirements tend to track the roadmap, so building out SBOM generation and vulnerability response ahead of time pays off.

---

## 5. How both standards contribute to supply chain security

ISO/IEC 5230 and ISO/IEC 18974 each address one of the two key risks in supply chain security.

- **ISO/IEC 5230**: removes the risk of license violations by ensuring transparency in open source use.
- **ISO/IEC 18974**: removes security risk by identifying and responding to known vulnerabilities.

Conforming to both standards together covers both the **licensing** and the **security** side of supply chain security.

| Risk type              | Responsible Standard | Main tools          |
| ---------------------- | -------------------- | ------------------- |
| License violation      | ISO/IEC 5230         | SBOM + License Scan |
| Security vulnerability | ISO/IEC 18974        | SBOM + CVE scan     |

The core tool shared by both standards is the **SBOM**. You need an SBOM to scan licenses, and you need it to look up CVEs. As the Log4Shell case showed, without an SBOM you cannot even tell where a component is being used.

---

## 6. Assessing your organization's supply chain risk

Now that you know the incidents and the regulations, the next question is "So how much risk does my organization carry?" Below is a simple assessment framework you can start with, no tools required.

### The four assessment axes

Gauge each open source component (or the product as a whole) along the four axes below. The higher the rating, the greater the risk.

| Assessment axis      | Key question                                                                                   | High-risk case                                                   |
| -------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Dependency depth** | Did you pull it in directly, or was it pulled in by another library (a transitive dependency)? | When a large share of dependencies are invisible transitive ones |
| **Exposure surface** | Does it process external input directly (parsers, networking, deserialization)?                | When it processes external input                                 |
| **Project health**   | Are the maintainers active? Are there recent releases and contributors?                        | When the project is unmaintained (the XZ Utils lesson)           |
| **Blast radius**     | If it is compromised, how far does the damage reach (authentication, payments, customer data)? | When it can reach critical assets                                |

### Dependency depth — the most commonly missed risk

Libraries you pull in directly (direct dependencies) are visible, but the **transitive dependencies** they pull in — dependencies of dependencies — are not. For both Log4Shell and XZ Utils, the reaction in many organizations was "but I never used that directly." An SBOM lays out all of these transitive dependencies, which makes it the starting point for risk assessment.

### A three-step assessment procedure

1. **Get the inventory** — use an SBOM to build a component list that includes transitive dependencies ([Create SBOM](../05-tools/sbom-generation/index.md)).
2. **Identify high risk** — rate each component high/medium/low along the four axes above and single out the high-risk ones.
3. **Apply first where it matters** — apply policy (approved licenses and approvals), vulnerability response, and continuous monitoring to the high-risk components first.

:::info Regular reviews
This assessment is not a one-time exercise. Dependencies and threats keep changing, so revisit it regularly.
:::

---

## 7. Self-study

:::info Self-study mode (about 1 hour)
You can simply read this chapter. Focus on understanding the concepts.
:::

1. Read this page — get the full context of supply chain security
2. Summarize, in your own words, the key lessons from the incidents
3. Identify which international regulations apply to your company
4. Read `sbom-101.md` for a detailed understanding of SBOM technical concepts

---

## 8. Completion checklist

- [ ] I can explain the supply chain security incidents (SolarWinds, Log4Shell, XZ Utils, tj-actions, ChainDrop)
- [ ] I can explain why the attack surface shifted from maintainer trust to credentials and build pipelines
- [ ] I understand why an SBOM is needed
- [ ] I have identified how EO 14028, the EU CRA, and Korea's phased implementation plan affect my company
- [ ] I understand the role each standard plays in supply chain security
- [ ] I can gauge my organization's high-risk components using the four assessment axes

---

## 9. Next steps

- **Learn the SBOM technical concepts**: go to `sbom-101.md` to learn the CycloneDX and SPDX formats and the SBOM minimum elements.
- **Go straight to environment preparation**: go to `docs/01-setup/` and start installing the toolchain.

Once you understand the concepts well enough, you can begin the hands-on work in `docs/01-setup/`. You can return to this chapter for reference at any time.
