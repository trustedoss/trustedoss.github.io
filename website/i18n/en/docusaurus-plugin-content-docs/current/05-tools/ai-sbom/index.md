---
date: 2026-07-09
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: [G3B.1 extension — extending SBOM scope to AI components]'
self_study_time: 1 hour
sidebar_label: '5.4 AI SBOM (optional)'
---

# AI SBOM: Building an SBOM for Models and Datasets (Optional)

## 1. What you do in this chapter

This is an **optional chapter** for organizations that work with AI systems (developing or
operating models). You will generate a CycloneDX **ML-BOM** for one HuggingFace model and learn to
read its model license and dataset entries. Organizations without AI systems can skip this chapter
with no impact on the certification journey.

Prerequisites: complete [5.1 SBOM Generation](../sbom-generation/index.md) first so you are
comfortable with SBOM concepts and tooling. The hands-on work requires Docker and a network
connection.

## 2. Background

### Why a conventional SBOM is not enough

An SBOM that covers only code dependencies misses two components of an AI system.

- **Pre-trained models** — often under non-standardized custom licenses (commercial-use conditions,
  MAU thresholds, derivative-model obligations).
- **Training datasets** — CC-family open data licenses carry attribution and share-alike duties.

The extension that records both is the AI SBOM, and the de facto standard formats are
**CycloneDX ML-BOM** (rich model-card metadata) and **SPDX 3.0 AI Profile** (precise license
expression).

### Relationship to the standards

The SBOM requirements of ISO/IEC 5230 and 18974 (the G3B group) target "open source components of
the supplied software," so an AI SBOM is not itself mandatory. But if you ship models or datasets
as part of your product, they are open source components too — extending the same principle to
them is the point of this chapter. For background, see the
[AI SBOM section of SBOM Basics](../../00-overview/sbom-101.md) and
[AI System Compliance](/ai-coding/iso42001).

:::tip See a finished example first
To see what the result looks like before you start, skim the clause checklist and tool-run outputs
in the [KWG AI SBOM Compliance Guide](https://openchain-project.github.io/OpenChain-KWG/guide/ai-sbom_guide/).
It includes a cdxgen run that demonstrates the license-information gaps of AI components.
:::

## 3. Self-study path

:::info Self-study mode (about 1 hour)
The hands-on work requires a running Docker environment and a network connection.
:::

The hands-on tool is [BomLens](https://github.com/sktelecom/sbom-tools). Given a HuggingFace model
identifier, it produces a CycloneDX 1.7 ML-BOM, an open source notice, and a risk report — all
locally on Docker.

### Step 1 — Prepare BomLens

```bash
git clone https://github.com/sktelecom/sbom-tools.git
cd sbom-tools
docker pull ghcr.io/sktelecom/bomlens:latest
```

:::warning On macOS/Windows, run from a Docker file-sharing path
If you run from a path outside Docker Desktop file sharing (such as `/tmp`), the scan succeeds but
the deliverables are not copied back to the host (the tool prints a hint). Clone and run under your
home directory.
:::

### Step 2 — Scan a model to generate the ML-BOM

```bash
./scripts/scan-sbom.sh --project bert-base --version 1.0.0 \
  --model "google-bert/bert-base-uncased" --generate-only
```

- Put a HuggingFace model identifier in `--model` — replace it with the model you are reviewing.
- The dedicated model-scan image (`ghcr.io/sktelecom/bomlens-aibom`) is pulled automatically.
- Deliverables land in the `bert-base_1.0.0/` subfolder: `bert-base_1.0.0_bom.json` (CycloneDX 1.7
  ML-BOM), a notice, a risk report, a security report, and an NTIA minimum-elements conformance
  check. A model has no package CVEs, so a security report with zero findings is expected.

### Step 3 — Read the ML-BOM

Check the following in the generated `bom.json`.

- **Model license**: whether the model component's license is a custom license (e.g., Llama
  Community License) or a standard one (Apache-2.0, etc.), and compare it against your allowlist
  using the same [license review procedure as 5.1](../sbom-generation/index.md).
- **Model-card metadata**: entries carried over from the model card, such as intended use and
  limitations.
- **Information gaps**: an empty license or dataset entry is itself a finding — verify directly on
  the HuggingFace model card and record the supplement (the same situation the KWG guide
  demonstrates as license-gap evidence).

### Alternative tool — OWASP AIBOM Generator

The vendor-neutral alternative is the OWASP AIBOM Generator, which also targets HuggingFace
models. For installation and usage, see the
[KWG AI SBOM Guide — tools](https://openchain-project.github.io/OpenChain-KWG/guide/ai-sbom_guide/).

### Relationship to the code SBOM

The full picture of an AI service combines two SBOMs: the code-dependency SBOM
([5.1](../sbom-generation/index.md), syft/cdxgen) and this chapter's model ML-BOM. Keep both
documents per release unit and the retention/sharing procedures of
[5.2 SBOM Management](../sbom-management/index.md) apply as-is.

### Continuing to automation

You can regenerate the ML-BOM in CI whenever the model version changes: add the scan command above
to a workflow the same way the SBOM-generation job works in [DevSecOps — SCA](/devsecops/sca).

## 4. Completion checklist

- [ ] I can explain the difference between a conventional SBOM and an AI SBOM (model and dataset licenses)
- [ ] I generated an ML-BOM for one HuggingFace model
- [ ] I checked the model license in the ML-BOM against the allowlist
- [ ] Where license/dataset information was missing, I verified it on the model card

## 5. Next steps

- SBOM retention and supply chain sharing: [5.2 SBOM Management](../sbom-management/index.md)
- Vulnerability response (code dependencies): [5.3 Vulnerability Analysis and Response](../vulnerability/index.md)
- Compliance for AI systems overall: [AI System Compliance](/ai-coding/iso42001)
