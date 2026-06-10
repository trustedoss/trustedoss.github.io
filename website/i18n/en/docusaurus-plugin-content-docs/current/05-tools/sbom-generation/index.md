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

In this chapter, you use syft and cdxgen to generate an SBOM (Software Bill of Materials). Both tools run with Docker, so no separate installation is required. With a few lines of commands, you can produce your project's entire dependency list as a JSON file.

The generated SBOM later becomes the basis for license analysis (05-sbom-analyst) and vulnerability scanning (05-vulnerability-analyst). The more accurate the SBOM, the better you can identify compliance risks and security vulnerabilities.

---

## 2. Background knowledge

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

> For a guide to adopting and using SCA and compliance tools such as FOSSLight, SW360, and FOSSology, see [KWG Open Source Guide — Tools](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/4-tool/).

For the actual Docker commands, GitHub Actions CI/CD setup, and the sample project walkthrough, see the [Docker and CI/CD execution guide](./docker-cicd.md).

### CycloneDX JSON format main fields

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "metadata": {
    "component": {
      "name": "my-app",
      "version": "1.0.0",
      "type": "application"
    }
  },
  "components": [
    {
      "name": "log4j-core",
      "version": "2.14.1",
      "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "licenses": [{"license": {"id": "Apache-2.0"}}]
    }
  ]
}
```

Key field descriptions:

- `bomFormat`, `specVersion`: CycloneDX format identifiers
- `metadata.component`: information about the software being analyzed
- `components[]`: the dependency list (includes license and PURL)
- `vulnerabilities[]`: vulnerability information (if present)

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

> **Recommended**: `samples/java-vulnerable/` — detect the Log4Shell vulnerability firsthand and see the value of an SBOM.

**Step 3** — Create output folder

```bash
mkdir -p output/sbom
```

**Step 4** — Run the sbom-guide agent

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-guide
claude
```

The agent asks three questions about your project:

- Project path (e.g. `samples/java-vulnerable`)
- Main language (e.g. `Java`)
- Package manager (e.g. `Maven`)

**Step 5** — Run the generated script

Executes when the agent generates `output/sbom/sbom-commands.sh`:

```bash
bash output/sbom/sbom-commands.sh
```

**Step 6** — Verify existence of SBOM file

```bash
ls -lh output/sbom/*.cdx.json
```

If the file exists and its size is greater than 0, it's OK. Open the file and check that the `components` array is not empty.

**Step 7** — Run license analysis

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-analyst
claude
```

**Step 8** — Check the analysis results

```bash
ls output/sbom/license-report.md output/sbom/copyleft-risk.md
```

**When stuck:**

If `output/sbom/sbom.cdx.json` is empty, first check whether a lock file exists (`package-lock.json`, `requirements.txt`, `pom.xml`, etc.). If no lock file is found, switch to cdxgen and retry.

```bash
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  ghcr.io/cyclonedx/cdxgen:latest \
  -r /app/samples/java-vulnerable \
  -o /app/output/sbom/java-vulnerable-cdxgen.cdx.json
```

**Expected result of each step:**

| After completing the step | Expected result                                                              |
| ------------------------- | ---------------------------------------------------------------------------- |
| Step 4 (sbom-guide)       | `output/sbom/sbom-commands.sh` created                                       |
| Step 5 (run script)       | `output/sbom/sbom.cdx.json` created (`components` entries should be present) |
| Step 7 (sbom-analyst)     | `output/sbom/license-report.md` and `output/sbom/copyleft-risk.md` created   |

:::info Standard requirements met
Completing this lab will meet the requirements below:

**ISO/IEC 5230**

| Item ID | Requirements                              | Self-certification checklist                                                                          |
| ------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 3.3.1   | SBOM creation and management              | Do you have a process for creating and managing a bill of materials for each supply software release? |
| 3.3.2   | License Identification and Classification | Do you have a process for identifying the licenses applicable to supply software?                     |
| 3.4.1   | Preparing compliance deliverables         | Do you have a process for creating the necessary compliance artifacts?                                |

**ISO/IEC 18974**

| Item ID | Requirements           | Self-certification checklist                                                   |
| ------- | ---------------------- | ------------------------------------------------------------------------------ |
| 4.3.1   | Supplied Software SBOM | Do you have a process for creating and maintaining a SBOM for supply software? |

:::

---

## 4. Completion checklist

Confirm all of the items below before moving on to the next step.

- [ ] `output/sbom/[project].cdx.json` created
- [ ] The `components` array in the SBOM file is not empty
- [ ] `output/sbom/sbom-commands.sh` created
- [ ] `output/sbom/license-report.md` created
- [ ] `output/sbom/copyleft-risk.md` created

**Expected results when practicing with the java-vulnerable sample:**

- log4j-core 2.14.1 component detected (4 components with syft)
- CVE-2021-44228 (Log4Shell) flagged as a vulnerability
- License identification: the `licenses` field in the tool output may be empty when packages declare no license, as in this sample. The 05-sbom-analyst agent in Step 7 fills in the Apache-2.0 identification in `license-report.md`.

> This step meets ISO/IEC 5230 3.3.1, 3.3.2, and 3.4.1, and ISO/IEC 18974 4.3.1 requirements.

:::note Example output
See the actual format of the generated files at [SBOM output best practice](/reference/samples/sbom).
:::

---

## 5. Next steps

Once SBOM creation and license analysis are complete, move on to setting up an SBOM management system.

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-management
claude
```

Or read the guide at [SBOM management: creating it is not the end; managing it is the beginning](../sbom-management/index.md).

To do vulnerability analysis first:

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/05-vulnerability-analyst
claude
```

When you are done, update `output/progress.md` to record your progress.
