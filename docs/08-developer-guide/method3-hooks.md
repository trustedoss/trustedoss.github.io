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
            "command": "node -e \"\nlet raw = '';\nprocess.stdin.on('data', (c) => (raw += c));\nprocess.stdin.on('end', () => {\n  const hook = JSON.parse(raw);\n  const file = (hook.tool_input && hook.tool_input.file_path) || '';\n  const depFiles = ['package.json', 'requirements.txt', 'pom.xml', 'go.mod', 'Cargo.toml'];\n  if (depFiles.some((f) => file.endsWith(f))) {\n    console.error('[OSS Policy Warning] 의존성 파일이 변경되었습니다.');\n    console.error('신규 패키지의 라이선스와 취약점을 반드시 확인하세요.');\n    console.error('확인 방법: /oss-policy-check 실행');\n    process.exit(2);\n  }\n});\n\""
          }
        ]
      }
    ]
  }
}
```

> 이 단계는 `output/process/usage-approval.md`에 정의된 패키지 추가 승인 절차를 자동으로 환기시킵니다.

Hook 커맨드는 표준 입력(stdin)으로 도구 호출 정보가 담긴 JSON(`tool_name`, `tool_input`, `tool_response`)을 받습니다.
위 예시는 `tool_input.file_path`로 의존성 파일 여부를 판단하고, 해당하면 exit code 2로 종료해
경고 메시지가 Claude에게 전달되도록 합니다.

**효과:** Claude Code가 `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml` 등을 수정할 때마다 Claude가 경고를 인지하고 라이선스·취약점 확인을 안내합니다.

**더 강한 통제:** 수정 자체를 차단하려면 같은 스크립트를 `PreToolUse` Hook으로 등록하세요. PreToolUse에서 exit code 2는 도구 호출을 실행 전에 차단합니다.

**한계:** Claude Code 외부에서 파일을 수정하면 Hook이 실행되지 않는다. CI/CD로 보완합니다.

---

→ 다음: [방법 4: CI/CD 파이프라인](./method4-cicd.md)
