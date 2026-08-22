---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 30 minutes to 1 hour
pagination_label: '1. Environment Setup'
---

# Environment setup: Install the tools needed for the exercises

## 1. What we do in this chapter

Install and verify the tools you will use across all exercises in this kit.

- You can only run the agents in later chapters once this step is complete.
- This chapter itself does not directly satisfy any ISO/IEC 5230 or ISO/IEC 18974 checklist item.
- However, none of the later exercises are possible without it, so it must be completed.

## 2. Open a terminal

From this chapter on, you will use a **terminal** (a program with a mostly-black screen where you
type commands to control your computer). Every code block below is a command you type into this
terminal.

**Opening a terminal on macOS**

1. Press `Cmd` and `Space` together (this opens Spotlight search).
2. Type `Terminal`.
3. Click (or press Enter on) the "Terminal" app in the search results.

**Opening a terminal on Windows**

1. Click the Start menu, or press the `Windows` key.
2. Type `PowerShell`.
3. Click "Windows PowerShell" to open it.

Once open, you will see a blinking cursor on an empty screen. Type or paste a code block from this
document there and press Enter to run it.

:::tip Copying and pasting a code block
Hover over a gray code block in this document and a copy icon appears in the top-right corner.
Click it to copy the whole block. Click into the terminal window, then paste with `Cmd+V` on macOS
or `Ctrl+V` on Windows (or right-click → Paste), and press Enter. A multi-line block runs all its
lines in order with one Enter.
:::

:::tip When you see "open a new terminal"
This guide repeatedly says things like "end your Claude session, then run this in a new terminal."
"Opening a new terminal" means opening the terminal app again the same way as above, leaving the
current window as is (you can close it or leave it open — either is fine).
:::

## 3. Tools you will need

| Tool           | Use                                                     | Installation                                 | Version requirement |
| -------------- | ------------------------------------------------------- | -------------------------------------------- | ------------------- |
| Docker Desktop | Runs chapter 05 hands-on tools (Dependency-Track, etc.) | Chapter 05 only (alternative path available) | 24.x or later       |
| Git            | Repository and version management                       | Required                                     | 2.x or later        |
| Claude Code    | AI-assisted practice; runs the agents                   | Required                                     | Latest version      |
| Node.js        | Only if you want to build the Docusaurus site yourself  | Optional (not needed for the exercises)      | v18 LTS or later    |

:::info You don't need Node.js to install Claude Code
The Claude Code install command in section 4 runs without Node.js. Node.js is only needed if you
want to build this documentation website yourself; none of the exercises in this kit (running
agents, generating deliverables) use it.
:::

:::tip If you cannot install Docker
Docker is used only in chapter 05 (SBOM and vulnerability tool exercises). If installation is difficult, for example due to company policy, you can continue with a pre-built sample SBOM via the "When proceeding without Docker" path in chapter 05. The remaining chapters (02 Organization through 04 Process, 06 Training through 07 Conformance) run on agent conversations alone, without Docker.
:::

## 4. Installation instructions (by OS)

### macOS

Paste these into your terminal, one block at a time (or all at once).

```bash
# Git — macOS needs no separate installer.
# Running the command below prompts "Install the Command Line Tools?" if git
# isn't already present. Click "Install" and wait a few minutes; git comes
# bundled with it.
git --version

# Claude Code (no Node.js, no Homebrew needed)
curl https://claude.sh | bash

# Docker Desktop — this opens the download page in your browser.
# Double-click the downloaded .dmg file and drag it into Applications.
open https://www.docker.com/products/docker-desktop
```

:::tip Installing Node.js yourself (optional)
Only needed if you want to build the documentation site yourself. Download the "LTS" installer
(.pkg) from [nodejs.org](https://nodejs.org) and double-click it.
:::

### Windows

We recommend using WSL2. When installing Docker Desktop, you must enable the WSL2 backend.

```powershell
# Git for Windows: download and run the installer from https://git-scm.com/download/win

# Claude Code (no Node.js needed)
curl https://claude.sh | bash

# Or, if you have winget:
winget install Anthropic.Claude

# Docker Desktop: download from https://www.docker.com/products/docker-desktop
# Check "Use WSL2" when the installer asks
```

### Linux (Ubuntu/Debian)

```bash
# Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER

# Git
sudo apt-get install git

# Claude Code (no Node.js needed)
curl https://claude.sh | bash
```

## 5. Installation verification script

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

## 6. Clone the repository and run it for the first time

**What is `git clone`?** All the files in this kit (agents, templates, guide documents) live on a
site called GitHub. `git clone` downloads that entire set of files to your computer as a copy. You
only run it once; after that, you work inside the `trustedoss-agents` folder it creates.

If you are just starting out:

```bash
# Clone the repository (download the files)
git clone https://github.com/trustedoss/trustedoss-agents.git
cd trustedoss-agents

# Create the output directory if it is missing
mkdir -p output

# Run Claude Code
claude
```

If you have already cloned it (downloaded it once before):

```bash
cd trustedoss-agents
git pull
claude
```

## 7. What to do after running Claude Code for the first time

When Claude Code starts:

1. **Type "Where do I start?"** → It analyzes your current status and automatically guides you to the next step.
2. On your first run, the `output/` folder is empty, so it will direct you to the `02-organization-designer` agent.
3. Claude Code automatically reads `CLAUDE.md` to understand the project context.

:::info
Claude Code also reads the `CLAUDE.md` in each chapter folder to pick up the context for that step.
:::

## 8. Troubleshooting

### When you see "Cannot connect to the Docker daemon"

This means the Docker Desktop app is not running yet (installing it and running it are different things).

- **macOS/Windows**: Open Launchpad (macOS) or the Start menu (Windows) and click "Docker Desktop"
  to launch it. Once the whale icon in the menu bar (macOS) or system tray (Windows) stops
  animating, it's ready. Then retry your command.
- **Linux**: Run `sudo systemctl start docker` and retry.

### When Docker Desktop won't start

- **macOS**: Go to System Preferences > Privacy & Security and click Allow.
- **Windows**: Requires Hyper-V and WSL2 to be enabled.
- **Linux**: Run `sudo systemctl start docker` and retry.

### When you see "brew: command not found" or similar

The macOS install commands in this guide are written to run without Homebrew. If you hit this
error, you may be following a different version of these instructions — paste the commands from
section 4 again.

### When you can't log in to Claude Code

- Run `claude`, then type `/login` inside the session to authenticate with your Anthropic account.
- If the browser does not open automatically, copy the URL shown in the terminal and open it manually.

### git clone permission error

- Clone over HTTPS: `git clone https://github.com/trustedoss/trustedoss-agents.git`
- If you hit a GitHub authentication error, run `git config --global credential.helper store` and retry.

### When your Node.js version is too old (below v18, only relevant if building the docs site)

- We recommend using nvm: `nvm install --lts && nvm use --lts`

## 9. Self-study

:::info Self-study mode (about 30 minutes to 1 hour)
The time required varies depending on your tool installation situation.
:::

1. Review the list of tools you need.
2. Install each tool (if not already installed).
3. Run the installation verification script.
4. Clone the repository and create `output/`.
5. After running `claude`, type "Where do I start?"

## 10. Completion checklist

- [ ] `docker --version` outputs normally (skip if you chose the no-Docker path)
- [ ] `git --version` outputs normally
- [ ] `claude --version` outputs normally
- [ ] Repository clone complete (or already exists)
- [ ] `output/` directory exists
- [ ] Confirmed normal operation after running `claude`

## 11. Next steps

Once your environment is ready, proceed to the organization design phase.

Read the [Organizational structure: Designating open source personnel and defining roles](../02-organization/index.md) chapter first, then run the agent — or you can run the agent right away.

:::tip Check before running
First terminate the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/en/02-organization-designer
claude
```

After the agent finishes, check the outputs: `ls output/organization/` — three files (role definition, RACI matrix, appointment template) mean success.
