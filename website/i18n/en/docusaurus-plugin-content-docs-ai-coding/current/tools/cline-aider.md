---
id: cline-aider
title: Cline / Aider Setup
sidebar_label: Cline / Aider
sidebar_position: 5
---

# Cline / Aider Setup

## Overview

Cline reads `.clinerules` files (a single root file or `.clinerules/` folder) as project instructions and applies them to AI behavior. Aider can augment the system prompt through `AGENTS.md` or the `system_prompt` field in `.aider.conf.yml`. Both tools apply rules at the project level.

Cline is an agent-style AI tool running as a VS Code extension, while Aider is a terminal-based CLI tool. Both are open source and run locally, so they are often preferred by teams that avoid sending code to external servers. If open source policy is written in each configuration file, AI automatically considers it when adding packages or generating code.

---

## Cline Setup

### Configuration File Location

- `.clinerules` (single root file, recommended)
- `.clinerules/` (folder, allows split files)

### How to Apply

1. Create `.clinerules` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

### Configuration Example

```markdown
## Open Source Policy

### License Management

When adding new external packages/libraries, always verify and document the license.

**Allowed Licenses**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Review Required Licenses** (legal review required): LGPL, MPL

**Prohibited Licenses** (cannot be used without prior approval): GPL, AGPL, SSPL, Commons Clause

### Security Management

- Do not use package versions with known CVEs
- After adding dependencies, run one of the following commands:
  - npm: `npm audit`
  - Python: `pip-audit`
  - Container/General: `trivy fs .`
- Use the latest stable package version whenever possible

### SBOM Management

- SBOM update required when dependencies change
- Generation tools: cdxgen, syft, trivy
- Recommended format: CycloneDX (alternative: SPDX)

### Copyright

- Keep existing code copyright headers
- Include project license header when creating new files
- When copying code from another project, include source and license
```

---

## Aider Setup

### Configuration File Location

- `AGENTS.md` (root, compatible with OpenAI Codex agent spec)
- `system_prompt` field in `.aider.conf.yml`

### How to Apply

1. Create `AGENTS.md` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. If you prefer concise setup, summarize only key policy points in `.aider.conf.yml` under `system_prompt`.

### Configuration Example

**AGENTS.md** — Include the entire Common Rules Template as-is.

```markdown
## Open Source Policy

### License Management

When adding new external packages/libraries, always verify and document the license.

**Allowed Licenses**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Review Required Licenses** (legal review required): LGPL, MPL

**Prohibited Licenses** (cannot be used without prior approval): GPL, AGPL, SSPL, Commons Clause

### Security Management

- Do not use package versions with known CVEs
- Use the latest stable package version whenever possible

### SBOM Management

- SBOM update required when dependencies change (Tools: cdxgen, syft)
```

**.aider.conf.yml** — Use a concise summary of key items only.

```yaml
system_prompt: |
  ## Open Source Policy
  Allowed Licenses: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
  Review Required Licenses (legal review required): LGPL, MPL
  Prohibited Licenses: GPL, AGPL, SSPL, Commons Clause
  CVE vulnerability Version Use 금지. 의존성 addition 후 audit run 권장.
```

---

## Notes

:::info Good to know
Both Cline and Aider treat rules as soft guidance rather than hard blocking. To fully block policy-violating packages, configure a CI/CD pipeline in parallel. Since Aider is CLI-based, if `.aider.conf.yml` does not exist, you can pass policy directly on each run with `--system-prompt`. For automated CI/CD gate setup, refer to [Quick CI/CD](../cicd-quick).
:::
