---
id: legal-considerations
title: 'Legal Considerations for AI-Generated Code'
sidebar_label: 'Legal Considerations for AI-Generated Code'
sidebar_position: 8
---

# Legal Considerations for AI-Generated Code

While Rules and CI gates handle license and security risks, this page answers the three remaining
legal questions: who owns the copyright in AI-generated code, who defends you in an infringement
dispute, and where must AI use be disclosed. It also covers the upstream AI contribution policies
you must follow when contributing to external open source projects.

:::note This is not legal advice
This page summarizes public sources as of 2026-07 for practical guidance. Consult your legal team
or an attorney for specific matters.
:::

## 1. Copyright attribution: how much did a human contribute?

The US Copyright Office set out its criteria in "Copyright and Artificial Intelligence" Part 2:
Copyrightability (finalized 2025-01). The US Supreme Court's denial of certiorari in Thaler v.
Perlmutter (2026-03) also settled the principle that an AI itself cannot be an author.

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

The deployer's deepfake and public-interest text disclosure duty (Article 50(1) and (4)) applies from
2026-08-02 with no grace period, for new and existing systems alike. Only the provider's marking duty
(Article 50(2)) is deferred, and only for systems already on the market before 2026-08-02. This
relaxation came out of the Digital Omnibus on AI negotiation: provisional agreement on 2026-05-07,
European Parliament approval on 2026-06-16, Council adoption on 2026-06-29.

**Best practices** — recommended even where not legally required.

- State AI tool use in internal commit messages and PRs (same as the working rules in section 1)
- For public repositories, add a one-line notice of AI tool use to README or CONTRIBUTING
- If you ship generative AI features to users in your product, you become directly subject to the
  regulations above — legal review is mandatory

## 4. Upstream open source projects' AI contribution policies

The rules you apply to in-house code are not the rules that apply when you send a patch to an
external open source project. Major projects began writing down AI contribution policies in the
second half of 2025, and what they allow differs widely. The range runs from an outright ban to
"allowed if you tag it," so failing to check before you contribute can mean discarding a finished
patch.

| Project      | Policy                                                                                                                                                                                                   | Timing                                                  |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Linux kernel | When AI tools assist a contribution, add an `Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL]` tag. AI agents must not add `Signed-off-by`; only humans can certify the DCO                                  | Authored 2025-12-23, merged to mainline 2026-01-06      |
| OpenJDK      | Contributions must not include content generated by large language models, diffusion models, or similar systems. This covers source code plus text and images in PRs, e-mail, wiki pages, and JBS issues | Interim policy dated 2026-04-09                         |
| QEMU         | Declines any contribution believed to include or derive from AI-generated content. Exceptions must first be proposed on the qemu-devel mailing list                                                      | Introduced 2025-06, exception process clarified 2025-09 |
| MicroPython  | The PR template asks you to declare generative AI use by keeping one of two statements. If you used it, you keep the statement that a human checked the code and is responsible                          | Current PR template                                     |

Even the outright bans do not forbid using the tools. OpenJDK allows private use for comprehending,
debugging, and reviewing code, while drawing the line at contributing what the tools produce. Its
FAQ goes as far as saying that generating 100 lines and editing 10 of them yourself still cannot be
contributed.

Across the wider landscape, disclosure and human review outnumber bans. In a study of 1,000 popular
GitHub repositories (Hora and Robbes, 2026), 118 had AI policies, and 78% of those permitted
AI-assisted contributions. Still, 51% required disclosure of AI use and 74% required human
involvement in the contribution process.

**Working rules**

- Check the target project's `CONTRIBUTING` document and PR template for AI-related items first.
- Do not send AI-drafted work to projects that ban it. Explaining that a human edited part of it
  does not resolve the issue.
- Where a tag or declaration is required, write it in the commit trailer or PR body in exactly the
  required format.
- Even where no policy exists, disclosing AI use helps reviewers decide how closely to look.

## 5. Copy-paste asset: AI coding tool usage policy

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

### External open source contributions

- Before contributing upstream, check that project's AI contribution policy
  (CONTRIBUTING document, PR template, project policy page).
- Do not submit AI-generated code or documents to projects that ban AI-generated content.
- Where disclosure or a dedicated tag is required, record it in the required format.
```

The full policy document structure is covered in [Chapter 3: Open Source Policy](/docs/policy),
and per-tool Rules application in the [Common Rules Template](./rules-template).

## 6. Standards linkage and sources

This page is based on §5 of the OpenChain KWG
[AI Compliance Guide](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/7-ai-compliance/)
(CC BY 4.0), re-verified against the primary sources below.

- US Copyright Office, [Copyright and Artificial Intelligence](https://www.copyright.gov/ai/) — Part 2 Copyrightability (2025-01)
- Microsoft, [Customer Copyright Commitment required mitigations](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/customer-copyright-commitment) / GitHub, [Generative AI Services Terms](https://github.com/customer-terms/github-generative-ai-services-terms)
- OpenAI, [Business Terms](https://openai.com/policies/business-terms/)
- Anthropic, [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) — Section K
- Google Cloud, [Generative AI indemnified services](https://cloud.google.com/terms/generative-ai-indemnified-services)
- EU AI Act, [Article 50](https://artificialintelligenceact.eu/article/50/) / Korea, [Framework Act on the Development of Artificial Intelligence and Establishment of Trust](https://www.law.go.kr/lsInfoP.do?lsiSeq=268543), Article 31
- Digital Omnibus on AI negotiation timeline and Article 50 grace scope, [Gibson Dunn analysis](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- Linux kernel, [AI Coding Assistants](https://docs.kernel.org/process/coding-assistants.html) (Documentation/process/coding-assistants.rst)
- OpenJDK, [Interim Policy on Generative AI](https://openjdk.org/legal/ai) (2026-04-09)
- QEMU, [Code provenance](https://www.qemu.org/docs/master/devel/code-provenance.html), AI content policy section
- MicroPython, [Pull request template](https://github.com/micropython/micropython/blob/master/.github/pull_request_template.md)
- Andre Hora and Romain Robbes, [AI Policy, Disclosure, and Human in the Loop](https://arxiv.org/abs/2605.16706) (arXiv:2605.16706)

For linkage to the ISO/IEC standards, see [ISO Standards Linkage](./iso-mapping); for compliance
of AI systems themselves, see [AI System Compliance (ISO 42001)](./iso42001); for security controls
on the tools agents call, see [Agent and MCP Tool Governance](./agent-governance).
