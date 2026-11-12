# AI Coding Tool Usage Policy

**Company**: {Company name}
**Date**: YYYY-MM-DD
**Owner**: {Policy owner}
**Version**: 1.0

<!-- Optional template. 03-policy-generator does not generate this file. Organizations that use AI
coding tools add it to the "AI-generated code policy" section of their open source policy
(oss-policy.md) or adopt it as a standalone policy. Background for each item:
https://trustedoss.github.io/en/ai-coding/usage-policy -->

## Scope

- Applies to all AI coding tools and agents used to write, review, test, and document internal code.

## Tool approval

- Use only tools and plans on the allow list for work. {Policy owner} maintains the allow list.
- Approval criteria: input data is not used for training, vendor IP indemnification applies,
  admins can enforce settings, and the organization can manage usage records and cost limits.
- Do not use free personal accounts or unapproved extensions with internal code.
- MCP servers and plugins go on the allow list only after a separate adoption review.

## Data handling

- Never send secrets (keys, tokens, certificates, passwords) to any tool; block reading them in agent settings.
- Do not send customer data or personal information in principle. If needed, pseudonymize it and get security approval.
- Check sharing scope before connecting external documents and systems to an agent.

## Way of working and verification

- For work that changes behavior, agree on tests first, then hand over implementation.
- Do not delete or weaken a failing test to make it pass. Test changes need owner approval.
- AI-generated code goes through the same CI gates and review as human code. AI review does not replace human approval.
- Split PRs to a reviewable size (guideline: 400 lines).

## Copyright attribution and records

- Record the AI tool used in the commit message or PR description.
- When an AI draft was edited, record in the PR description the design and editing decisions made by a person.
- Review copyright notices with legal before releasing unmodified AI output externally.

## License risk control

- Check whether AI-suggested code resembles copyleft-licensed code (use a matching tool such as SCANOSS).
- Include AI-suggested dependencies in SBOM and vulnerability management like any open source component.
- Escalate suspected cases to legal.

## External open source contributions

- Check the upstream project's AI contribution policy before contributing.
- Do not submit AI-generated code or documents to projects that prohibit AI-generated contributions.
- Where a project requires disclosure or a dedicated tag, record it in the required format.

## Cost

- Set an organization monthly limit ({amount}) and per-team limits. Alert the tool administrator at 80% and 100%.
- Issue dedicated AI keys for CI and set a limit for each key.

## Accountability and training

- The person who approves the merge is responsible for AI-generated code.
- Include this policy in onboarding and yearly training and keep completion records.

## Exceptions and review

- Approve exceptions for a fixed period after security and legal review.
- The policy owner reviews the allow list and this policy once a year and whenever vendor terms change.
