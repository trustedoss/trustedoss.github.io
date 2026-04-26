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
            "command": "node -e \"\nconst fs = require('fs');\nconst result = process.env.CLAUDE_TOOL_RESULT || '';\nconst changedFiles = ['package.json', 'requirements.txt', 'pom.xml', 'go.mod', 'Cargo.toml'];\nconst hasDepChange = changedFiles.some(f => result.includes(f));\nif (hasDepChange) {\n  console.error('[OSS Policy Warning] 의존성 파일이 변경되었습니다.');\n  console.error('신규 패키지의 라이선스와 취약점을 반드시 확인하세요.');\n  console.error('확인 방법: /oss-policy-check 실행');\n}\n\""
          }
        ]
      }
    ]
  }
}
```

> This step automatically invokes the package addition approval process defined in `output/process/usage-approval.md`.

**effect:** Claude Code `package.json`, `requirements.txt`, `pom.xml`, `go.mod`,Whenever you modify `Cargo.toml` etc. you will automatically see a warning message.

**margin:** If you modify the file outside of Claude Code, the Hook will not be executed. Complemented by CI/CD.

---

→ next: [Method 4:CI/CD pipeline](./method4-cicd.md)
