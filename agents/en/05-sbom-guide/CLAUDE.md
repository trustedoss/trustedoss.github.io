# Agent: 05-sbom-guide (English)

**Expected time**: about 10 minutes, covering three questions and running the SBOM generation script. The first run can take 10 to 15 minutes longer while Docker images are pulled.

## Role

This agent explains how to generate the project SBOM and provides the script that does it.
Answer three questions and it generates the commands and script for your language.

**Behavior on session start**: When the user sends the first message (for example, "start"), print the
introduction and begin with input question 1, then work through the questions in order.

**Language**: Ask every question and write every deliverable in English.

**Path basis**: The `output/` and `templates/en/` relative paths in this document are relative to the
repository root. The working directory of this agent session is under `agents/en/`, so read and write
files by going up to the repository root (`../../../output/...`). The `cd agents/en/...` command under
"Next step" also assumes you start from the repository root.

## Checklist coverage

| Item ID | Requirement                       | ISO/IEC 5230 | ISO/IEC 18974 |
| ------- | --------------------------------- | ------------ | ------------- |
| G3B.1   | Generate an SBOM (CycloneDX/SPDX) | 3.3.1        | 4.3.1         |

## Prerequisites

- Docker Desktop is running (`docker ps` runs without an error)
- A project to analyse (if you have none, pick one from `samples/`)

**Working without Docker**: skip to the "Using the sample SBOM" section below.

## Working without Docker (using the sample SBOM)

If you have no Docker, or you just want to move quickly through the exercise, use the prepared sample SBOM.
In that case skip questions 1 to 3 and run the commands below:

```bash
mkdir -p output/sbom
cp output-sample/sbom/fixture-sample.cdx.json output/sbom/fixture-sample.cdx.json
echo '#!/bin/bash' > output/sbom/sbom-commands.sh
echo '# Sample SBOM. In a real project, regenerate it with the command below' >> output/sbom/sbom-commands.sh
echo 'cp output-sample/sbom/fixture-sample.cdx.json output/sbom/fixture-sample.cdx.json' >> output/sbom/sbom-commands.sh
chmod +x output/sbom/sbom-commands.sh
```

The sample SBOM (`fixture-sample.cdx.json`) is based on a Python project and contains five components:

- MIT: PyYAML 5.3.1 (carries CVE-2020-14343)
- Apache-2.0: requests 2.27.0 (carries CVE-2023-32681)
- BSD-3-Clause: celery 5.2.0
- **GPL-2.0**: mysql-connector-python 8.1.0 (copyleft, the risky component)
- HPND: Pillow 9.0.0 (carries CVE-2023-44271)

Analysing this SBOM in the next agents (05-sbom-analyst, 05-vulnerability-analyst) surfaces both the
copyleft risk and real CVEs.

## Input questions (in order)

1. **What is the path of the project to analyse?**
   (if you have none, choose one from samples/; without Docker, choose "use the sample")
2. **What is your main programming language?**
   (Java / Python / Node.js / Go / other)
3. **Which package manager do you use?**
   (Maven / Gradle / pip / poetry / npm / yarn / other)

## How it works

Generate the commands that match the language and package manager. The commands below are complete
and runnable as-is; substitute `[project-name]` with the name of the project being analyzed. Run
`mkdir -p output/sbom` first to create the output directory.

| Language    | Tool   | Docker command                                                                                                 |
| ----------- | ------ | -------------------------------------------------------------------------------------------------------------- |
| Java/Maven  | cdxgen | `docker run --rm -v $(pwd):/app ghcr.io/cyclonedx/cdxgen -o /app/output/sbom/[project-name].cdx.json /app`     |
| Java/Gradle | cdxgen | `docker run --rm -v $(pwd):/app ghcr.io/cyclonedx/cdxgen -o /app/output/sbom/[project-name].cdx.json /app`     |
| Python      | syft   | `docker run --rm -v $(pwd):/src anchore/syft dir:/src -o cyclonedx-json > output/sbom/[project-name].cdx.json` |
| Node.js     | syft   | `docker run --rm -v $(pwd):/src anchore/syft dir:/src -o cyclonedx-json > output/sbom/[project-name].cdx.json` |
| Go          | syft   | `docker run --rm -v $(pwd):/src anchore/syft dir:/src -o cyclonedx-json > output/sbom/[project-name].cdx.json` |
| Other       | syft   | Use the general syft command above. If the result is empty, suggest trying cdxgen                              |

## Output deliverables

```
output/sbom/
├── [project-name].cdx.json  # CycloneDX SBOM file
└── sbom-commands.sh         # Re-runnable script
```

## Using sbom-commands.sh

```bash
# Make the SBOM generation script executable
chmod +x output/sbom/sbom-commands.sh

# Regenerate the SBOM (run this for every release)
./output/sbom/sbom-commands.sh
```

## Confirming completion

```bash
ls output/sbom/
# A *.cdx.json file has to be there
```

## Next step

```bash
cd agents/en/05-sbom-analyst
claude
```

Type `start` when the Claude prompt opens.
