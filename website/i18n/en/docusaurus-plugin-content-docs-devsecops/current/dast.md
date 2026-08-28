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

:::tip The configuration below is an example — a fully working implementation lives in the reference repository
The YAML and commands on this page are examples that show the essentials. For a complete, copy-and-run pipeline (including policy files and a sample app), see the [Best Practice repository](/ai-coding/best-practice-repo).
:::

:::note Tags in these examples versus production settings
The examples below keep mutable tags such as `@v7` for readability. A tag can be repointed to a different commit later, so in production pin each action to a full commit SHA and grant only the permissions a job needs with a `permissions:` block. See [Pipeline Security](/devsecops/pipeline-security) for the reasoning and the procedure.
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
    permissions:
      contents: read
      issues: write # the ZAP action files findings as issues
    steps:
      - uses: actions/checkout@v7

      # run app (e.g., Docker Compose)
      - name: Start application
        run: |
          docker compose up -d
          sleep 10  # wait for app startup

      # ZAP Baseline scan (baseline vulnerability detection without manual intervention)
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.15.0
        with:
          target: http://localhost:8080
          rules_file_name: zap-rules.tsv
          fail_action: true

      # ZAP API scan (based on OpenAPI spec)
      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.10.0
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

We recommend a two-tier strategy: run Baseline during the PR phase and Full Scan before release. Attach the Full Scan only once you have settled **what it will point at**, for the reason below.

### What separates Baseline from Full

The difference is not duration. It is what gets sent to the target.

|                       | Baseline                                                                     | Full Scan                                                                         |
| --------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Behavior              | Spiders the site and observes the traffic                                    | Sends attack payloads to every parameter it finds                                 |
| Requests sent         | Ordinary retrieval requests                                                  | Real attack strings: SQL injection, path traversal, command injection             |
| What it finds         | What the responses reveal (missing headers, cookie flags, information leaks) | Whether a vulnerability actually holds                                            |
| What it leaves behind | Access log entries                                                           | Attack attempts in logs, created or modified data, failed authentication attempts |

Baseline sends no attack payloads, which is what makes it safe to point at an environment people are using, such as a demo or a staging deployment. Production stays out of scope, per the caution further down this page. In exchange it only sees what the responses reveal.

### Pointing a Full Scan at something in use

Full Scan is a different proposition. The first two of the following hold even when the target is read-only.

- **Resource exhaustion.** Every parameter it discovers gets dozens to hundreds of request variants. Aimed at an expensive path such as search or a listing endpoint, real users feel it.
- **Account lockout.** Finding a login path, it repeatedly attempts authentication bypass. On a system with a lockout policy, real accounts can be locked when the scan finishes.
- **Data contamination.** Even with writes blocked, any path left open is a path it will go through. Endpoints designed to accept external input, such as scan-result upload or webhook receivers, are the usual candidates.

So a Full Scan belongs on a scan-only instance: somewhere data can be wiped and recreated, where a locked account belongs to nobody, and where a load spike inconveniences no one.

### How this was set up in TRUSCA

[TRUSCA](https://github.com/trustedoss/trusca) has Baseline only, for now.

The demo host runs with `DEMO_READ_ONLY` on, rejecting anything but GET, HEAD and OPTIONS, so most of the write risk was already closed. Full was still deferred, because the first two concerns above have nothing to do with writes. Retrieval alone consumes resources, and authentication attempts still trip lockout policy. The third does not vanish either: permitting sandbox scans opens a path that ingests scan results. Full waits for a scan-only instance.

Baseline got caps too: two minutes of spidering, six for the whole run. Not to shorten CI. The demo is deliberately cheap to run and carries memory limits, so the retrieval load of an unbounded spider is itself too much for that size. Raise them after watching a run leave the response times steady, not before.

The target URL lives in a repository variable rather than in the workflow. With the variable empty, the job logs that it scanned nothing and exits successfully. Merging a workflow and pointing it at a specific host are separate decisions, and the second should not arrive as a side effect of the first.

That structure carries its own matching risk. Leave the variable unset and the workflow stays green, and anyone reading only the badge concludes DAST is running. So the job summary reports alert counts by risk **and how many distinct URLs were reached**, with a note that zero URLs means a failed scan rather than a clean one. Turning something off is only safe if the log says it is off.

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
    permissions:
      contents: read
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

:::note
The browser-based result analyzers offered on the SCA, SAST, secret detection, and IaC pages do not yet exist for this topic.
The ZAP report (zap-report.html) already includes priorities, so you can review it as is.
:::

## Next steps

- Full security pipeline integration: [Pipeline Design](./pipeline-design)
- Continuous security monitoring after deployment: [Monitoring and Automated Remediation](./monitoring)
