---
sidebar_position: 5
sidebar_label: 'Method 4:CI/CD pipeline'
---

# Method 4:Adding a CI/CD Pipeline

:::info Self-study mode(About 45 minutes)
Automatic blocking at the PR stage prevents violations from entering the main branch.
:::

Generates `.github/workflows/oss-policy-check.yml`.
The examples below use **free open source tools only**(syft,grype is all open source).

```yaml
name: OSS Policy Check

on:
  pull_request:
    branches: [main, master]
    paths:
      - 'package.json'
      - 'package-lock.json'
      - 'requirements.txt'
      - 'pom.xml'
      - 'go.mod'
      - 'Cargo.toml'

jobs:
  license-check:
    name: License policy check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM with syft
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: License extract and policy check
        run: |
          # Extract license list with syft
          syft . -o json | jq -r '.artifacts[].licenses[].value' | sort -u > detected-licenses.txt

          echo "=== Detected licenses ==="
          cat detected-licenses.txt

          # Check prohibited licenses
          FORBIDDEN="GPL-2.0\|GPL-3.0\|AGPL-3.0\|LGPL-2.0"
          if grep -qE "$FORBIDDEN" detected-licenses.txt; then
            echo "::error::Prohibited licenses detected. Obtain Program Manager approval or use an alternative package."
            grep -E "$FORBIDDEN" detected-licenses.txt
            exit 1
          fi

          echo "✅ License check passed"

  vulnerability-check:
    name: vulnerability check (block High or above)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan vulnerabilities with grype
        uses: anchore/scan-action@v3
        with:
          path: '.'
          fail-build: true
          severity-cutoff: high # High / Critical vulnerability block merge if found
          output-format: table

      - name: vulnerability upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: vulnerability-report
          path: results.sarif
```

> This step is ISO/IEC 18974 G3S.1(Identify known vulnerabilities)Supports **automated continuous verification** of requirements.

**effect:**

- Run license check automatically on all PRs
- Block PR merge when prohibited licenses such as GPL are found
- CVSS High(7.0)Block merge when abnormal vulnerabilities are discovered
- Test results are displayed directly on the PR screen

**Free Tool Information:**

- [syft](https://github.com/anchore/syft):SBOM Generation Tool(Apache-2.0)
- [grype](https://github.com/anchore/grype):vulnerability scanner(Apache-2.0)
