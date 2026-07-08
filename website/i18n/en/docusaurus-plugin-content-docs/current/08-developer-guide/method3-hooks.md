---
sidebar_position: 4
sidebar_label: 'Method 3:Hooks settings'
---

# Method 3:Setting up hooks

:::info Self-study mode(About 30 minutes)
Alerts are automatically issued whenever dependency files change.
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
            "command": "node -e \"\nlet raw = '';\nprocess.stdin.on('data', (c) => (raw += c));\nprocess.stdin.on('end', () => {\n  const hook = JSON.parse(raw);\n  const file = (hook.tool_input && hook.tool_input.file_path) || '';\n  const depFiles = ['package.json', 'requirements.txt', 'pom.xml', 'go.mod', 'Cargo.toml'];\n  if (depFiles.some((f) => file.endsWith(f))) {\n    console.error('[OSS Policy Warning] Dependency files were changed.');\n    console.error('Always check licenses and vulnerabilities for new packages.');\n    console.error('How to check: run /oss-policy-check');\n    process.exit(2);\n  }\n});\n\""
          }
        ]
      }
    ]
  }
}
```

> This step automatically invokes the package addition approval process defined in `output/process/usage-approval.md`.

The hook command receives the tool-call information as JSON (`tool_name`, `tool_input`, `tool_response`) on standard input.
The example above checks `tool_input.file_path` for dependency files and exits with code 2 so the warning is delivered to Claude.

**Effect:** whenever Claude Code modifies `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`, and similar files, Claude sees the warning and prompts a license and vulnerability check.

**Stronger control:** to block the modification itself, register the same script as a `PreToolUse` hook. In PreToolUse, exit code 2 blocks the tool call before it runs.

**Limitation:** if a file is modified outside Claude Code, the hook does not run. Complement it with CI/CD.

---

→ next: [Method 4:CI/CD pipeline](./method4-cicd.md)
