[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# 운영 방식

Trusted OSS는 OpenChain KWG 커뮤니티에서 출발한 오픈소스 이니셔티브입니다. 누구나 기여할 수 있고,
운영은 아래 절차를 따릅니다.

---

## 구성 프로젝트

Trusted OSS는 이름 하나로 여러 프로젝트를 묶습니다. 아래 프로젝트 모두 이 문서의 절차를 따릅니다.

| 프로젝트              | 저장소                                                                           | 내용                                                    |
| --------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Trusted OSS 가이드    | [trustedoss.github.io](https://github.com/trustedoss/trustedoss.github.io)       | ISO/IEC 5230·18974 가이드와 브라우저 기반 도구          |
| Trusted OSS Agent     | [trustedoss-agents](https://github.com/trustedoss/trustedoss-agents)             | 인증 산출물을 생성하는 Claude Code 에이전트             |
| TRUSCA                | [trusca](https://github.com/trustedoss/trusca)                                   | 취약점·라이선스·SBOM 자체 호스팅 SCA 포털               |
| AI 코딩 Best Practice | [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) | 가이드의 AI 코딩 5단계 전략을 파일로 구현한 참조 저장소 |

AI 코딩 Best Practice 는 독립 제품이 아니라 가이드에 딸린 참조 구현입니다. 가이드의 서술과
저장소의 실제 파일이 어긋나면 저장소를 기준으로 삼고 가이드를 고칩니다.

문서에서 소개하는 외부 도구는 구성 프로젝트가 아닙니다. 예를 들어 BomLens는 SK텔레콤이 만든
별개의 오픈소스 도구이며, 가이드에서 대안으로 소개할 뿐입니다.

---

## 의사결정

작은 변경은 Pull Request로 바로 진행합니다. 방향이 갈릴 수 있는 변경은 이슈에서 먼저 논의하고,
일주일간 반대가 없으면 합의된 것으로 봅니다. 이견이 남으면 [메인테이너](./MAINTAINERS.md)가
논의 내용을 근거로 결정하고, 그 이유를 이슈에 남깁니다.

---

## 벤더 중립

Trusted OSS는 특정 상용 도구나 컨설팅을 배제하지도, 권유하지도 않습니다.

- 도구를 소개할 때는 기능, 라이선스, 유지 상태 같은 확인 가능한 사실에 근거합니다.
- 무료로 시작할 수 있는 경로를 함께 제시하되, 상용 도구가 더 맞는 상황이면 그렇게 적습니다.
- 메인테이너 개인이 속한 회사나 커뮤니티의 이해관계는 프로젝트 결정의 근거가 되지 않습니다.

---

## OpenChain KWG와의 관계

Trusted OSS는 KWG가 CC BY 4.0으로 공개한 가이드와 템플릿을 출처를 밝히고 활용합니다.
사본은 [`.claude/reference/kwg/`](./.claude/reference/kwg/README.md)에 두고 원저작자를 표기합니다.
프로젝트 운영은 이 문서의 절차를 따릅니다.

---

## 라이선스와 저작권

기여하신 내용의 저작권은 기여자 본인이 그대로 보유합니다. 프로젝트는 그 기여를 문서는
[CC BY 4.0](./LICENSE-docs), 코드는 [MIT](./LICENSE)로 배포합니다. 기여 시 DCO 사인오프가
필요하며, 방법은 [`CONTRIBUTING.md`](./CONTRIBUTING.md)에 있습니다.

---

<a id="english"></a>

# Governance

Trusted OSS is an open source initiative that grew out of the OpenChain KWG community. Anyone
can contribute, and the initiative runs on the process below.

---

## Projects

Trusted OSS is one name covering several projects. All of them follow the process in this
document.

| Project                 | Repository                                                                       | Content                                                                  |
| ----------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Trusted OSS Guide       | [trustedoss.github.io](https://github.com/trustedoss/trustedoss.github.io)       | ISO/IEC 5230 and 18974 guides plus browser-based tools                   |
| Trusted OSS Agent       | [trustedoss-agents](https://github.com/trustedoss/trustedoss-agents)             | Claude Code agents that generate conformance deliverables                |
| TRUSCA                  | [trusca](https://github.com/trustedoss/trusca)                                   | Self-hosted SCA portal for vulnerabilities, licenses, SBOM               |
| AI Coding Best Practice | [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) | Reference repository implementing the guide's 5-stage AI coding strategy |

AI Coding Best Practice is not a standalone product but a reference implementation that belongs
to the guide. When the guide and the files in that repository disagree, the repository is the
source of truth and the guide gets corrected.

External tools covered in the documentation are not part of the initiative. BomLens, for
example, is a separate open source tool built by SK Telecom that the guides present as an option.

---

## Decisions

Small changes go straight to a pull request. Changes that could go more than one way are
discussed in an issue first, and if nobody objects within a week the direction is considered
agreed. If disagreement remains, the [maintainers](./MAINTAINERS.md) decide based on the
discussion and record the reasoning in the issue.

---

## Vendor neutrality

Trusted OSS neither rules out nor promotes any commercial tool or consultancy.

- Tools are described from verifiable facts: capability, license, and maintenance status.
- We always show a path that costs nothing to start, and we say so plainly when a commercial
  tool is the better fit for a situation.
- The interests of a maintainer's employer or community are not grounds for a project decision.

---

## Relationship with OpenChain KWG

Trusted OSS builds on the guides and templates KWG publishes under CC BY 4.0, with attribution.
Copies live in [`.claude/reference/kwg/`](./.claude/reference/kwg/README.md) and carry the
original authorship. The project itself runs on the process in this document.

---

## License and copyright

You keep the copyright in what you contribute. The project distributes contributions as
[CC BY 4.0](./LICENSE-docs) for documentation and [MIT](./LICENSE) for code. Contributions
require a DCO sign-off; see [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how.
