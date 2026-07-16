---
sidebar_position: 5
sidebar_label: 'Method 4: CI/CD Pipeline'
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 45 minutes
---

# Method 4: Adding a CI/CD Pipeline

:::info Self-study mode (about 45 minutes)
Blocking automatically at the PR stage keeps violations out of the main branch.
:::

Create `.github/workflows/oss-policy-check.yml`.
The example below uses **free open source tools only** (syft and grype are both open source).

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
      - uses: actions/checkout@v7

      - name: Generate SBOM with syft
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: Extract licenses and check policy
        run: |
          # Extract the license list from the SBOM (sbom.cdx.json) generated in the previous step
          jq -r '.components[]?.licenses[]? | (.license.id // .license.name // .expression) // empty' sbom.cdx.json | sort -u > detected-licenses.txt

          echo "=== Detected licenses ==="
          cat detected-licenses.txt

          # Check for prohibited licenses (grep -E extended regex; -only/-or-later variants also match partially)
          FORBIDDEN='GPL-2\.0|GPL-3\.0|AGPL-3\.0|LGPL-2\.0'
          if grep -qE "$FORBIDDEN" detected-licenses.txt; then
            echo "::error::Prohibited licenses detected. Obtain program manager approval or use an alternative package."
            grep -E "$FORBIDDEN" detected-licenses.txt
            exit 1
          fi

          echo "✅ License check passed"

  vulnerability-check:
    name: Vulnerability check (block High or above)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Scan vulnerabilities with grype
        id: scan
        uses: anchore/scan-action@v7
        with:
          path: '.'
          fail-build: true
          severity-cutoff: high # Block the merge when a High / Critical vulnerability is found
          output-format: sarif # The result file path is referenced below via outputs

      - name: Upload vulnerability report
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: vulnerability-report
          # Since v6 the result file is written to a temp path; reference it via outputs.
          path: ${{ steps.scan.outputs.sarif }}
```

> This step supports **automated continuous verification** of the ISO/IEC 18974 G3S.1 (identification of known vulnerabilities) requirement.

**Effect:**

- License checks run automatically on every PR
- PR merges are blocked when prohibited licenses such as GPL are found
- Merges are blocked when vulnerabilities of CVSS High (7.0) or above are found
- Check results are displayed directly on the PR page

**About the free tools:**

- [syft](https://github.com/anchore/syft): SBOM generation tool (Apache-2.0)
- [grype](https://github.com/anchore/grype): vulnerability scanner (Apache-2.0)

---

→ Next: [Completion check](./index.md#6-completion-check)
