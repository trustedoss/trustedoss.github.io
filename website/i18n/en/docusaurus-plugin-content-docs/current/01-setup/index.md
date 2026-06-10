---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 30 minutes to 1 hour
---

# Environment setup: Install the tools needed for the exercises

## 1. What we do in this chapter

Install and verify the tools you will use across all exercises in this kit.

- You can only run the agents in later chapters once this step is complete.
- This chapter itself does not directly satisfy any ISO/IEC 5230 or ISO/IEC 18974 checklist item.
- However, none of the later exercises are possible without it, so it must be completed.

## 2. Tools you will need

| Tool           | Use                                                     | Installation                                 | Version requirement |
| -------------- | ------------------------------------------------------- | -------------------------------------------- | ------------------- |
| Docker Desktop | Runs chapter 05 hands-on tools (Dependency-Track, etc.) | Chapter 05 only (alternative path available) | 24.x or later       |
| Git            | Repository and version management                       | Required                                     | 2.x or later        |
| Claude Code    | AI-assisted practice; runs the agents                   | Required                                     | Latest version      |
| Node.js        | Builds the Docusaurus documentation site                | Optional (only if you need the docs site)    | v18 LTS or later    |

:::tip If you cannot install Docker
Docker is used only in chapter 05 (SBOM and vulnerability tool exercises). If installation is difficult, for example due to company policy, you can continue with a pre-built sample SBOM via the "When proceeding without Docker" path in chapter 05. The remaining chapters (02 Organization through 04 Process, 06 Training through 07 Conformance) run on agent conversations alone, without Docker.
:::

## 3. Installation instructions (by OS)

### macOS

```bash
# Docker Desktop
# Download from https://www.docker.com/products/docker-desktop

# Git (via Homebrew)
brew install git

# Claude Code
npm install -g @anthropic-ai/claude-code

# Node.js (optional - Homebrew)
brew install node
```

### Windows

We recommend using WSL2. When installing Docker Desktop, you must enable the WSL2 backend.

```powershell
# Docker Desktop: download from https://www.docker.com/products/docker-desktop
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

## 4. Installation verification script

Run the script below to check whether all required tools are installed correctly.

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
echo "Proceed to the next step once all required tools are installed."
```

## 5. Clone the repository and run it for the first time

If you are just starting out:

```bash
# Clone the repository
git clone https://github.com/trustedoss/trustedoss-agents.git
cd trustedoss-agents

# Create the output directory if it is missing
mkdir -p output

# Run Claude Code
claude
```

If you have already cloned it:

```bash
cd trustedoss-agents
git pull
claude
```

## 6. What to do after running Claude Code for the first time

When Claude Code starts:

1. **Type "Where do I start?"** → It analyzes your current status and automatically guides you to the next step.
2. On your first run, the `output/` folder is empty, so it will direct you to the `02-organization-designer` agent.
3. Claude Code automatically reads `CLAUDE.md` to understand the project context.

> Claude Code also reads the `CLAUDE.md` in each chapter folder to pick up the context for that step.

## 7. Troubleshooting

### When Docker Desktop won't start

- **macOS**: Go to System Preferences > Privacy & Security and click Allow.
- **Windows**: Requires Hyper-V and WSL2 to be enabled.
- **Linux**: Run `sudo systemctl start docker` and retry.

### When you can't log in to Claude Code

- Run `claude login` to authenticate with your Anthropic account.
- If the browser does not open automatically, copy the URL shown in the terminal and open it manually.

### git clone permission error

- Clone over HTTPS: `git clone https://github.com/trustedoss/trustedoss-agents.git`
- If you hit a GitHub authentication error, run `git config --global credential.helper store` and retry.

### When your Node.js version is too old (below v18)

- We recommend using nvm: `nvm install --lts && nvm use --lts`

## 8. Self-study

:::info Self-study mode (about 30 minutes to 1 hour)
The time required varies depending on your tool installation situation.
:::

1. Review the list of tools you need.
2. Install each tool (if not already installed).
3. Run the installation verification script.
4. Clone the repository and create `output/`.
5. After running `claude`, type "Where do I start?"

## 9. Completion checklist

- [ ] `docker --version` outputs normally (skip if you chose the no-Docker path)
- [ ] `git --version` outputs normally
- [ ] `claude --version` outputs normally
- [ ] Repository clone complete (or already exists)
- [ ] `output/` directory exists
- [ ] Confirmed normal operation after running `claude`

## 10. Next steps

Once your environment is ready, proceed to the organization design phase.

Read the [Organizational structure: Designating open source personnel and defining roles](../02-organization/index.md) chapter first, then run the agent — or you can run the agent right away.

:::tip Check before running
First terminate the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/02-organization-designer
claude
```

After the agent finishes, check the outputs: `ls output/organization/` — three files (role definition, RACI matrix, appointment template) mean success.
