---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: [3.3.1, 3.3.2, 3.4.1]'
  - 'ISO/IEC 18974: [4.3.1]'
self_study_time: 1.5 hours
---

# Create SBOM: Build a software bill of materials with syft and cdxgen

## 1. What we do in this chapter

In this chapter, you use syft and cdxgen to generate a CycloneDX-format SBOM (Software Bill of Materials) for your project. Both tools run with Docker, so no separate installation is required. With a few lines of commands, you can produce your project's entire dependency list as a JSON file.

The generated SBOM later becomes the basis for license analysis (05-sbom-analyst) and vulnerability scanning (05-vulnerability-analyst). The more accurate the SBOM, the better you can identify compliance risks and security vulnerabilities.

:::note How SBOM, vulnerability analysis, and SCA relate
The **SBOM** (software bill of materials) is the input; **vulnerability analysis** is the step that uses that SBOM to find risks.
Running both together automatically in CI is **SCA** (Software Composition Analysis) — automation is covered in [DevSecOps → SCA](/devsecops/sca).
:::

---

## 2. Background knowledge

:::tip
For plain-language explanations of unfamiliar acronyms such as SBOM, CycloneDX, and SPDX, see the [glossary](/reference/glossary).
:::

### What is SBOM?

An SBOM (Software Bill of Materials) is a list of every component included in the software. Like a food nutrition label, it specifies which open source packages and versions the software contains. Both ISO/IEC 5230 and 18974 specify SBOM generation as a core requirement (G3B.1).

Why SBOM matters:

- Know which open source licenses are included (compliance)
- Check whether you ship a vulnerable version of a library (security)
- Provide software composition information to customers or regulators when distributing products

### The tools used

There are two approaches to generating an SBOM. **Dependency analysis** identifies dependencies declared in package manager files (pom.xml, package-lock.json, etc.), while **source code scanning** detects open source embedded directly in your code at the file level. By combining the two, you can build a more complete SBOM that also covers copied or pasted code fragments that have no package declaration.

**Dependency analysis tools** (used in this chapter)

| Tool   | Vendor    | Features                                            | Best suited for                                        |
| ------ | --------- | --------------------------------------------------- | ------------------------------------------------------ |
| syft   | Anchore   | Fast and lightweight, single binary, many languages | Python, Node.js, Go                                    |
| cdxgen | CycloneDX | CycloneDX only, detailed per-language analysis      | Java (Maven/Gradle), when precise analysis is required |

Both tools can output CycloneDX JSON; this chapter uses CycloneDX as the standard format.

**Source code scanning tool** (optional)

| Tool    | Vendor  | Features                                                                        | Best suited for                                                         |
| ------- | ------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| SCANOSS | SCANOSS | File-by-file snippet scanning, cloud + on-premise, API integration, SBOM output | Detecting directly embedded source code, precise license identification |

[SCANOSS](https://www.scanoss.com/) excels at detecting open source code fragments that were copied and pasted directly, without any package declaration, at the file level. Because its role complements syft/cdxgen, using it in parallel is recommended when source-level precision is required.

:::tip Integrated option from Korea — BomLens (SK Telecom)
If you need to handle many languages and scan targets in one run, [BomLens](https://github.com/sktelecom/bomlens) is convenient. It accepts source code, container images, binaries and RootFS, firmware, SBOMs you received (for reassessment), and even HuggingFace models (ML-BOM), and produces a CycloneDX SBOM together with an attribution notice (NOTICE) and a license/security risk report. It wraps syft, cdxgen, and Trivy under the hood, is Apache-2.0, and runs entirely locally on Docker with no data leaving your machine. Besides the CLI it offers a web UI and desktop installers. Keep syft as this chapter's main tool and consider BomLens when you need an integrated run.
:::

:::tip
For a guide to adopting and using SCA and compliance tools such as FOSSLight, SW360, and FOSSology, see [KWG Open Source Guide — Tools](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/4-tool/).
:::

For the actual Docker commands, GitHub Actions CI/CD setup, and the sample project walkthrough, see the [Docker and CI/CD execution guide](./docker-cicd.md).

### CycloneDX JSON format main fields

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.7",
  "serialNumber": "urn:uuid:1b2f3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
  "metadata": {
    "timestamp": "2026-08-20T09:30:00Z",
    "lifecycles": [{"phase": "build"}],
    "tools": {
      "components": [
        {
          "type": "application",
          "author": "anchore",
          "name": "syft",
          "version": "1.51.1"
        }
      ]
    },
    "component": {
      "name": "my-app",
      "version": "1.0.0",
      "type": "application"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "log4j-core",
      "version": "2.14.1",
      "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "supplier": {"name": "Apache Software Foundation"},
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "3a5f1b9f2c7d4e8a1b0c6d5e4f3a2b1c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a"
        }
      ],
      "licenses": [{"license": {"id": "Apache-2.0"}}]
    }
  ]
}
```

Key field descriptions:

| Field                         | Description                                                                                         |
| ----------------------------- | --------------------------------------------------------------------------------------------------- |
| `bomFormat`, `specVersion`    | CycloneDX format identifier and specification version. Both syft and cdxgen emit 1.7 by default     |
| `metadata.timestamp`          | When the SBOM was generated                                                                         |
| `metadata.tools.components[]` | Name and version of the tool that built the SBOM, the "SBOM generation tool" CISA 2026 requires     |
| `metadata.lifecycles[]`       | Lifecycle phase the SBOM was captured in, the "generation context"                                  |
| `metadata.component`          | Information about the software being analyzed                                                       |
| `components[].supplier`       | Supplier of the component                                                                           |
| `components[].hashes[]`       | Component file hash. The `alg` (SHA-256 and so on) and `content` (hex value) pair proves integrity  |
| `components[].licenses[]`     | License of the component                                                                            |
| `components[].purl`           | PURL (Package URL, a standard string that uniquely identifies a package)                            |
| `signature`                   | Top-level BOM signature in JSON Signature Format (JSF), which proves the SBOM was not tampered with |
| `vulnerabilities[]`           | Vulnerability information (if present)                                                              |

Hashes, the generation tool name, the generation context, and licenses are the fields that the CISA 2026
minimum elements described in [SBOM Basics: An Introduction to the Software Bill of Materials](../../00-overview/sbom-101.md)
newly made mandatory or promoted to core fields. Which of them actually get filled in depends on the tool
and the ecosystem.

| Field                 | syft                                                | cdxgen                                                            |
| --------------------- | --------------------------------------------------- | ----------------------------------------------------------------- |
| `metadata.tools`      | Filled (name `syft`, author `anchore`)              | Filled                                                            |
| `metadata.lifecycles` | Not filled                                          | Filled (`pre-build`, `build`, `post-build` decided automatically) |
| `components[].hashes` | Not filled for package components                   | Filled when a lock file or archive exposes a hash                 |
| `signature`           | Needs a separate signing step (in-toto attestation) | `--generate-key-and-sign` produces a JSF signature                |

If you need the lifecycle phase or hashes and syft leaves them empty, generate the same project once more
with cdxgen and compare. To pin the specification version, use `-o cyclonedx-json@1.7` with syft and
`--spec-version 1.7` with cdxgen.

:::tip MCP servers belong in the SBOM too
For how to list MCP (Model Context Protocol, the convention by which an agent calls external tools)
servers that AI agents call, see [Agent and MCP Tool Governance](/ai-coding/agent-governance).
No standards body guidance exists yet, so this area interprets the existing specification.
:::

---

## 3. Self-study

:::info Self-study mode (approximately 1 hour 30 minutes)
The first run may take an extra 10-15 minutes while Docker images are pulled.
:::

Step-by-step practice:

**Step 1** — Verify Docker Desktop is running

```bash
docker ps
```

If it runs without errors, Docker is ready.

:::tip When proceeding without Docker
If you don't have Docker installed, or just want to get started quickly for lab purposes, use the pre-prepared sample SBOM with the command below.

```bash
mkdir -p output/sbom
cp output-sample/sbom/fixture-sample.cdx.json output/sbom/fixture-sample.cdx.json
```

The sample SBOM includes GPL-2.0 copyleft components and packages with CVE vulnerabilities, so you can still practice the later analysis steps.
In this case, skip the SBOM generation steps 4-6 (the sbom-guide agent and script) and jump straight to **Step 7 (run the license analysis)**.
:::

**Step 2** — Select a project to analyze

You can use your own project, or one of the bundled samples.

If this is your first time, choose one of the samples below:

| Sample path                     | Language      | Features                            | Learning points                           |
| ------------------------------- | ------------- | ----------------------------------- | ----------------------------------------- |
| `samples/java-vulnerable/`      | Java (Maven)  | Includes Log4Shell (CVE-2021-44228) | Critical vulnerability detection practice |
| `samples/python-mixed-license/` | Python (pip)  | Mixed GPL + MIT use                 | Copyleft license conflict practice        |
| `samples/nodejs-unlicensed/`    | Node.js (npm) | Unlicensed package                  | License identification practice           |

:::tip Recommended sample
`samples/java-vulnerable/` — detect the Log4Shell vulnerability firsthand and see the value of an SBOM.
:::

**Step 3** — Create the output folder

```bash
mkdir -p output/sbom
```

**Step 4** — Run the sbom-guide agent

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/en/05-sbom-guide
claude
```

The agent asks three questions about your project:

- Project path (e.g. `samples/java-vulnerable`)
- Main language (e.g. `Java`)
- Package manager (e.g. `Maven`)

**Step 5** — Run the generated script

When the agent has generated `output/sbom/sbom-commands.sh`, return to the repo root (`cd ../..`) and run it.
The verification commands from step 6 onward are also repo-root relative.

```bash
cd ../..
bash output/sbom/sbom-commands.sh
```

**Step 6** — Verify the SBOM file exists

```bash
ls -lh output/sbom/*.cdx.json
```

If the file exists and its size is greater than 0, it's OK. Next, check that the minimum elements are filled in.

```bash
jq '{specVersion, timestamp: .metadata.timestamp, tool: .metadata.tools, lifecycles: .metadata.lifecycles, components: (.components | length), withHash: ([.components[] | select(.hashes)] | length), withLicense: ([.components[] | select(.licenses)] | length)}' output/sbom/*.cdx.json
```

`specVersion`, `timestamp`, `tool`, and `components` must have values. `lifecycles` and `withHash` can be
empty in syft output, as the tool comparison table above explains. If you don't have jq, open the file and
check the same items by eye.

**Step 7** — Run license analysis

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/en/05-sbom-analyst
claude
```

**Step 8** — Check the analysis results

```bash
ls output/sbom/license-report.md output/sbom/copyleft-risk.md
```

**When stuck:**

If `output/sbom/[project].cdx.json` is empty, first check whether a lock file exists (`package-lock.json`, `requirements.txt`, `pom.xml`, etc.). If no lock file is found, switch to cdxgen and retry.

```bash
docker run --rm \
  -v "$(pwd)":/app \
  -w /app \
  ghcr.io/cyclonedx/cdxgen:latest \
  -o /app/output/sbom/java-vulnerable-cdxgen.cdx.json \
  /app/samples/java-vulnerable
```

**Expected result of each step:**

| After completing the step | Expected result                                                                   |
| ------------------------- | --------------------------------------------------------------------------------- |
| Step 4 (sbom-guide)       | `output/sbom/sbom-commands.sh` created                                            |
| Step 5 (run script)       | `output/sbom/[project].cdx.json` created (`components` entries should be present) |
| Step 7 (sbom-analyst)     | `output/sbom/license-report.md` and `output/sbom/copyleft-risk.md` created        |

:::info Standard requirements met
Completing this exercise satisfies the requirements below.

5230 §3.3.1, §3.3.2, §3.4.1 · 18974 §4.3.1

The original self-certification question and the verification material for each item are in the [Requirements Detail Matrix](/reference/requirements-matrix).
:::

---

## 4. Completion checklist

Confirm all of the items below before moving on to the next step.

- [ ] `output/sbom/[project].cdx.json` created
- [ ] The `components` array in the SBOM file is not empty
- [ ] `specVersion` is `1.7` (if it is lower, upgrade the tool or pin the specification version and regenerate)
- [ ] `metadata.timestamp` and `metadata.tools` record the generation time and the generating tool
- [ ] Every entry in `components[]` has a `purl`
- [ ] Component hashes (`hashes`) and licenses (`licenses`) have been checked (they can be empty depending on the tool; if so, compare against cdxgen output)
- [ ] For an SBOM you will share externally, decided whether to sign it
- [ ] `output/sbom/sbom-commands.sh` created
- [ ] `output/sbom/license-report.md` created
- [ ] `output/sbom/copyleft-risk.md` created

**Expected results when practicing with the java-vulnerable sample:**

- log4j-core 2.14.1 component detected (4 components with syft)
- CVE-2021-44228 (Log4Shell) expected to be flagged as a vulnerability
- License identification: the `licenses` field in the tool output may be empty when packages declare no license, as in this sample. The 05-sbom-analyst agent in Step 7 fills in the Apache-2.0 identification in `license-report.md`.

> This step meets ISO/IEC 5230 3.3.1, 3.3.2, and 3.4.1, and ISO/IEC 18974 4.3.1 requirements.

:::tip Example deliverables
See the actual format of the generated files at [SBOM deliverables best practice](/reference/samples/sbom).
:::

---

## 5. Next steps

Once SBOM creation and license analysis are complete, move on to setting up an SBOM management system.

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/en/05-sbom-management
claude
```

Or read the guide at [SBOM management: creating it is not the end; managing it is the beginning](../sbom-management/index.md).

To do vulnerability analysis first:

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/en/05-vulnerability-analyst
claude
```

When you are done, update `output/progress.md` to record your progress.
