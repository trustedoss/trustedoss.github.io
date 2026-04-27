---
sidebar_position: 2
sidebar_label: 'Docker·CI/CD execution guide'
---

# Create SBOM:Docker implementation guide and CI/CD automation

This document describes the actual Docker execution commands for syft·cdxgen.,Setting up GitHub Actions automation,Sample Project Practice,It contains troubleshooting.

---

## Running syft with Docker — Commands for each language/package manager

| language | Package Manager | command                                                                                                               |
| -------- | --------------- | --------------------------------------------------------------------------------------------------------------------- |
| Java     | Maven/Gradle    | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Python   | pip             | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Node.js  | npm             | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |
| Go       | go mod          | `docker run --rm -v $(pwd):/project anchore/syft:latest /project --output cyclonedx-json > output/sbom/sbom.cdx.json` |

full command(Same for each language,Adjust directories only):

```bash
# create output/sbom directory
mkdir -p output/sbom

# Generate SBOM with syft
docker run --rm \
  -v $(pwd):/project \
  anchore/syft:latest \
  /project \
  --output cyclonedx-json \
  > output/sbom/sbom.cdx.json
```

---

## Running cdxgen with Docker(When more precise analysis is needed)

```bash
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  ghcr.io/cyclonedx/cdxgen:latest \
  -r /app \
  -o /app/output/sbom/sbom-cdxgen.cdx.json
```

Recommended for Java Maven projects. Dependency tracking is more precise than syft,transitive dependency(transitive dependencies)Until more fully collected.

---

## Automate GitHub Actions

Integrating SBOM generation into your CI/CD pipeline will automatically generate the latest SBOM for every release.

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
      - uses: actions/checkout@v4
      - name: Generate SBOM with syft
        run: |
          docker run --rm \
            -v ${{ github.workspace }}:/project \
            anchore/syft:latest \
            /project --output cyclonedx-json \
            > sbom.cdx.json
      - name: Upload SBOM as artifact
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.cdx.json
```

---

## Practice with samples/ project

Two sample projects are provided for practice.:

- `samples/java-vulnerable/`:log4j-core includes 2.14.1 → Expected detection of CVE-2021-44228
- `samples/python-mixed-license/`:GPL mixed → Expect license conflict detection

```bash
# practice with java-vulnerable sample
docker run --rm \
  -v $(pwd)/samples/java-vulnerable:/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > output/sbom/java-vulnerable.cdx.json
```

---

## Troubleshooting

| Symptoms                        | Cause             | Solution                                                     |
| ------------------------------- | ----------------- | ------------------------------------------------------------ |
| SBOM is empty(`components: []`) | no lock file      | `package-lock.json`, `requirements.txt`,Check `pom.xml` etc. |
| Docker volume mount error       | path problem      | change to absolute path: `-v /full/path:/project`            |
| Permission denied               | Permission issues | Add `sudo` or Docker group                                   |
| Image pulling takes a long time | network           | Normal on first run,Use cache after                          |
