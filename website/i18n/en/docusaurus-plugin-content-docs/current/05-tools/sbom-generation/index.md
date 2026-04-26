---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: [3.3.1, 3.3.2, 3.4.1]'
  - 'ISO/IEC 18974: [4.3.1]'
self_study_time: 1.5 hours
---

# Create SBOM:Creating a software configuration specification with syft and cdxgen

## 1. What we do in this chapter

In this chapter, you use syft and cdxgen to(Software Bill of Materials)generates . Both tools run with Docker, so no separate installation is required.,With a few lines of commands, you can create your project's entire dependency list as a JSON file.

The generated SBOM is later analyzed for license(05-sbom-analyst)and vulnerability scanning(05-vulnerability-analyst)It becomes the basis of. The more accurate SBOM is, the better you can identify compliance risks and security vulnerabilities.

---

## 2. Background knowledge

### What is SBOM?

SBOM(Software Bill of Materials)is a list of all components included in the software. Like the food nutrition facts table,Specifies which open sources and versions are included in the software. Both ISO/IEC 5230 and 18974 specify the generation of SBOM as a core requirement(G3B.1).

Why SBOM is important:

- Know what open source licenses are included(compliance)
- Check if you have a vulnerable version of a library(security)
- Providing software configuration information to customers or regulatory agencies when distributing products

### Introduction to tools used

There are two approaches to generating SBOM: **Dependency Analysis** is a package manager file(pom.xml,package-lock.json, etc.)Identify declared dependencies based on,**Source Code Scan** detects open source embedded directly within your code at the file level. By combining the two methods, you can create a more complete SBOM that includes copied/inserted code fragments without package declarations.

**Dependency Analysis Tool**(Exercises in this chapter)

| tools  | Production company | Features                                               | suitable situation                                   |
| ------ | ------------------ | ------------------------------------------------------ | ---------------------------------------------------- |
| syft   | Anchore            | fast and light,single binary,Multiple language support | Python, Node.js, Go                                  |
| cdxgen | CycloneDX          | CycloneDX only,Detailed analysis by language           | Java(Maven/Gradle),When precise analysis is required |

Both tools can output in CycloneDX JSON format,,This chapter uses CycloneDX as the standard format.

**Source Code Scan Tool**(optional)

| tools   | Operating entity | Features                                                                     | suitable situation                                                    |
| ------- | ---------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| SCANOSS | SCANOSS          | File-by-file snippet scanning,Cloud + On-Premise,API integration,create SBOM | Source code direct embedding detection,Precise License Identification |

[SCANOSS](https://www.scanoss.com/)has the advantage of detecting open source code fragments copied and inserted directly without package declaration at the file level. Because their roles are complementary to syft/cdxgen,,Parallel use is recommended when source level precision is required.

> FOSSLight, SW360,For a guide to the introduction and use of SCA and compliance tools such as FOSSology, see [KWG Open Source Guide — Tools](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/4-tool/)See .

Actual Docker execution command,GitHub Actions CI/CD Settings,Sample project practice is [Docker·CI/CD execution guide](./docker-cicd.md)Please refer to the page.

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

- `bomFormat`, `specVersion`:CycloneDX format identifier
- `metadata.component`:Software information to be analyzed
- `components[]`:Dependency list(license,Includes PURL)
- `vulnerabilities[]`:Vulnerability information(If there is)

---

## 3. Self-study

:::info Self-study mode(Approximately 1 hour and 30 minutes)
The first run may take an additional 10-15 minutes due to Docker image pulling.
:::

Step-by-step practice:

**Step 1** — Verify Docker Desktop is running

```bash
docker ps
```

If it runs without errors, Docker is ready.

:::tip When proceeding without Docker
If you don't have Docker installed or just want to get started quickly for lab purposes,,Use the pre-prepared sample SBOM with the command below.

```bash
mkdir -p output/sbom
cp output-sample/sbom/fixture-sample.cdx.json output/sbom/fixture-sample.cdx.json
```

Sample SBOM includes GPL-2.0 Copyleft components and packages with CVE vulnerabilities, allowing for subsequent analysis practice.
In this case, skip running the 05-sbom-guide agent and go directly to **step 5.(Run analysis agent)Go to **.
:::

**Step 2** — Select projects to analyze

You can also use your own project,Samples are also available.

If this is your first time, choose one of the samples below::

| sample path                     | language      | Features                          | Learning Points                            |
| ------------------------------- | ------------- | --------------------------------- | ------------------------------------------ |
| `samples/java-vulnerable/`      | Java (Maven)  | Log4Shell(CVE-2021-44228)Included | Critical vulnerability detection practice  |
| `samples/python-mixed-license/` | Python (pip)  | GPL + MIT mixed use               | Copyleft License Conflict Practice         |
| `samples/nodejs-unlicensed/`    | Node.js (npm) | Unlicensed package                | License identification processing practice |

> **Recommended**:`samples/java-vulnerable/` — Detect Log4Shell vulnerabilities directly and experience the value of SBOM.

**Step 3** — Create output folder

```bash
mkdir -p output/sbom
```

**Step 4** — Run the sbom-guide agent

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-guide
claude
```

The agent asks three questions asking for project information.:

- project path(yes: `samples/java-vulnerable`)
- main language(yes: `Java`)
- package manager(yes: `Maven`)

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

**Step 7** — Run License Analysis

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-analyst
claude
```

**Step 8** — Check analysis results

```bash
ls output/sbom/license-report.md output/sbom/copyleft-risk.md
```

**When stuck:**

If `output/sbom/sbom.cdx.json` is empty, the existence of a lock file is first checked.(`package-lock.json`, `requirements.txt`,`pom.xml` etc.). If the lock file is not found, switch to cdxgen and retry.

```bash
docker run --rm \
  -v $(pwd)/samples/java-vulnerable:/app \
  -w /app \
  ghcr.io/cyclonedx/cdxgen:latest \
  -r /app \
  -o /app/output/sbom/java-vulnerable-cdxgen.cdx.json
```

**Expected results of each step:**

| After completing the steps | Expected results                                                         |
| -------------------------- | ------------------------------------------------------------------------ |
| Number 4(sbom-guide)       | `output/sbom/sbom-commands.sh` created                                   |
| Number 5(run script)       | `output/sbom/sbom.cdx.json` created(`components` entry should be normal) |
| Number 7(sbom-analyst)     | `output/sbom/license-report.md`,`output/sbom/copyleft-risk.md` created   |

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

## 4. Completion Confirmation Checklist

After checking all the items below, proceed to the next step.

- [ ] `output/sbom/[project].cdx.json` created
- [ ] The `components` array in the SBOM file is not empty.
- [ ] `output/sbom/sbom-commands.sh` created
- [ ] `output/sbom/license-report.md` created
- [ ] `output/sbom/copyleft-risk.md` created

**Expected results when practicing the java-vulnerable sample:**

- log4j-core 2.14.1 component detection
- Apache-2.0 License Identification
- CVE-2021-44228 (Log4Shell)Expect vulnerability flags

> This step is ISO/IEC 5230 3.3.1, 3.3.2,Meets 3.4.1 and ISO/IEC 18974 4.3.1 requirements.

> 📋 **Example of output**: [SBOM Output Best Practice](/reference/samples/sbom)You can check the actual format of the generated file at .

---

## 5. Next steps

When SBOM creation and license analysis are completed,,SBOM Moves to the stage of establishing a management system.

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/05-sbom-management
claude
```

or [SBOM Management:Creating is not the end; management is the beginning.](../sbom-management/index.md)Go to to view the guide.

To proceed with vulnerability analysis first::

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/05-vulnerability-analyst
claude
```

After completion, update `output/progress.md` to record progress.
