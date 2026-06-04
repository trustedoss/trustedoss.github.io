---
sidebar_position: 4
sidebar_label: '방법 3: Hooks 설정'
---

# 방법 3: Hooks 설정하기

:::info 셀프스터디 모드 (약 30분)
의존성 파일이 변경될 때마다 자동으로 경고가 발생합니다.
:::

`.claude/settings.json`에 아래 Hook을 추가합니다.

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

> 이 단계는 `output/process/usage-approval.md`에 정의된 패키지 추가 승인 절차를 자동으로 환기시킵니다.

**효과:** Claude Code가 `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml` 등을 수정할 때마다 자동으로 경고 메시지가 표시됩니다.

**한계:** Claude Code 외부에서 파일을 수정하면 Hook이 실행되지 않는다. CI/CD로 보완합니다.

---

→ 다음: [방법 4: CI/CD 파이프라인](./method4-cicd.md)
