---
id: pipeline-security
title: Pipeline Security and Build Provenance
sidebar_label: Pipeline Security
sidebar_position: 10
---

# Pipeline Security and Build Provenance

Other pages in this guide cover what the pipeline inspects. This page covers how you protect the pipeline itself.
No matter how tightly you wire up SAST, SCA, and secret scanning, the results mean nothing if the workflow running those checks is executing an attacker's code.

:::tip These settings are examples. The working implementation lives in the reference repository
The YAML and commands on this page illustrate the core idea. For a full pipeline you can copy and run (policy files and a sample app included), see the [Best Practice repository](/ai-coding/best-practice-repo).
:::

## Why the pipeline itself is a target

A CI runner is an execution environment that gathers repository secrets, cloud credentials, and deployment permissions in one place.
Breaking into the workflow that builds the code pays off far better than breaking into the application code.

:::info A tag your workflow references can point at a different commit at any time
`uses: owner/repo@v45` means "run whatever commit the label v45 currently points at."
The repository owner can move that label to another commit whenever they want.
:::

**tj-actions/changed-files (2025-03, CVE-2025-30066).** The tags of a widely used GitHub Action were
repointed to a malicious commit, `0e58ed86`. Several tags including `v1.0.0`, `v35.7.7-sec`, and
`v44.5.1` were made to point at the same commit, and the script in that commit extracted secrets from
the runner worker process memory and printed them into the workflow log in plain text. In repositories
with public logs, API keys, cloud credentials, and SSH keys were exposed directly. More than 23,000
repositories were affected. Not a single line of application code changed.

**Trivy Action composite-action script injection (2026-02-18, GHSA-9p44-j4g5-cfx5).** A
widely used security scanner Action had its own vulnerability. The composite action sourced
an environment file, and an attacker who could control that file's contents could execute
arbitrary commands. A workflow step you add to scan for security issues becomes an intrusion
path the moment it is exempted from scrutiny.

**Trivy ecosystem supply chain compromise (2026-03-19, GHSA-69fq-xp46-6x23).** A month later the
same Action was breached again, by an entirely different route. Using stolen credentials, an
attacker force-pushed 76 of the 77 tags in `aquasecurity/trivy-action` to malicious commits,
replaced all 7 tags in `aquasecurity/setup-trivy`, and published a malicious Trivy v0.69.4
release. The exposure window for trivy-action ran from 2026-03-19 17:43 to 2026-03-20 05:40 UTC,
about 12 hours. This is a separate incident from the script injection above.

The shared lesson from all three incidents is that everything a workflow executes, both the
references it resolves and the input values it trusts, needs verification. tj-actions and the
2026-03 Trivy compromise failed on unpinned tag references; the 2026-02 Trivy Action
vulnerability failed on an unverified input value. Note also that one repository can be hit
through both routes, and that being a security tool earns no exemption.

---

## Pinning to commit SHAs

Referencing a 40-character commit SHA instead of a mutable tag means the code that runs does not change
even if the tag is repointed. Keep the original version in a comment so people can still read it.

Pinning protects only the reference you pin, though. The advisory for the 2026-03 Trivy compromise
notes that a trivy-action pinned to a commit from before it started pinning the actions it calls
would still pull in a malicious `setup-trivy`. Check what a pinned action calls in turn.

```yaml
# .github/workflows/ci.yml

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Not recommended. A tag can be repointed to another commit
      - uses: actions/checkout@v7

      # Recommended. The content is pinned
      - uses: actions/checkout@<40-character commit SHA> # v7
      - uses: aquasecurity/trivy-action@<40-character commit SHA> # v0.36.0
```

Look up the SHA behind a tag like this.

```bash
# Resolve the commit SHA a tag currently points at
gh api repos/actions/checkout/git/ref/tags/v7 --jq '.object.sha'

# Find every tag reference across the repository's workflows
grep -rn "uses: .*@v[0-9]" .github/workflows/
```

### Keeping pinned SHAs from going stale

Pinning a SHA also freezes security patches. Automated update tools solve this.
Both Dependabot and Renovate recognize SHA-pinned references, open pull requests that move them to the
SHA of a new release, and update the version comment along with it.

```yaml
# .github/dependabot.yml

version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

With Renovate, the `helpers:pinGitHubActionDigests` preset converts existing tag references to pinned
SHAs in one pass and keeps later updates in the same form.

```json
// renovate.json

{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "helpers:pinGitHubActionDigests"
  ]
}
```

For the differences between the two tools, see the comparison table on the [Monitoring and Automated Remediation](./monitoring) page.

---

## Minimizing workflow permissions

The `GITHUB_TOKEN` in GitHub Actions is issued automatically for every workflow run.
If repository settings give that token write permission, a single compromised action can modify repository content.

Set the whole workflow to read-only at the top level, then grant only the scopes each job actually needs.

```yaml
# .github/workflows/ci.yml

name: CI

on:
  pull_request:
    branches: [main]

# Workflow-wide default. Any permission not listed becomes none
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    # Uses only the inherited contents: read
    steps:
      - uses: actions/checkout@<40-character commit SHA> # v7
        with:
          # Prevents later steps from reusing the token
          persist-credentials: false
      - run: npm ci && npm test

  sast:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      # Opens the SARIF upload permission in this job only
      security-events: write
    steps:
      - uses: actions/checkout@<40-character commit SHA> # v7
```

Starting from `permissions: {}` and adding only what is needed is stricter still.
In repository settings, also set the default `GITHUB_TOKEN` permission to read-only under the Actions menu.

### Care with pull_request_target

The `pull_request` event runs fork pull requests in a read-only environment with no secrets.
`pull_request_target` does the opposite: it runs with the target repository's secrets and write permissions.
If you check out and execute the pull request branch's code there, an outsider's code runs while holding your secrets.

```yaml
# A dangerous combination. Do not write it this way
on: pull_request_target

jobs:
  build:
    steps:
      - uses: actions/checkout@<40-character commit SHA> # v7
        with:
          # Checks out fork code in an environment that has secrets
          ref: ${{ github.event.pull_request.head.sha }}
      - run: npm ci # An install hook planted by the fork runs here
```

Use `pull_request_target` only for work that does not execute pull request code, such as labeling or
commenting. If you must build fork code, use `pull_request` or require approval before the run.

---

## Scanning workflows with zizmor

[zizmor](https://github.com/zizmorcore/zizmor) is a static analysis tool for GitHub Actions workflow YAML.
It is written in Rust, released under the MIT license, and finds the problems covered above automatically.

| Detection                 | What it covers                                                       |
| ------------------------- | -------------------------------------------------------------------- |
| Template injection        | Values taken through `${{ }}` that flow straight into shell commands |
| Credential persistence    | Checkout tokens left available for later steps to reuse              |
| Excessive permissions     | Jobs granted write permissions they never use                        |
| Impostor commits and refs | Commits pushed from a fork that look like legitimate references      |

Run it against `.github/workflows/`. Exporting SARIF sends the results to the GitHub Security tab.

```bash
# Local run
zizmor .github/workflows/

# SARIF output
zizmor --format=sarif .github/workflows/ > zizmor.sarif
```

Wire it into CI with the official action, which itself follows SHA pinning and least privilege.

```yaml
# .github/workflows/zizmor.yml

name: Workflow Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: ['**']

permissions: {}

jobs:
  zizmor:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      actions: read
      security-events: write
    steps:
      - uses: actions/checkout@<40-character commit SHA> # v7
        with:
          persist-credentials: false

      - uses: zizmorcore/zizmor-action@<40-character commit SHA> # v0.2.0
```

zizmor returns different exit codes by severity, so start by reporting findings without blocking,
clear the existing backlog, and only then promote it to a blocking gate.

---

## Build provenance and signing

The three sections above are prevention: keeping the pipeline from being compromised.
Provenance and signing answer the next question. Did this artifact in my hands really come out of that pipeline?

| Layer               | What it solves                                                                                                      | Representative implementation         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Build provenance    | Records which repository, which commit, and which build process produced the artifact, in a machine-verifiable form | SLSA provenance, in-toto attestations |
| Publishing identity | Removes long-lived tokens, closing the path where a stolen token publishes a package                                | npm trusted publishing (OIDC)         |
| Artifact signing    | Verifies that a published image or file has not changed since it was published                                      | Sigstore, cosign                      |

### The SLSA Build Track

[SLSA](https://slsa.dev/spec/) is a framework that defines build trust in levels.
The current specification is v1.2, and the Build Track has three levels.

| Level    | Requirement                                                                                                                 |
| -------- | --------------------------------------------------------------------------------------------------------------------------- |
| Build L1 | Follow a consistent build process and distribute provenance alongside the package                                           |
| Build L2 | A hosted build platform generates and signs the provenance itself. Consumers verify the signature                           |
| Build L3 | Isolate build runs so they cannot influence one another, and keep signing material out of reach of user-defined build steps |

Beyond the Build Track, v1.2 adds a Source Track covering the controls on the source repository itself.

### npm trusted publishing

npm supports publishing packages by authenticating with OIDC from GitHub Actions, GitLab CI/CD, and CircleCI.
Because you no longer store a long-lived npm token in repository secrets, the path where a leaked token
publishes a malicious version disappears.
Publishing from GitHub Actions or GitLab CI/CD also publishes provenance attestations automatically.
Self-hosted runners are not supported yet.

### Sigstore and cosign

Sigstore is a signing system that does not require you to hold keys yourself.
Fulcio verifies an OIDC identity and issues a short-lived certificate, and the signing record is written
to the Rekor transparency log.
Signers need no long-lived private key, and anyone can check who signed what and when in a public log.
For container images, cosign handles signing and verification.

```bash
# Keyless signing, using the execution environment's OIDC identity
cosign sign ghcr.io/myorg/myapp@sha256:<digest>

# Verification, down to which repository and workflow signed it
cosign verify ghcr.io/myorg/myapp@sha256:<digest> \
  --certificate-identity-regexp '^https://github.com/myorg/myapp/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

OpenSSF Model Signing v1.0 (2025-04) applies the same system to AI model artifacts.

---

## What signing and attestation do not prevent

Plenty of material presents attestation and signing as a complete answer. They are not.

:::warning Malicious packages have shipped with valid SLSA attestations
In the Mini Shai-Hulud attack against npm in 2026-05, 84 malicious packages were published carrying valid
SLSA Build Level 3 provenance attestations. The attestations were not forged. A compromised pipeline
issued them through the normal process.
:::

What a SLSA attestation guarantees is that the artifact came out of the declared pipeline.
It does not guarantee that the pipeline was not compromised. Once an attacker controls the workflow,
the attestations that workflow produces are issued through the normal procedure as well.
From the verifier's side, the two are indistinguishable.

So there is an order to follow.

| Order | What                                       | Why it comes first                                                   |
| ----- | ------------------------------------------ | -------------------------------------------------------------------- |
| 1     | Pin commit SHAs and automate updates       | Blocks tag repointing attacks directly, at the lowest cost           |
| 2     | Minimize workflow permissions              | Reduces what a compromise can take away                              |
| 3     | Scan the workflows themselves, with zizmor | Automatically confirms that 1 and 2 stay in place                    |
| 4     | Build provenance and artifact signing      | Becomes meaningful only on a pipeline where 1 through 3 are in place |

Adopting item 4 first does no harm, but with items 1 through 3 missing, item 4 mostly puts a
genuine-looking mark on the output of a compromised pipeline.

The tools and IDE extensions an agent invokes form a supply chain with the same structure. For how to
control the tools themselves, see [Agent and MCP Tool Governance](/ai-coding/agent-governance).

---

## Self-check

Pick one repository and check these six items.

- How many tag references starting with `@v` are in `.github/workflows/`
- Is there a `permissions:` block at the top of the workflow. If not, what is the repository default
- Does any workflow use `pull_request_target`. If so, does it execute pull request branch code
- Is `persist-credentials: false` set on `actions/checkout`
- Is the `github-actions` ecosystem registered in `.github/dependabot.yml`
- Do release artifacts carry provenance or signatures

Running zizmor once confirms the first four automatically.

## References

- [SLSA specification](https://slsa.dev/spec/)
- [zizmor documentation](https://docs.zizmor.sh/)
- [Sigstore cosign](https://docs.sigstore.dev/cosign/signing/overview/)
- [npm trusted publishing documentation](https://docs.npmjs.com/trusted-publishers)
- [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

## Next steps

- Full pipeline composition: [Pipeline Design](./pipeline-design)
- Post-deployment detection: [Monitoring and Automated Remediation](./monitoring)
- Mapping to ISO/IEC 18974 requirements: [ISO Standard Mapping](./iso-mapping)
