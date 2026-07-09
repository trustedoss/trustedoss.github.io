---
id: legal-considerations
title: 'Legal Considerations for AI-Generated Code'
sidebar_label: 'Legal Considerations for AI-Generated Code'
---

# Legal Considerations for AI-Generated Code

While Rules and CI gates handle license and security risks, this page answers the three remaining
legal questions: who owns the copyright in AI-generated code, who defends you in an infringement
dispute, and where must AI use be disclosed.

:::note This is not legal advice
This page summarizes public sources as of 2026-07 for practical guidance. Consult your legal team
or an attorney for specific matters.
:::

## 1. Copyright attribution: how much did a human contribute?

The US Copyright Office set out its criteria in "Copyright and Artificial Intelligence" Part 2:
Copyrightability (finalized 2025-01). The US Supreme Court's denial of certiorari in Thaler v.
Perlmutter (2025) also settled the principle that an AI itself cannot be an author.

| Scenario                                                      | Human authorship | Copyright protection                                     |
| ------------------------------------------------------------- | ---------------- | -------------------------------------------------------- |
| Prompt only, output used as-is                                | Not recognized   | Not protectable — cannot be registered as a company work |
| AI draft with creative human modification and arrangement     | Recognized       | Protectable for the human contribution only              |
| AI as an assistive tool, human decides design and integration | Recognized       | Protection of the overall work is not defeated           |

There is no quantitative threshold such as a percentage of changes. The question is decided
case by case: did human creative contribution determine the expressive elements?

**Working rules** — leave records at development time so attribution can be proven later.

- State AI tool use in commit messages, e.g. `feat: implement order API handler (assisted by Claude Code)`
- When you modify an AI draft, note in the PR body which design and modification decisions a human made
- For code used verbatim from AI output, review the copyright notice with your legal team before external release

## 2. Vendor IP indemnification: who defends an infringement claim?

Major vendors offer IP indemnification — the vendor defends and covers third-party copyright
claims — to paid commercial-plan customers. Status as of 2026-07:

| Vendor                     | Program and basis                                                                      | Covered                                                           | Watch out                                                                                                                             |
| -------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Microsoft (GitHub Copilot) | Customer Copyright Commitment — GitHub Generative AI Services Terms (replaced 2026-03) | Copilot Business, Enterprise                                      | Personal Free and Pro excluded. The public-code-matching filter is no longer a coverage condition since 2026-04 (now optional)        |
| OpenAI                     | Copyright Shield (announcement name) — indemnity clause in the Business Terms          | ChatGPT Enterprise, API                                           | Free and personal plans excluded. Claims arising from customer modifications or combinations with third-party technology are excluded |
| Anthropic                  | Commercial Terms of Service Section K (Indemnification)                                | Paid commercial customers                                         | Limited to authorized use and its Output. Use the customer knew or should have known was infringing is excluded                       |
| Google Cloud               | Generative AI indemnification — dual coverage for training data and generated output   | Gemini for Google Cloud (including Gemini Code Assist) and others | Google updates the covered-services list frequently — always check the official list page                                             |

**Pre-adoption checklist**

- [ ] Is your plan actually covered? (personal free accounts are mostly excluded)
- [ ] Have you standardized internal settings to meet the coverage conditions (authorized use, filter settings, no content modification)?
- [ ] Terms change often — did you review the terms at adoption time and schedule an annual re-check?

## 3. AI-use disclosure: legal duty vs. best practice

Under both regulations, the disclosure duty falls on **operators who provide AI systems or
generative AI services**. Using AI coding tools for in-house development does not by itself
create a legal duty to label your code. The practices below are still recommended for
attribution evidence (section 1) and traceability.

| Regulation                         | Core duty                                                                                                           | Timing                                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| EU AI Act Article 50               | Providers must machine-readably mark synthetic content; deployers must disclose deepfakes and public-interest texts | Applies from 2026-08-02 (marking for systems already on the market deferred to 2026-12-02) |
| Korean AI Framework Act Article 31 | Notify that a generative AI product or service is provided and label its outputs                                    | In force since 2026-01-22 (grace period in effect)                                         |

**Best practices** — recommended even where not legally required.

- State AI tool use in internal commit messages and PRs (same as the working rules in section 1)
- For public repositories, add a one-line notice of AI tool use to README or CONTRIBUTING
- If you ship generative AI features to users in your product, you become directly subject to the
  regulations above — legal review is mandatory

## 4. Copy-paste asset: AI coding tool usage policy

Add the block below to the AI-generated-code section of your open source policy document
(chapter 03 deliverable), or use it as a standalone policy.

```markdown
## AI Coding Tool Usage Policy

### Approved tools

- Use only paid commercial plans covered by vendor IP indemnification.
  (e.g., GitHub Copilot Business, ChatGPT Enterprise, paid commercial Claude plans, Gemini Code Assist)
- Personal free accounts must not be used for company code.

### Copyright attribution records

- When AI output is used as-is, state it in the commit message.
- When an AI draft is modified, record the human design and modification decisions in the PR body.
- Review copyright notices with the legal team before releasing verbatim AI output externally.

### License risk controls

- Verify whether AI-suggested code resembles copyleft-licensed code (use matching tools such as SCANOSS).
- Treat AI-suggested dependencies like any open source: include them in SBOM and vulnerability management.
- Escalate suspicious cases to the legal team.
```

The full policy document structure is covered in [Chapter 3: Open Source Policy](/docs/policy),
and per-tool Rules application in the [Common Rules Template](./rules-template).

## 5. Standards linkage and sources

This page is based on §5 of the OpenChain KWG
[AI Compliance Guide](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/7-ai-compliance/)
(CC BY 4.0), re-verified against the primary sources below.

- US Copyright Office, [Copyright and Artificial Intelligence](https://www.copyright.gov/ai/) — Part 2 Copyrightability (2025-01)
- Microsoft, [Customer Copyright Commitment required mitigations](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/customer-copyright-commitment) / GitHub, [Generative AI Services Terms](https://github.com/customer-terms/github-generative-ai-services-terms)
- OpenAI, [Business Terms](https://openai.com/policies/business-terms/)
- Anthropic, [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) — Section K
- Google Cloud, [Generative AI indemnified services](https://cloud.google.com/terms/generative-ai-indemnified-services)
- EU AI Act, [Article 50](https://artificialintelligenceact.eu/article/50/) / Korea, [Framework Act on the Development of Artificial Intelligence and Establishment of Trust](https://www.law.go.kr/lsInfoP.do?lsiSeq=268543), Article 31

For linkage to the ISO/IEC standards, see [ISO Standards Linkage](./iso-mapping); for compliance
of AI systems themselves, see [AI System Compliance (ISO 42001)](./iso42001); for security controls
on the tools agents call, see [Agent and MCP Tool Governance](./agent-governance).
