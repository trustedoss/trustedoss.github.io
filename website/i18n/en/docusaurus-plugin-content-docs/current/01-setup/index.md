---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 30 minutes to 1 hour
---

# environmental preparation:Install tools needed for practice

## 1. What we do in this chapter

Install and validate the tools you will use in all exercises in this kit.

- Only after this step is completed can the agent be executed later.
- This chapter itself does not directly meet the checklist items of ISO/IEC 5230 or ISO/IEC 18974
- However, without this step, all subsequent exercises are impossible, so it must be completed.

## 2. List of tools needed

| tools          | Use                                           | Installation required           | Version Requirements |
| -------------- | --------------------------------------------- | ------------------------------- | -------------------- |
| Docker Desktop | All hands-on tools(Dependency-Track, etc.)Run | Required                        | 24.x and above       |
| Git            | Repository Management and Version Management  | Required                        | 2.x and above        |
| Claude Code    | AI-based practice assistance,run agent        | Required                        | Latest version       |
| Node.js        | Build Docusaurus Documentation Site           | select(Document site if needed) | v18 LTS or later     |

## 3. Installation instructions(By OS)

### macOS

```bash
# Docker Desktop
# https://www.docker.com/products/docker-desktop download from

# Git (Homebrew Use)
brew install git

# Claude Code
npm install -g @anthropic-ai/claude-code

# Node.js (optional - Homebrew)
brew install node
```

### Windows

We recommend using WSL2. When installing Docker Desktop, you must enable the WSL2 backend.

```powershell
# Docker Desktop: https://www.docker.com/products/docker-desktop download from
# WSL2 must be enabled

# Git for Windows: https://git-scm.com/download/win

# Claude Code (PowerShell)
npm install -g @anthropic-ai/claude-code
```

### Linux (Ubuntu/Debian)

```bash
# Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER

# Git
sudo apt-get install git

# Claude Code
npm install -g @anthropic-ai/claude-code

# Node.js (optional - nvm recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

## 4. Set of installation confirmation commands

Run the script below to check whether all required tools are installed properly.

```bash
#!/bin/bash
echo "=== trustedoss environment check ==="

echo -n "Docker: "
docker --version 2>/dev/null || echo "❌ not installed"

echo -n "Git: "
git --version 2>/dev/null || echo "❌ not installed"

echo -n "Claude Code: "
claude --version 2>/dev/null || echo "❌ not installed"

echo -n "Node.js (optional): "
node --version 2>/dev/null || echo "⚪ not installed (optional)"

echo ""
echo "Proceed to the next step when all required tools are installed."
```

## 5. Clone the repository and first run it

If you're just starting out:

```bash
# clone repository
git clone https://github.com/trustedoss/trustedoss.github.io.git
cd trustedoss.github.io

# output create directory if missing
mkdir -p output

# Claude Code run
claude
```

If you have already cloned:

```bash
cd trustedoss.github.io
git pull
claude
```

## 6. What to do after running Claude Code for the first time

When Claude Code runs:

1. **Type “Where do I start?”** → Automatically guides you to the next step after analyzing the current status
2. If this is your first run, the `output/` folder is empty, so you will be guided to the `02-organization-designer` agent.
3. Claude Code automatically reads `CLAUDE.md` to understand project context.

> Claude Code also reads `CLAUDE.md` in each chapter folder to get context for that step.

## 7. Troubleshooting

### When Docker Desktop does not run

- **macOS**:System Preferences > Privacy & Security > Click Allow
- **Windows**:Requires Hyper-V and WSL2 activation
- **Linux**:`sudo systemctl start docker` Run and retry

### Claude Code When you can't log in

- Run `claude login` to authenticate with your Anthropic account.
- If the browser does not open automatically, copy the URL displayed in the terminal and access it manually.

### git clone permission error

- Clone via HTTPS: `git clone https://github.com/trustedoss/trustedoss.github.io.git`
- In case of GitHub authentication error:`git config --global credential.helper store` Run and retry

### When your Node.js version is too low(Below v18)

- Recommended to use nvm: `nvm install --lts && nvm use --lts`

## 8. Self-study

:::info Self-study mode(Approximately 30 minutes to 1 hour)
The time required will vary depending on the tool installation situation.
:::

1. Check out the list of tools you need
2. Install each tool(If not installed)
3. Run the installation verification script
4. Clone the repository and create `output/`
5. After running `claude` “Where do I start?” input

## 9. Completion Confirmation Checklist

- [ ] `docker --version` Normal output
- [ ] `git --version` Normal output
- [ ] `claude --version` Normal output
- [ ] Repository clone complete(or already exists)
- [ ] `output/` directory exists
- [ ] Check normal operation after executing `claude`

## 10. Next steps

Once the environment preparation is complete, proceed to the organization design phase.

[organizational structure:Designating open source personnel and defining roles](../02-organization/index.md)Read the chapter first and then run the agent,You can run the agent right away.

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/02-organization-designer
claude
```
