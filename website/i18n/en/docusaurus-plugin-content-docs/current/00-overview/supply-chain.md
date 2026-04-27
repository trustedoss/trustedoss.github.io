---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 1 hour
sidebar_position: 3
sidebar_label: supply chain security
---

# Software Supply Chain Security:Why It Matters Now

## 1. What we do in this chapter

This chapter is a background knowledge chapter to be read only without practice.
Understand the reality of software supply chain security through actual accident cases and,
SBOM(Software Bill of Materials)Why this has become an essential tool,
And we understand the flow of international regulations that require it.

After reading this chapter, you will get a clear answer to the question “Why do you need this kit?”
Everything you do in later chapters — policy making,process design,Create SBOM,vulnerability analysis —
The purpose becomes clearer in the context of this chapter.

---

## 2. What is the software supply chain?

### How open source enters the product

Software is not created alone.
Developer npm, PyPI,Use open source libraries from package repositories such as Maven,
That library depends on another library.
This entire chain structure is the **Software Supply Chain**.

```mermaid
flowchart LR
    A[Open source community] -->|Source code/packages| B[Package registries\nnpm/PyPI/Maven]
    B -->|Install dependencies| C[Developers\nInternal codebase]
    C -->|Build/Release| D[Software product]
    D -->|Delivery/Distribution| E[Customers/Recipients]

    style A fill:#e8f5e9
    style E fill:#e3f2fd
```

Modern software consists of **70-90% open source components**.
This means that there is a lot more code coming from outside than our own code.
This is an advantage that speeds up development, but,At the same time, it is also a conduit through which external threats flow internally.

Supply chain security refers to the risks — vulnerabilities — that can arise throughout this path.,malware,License violation —
refers to a system that identifies and manages

---

## 3. Three real-life supply chain attack cases

The following three examples show that supply chain security is not an abstract concept.

#### SolarWinds (2020)

**Incident Overview**
The attacker installed malware into SolarWinds' internal build pipeline.(Sunburst)inserted.
Normal software update package(Orion Platform)Because it was distributed and included in,
Detection was extremely difficult with existing security tools.

**Scope of Influence**
us treasury,18 worldwide, including federal agencies such as the Department of State,More than 000 organizations
A malicious update was installed. Access to the internal network was allowed undetected for months.

**lesson**
The build pipeline that creates the software itself can be a target of attack.
Where all the components included in the product come from,A system is needed to verify that the build process is safe.

---

#### Log4Shell (2021, CVE-2021-44228)

**Incident Overview**
In Apache Log4j 2, a logging library almost universally used in Java applications.
JNDI(Java Naming and Directory Interface)An injection vulnerability was discovered.
An attacker can execute remote code with a single specially crafted string.(RCE)This was possible.

**Scope of Influence**
Hundreds of millions of systems worldwide were affected., Apple, Amazon, Tesla,Twitter, etc.
Virtually all large technology companies' services were covered.
Millions of exploit attempts were detected within 72 hours of discovery.

**lesson**
Even patching is impossible if you don’t know where and which open source is being used.
If we had SBOM, we would have been able to immediately identify and respond to all systems using Log4j.

---

#### XZ Utils (2024, CVE-2024-3094)

**Incident Overview**
The attacker had been working on the XZ Utils open source project for two years under the pseudonym "Jia Tan".
Acted as a reliable contributor. After building trust through regular contributions over a long period of time,,
sshd(SSH daemon)committed malicious code to insert a backdoor into
Full-scale spread was prevented due to the discovery of anomalies by a developer just before distribution.

**Scope of Influence**
Fedora, Debian,Many major Linux distributions, including Ubuntu, already included vulnerable versions.
If discovery had been delayed by just a few days, backdoors would have been planted on millions of servers.

**lesson**
The identity and long-term behavioral patterns of open source project contributors should be monitored.
Management status of dependent open source projects(governance,Maintainer activities)It is also part of supply chain security.

---

## 4. International regulatory trends

Supply chain security is now moving beyond voluntary best practice and becoming a legal requirement.

#### U.S. Executive Order EO 14028(2021)

**background**
SolarWinds,In response to a series of large-scale supply chain attacks such as Microsoft Exchange,
This is an executive order strengthening cybersecurity signed by the Biden administration in May 2021.

**Key Requirements**

- Mandatory submission of **SBOM for software delivered to the federal government**
- NTIA(U.S. Communications and Information Administration)Complies with the **SBOM minimum elements** criteria defined by
- Software Development Security Practices(Secure Software Development Practices)Compliance confirmation

**Impact on Korean companies**
Companies that supply directly to the U.S. federal government are immediately affected.
indirect supply chain(Subcontracting by the delivery company)Since there is a trend of receiving the same requirements,,
It should be assumed that most companies operating in the US market will be affected.

---

#### EU Cyber Resilience Act - CRA (2024)

**background**
To strengthen the cybersecurity of digital products launched in the EU Digital Single Market
This is an EU-wide regulation adopted in 2024.

**Key Requirements**

- Digital products launching on the EU market(Software included)Apply security requirements to
- Mandatory management of open source component list and response to vulnerabilities
- Scheduled to be fully implemented in 2027

**sanctions**
Up to **1 in case of default,EUR 5 million** or **2.5% of annual global sales**, whichever is greater.

**Impact on Korean companies**
This applies to **any business** that sells software products or services in the EU.
cloud service,mobile app,All products with digital elements, such as IoT devices, are eligible.

---

#### domestic trends

Discussions on mandatory supply chain security are also progressing rapidly in Korea.

- **Ministry of Science and Technology/KISA Software Supply Chain Security Guidelines(2023)**:Korea’s first official guideline recommending the introduction of SBOM
- **Review of public SW project SBOM introduction**:We are considering a plan to require submission of SBOM for software projects ordered by public institutions.
- **Discussion on mandatory domestic SBOM**:It is highly likely that similar domestic regulations will be introduced after the implementation of EU CRA.

---

## 5. How both standards contribute to supply chain security

ISO/IEC 5230 and ISO/IEC 18974 each address two key risks in supply chain security.

- **ISO/IEC 5230**:Eliminate the risk of license violations by ensuring transparency in the use of open source
- **ISO/IEC 18974**:Eliminate security risks by identifying and responding to known vulnerabilities

Compliance with both standards together covers both the **licensing** and **security** sides of supply chain security.

| Risk type              | Responsible Standard | Main tools          |
| ---------------------- | -------------------- | ------------------- |
| License violation      | ISO/IEC 5230         | SBOM + License Scan |
| Security vulnerability | ISO/IEC 18974        | SBOM + CVE scan     |

The common core tool for both standards is **SBOM**.
You must have SBOM to scan the license.,You can also search for CVEs.
As we saw in the Log4Shell example:,Without SBOM you wouldn't even know where something is.

---

## 6. Self-study path

:::info Self-study mode(About 1 hour)
You can just read this chapter. Focus on understanding the concepts.
:::

1. Read this article — Get the full context of supply chain security
2. 3 key lessons from accident cases summarized in your own words
3. Check which items apply to your company among international regulations
4. Read `sbom-101.md` → SBOM Detailed understanding of technical concepts

---

## 7. Completion Confirmation Checklist

- [ ] 3 supply chain security incidents(SolarWinds, Log4Shell, XZ Utils)can explain
- [ ] I understand why SBOM is needed
- [ ] We identified the impact of EO 14028 / EU CRA on our company
- [ ] Understand the role both standards play in supply chain security

---

## 8. Next steps

- **SBOM Learn technical concepts**:Go to `sbom-101.md` and then CycloneDX,Learn SPDX format and SBOM minimum elements
- **Go straight to environment preparation**:Go to `docs/01-setup/` and start installing the toolchain.

If you have a sufficient understanding of the concept, you can start practicing from `docs/01-setup/`.
You can come back to this chapter and refer to it at any time.
