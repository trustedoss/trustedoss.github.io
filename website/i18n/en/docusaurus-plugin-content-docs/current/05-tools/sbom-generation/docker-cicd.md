---
sidebar_position: 2
sidebar_label: 'Docker and CI/CD execution guide'
date: 2026-06-05
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 30 minutes
---

# Create SBOM: Docker execution guide and CI/CD automation

This page contains the actual Docker commands for syft and cdxgen, the GitHub Actions automation setup, the sample project walkthrough, and troubleshooting.

---

## Running syft with Docker — commands per language/package manager

| Language | Package manager | Command                                                                                                               |
| -------- | --------------- | --------------------------------------------------------------------------------------------------------------------- |
| Java     | Maven/Gradle    | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Python   | pip             | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Node.js  | npm             | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Go       | go mod          | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |

Full command (identical for every language; only the directory changes):

```bash
# Create the output/sbom folder
mkdir -p output/sbom

# Generate the SBOM with syft
docker run --rm \
  -v $(pwd):/project \
  anchore/syft:latest \
  /project \
  --output cyclonedx-json \
  > output/sbom/sbom.cdx.json
```

---

## Running cdxgen with Docker (when more precise analysis is needed)

```bash
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  ghcr.io/cyclonedx/cdxgen:latest \
  -r /app \
  -o /app/output/sbom/sbom-cdxgen.cdx.json
```

Recommended for Java Maven projects. Its dependency resolution is more precise than syft's, and it collects transitive dependencies more completely.

---

## GitHub Actions automation

Integrating SBOM generation into your CI/CD pipeline gives you an up-to-date SBOM automatically for every release.

```yaml
# .github/workflows/sbom.yml
name: Generate SBOM

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - name: Generate SBOM with syft
        run: |
          docker run --rm \
            -v ${{ github.workspace }}:/project \
            anchore/syft:latest \
            /project --output cyclonedx-json \
            > sbom.cdx.json
      - name: Upload SBOM as artifact
        uses: actions/upload-artifact@v7
        with:
          name: sbom
          path: sbom.cdx.json
```

---

## Practicing with the samples/ projects

Three sample projects are provided for practice:

- `samples/java-vulnerable/`: includes log4j-core 2.14.1 → expect CVE-2021-44228 to be detected
- `samples/python-mixed-license/`: mixed GPL use → expect a license conflict to be detected
- `samples/nodejs-unlicensed/`: local package with no declared license → expect an unidentified license (NOASSERTION) to be detected

```bash
# Practice with the java-vulnerable sample
docker run --rm \
  -v $(pwd)/samples/java-vulnerable:/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > output/sbom/java-vulnerable.cdx.json
```

---

## Troubleshooting

| Symptom                             | Cause                                                                                     | Solution                                                                                                                             |
| ----------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| SBOM is empty (`components: []`)    | No lock file                                                                              | Check for `package-lock.json`, `requirements.txt`, `pom.xml`, etc.                                                                   |
| SBOM is empty but there is no error | Docker file-sharing restriction — the mount resolves to an empty directory (colima, etc.) | Check that the working directory is included in Docker Desktop > Settings > Resources > File Sharing (or your colima mount settings) |
| Docker volume mount error           | Path problem                                                                              | Switch to an absolute path: `-v /full/path:/project`                                                                                 |
| Permission denied                   | Permission problem                                                                        | Use `sudo` or add yourself to the Docker group                                                                                       |
| Image pull takes a long time        | Network                                                                                   | Normal on the first run; the cache is used afterwards                                                                                |
