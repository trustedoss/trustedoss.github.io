---
id: ai-fuzzing
title: AI Fuzzing
sidebar_label: AI Fuzzing
sidebar_position: 8
---

# AI Fuzzing (Stage 4b)

Stage 3 tools find what a rule describes. What no rule describes — business logic flaws, edge-case
input handling — does not get caught, by definition. Stage 4b fills that gap by having the model
**search it directly**. Where [4a](./ai-security-review) re-judges what was already flagged, 4b
looks where nothing was flagged at all.

:::info This is the only stage that runs the application

Stages 1 to 3 and 4a read code. 4b starts the app and sends it requests. That is why it finds
defects static analysis cannot reach, and also why it runs on a schedule rather than on every
commit.

:::

## What it does

| Step     | What happens                                                            |
| -------- | ----------------------------------------------------------------------- |
| Read     | The app's code goes to the model, which maps endpoints and parameters   |
| Generate | Boundary and malformed inputs are produced per endpoint                 |
| Run      | Real requests go to the running app                                     |
| Watch    | 5xx responses, malformed replies and inconsistent state become findings |

This differs from traditional fuzzing, which feeds random bytes. The model reads the endpoint
signature and produces **meaningful boundaries**: values near a length limit, negatives, empty
values, wrong types, path traversal strings.

## Tool combinations by target

| Combination       | Detection target                        | Cadence              |
| ----------------- | --------------------------------------- | -------------------- |
| Claude + requests | Web API edge cases, abnormal responses  | Push to main         |
| Claude + AFL++    | Low-level binary crashes                | Weekly schedule      |
| Claude + OSS-Fuzz | Parser vulnerabilities in OSS libraries | Per-project settings |

For low-level C/C++ or Rust, tracking execution coverage matters more than clever inputs, so
OSS-Fuzz integration is the better route.

## In practice — ai-coding-best-practice

The [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) repository
runs this stage weekly. It is two files.

### The workflow

[ai-fuzzing.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/ai-fuzzing.yml)
runs on pushes to main and every Sunday.

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 4 * * 0'
```

It starts the app, confirms readiness with a health check, then runs the script. The result is kept
as an artifact for 30 days.

```yaml
- name: Start app
  run: |
    python src/app.py &
    sleep 5
    curl -sf http://localhost:8080/health || (echo "app failed to start" && exit 1)
```

**Without a key it skips.** Forks and early adopters see the job succeed rather than fail, the same
design the 4a workflow uses.

```yaml
if [ -z "$ANTHROPIC_API_KEY" ]; then
echo "::warning::ANTHROPIC_API_KEY is not set, skipping AI fuzzing."
exit 0
fi
```

### The script

[scripts/ai-fuzz.py](https://github.com/trustedoss/ai-coding-best-practice/blob/main/scripts/ai-fuzz.py)
does three things.

- `generate_fuzz_cases()` sends the app's code to the model and receives cases as a JSON array. It
  asks for at least 20 and names injection, path traversal and malformed input as targets
- `run_fuzz_cases()` issues each case as a real request. Under 500 passes; anything above, or an
  exception, is recorded as a failure with the start of the response body
- Results are written to `fuzz-report.json`

## What to watch when adopting it

**Do not make it a blocking gate.** The inputs come from a model, so false positives are part of
the deal, and a single failure blocking a release gets the job switched off. Same principle as 4a.

**Run it against an isolated instance.** It sends real requests, so production is not a target. The
app is started fresh inside CI and only that instance is touched.

**Control cost with cadence.** Generating and running 20-plus cases on every commit costs tokens
and minutes. The example above limits it to main pushes and once a week.

## Self-study

- Fork the repository, register `ANTHROPIC_API_KEY`, and trigger the workflow by hand. Watching how
  the job ends _without_ a key first tells you what adoption costs
- Open `fuzz-report.json` and read the `description` on failed cases — it says what the model was
  aiming at
- To point it at your own app, change `BASE_URL` and the start command

## Next steps

- [AI Security Code Review](./ai-security-review) — 4a, re-judging what was already flagged
- [Agent and MCP Tool Governance](./agent-governance) — 4c, governing what the AI calls
- [5-Stage Strategy](./strategy) — where this stage sits in the model
