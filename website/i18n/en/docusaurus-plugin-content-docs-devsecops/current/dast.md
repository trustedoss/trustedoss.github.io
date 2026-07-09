---
id: dast
title: Dynamic Analysis (DAST)
sidebar_label: DAST
sidebar_position: 8
---

# Dynamic Analysis (DAST)

## What is DAST?

:::info DAST is a complement to SAST, not a replacement
SAST looks at the code and DAST looks at the running app. The two must be applied together to reduce blind spots.
:::

**Definition:** DAST sends real HTTP requests to a running application to detect runtime vulnerabilities such as SQL injection, XSS, authentication bypass, and sensitive information disclosure.

**How it differs from SAST:** SAST scans quickly during the coding phase but cannot observe runtime behavior. DAST verifies actual behavior after deployment, helping you find vulnerabilities that SAST misses.

---

## Tool Comparison

| Tool      | Features                                      | Main uses                                 | License    |
| --------- | --------------------------------------------- | ----------------------------------------- | ---------- |
| OWASP ZAP | Industry-standard, GUI and automation support | Full scan of web apps/APIs                | Apache-2.0 |
| Nuclei    | Template-based, fast, lightweight             | Scanning for known vulnerability patterns | MIT        |

We recommend OWASP ZAP for in-depth web application scanning, and Nuclei for quick checks of known CVEs and misconfigurations.

---

## OWASP ZAP setup

### GitHub Actions

```yaml
# .github/workflows/dast-zap.yml

name: DAST — OWASP ZAP

on:
  push:
    branches: [main]

jobs:
  zap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      # run app (e.g., Docker Compose)
      - name: Start application
        run: |
          docker compose up -d
          sleep 10  # wait for app startup

      # ZAP Baseline scan (baseline vulnerability detection without manual intervention)
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: http://localhost:8080
          rules_file_name: zap-rules.tsv
          fail_action: true

      # ZAP API scan (based on OpenAPI spec)
      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: http://localhost:8080/api/openapi.json
          format: openapi
          fail_action: true

      - name: Upload ZAP report
        uses: actions/upload-artifact@v7
        if: always()
        with:
          name: zap-report
          path: report_html.html
```

### Select scan type

| Scan Type | Action           | Time required | Recommended situation                |
| --------- | ---------------- | ------------- | ------------------------------------ |
| Baseline  | action-baseline  | 2~5 minutes   | Basic check per PR                   |
| API Scan  | action-api-scan  | 5~15 minutes  | When an OpenAPI specification exists |
| Full Scan | action-full-scan | 20 minutes+   | In-depth pre-release check           |

We recommend a two-tier strategy: run Baseline during the PR phase and Full Scan before release.

### Rules file configuration

Rules that ignore or fail specific alerts are managed in the `zap-rules.tsv` file.

```
# zap-rules.tsv
10016	IGNORE	(Browser XSS protection header — legacy browser support not required)
10020	WARN	(X-Frame-Options header not set)
10021	FAIL	(Anti-CSRF token not set)
```

You can set the handling for each item at three levels: `IGNORE`·`WARN`·`FAIL`.

---

## Nuclei setup

### GitHub Actions

```yaml
# .github/workflows/dast-nuclei.yml

name: DAST — Nuclei

on:
  push:
    branches: [main]

jobs:
  nuclei:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Start application
        run: |
          docker compose up -d
          sleep 10

      - name: Run Nuclei
        uses: projectdiscovery/nuclei-action@v3
        with:
          target: http://localhost:8080
          # Since v3, individual inputs such as templates/severity were removed;
          # pass nuclei CLI flags directly via flags.
          flags: '-t cves/ -t misconfiguration/ -t exposures/ -severity medium,high,critical -o nuclei.log'

      - name: Upload Nuclei report
        uses: actions/upload-artifact@v7
        if: always()
        with:
          name: nuclei-report
          path: nuclei.log
```

### Main template categories

| Category         | Description                         |
| ---------------- | ----------------------------------- |
| cves             | Known CVE vulnerability patterns    |
| misconfiguration | Security misconfigurations          |
| exposures        | Sensitive information/file exposure |
| default-logins   | Default accounts/passwords          |
| takeovers        | Potential subdomain takeover        |

---

## Precautions when adopting DAST

:::warning Always run DAST in an isolated test environment.
:::

**Environment separation:** Because DAST sends real HTTP requests, running it against production can corrupt data and disrupt service. Always run it only in a staging or test environment.

**Authentication setup:** For endpoints that require authentication, pass a token through ZAP's authentication settings or Nuclei's header option to ensure full coverage.

**False positive management:** DAST has a higher false positive rate than SAST. We recommend a phased approach: start with `WARN` and switch to `FAIL` after reviewing the results.

---

## Next steps

- Full security pipeline integration: [Pipeline Design](./pipeline-design)
- Continuous security monitoring after deployment: [Monitoring and Automated Remediation](./monitoring)
