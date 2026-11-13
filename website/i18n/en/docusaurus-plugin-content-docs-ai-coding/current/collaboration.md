---
id: collaboration
title: 'Productivity and Collaboration in AI Coding'
sidebar_label: 'Productivity and Collaboration'
description: Explains for development teams where bottlenecks shift with AI coding, how to run rule files as team assets, and how to agree on plans and share reviews.
sidebar_position: 12
---

# Productivity and Collaboration in AI Coding

:::info What this page covers

- Where the bottleneck moves once code writing gets faster
- How to run rules files as a shared team asset
- Agreeing on a plan, small PRs (pull requests), sharing the review load, parallel agent work
- What to measure and in what order to adopt

It is written for development leads, engineering managers, and developers who use agents as a team.
:::

AI coding tools reduce the time spent writing code. A team's delivery speed, however, is not set by
writing time alone. Defining requirements, splitting work, reviewing, integrating, and operating come
before and after it. If only code writing gets faster, those steps become the bottleneck.

This page covers how to keep the extra changes AI produces from piling up in review and integration.
The goal is to move from AI that each person uses alone to AI that the team uses under the same rules.
It looks at three things in turn: letting agents know the team's context, how people and agents split
work, and checking what agents did and measuring results.

## 1. Where does the bottleneck move?

The findings below show where the bottleneck moves once code is written faster.

| Source                                       | Scope and date                                             | Finding                                                                                                                        |
| -------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Atlassian State of Developer Experience 2025 | 3,500 respondents, 2025-07                                 | Writing code takes 16% of working time (citing an IDC survey from 2025-02). 50% lose 10 or more hours a week to friction       |
| Atlassian State of Developer Experience 2026 | 2026-10                                                    | 72% experience the same or more friction than before AI. The share saving 10 or more hours a week with AI fell from 68% to 25% |
| METR randomized controlled trial             | 16 experienced open source developers, 246 issues, 2025-07 | Tasks done with AI tools took 19% longer. Developers still believed afterwards that they had been 20% faster                   |
| Faros AI                                     | Data from more than 10,000 developers, 2025-07             | Teams with high AI use merged 98% more PRs, while PR review time grew 91% and PR size grew 154%                                |
| GitHub Octoverse 2026                        | 2026-10                                                    | Merged PRs more than tripled to 1.3 billion. More than 40% of PRs started from an agent's first draft                          |

Writing code is only part of a developer's work, and the extra changes accumulate in review. The number
of reviewers is the same; the amount to review is not. Perceived speed and actual speed can also
differ. A 2026-02 METR follow-up pointed toward a speedup, but METR itself says the result is unreliable
because developers who did not want to work without AI dropped out, and it is redesigning the study.
The lesson stands: measure, do not judge by feel.

Taken together, raising individual coding speed alone does not raise team results. If review and
integration cannot absorb the extra changes, waiting and rework grow instead. The sections below deal
with what comes before and after coding.

## 2. Context: running rules files as a team asset

Agents learn a team's conventions from rules files in the repository (AGENTS.md, CLAUDE.md,
`.cursor/rules`, and so on). If those files stay in personal settings, the agent behaves differently
for each person working in the same repository. Running rules files like code gives the whole team the
same starting context.

- Commit them to the repository. Keep only personal preferences in personal settings
  (`~/.claude/`, user rules).
- Assign an owner. Put rules files in CODEOWNERS so changes go through review.
- Keep them short. Agents read them every time, so write the conventions and prohibitions specific to
  this repository rather than everything. Models already know general coding principles.
- Fix them from failures. When an agent makes the same mistake twice, add one line to the rules.
- Rules files are also an attack surface. How to check them for hidden instructions is in the
  [Common Rules Template](./rules-template#the-rules-file-itself-is-an-attack-surface).

Context also includes material outside rules files. Connecting design documents, issues, and wikis to
an agent improves its answers, but the agent reads them with the permissions of the person who
connected it. A document shared too widely is found by the agent just as widely. Clean up permissions
and stale documents before connecting. Data-handling rules are in the
[AI Coding Tool Usage Policy](./usage-policy).

## 3. Collaboration: how people and agents split work

### Agree on a plan first

Hand a large task to an agent in one go and a large diff comes back; the reviewer must first work out
whether the direction is right. If the agent first proposes a plan (files to change, approach, units
to split into) and a person approves it before implementation, the decision about direction is made
before any code is written. Most coding agents offer a plan mode or a read-only mode.

### Split into small PRs

A reviewer can read only so much carefully at once. Agents produce large changes easily, so without a
size guideline review becomes a formality. In ai-coding-best-practice,
[pr-size.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/pr-size.yml)
warns when a change exceeds 400 lines excluding lock files. It never fails the build; the reviewer
decides whether to ask for a split.

### Share the review load

Split review into two layers. What machines can check, machines check first: Stage 3 gates, tests, and
[AI Security Code Review](./ai-security-review). People then look at design, fit with requirements, and
maintainability on top of those results. AI review does not replace human approval. Posting AI review
results only as PR comments and keeping them out of merge conditions is the principle of
[Stage 4a](./strategy#4a-findings-driven-ai-review).

Put the burden of explaining a change on its author. The
[PR template](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/pull_request_template.md)
in ai-coding-best-practice asks for AI use, decisions made by a person, and test checks. The field for
decisions made by a person tells the reviewer what to trust and where to look, and doubles as a
[copyright attribution](./legal-considerations#1-copyright-attribution-how-much-did-a-human-contribute)
record.

### Parallel agent work

Running several agents at once causes conflicts, where two agents change the same file differently,
and duplication, where the same work is done twice.

- Use a separate branch and working tree (`git worktree`) per task. Several agents editing files in one
  directory overwrite each other's changes.
- Split tasks so the files they touch do not overlap. If they overlap, set an order and merge one at a
  time.
- Record assigned tasks and their status in the issue tracker. If you cannot see which agent is doing
  what, you cannot prevent duplication.
- Match the number of concurrent agents to what you can review. If people cannot review the PRs agents
  open, parallel runs only lengthen the queue.

## 4. Checking and measuring

### Make what agents did visible

The scope you can hand to agents equals the scope in which you can later check what they did. Which
agent changed what, on whose instruction, and with what permissions must be recorded. Commit trailers
or AI-use notes in PR descriptions, dedicated agent accounts, and audit logs serve this purpose.
Permissions and identity management are covered in
[Agent and MCP Tool Governance](./agent-governance). MCP stands for Model Context Protocol.

### What to measure

AI tool usage (active users, accepted suggestions, lines of generated code) shows adoption, not
results. Measure the team's delivery performance and quality, and compare before and after adoption.

| Area       | Metric                                                  | What it tells you                             |
| ---------- | ------------------------------------------------------- | --------------------------------------------- |
| Delivery   | Lead time for changes, deployment frequency             | Does faster coding turn into actual releases? |
| Stability  | Change failure rate, time to restore                    | Do the extra changes lead to incidents?       |
| Bottleneck | PR review wait time, PR size distribution               | Can review absorb the extra changes?          |
| Rework     | Share of reverted changes, re-edits shortly after merge | Is quickly written code fixed again soon?     |
| Tests      | Count of test-integrity approval labels, mutation score | Is the verification standard holding?         |

The first two rows are DORA (DevOps Research and Assessment) metrics. DORA's 2025 report finds that AI adoption raises delivery
throughput but also raises delivery instability, and it lists seven organizational capabilities that
amplify AI's benefits: a clear and communicated AI stance, healthy data ecosystems, AI-accessible
internal data, strong version control practices, working in small batches, a user-centric focus, and
quality internal platforms. Running rules files, small PRs, and the [usage policy](./usage-policy) on
this page correspond to these capabilities.

Record current values as a baseline before you start. Without a baseline you cannot state the effect
of adoption. Use metrics to find bottlenecks, not to rate teams. Ranking individuals by AI usage pushes
people to raise usage, and results do not follow.

## 5. Adoption order

Expand only after confirming one step.

1. Organize context. Put rules files in the repository and assign owners. Clean up permissions and
   stale documents that agents will be connected to.
2. Pilot with one task. Pick a repeated, measurable task, record its baseline, and run it with a human
   approval point.
3. Set operating rules. From the pilot results, set approval points, permission scope, cost limits, and
   a PR size guideline, then expand to other tasks.

## Sources

- Atlassian, [State of Developer Experience Report 2025](https://www.atlassian.com/blog/developer/developer-experience-report-2025) (2025-07-09; the 16% coding figure cites IDC Survey Spotlight, 2025-02) and the 2026 edition (2026-10-20)
- METR, [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://arxiv.org/abs/2507.09089) (2025-07-10), [follow-up update](https://metr.org/blog/2026-02-24-uplift-update/) (2026-02-24)
- Faros AI, [The AI Productivity Paradox Report 2025](https://www.faros.ai/blog/ai-productivity-paradox-report-2025) (2025-07-23)
- GitHub, [Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/) (2026-10-28)
- DORA, [State of AI-assisted Software Development 2025](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf) (2025-09), AI Capabilities Model

All sources were checked on 2026-11-12.

## Next steps

- [Testing for AI-Written Code](./testing): the verification standard that lightens review
- [AI Security Code Review](./ai-security-review): the review layer machines handle before people
- [AI Coding Tool Usage Policy](./usage-policy): setting approval points, permissions, and cost limits as policy
- [Best Practice Repository](./best-practice-repo): PR size check, PR template, and CODEOWNERS examples
