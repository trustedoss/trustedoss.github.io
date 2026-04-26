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

**Definition:** Sends actual HTTP requests to a running application to detect runtime vulnerabilities such as SQL injection, XSS, authentication bypass, and sensitive information disclosure.

**Differences from SAST:** SAST detects quickly during the code writing phase but cannot determine runtime behavior. DAST verifies actual behavior after deployment, helping you discover vulnerabilities that SAST misses.

---

## Tool Comparison

| tools     | Features                                             | Main uses                             | License    |
| --------- | ---------------------------------------------------- | ------------------------------------- | ---------- |
| OWASP ZAP | Supports all industry standards, GUI, and automation | Full scan of web app/API              | Apache-2.0 |
| Nuclei    | Template-based, fast, lightweight                    | Scan for known vulnerability patterns | MIT        |

We recommend OWASP ZAP for deep web app scanning, and Nuclei for quick checks for known CVE·unconfigured vulnerabilities.

---

## OWASP ZAP settings

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
      - uses: actions/checkout@v4

      # 앱 실행 (예: Docker Compose)
      - name: Start application
        run: |
          docker compose up -d
          sleep 10  # 앱 기동 대기

      # ZAP Baseline 스캔 (수동 개입 없이 기본 취약점 탐지)
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: http://localhost:8080
          rules_file_name: zap-rules.tsv
          fail_action: true

      # ZAP API 스캔 (OpenAPI 명세 기반)
      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: http://localhost:8080/api/openapi.json
          format: openapi
          fail_action: true

      - name: Upload ZAP report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: zap-report
          path: report_html.html
```

### Select scan type

| Scan Type | Action           | Time required | Recommended Situation                 |
| --------- | ---------------- | ------------- | ------------------------------------- |
| Baseline  | action-baseline  | 2~5 minutes   | Basic inspection per PR               |
| API Scan  | action-api-scan  | 5~15 minutes  | OpenAPI When there is a specification |
| Full Scan | action-full-scan | 20 minutes+   | In-depth pre-release inspection       |

We recommend a dual strategy of running Baseline during the PR phase and Full Scan before release.

### Rules file settings

Rules to ignore or fail specific notifications are managed in the `zap-rules.tsv` file.

```
# zap-rules.tsv
10016	IGNORE	(웹 브라우저 XSS 보호 헤더 — 레거시 브라우저 대응 불필요)
10020	WARN	(X-Frame-Options 헤더 미설정)
10021	FAIL	(Anti-CSRF 토큰 미설정)
```

You can specify processing for each item at three levels: `IGNORE`·`WARN`·`FAIL`.

---

## Nuclei settings

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
      - uses: actions/checkout@v4

      - name: Start application
        run: |
          docker compose up -d
          sleep 10

      - name: Run Nuclei
        uses: projectdiscovery/nuclei-action@main
        with:
          target: http://localhost:8080
          templates: cves,misconfiguration,exposures
          severity: medium,high,critical
          fail-on-severity: high

      - name: Upload Nuclei report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: nuclei-report
          path: nuclei.log
```

### Main template categories

| Category         | Description                         |
| ---------------- | ----------------------------------- |
| cves             | Known CVE vulnerability patterns    |
| misconfiguration | Security settings error             |
| exposures        | Sensitive information/file exposure |
| default-logins   | Default account/password            |
| takeovers        | Possibility of subdomain hijacking  |

---

## Precautions when introducing DAST

:::warning Be sure to run DAST in an isolated test environment.
:::

**Environment Separation:** Because DAST sends actual HTTP requests, running it in a production environment may cause data corruption and service disruption. Be sure to run it only in a staging/testing environment.

**Authentication Settings:** Endpoints that require authentication must pass a token through ZAP's authentication settings or Nuclei's header option to ensure coverage.

**False positive management:** DAST has a higher false positive rate than SAST. We recommend a phased approach, starting with `WARN` and switching to `FAIL` after reviewing the results.

---

## Next steps

- Full security pipeline integration: [Pipeline Design](./pipeline-design)
- Continuous security monitoring after deployment: [Monitoring·Automatic Correction](./monitoring)
