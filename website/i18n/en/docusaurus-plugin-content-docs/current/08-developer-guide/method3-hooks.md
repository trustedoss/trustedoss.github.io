---
sidebar_position: 4
sidebar_label: 'Method 3: Hooks Setup'
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 30 minutes
---

# Method 3: Setting Up Hooks

:::info Self-study mode (about 30 minutes)
A warning is raised automatically whenever a dependency file changes.
:::

Add the Hook below to `.claude/settings.json`.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"\nlet raw = '';\nprocess.stdin.on('data', (c) => (raw += c));\nprocess.stdin.on('end', () => {\n  const hook = JSON.parse(raw);\n  const file = (hook.tool_input && hook.tool_input.file_path) || '';\n  const depFiles = ['package.json', 'requirements.txt', 'pom.xml', 'go.mod', 'Cargo.toml'];\n  if (depFiles.some((f) => file.endsWith(f))) {\n    console.error('[OSS Policy Warning] A dependency file was changed.');\n    console.error('Always check the licenses and vulnerabilities of new packages.');\n    console.error('How to check: run /oss-policy-check');\n    process.exit(2);\n  }\n});\n\""
          }
        ]
      }
    ]
  }
}
```

This Hook serves as an automatic reminder of the package addition approval procedure defined in `output/process/usage-approval.md`.

The Hook command receives the tool-call information as JSON (`tool_name`, `tool_input`, `tool_response`) on standard input.
The example above uses `tool_input.file_path` to determine whether a dependency file is involved, and if so exits with code 2
so that the warning message is delivered to Claude.

**Effect:** Whenever Claude Code modifies `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`, and similar files, Claude sees the warning and guides you through the license and vulnerability check.

**Stronger control:** To block the modification itself, register the same script as a `PreToolUse` Hook. In PreToolUse, exit code 2 blocks the tool call before it runs.

**Limitation:** If a file is modified outside Claude Code, the Hook does not run. Complement it with CI/CD.

---

→ Next: [Method 4: CI/CD Pipeline](./method4-cicd.md)
