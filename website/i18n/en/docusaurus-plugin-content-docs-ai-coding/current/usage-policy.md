---
id: usage-policy
title: 'AI Coding Tool Usage Policy'
sidebar_label: 'AI Coding Tool Usage Policy'
sidebar_position: 2
---

# AI Coding Tool Usage Policy

The first thing an organization that uses AI coding tools needs is not a tool configuration but a set
of usage rules: which tools are allowed, which code and data may be sent to them, who approves and who
is accountable, what people are taught, and how much may be spent. Without these rules, people work
with whatever tools and accounts they picked themselves, and the other controls in this section (Rules,
CI gates, MCP controls) lose a clear scope.

This page puts those rules in one document. You can add the copy-paste block in the last section to
your [open source policy](/en/docs/policy) or adopt it as a standalone policy.

:::note Not legal advice
Vendor terms and data-handling conditions summarize public documents as of 2026-11. Terms change
often, so check the original documents again when you adopt a tool.
:::

## 1. Tool approval

### Approval criteria

Check the items below before adding a tool to the allow list. The same product has different
conditions on different plans, so approve a "product and plan" pair rather than a product.

| Item               | What to check                                                                                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Data handling      | Are submitted code and prompts excluded from model training? How long are they retained?                                                                                                |
| IP indemnification | Does the vendor defend copyright claims against the output? See [Legal Considerations, section 2](./legal-considerations#2-vendor-ip-indemnification-who-defends-an-infringement-claim) |
| Admin control      | Can organization admins enforce settings that individuals cannot override?                                                                                                              |
| Records            | Can the organization see usage records and audit logs?                                                                                                                                  |
| Cost control       | Can you set organization-level usage limits and alerts?                                                                                                                                 |
| Extensions         | Can admins restrict MCP servers, plugins, and external connections? See [Agent and MCP Tool Governance](./agent-governance)                                                             |

### Data-handling conditions by vendor

The table covers business plans. Individual plans of the same vendor differ. For example, since
2026-04-24 GitHub uses interaction data from Copilot Free, Pro, and Pro+ users for training (users can
opt out), while Business and Enterprise are excluded from that change.

| Tool                                           | Training                                                             | Retention and zero-retention option                                                                    | Admin enforcement                                                                                   |
| ---------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| GitHub Copilot Business and Enterprise         | Not used for training                                                | Chat on github.com is retained for the life of the account from 2026-09-28 onward (previously 28 days) | Enterprise policies cannot be overridden by organizations. Content exclusion by repository and path |
| Anthropic (Team, Enterprise, API, Claude Code) | Not used for training (unless the customer joins a separate program) | 30 days by default. Zero data retention (ZDR) is enabled by Anthropic per qualified organization       | Keys in managed settings (`managed-settings.json`) cannot be overridden by user settings            |
| OpenAI (ChatGPT Business and Enterprise, API)  | Not used for training by default                                     | API abuse-monitoring logs kept up to 30 days. Zero retention needs prior approval from OpenAI          | Workspace admin settings                                                                            |
| Cursor (Teams, Enterprise)                     | Not used for training in Privacy Mode                                | In Privacy Mode, zero-retention agreements with model providers; some models are exceptions            | Admins can turn on Privacy Mode and stop members from turning it off                                |
| Gemini Code Assist                             | Prompts and responses not used for training                          | No retention period stated in the official documentation                                               | Not confirmed in official documentation                                                             |

Two points need care. First, GitHub's documentation states that content exclusion may miss indirect
file access by agents and does not replace operating-system permissions. Second, Copilot's policy that
blocks suggestions matching public code does not apply to Copilot CLI and works only in annotate mode
for the cloud agent. When you approve a tool, check the conditions for its CLI and agent features
separately from its IDE features.

### Unapproved tools

Use of personal accounts or unapproved extensions for work (shadow AI) is hard to stop by prohibition
alone. If there is no approved tool, or the approved one is inconvenient, people go back to personal
accounts. Keeping the approval process short and providing an approved tool first works better.
Technical options include blocking unapproved AI service domains on the corporate network and
maintaining an IDE extension allow list.

## 2. Data handling

Data classification decides what may be sent to a tool. Even an approved tool should not receive some
data.

| Class      | Examples                                                | Sending to an approved tool                                                 |
| ---------- | ------------------------------------------------------- | --------------------------------------------------------------------------- |
| Public     | Code in public repositories, public documents           | Allowed                                                                     |
| Internal   | Code in internal repositories, design documents, issues | Allowed if the plan does not train on it                                    |
| Restricted | Customer data, personal information, production logs    | Not allowed in principle. If needed, pseudonymize and get separate approval |
| Secret     | API keys, tokens, certificates, passwords               | Not allowed. Block reading them in agent settings                           |

Agent tools read files directly without anyone pasting them. A rule that says "do not send" is only
kept when it becomes a setting that says "cannot read". The
[ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.claude/settings.json)
repository blocks reads of `.env` and `secrets/` with Claude Code's `permissions.deny`, and GitHub
Copilot offers content exclusion by repository or path.

The same rule applies when you connect external documents and systems to an agent. The agent reads
with the permissions of the person who connected it, so a document shared too widely is found by the
agent just as widely. Clean up sharing scope before connecting.

## 3. Roles and responsibilities

| Role               | Responsibilities                                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------------------- |
| Policy owner       | Writes and revises the usage policy, maintains the allow list, reviews it once a year                           |
| Tool administrator | Deploys admin settings (managed settings, organization policies), accounts and licenses, cost limits and alerts |
| Security           | Reviews tools and MCP servers before adoption, decides data classification, handles incidents                   |
| Legal              | Reviews vendor terms and IP indemnification, decides copyright attribution, reviews before external release     |
| Development lead   | Owns the team's rules file, runs PR review criteria and approval points                                         |
| Developer          | Uses approved tools only, records AI use, holds final responsibility for generated code                         |

In a small organization one person may hold several roles. When the person who approves a tool also
approves code made with it, keep review records so the reasoning stays visible. Where to place the AI
coding tool policy role in your organization design is covered in
[Organization](/en/docs/organization).

The last row matters. The person who merges AI-generated code is responsible for it. The Linux kernel
forbids AI agents from adding `Signed-off-by` and lets only humans certify the DCO (Developer
Certificate of Origin) for the same reason
([Legal Considerations, section 4](./legal-considerations#4-upstream-open-source-projects-ai-contribution-policies)).

## 4. Training and awareness

Allowing a tool is not the same as people using it safely. Include the items below in onboarding and
regular training.

- Approved tools and plans, and why personal accounts are not allowed
- Data classes and data that must not be sent
- Common defects in AI-generated code: vulnerable patterns, suggestions of packages that do not exist,
  code with an incompatible license
- The workflow of agreeing on tests first and then handing over implementation ([Testing](./testing))
- How to record AI use (commit messages, PR template)
- Checking an upstream project's AI policy before contributing

For organizations that provide or use AI systems in the EU, training is also a legal duty. Article 4
of the EU AI Act (AI literacy) has applied to providers and deployers since 2025-02-02. The Digital
Omnibus on AI (Regulation (EU) 2026/1744, in force 2026-07-27) amended it: providers and deployers must
take measures to support the AI literacy of their staff, without having to guarantee a specific level
for any individual. The duty was softened, not removed, so training plans and completion records still
serve as evidence.

Keep training records the same way as open source training records. Adding AI coding items to the
deliverables of the [Training](/en/docs/training) chapter avoids a separate system.

## 5. Cost limits

Costs of agent tools vary widely with use. An agent repeating a long task uses far more tokens than
chat use. Without limits, you learn about actual usage only when the invoice arrives.

- Set a monthly organization limit and per-user or per-team limits.
- Send alerts at set shares of the limit (for example 80% and 100%), and check that the recipient is
  the person who will act.
- AI jobs that run in CI (AI review, AI fuzzing) use dedicated keys, each with its own limit.

Cost controls of major tools (checked 2026-11):

| Tool                      | Cost control                                                                                                                                                                                                                                                   |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude (Team, Enterprise) | When an admin turns on usage credits, use continues on credits past the seat allowance. Spend limits per organization, group, or member, admin analytics dashboard. In Claude Code, `/usage` shows usage                                                       |
| Claude API (Console)      | Spend limits per workspace, a dedicated Claude Code workspace                                                                                                                                                                                                  |
| GitHub Copilot            | Since 2026-06-01, billed in GitHub AI Credits instead of premium requests. Budgets per user, organization, cost center, and enterprise. User budgets stop usage at the limit, but for other levels "stop usage when budget limit is reached" is off by default |
| Cursor                    | Team-level additional usage limit (fixed or per seat); Enterprise adds per-member limits. Enforcement has a delay                                                                                                                                              |

GitHub Copilot's default needs particular attention. If you create an organization budget without
turning on the stop option, charges continue past the limit.

## 6. Exceptions and periodic review

- If a tool that is not on the allow list is needed, approve it as a time-limited exception after
  security and legal review.
- Vendor terms, data-handling conditions, and plan structures change often. Review the allow list once
  a year and whenever a major terms change is announced.
- After an incident (leaked secret, merged code with a license violation, unintended agent action),
  check whether the policy needs to change.

## 7. Copy-paste asset: AI coding tool usage policy

Add the block below to the AI-generated-code section of your open source policy document (chapter 03
deliverable), or use it as a standalone policy. Replace the values in parentheses for your
organization.

```markdown
## AI Coding Tool Usage Policy

### Scope

- Applies to all AI coding tools and agents used to write, review, test, and document internal code.

### Tool approval

- Use only tools and plans on the allow list for work. The policy owner maintains the allow list.
- Approval criteria: input data is not used for training, vendor IP indemnification applies,
  admins can enforce settings, and the organization can manage usage records and cost limits.
- Do not use free personal accounts or unapproved extensions with internal code.
- MCP servers and plugins go on the allow list only after a separate adoption review.

### Data handling

- Never send secrets (keys, tokens, certificates, passwords) to any tool; block reading them in agent settings.
- Do not send customer data or personal information in principle. If needed, pseudonymize it and get security approval.
- Check sharing scope before connecting external documents and systems to an agent.

### Way of working and verification

- For work that changes behavior, agree on tests first, then hand over implementation.
- Do not delete or weaken a failing test to make it pass. Test changes need owner approval.
- AI-generated code goes through the same CI gates and review as human code. AI review does not replace human approval.
- Split PRs to a reviewable size (guideline: 400 lines).

### Copyright attribution and records

- Record the AI tool used in the commit message or PR description.
- When an AI draft was edited, record in the PR description the design and editing decisions made by a person.
- Review copyright notices with legal before releasing unmodified AI output externally.

### License risk control

- Check whether AI-suggested code resembles copyleft-licensed code (use a matching tool such as SCANOSS).
- Include AI-suggested dependencies in SBOM and vulnerability management like any open source component.
- Escalate suspected cases to legal.

### External open source contributions

- Check the upstream project's AI contribution policy before contributing.
- Do not submit AI-generated code or documents to projects that prohibit AI-generated contributions.
- Where a project requires disclosure or a dedicated tag, record it in the required format.

### Cost

- Set an organization monthly limit (amount) and per-team limits. Alert the tool administrator at 80% and 100%.
- Issue dedicated AI keys for CI and set a limit for each key.

### Accountability and training

- The person who approves the merge is responsible for AI-generated code.
- Include this policy in onboarding and yearly training and keep completion records.

### Exceptions and review

- Approve exceptions for a fixed period after security and legal review.
- The policy owner reviews the allow list and this policy once a year and whenever vendor terms change.
```

## 8. Standards linkage and sources

| Item on this page                 | Related requirement                                    |
| --------------------------------- | ------------------------------------------------------ |
| Policy document and communication | ISO/IEC 5230 §3.1.1, ISO/IEC 18974 §4.1.1              |
| Roles and competence              | ISO/IEC 5230 §3.1.2, ISO/IEC 18974 §4.1.2              |
| Training and awareness            | ISO/IEC 5230 §3.1.3, ISO/IEC 18974 §4.1.3              |
| AI policy                         | ISO/IEC 42001 §5.2. [AI System Compliance](./iso42001) |

- GitHub, [Updates to GitHub Copilot interaction data usage policy](https://github.blog/news-insights/company-news/updates-to-github-copilot-interaction-data-usage-policy/) (2026-03-25), [Upcoming changes to GitHub Copilot policies and billing](https://github.blog/changelog/2026-08-28-upcoming-changes-to-github-copilot-policies-and-billing/) (2026-08-28)
- GitHub Docs, [Excluding content from GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot), [Managing policies for Copilot in your organization](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies), [Budgets for usage-based billing](https://docs.github.com/en/copilot/concepts/billing/budgets-for-usage-based-billing)
- GitHub, [GitHub Copilot is moving to usage-based billing](https://github.blog/news-insights/github-copilot-is-moving-to-usage-based-billing/)
- Anthropic, [Claude Code data usage](https://code.claude.com/docs/en/data-usage), [Zero data retention](https://code.claude.com/docs/en/zero-data-retention), [Managed settings](https://code.claude.com/docs/en/managed-settings), [Manage costs](https://code.claude.com/docs/en/costs)
- OpenAI, [Enterprise privacy](https://openai.com/enterprise-privacy/), [Your data (API)](https://developers.openai.com/api/docs/guides/your-data)
- Cursor, [Data use](https://cursor.com/data-use), [Privacy and data governance](https://cursor.com/docs/enterprise/privacy-and-data-governance), [Spend limits](https://cursor.com/help/account-and-billing/spend-limits)
- Google Cloud, [Gemini for Google Cloud data governance](https://docs.cloud.google.com/gemini/docs/discover/data-governance)
- EU, [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) (Digital Omnibus on AI, amendment of Article 4)

All sources were checked on 2026-11-12.
