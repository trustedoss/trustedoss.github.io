[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![OpenChain](https://img.shields.io/badge/OpenChain-ISO%2FIEC%205230%20%26%2018974-blue)](https://www.openchainproject.org/conformance)
[![Site](https://img.shields.io/badge/Site-trustedoss.github.io-green)](https://trustedoss.github.io)

[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# Trusted OSS

**신뢰할 수 있는 오픈소스 공급망 관리** — ISO/IEC 5230 & 18974 실전 키트 + AI 코딩·DevSecOps 자동화 가이드

오픈소스 관리 경험이 전혀 없는 신규 담당자도 이 키트를 따라가면 ISO/IEC 5230과 18974 자체 인증 선언까지 완성할 수 있습니다. Agent가 회사 상황에 맞는 산출물을 자동 생성하며, 셀프스터디 방식으로 활용할 수 있습니다.

**[trustedoss.github.io](https://trustedoss.github.io)** 에서 웹 가이드와 브라우저 기반 도구를 바로 사용할 수 있습니다.

---

## 무엇을 제공하나요?

| 메뉴                                                      | 내용                                                                 |
| --------------------------------------------------------- | -------------------------------------------------------------------- |
| [체계구축](https://trustedoss.github.io/docs)             | ISO/IEC 5230 & 18974 기반 오픈소스 거버넌스 체계 구축 단계별 가이드  |
| [AI 코딩](https://trustedoss.github.io/ai-coding/intro)   | Claude Code·Cursor·Copilot 등 AI 코딩 도구의 오픈소스 정책 자동 준수 |
| [DevSecOps](https://trustedoss.github.io/devsecops/intro) | SAST·SCA·시크릿 탐지·컨테이너·IaC·DAST CI/CD 파이프라인 자동화       |
| [레퍼런스](https://trustedoss.github.io/reference/intro)  | 정책 템플릿·SBOM 샘플·자체 인증 체크리스트                           |

---

## 빠른 시작

### 웹사이트에서 바로 사용 (Claude Code 불필요)

브라우저에서 Anthropic API 키만으로 즉시 사용할 수 있는 도구를 제공합니다.

| 도구              | 설명                                        | 위치                                                                               |
| ----------------- | ------------------------------------------- | ---------------------------------------------------------------------------------- |
| Rules 생성기      | AI 코딩 도구용 오픈소스 정책 파일 자동 생성 | [AI코딩 → Rules 템플릿](https://trustedoss.github.io/ai-coding/rules-template)     |
| 워크플로우 생성기 | DevSecOps CI/CD 파이프라인 YAML 자동 생성   | [AI코딩 → Quick CI/CD](https://trustedoss.github.io/ai-coding/cicd-quick)          |
| SBOM 분석기       | SBOM 파일 업로드 → 취약점 대응 리포트       | [DevSecOps → SCA](https://trustedoss.github.io/devsecops/sca)                      |
| SAST 분석기       | Semgrep·CodeQL 결과 → 수정 가이드           | [DevSecOps → SAST](https://trustedoss.github.io/devsecops/sast)                    |
| 시크릿 분석기     | Gitleaks 결과 → 즉시 대응 절차              | [DevSecOps → 시크릿 탐지](https://trustedoss.github.io/devsecops/secret-detection) |
| IaC 수정기        | Checkov 결과 → 수정 코드 자동 생성          | [DevSecOps → IaC 보안](https://trustedoss.github.io/devsecops/iac-security)        |

### Claude Code로 실행

```bash
# 1. 저장소 클론
git clone https://github.com/trustedoss/trustedoss.github.io.git

# 2. 프로젝트 진입 및 Claude Code 실행
cd trustedoss.github.io && claude

# 3. 시작 안내 요청
# "어디서 시작해야 해?" 입력
```

---

## Agent 목록

### 체계구축 Agent (ISO/IEC 5230 & 18974)

| Agent                             | 역할                          | 실행 방법                                      |
| --------------------------------- | ----------------------------- | ---------------------------------------------- |
| `agents/02-organization-designer` | 조직·담당자 산출물 생성       | `cd agents/02-organization-designer && claude` |
| `agents/03-policy-generator`      | 오픈소스 정책 문서 생성       | `cd agents/03-policy-generator && claude`      |
| `agents/04-process-designer`      | 프로세스 문서 및 흐름도 생성  | `cd agents/04-process-designer && claude`      |
| `agents/05-sbom-guide`            | SBOM 생성 명령어 및 스크립트  | `cd agents/05-sbom-guide && claude`            |
| `agents/05-sbom-analyst`          | SBOM 라이선스 분석 리포트     | `cd agents/05-sbom-analyst && claude`          |
| `agents/05-sbom-management`       | SBOM 관리 계획 및 공유 템플릿 | `cd agents/05-sbom-management && claude`       |
| `agents/05-vulnerability-analyst` | 취약점 분석 리포트            | `cd agents/05-vulnerability-analyst && claude` |
| `agents/06-training-manager`      | 교육 커리큘럼 및 이수 추적    | `cd agents/06-training-manager && claude`      |
| `agents/07-conformance-preparer`  | 갭 분석 및 인증 선언문        | `cd agents/07-conformance-preparer && claude`  |

### AI 코딩·DevSecOps Agent (레벨 1 — 설정 파일 생성)

| Agent                    | 역할                                        | 실행 방법                             |
| ------------------------ | ------------------------------------------- | ------------------------------------- |
| `agents/ai-coding-setup` | 프로젝트 분석 후 맞춤형 Rules 파일 생성     | `cd agents/ai-coding-setup && claude` |
| `agents/devsecops-setup` | 프로젝트 분석 후 CI/CD 파이프라인 파일 생성 | `cd agents/devsecops-setup && claude` |

### AI 코딩·DevSecOps Agent (레벨 1 — 결과 분석)

| Agent                      | 역할                                 | 실행 방법                               |
| -------------------------- | ------------------------------------ | --------------------------------------- |
| `agents/sbom-vuln-analyst` | SBOM·grype 결과 → 취약점 대응 리포트 | `cd agents/sbom-vuln-analyst && claude` |
| `agents/sast-analyst`      | Semgrep·CodeQL 결과 → 수정 가이드    | `cd agents/sast-analyst && claude`      |
| `agents/secret-analyst`    | Gitleaks 결과 → 시크릿 대응 절차     | `cd agents/secret-analyst && claude`    |
| `agents/iac-fixer`         | Checkov 결과 → IaC 수정 코드 생성    | `cd agents/iac-fixer && claude`         |

### CI/CD 연동 자동화 Agent (레벨 2)

| Agent                                    | 역할                                     | 실행 방법                                             |
| ---------------------------------------- | ---------------------------------------- | ----------------------------------------------------- |
| `agents/level2-automation/pr-comment`    | PR 보안 분석 자동 코멘트 워크플로우 생성 | `cd agents/level2-automation/pr-comment && claude`    |
| `agents/level2-automation/issue-tracker` | 정기 스캔 이슈 자동 등록 워크플로우 생성 | `cd agents/level2-automation/issue-tracker && claude` |

---

## 저장소 구조

```
trustedoss/
├── docs/                    # 챕터별 가이드 문서 (체계구축)
├── agents/                  # 산출물 자동 생성 Agent
│   ├── 02-organization-designer/
│   ├── 03-policy-generator/
│   ├── ...
│   ├── ai-coding-setup/     # AI 코딩 Rules 파일 생성
│   ├── devsecops-setup/     # DevSecOps 파이프라인 파일 생성
│   ├── sbom-vuln-analyst/   # SBOM 취약점 분석
│   ├── sast-analyst/        # SAST 결과 분석
│   ├── secret-analyst/      # 시크릿 탐지 결과 분석
│   ├── iac-fixer/           # IaC 수정 코드 생성
│   └── level2-automation/   # CI/CD 연동 자동화
├── templates/               # 문서 템플릿
├── samples/                 # 실습용 샘플 프로젝트
├── output/                  # 생성된 산출물 (.gitignore)
├── .claude/                 # Claude Code 설정 및 skills
└── website/                 # 문서 웹사이트 소스 (Docusaurus)
```

---

## 체계구축 챕터 목록

| 챕터                     | 내용                                 | 셀프스터디 |
| ------------------------ | ------------------------------------ | ---------- |
| 00-overview              | 두 표준 개요 및 체크리스트 매핑      | 1시간      |
| 00-overview/supply-chain | 소프트웨어 공급망 보안 + SBOM 개념   | 1시간      |
| 01-setup                 | 환경 준비 (Docker, Git, Claude Code) | 30분       |
| 02-organization          | 조직 구성 및 담당자 지정             | 1시간      |
| 03-policy                | 오픈소스 정책 수립                   | 1시간      |
| 04-process               | 오픈소스 프로세스 설계               | 1시간      |
| 05-tools/sbom-generation | SBOM 생성                            | 1시간      |
| 05-tools/sbom-management | SBOM 관리 및 공유                    | 1시간      |
| 05-tools/vulnerability   | 취약점 분석 및 대응                  | 1시간      |
| 06-training              | 교육 체계 구축                       | 30분       |
| 07-conformance           | 자체 인증 선언                       | 30분       |

---

## 최종 산출물 목록

| 파일                                          | 설명                      | 충족 표준    |
| --------------------------------------------- | ------------------------- | ------------ |
| `output/organization/role-definition.md`      | 오픈소스 담당자 역할 정의 | 5230 + 18974 |
| `output/organization/raci-matrix.md`          | 역할·책임 매트릭스        | 5230 + 18974 |
| `output/organization/appointment-template.md` | 담당자 지정 공문 템플릿   | 5230 + 18974 |
| `output/policy/oss-policy.md`                 | 오픈소스 정책 문서        | 5230 + 18974 |
| `output/policy/license-allowlist.md`          | 허용 라이선스 목록        | 5230         |
| `output/process/usage-approval.md`            | 오픈소스 사용 승인 절차   | 5230         |
| `output/process/distribution-checklist.md`    | 배포 전 체크리스트        | 5230         |
| `output/process/vulnerability-response.md`    | 취약점 대응 절차          | 18974        |
| `output/process/process-diagram.md`           | 전체 프로세스 다이어그램  | 5230 + 18974 |
| `output/sbom/[project].cdx.json`              | SBOM (CycloneDX 형식)     | 5230 + 18974 |
| `output/sbom/license-report.md`               | 라이선스 분석 리포트      | 5230         |
| `output/sbom/copyleft-risk.md`                | Copyleft 위험 분석        | 5230         |
| `output/sbom/sbom-management-plan.md`         | SBOM 관리 계획            | 18974        |
| `output/vulnerability/cve-report.md`          | CVE 취약점 분석 리포트    | 18974        |
| `output/vulnerability/remediation-plan.md`    | 취약점 대응 계획          | 18974        |
| `output/training/curriculum.md`               | 교육 커리큘럼             | 5230 + 18974 |
| `output/conformance/gap-analysis.md`          | 갭 분석 보고서            | 5230 + 18974 |
| `output/conformance/declaration-draft.md`     | 자체 인증 선언문 초안     | 5230 + 18974 |

---

## 관련 링크

- [Trusted OSS 웹사이트](https://trustedoss.github.io)
- [OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/)
- [ISO/IEC 5230](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974](https://www.iso.org/standard/86450.html)
- [OpenChain 자체 인증 등록](https://www.openchainproject.org/conformance)

---

## 기여 방법

OpenChain KWG 커뮤니티와 연계하여 운영됩니다. PR과 이슈 제출을 환영합니다.

---

## 라이선스

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

<a id="english"></a>

# Trusted OSS — English

**Trusted Open Source Supply Chain Management** — ISO/IEC 5230 & 18974 Practical Kit + AI Coding & DevSecOps Automation Guide

Even those with no prior open source management experience can complete ISO/IEC 5230 and ISO/IEC 18974 self-certification declarations by following this kit. Agents automatically generate deliverables tailored to your organization, and the kit is designed for self-study.

The web guide and browser-based tools are available at **[trustedoss.github.io/en](https://trustedoss.github.io/en)**.

---

## What We Offer

| Section                                                      | Content                                                                                           |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [Build Your System](https://trustedoss.github.io/en/docs)    | Step-by-step guide to building an open source governance system based on ISO/IEC 5230 & 18974     |
| [AI Coding](https://trustedoss.github.io/en/ai-coding/intro) | Automated open source policy compliance for AI coding tools like Claude Code, Cursor, and Copilot |
| [DevSecOps](https://trustedoss.github.io/en/devsecops/intro) | CI/CD pipeline automation for SAST, SCA, secret detection, container, IaC, and DAST               |
| [Reference](https://trustedoss.github.io/en/reference/intro) | Policy templates, SBOM samples, and self-certification checklists                                 |

---

## Quick Start

### Use in the Browser (No Claude Code Required)

Browser-based tools are available with just an Anthropic API key.

| Tool               | Description                                                | Location                                                                                   |
| ------------------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Rules Generator    | Auto-generate open source policy files for AI coding tools | [AI Coding → Rules Template](https://trustedoss.github.io/en/ai-coding/rules-template)     |
| Workflow Generator | Auto-generate DevSecOps CI/CD pipeline YAML                | [AI Coding → Quick CI/CD](https://trustedoss.github.io/en/ai-coding/cicd-quick)            |
| SBOM Analyzer      | Upload SBOM file → vulnerability response report           | [DevSecOps → SCA](https://trustedoss.github.io/en/devsecops/sca)                           |
| SAST Analyzer      | Semgrep/CodeQL results → fix guide                         | [DevSecOps → SAST](https://trustedoss.github.io/en/devsecops/sast)                         |
| Secret Analyzer    | Gitleaks results → immediate response procedure            | [DevSecOps → Secret Detection](https://trustedoss.github.io/en/devsecops/secret-detection) |
| IaC Fixer          | Checkov results → auto-generate fix code                   | [DevSecOps → IaC Security](https://trustedoss.github.io/en/devsecops/iac-security)         |

### Run with Claude Code

```bash
# 1. Clone the repository
git clone https://github.com/trustedoss/trustedoss.github.io.git

# 2. Enter the project and launch Claude Code
cd trustedoss.github.io && claude

# 3. Ask for guidance (type in Korean)
# "어디서 시작해야 해?" (meaning: "Where should I start?")
```

---

## Agent List

### Compliance Agents (ISO/IEC 5230 & 18974)

| Agent                             | Role                                      | How to Run                                     |
| --------------------------------- | ----------------------------------------- | ---------------------------------------------- |
| `agents/02-organization-designer` | Generate organization & role deliverables | `cd agents/02-organization-designer && claude` |
| `agents/03-policy-generator`      | Generate open source policy document      | `cd agents/03-policy-generator && claude`      |
| `agents/04-process-designer`      | Generate process documents & flowcharts   | `cd agents/04-process-designer && claude`      |
| `agents/05-sbom-guide`            | Generate SBOM commands & scripts          | `cd agents/05-sbom-guide && claude`            |
| `agents/05-sbom-analyst`          | Generate SBOM license analysis report     | `cd agents/05-sbom-analyst && claude`          |
| `agents/05-sbom-management`       | Generate SBOM management plan & templates | `cd agents/05-sbom-management && claude`       |
| `agents/05-vulnerability-analyst` | Generate vulnerability analysis report    | `cd agents/05-vulnerability-analyst && claude` |
| `agents/06-training-manager`      | Generate training curriculum & tracking   | `cd agents/06-training-manager && claude`      |
| `agents/07-conformance-preparer`  | Generate gap analysis & declaration draft | `cd agents/07-conformance-preparer && claude`  |

### AI Coding & DevSecOps Agents (Level 1 — Config Generation)

| Agent                    | Role                                              | How to Run                            |
| ------------------------ | ------------------------------------------------- | ------------------------------------- |
| `agents/ai-coding-setup` | Analyze project and generate custom Rules files   | `cd agents/ai-coding-setup && claude` |
| `agents/devsecops-setup` | Analyze project and generate CI/CD pipeline files | `cd agents/devsecops-setup && claude` |

### AI Coding & DevSecOps Agents (Level 1 — Result Analysis)

| Agent                      | Role                                         | How to Run                              |
| -------------------------- | -------------------------------------------- | --------------------------------------- |
| `agents/sbom-vuln-analyst` | SBOM/grype results → vulnerability report    | `cd agents/sbom-vuln-analyst && claude` |
| `agents/sast-analyst`      | Semgrep/CodeQL results → fix guide           | `cd agents/sast-analyst && claude`      |
| `agents/secret-analyst`    | Gitleaks results → secret response procedure | `cd agents/secret-analyst && claude`    |
| `agents/iac-fixer`         | Checkov results → auto-generate IaC fix code | `cd agents/iac-fixer && claude`         |

### CI/CD Automation Agents (Level 2)

| Agent                                    | Role                                                | How to Run                                            |
| ---------------------------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| `agents/level2-automation/pr-comment`    | Generate PR security analysis auto-comment workflow | `cd agents/level2-automation/pr-comment && claude`    |
| `agents/level2-automation/issue-tracker` | Generate scheduled scan issue auto-filing workflow  | `cd agents/level2-automation/issue-tracker && claude` |

---

## Repository Structure

```
trustedoss/
├── docs/                    # Chapter-by-chapter guide documents
├── agents/                  # Deliverable auto-generation agents
│   ├── 02-organization-designer/
│   ├── 03-policy-generator/
│   ├── ...
│   ├── ai-coding-setup/     # AI coding Rules file generation
│   ├── devsecops-setup/     # DevSecOps pipeline file generation
│   ├── sbom-vuln-analyst/   # SBOM vulnerability analysis
│   ├── sast-analyst/        # SAST result analysis
│   ├── secret-analyst/      # Secret detection result analysis
│   ├── iac-fixer/           # IaC fix code generation
│   └── level2-automation/   # CI/CD integration automation
├── templates/               # Document templates
├── samples/                 # Sample projects for practice
├── output/                  # Generated deliverables (.gitignore)
├── .claude/                 # Claude Code configuration & skills
└── website/                 # Documentation website source (Docusaurus)
```

---

## Chapter List

| Chapter                  | Content                                        | Self-study |
| ------------------------ | ---------------------------------------------- | ---------- |
| 00-overview              | Overview of both standards & checklist mapping | 1 hour     |
| 00-overview/supply-chain | Software supply chain security + SBOM concepts | 1 hour     |
| 01-setup                 | Environment setup (Docker, Git, Claude Code)   | 30 min     |
| 02-organization          | Organizational structure & role assignment     | 1 hour     |
| 03-policy                | Open source policy establishment               | 1 hour     |
| 04-process               | Open source process design                     | 1 hour     |
| 05-tools/sbom-generation | SBOM generation                                | 1 hour     |
| 05-tools/sbom-management | SBOM management & sharing                      | 1 hour     |
| 05-tools/vulnerability   | Vulnerability analysis & response              | 1 hour     |
| 06-training              | Training program setup                         | 30 min     |
| 07-conformance           | Self-certification declaration                 | 30 min     |

---

## Deliverables

| File                                          | Description                                 | Standard     |
| --------------------------------------------- | ------------------------------------------- | ------------ |
| `output/organization/role-definition.md`      | Open source program manager role definition | 5230 + 18974 |
| `output/organization/raci-matrix.md`          | RACI responsibility matrix                  | 5230 + 18974 |
| `output/organization/appointment-template.md` | Role appointment letter template            | 5230 + 18974 |
| `output/policy/oss-policy.md`                 | Open source policy document                 | 5230 + 18974 |
| `output/policy/license-allowlist.md`          | Approved license list                       | 5230         |
| `output/process/usage-approval.md`            | Open source usage approval procedure        | 5230         |
| `output/process/distribution-checklist.md`    | Pre-distribution checklist                  | 5230         |
| `output/process/vulnerability-response.md`    | Vulnerability response procedure            | 18974        |
| `output/process/process-diagram.md`           | End-to-end process diagram                  | 5230 + 18974 |
| `output/sbom/[project].cdx.json`              | SBOM (CycloneDX format)                     | 5230 + 18974 |
| `output/sbom/license-report.md`               | License analysis report                     | 5230         |
| `output/sbom/copyleft-risk.md`                | Copyleft risk analysis                      | 5230         |
| `output/sbom/sbom-management-plan.md`         | SBOM management plan                        | 18974        |
| `output/vulnerability/cve-report.md`          | CVE vulnerability analysis report           | 18974        |
| `output/vulnerability/remediation-plan.md`    | Vulnerability remediation plan              | 18974        |
| `output/training/curriculum.md`               | Training curriculum                         | 5230 + 18974 |
| `output/conformance/gap-analysis.md`          | Gap analysis report                         | 5230 + 18974 |
| `output/conformance/declaration-draft.md`     | Self-certification declaration draft        | 5230 + 18974 |

---

## Links

- [Trusted OSS Website](https://trustedoss.github.io/en)
- [OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/)
- [ISO/IEC 5230](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974](https://www.iso.org/standard/86450.html)
- [OpenChain Self-Certification Registration](https://www.openchainproject.org/conformance)

---

## Contributing

This project is operated in collaboration with the OpenChain KWG community. Pull requests and issues are welcome.

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
