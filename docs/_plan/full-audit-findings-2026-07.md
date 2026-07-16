# 전 영역 전수 감사 결과 (2026-07-16)

> 멀티 에이전트 전수 감사(finder 22유닛 + P0/P1 적대적 검증 160 에이전트) 결과.
> 총 252건: 확정 P0 24 / 확정 P1 110 / 미검증 P1 13(검증 상한 초과) / P2 101 / 반박 4.
> 실행 계획은 excellence-plan.md 참조. 형식: [심각도|감사유닛] 파일:행 — 요약 / 제안.

## 확정 P0

- [P0|docs-00] docs/00-overview/checklist-mapping.md:43 — 두 표준 비교 표에서 ISO/IEC 5230의 최신 버전을 '2.1 (2023)'으로 표기했으나 실제 제정 연도는 2020년입니다.
  제안: '2.1 (2020)'으로 수정합니다.
- [P0|docs-01-02] docs/01-setup/index.md:152 — 트러블슈팅의 `claude login` 명령이 존재하지 않아 따라 하면 실패합니다.
  제안: `claude auth login` 실행(또는 세션 내 `/login` 입력)으로 안내를 수정합니다.
- [P0|docs-05-sbom] docs/05-tools/sbom-management/index.md:151 — 주간 취약점 스캔 워크플로 예시가 GitHub Actions ubuntu-latest에 설치되어 있지 않은 syft와 grype를 직접 호출하고, checkout 직후 존재하지 않는 output/sbom/ 경로로 리다이렉트하므로 그대로 복사하면 실패한다.
  제안: sca.mdx와 동일하게 syft·grype 설치 스텝(또는 docker run 방식)과 `mkdir -p output/sbom`을 워크플로에 추가한다.
- [P0|docs-08] docs/08-developer-guide/method2-skill.md:36 — SKILL.md 예시를 감싼 4-백틱 markdown 펜스가 1단계 Node.js 블록 직후(36행)에서 조기 종료되어, 스킬 파일 예시가 잘리고 문서 끝의 '효과' 문장과 방법 3 이동 링크(105행)가 99~106행의 잉여 코드펜스 안에 갇혀 링크가 렌더링되지 않습니다.
  제안: SKILL.md 전체 내용(1~4단계, 보고 형식 포함)이 하나의 4-백틱 블록에 들어가도록 36행의 조기 종료 펜스를 제거하고 97행 부근에서 닫으며, 99·106행의 잉여 펜스를 삭제해 효과 문장과 다음 링크를 일반 본문으로 복원합니다.
- [P0|docs-08] docs/08-developer-guide/method4-cicd.md:51 — 금지 라이선스 검사에서 grep -E(확장 정규식)에 BRE식 이스케이프 파이프(\|) 패턴을 넘겨, GPL-3.0이 있어도 절대 매치되지 않아 라이선스 차단 게이트가 항상 통과합니다.
  제안: FORBIDDEN을 이스케이프 없는 ERE 대체 패턴(예: 'GPL-2\.0|GPL-3\.0|AGPL-3\.0|LGPL-2\.0')으로 바꾸거나 grep -F -f 금지목록파일 방식으로 교체합니다.
- [P0|docs-08] docs/08-developer-guide/method4-cicd.md:45 — license-check 잡의 run 단계가 syft CLI를 직접 호출하지만 러너에 syft가 설치되어 있지 않아 'syft: command not found'로 실패하고, 앞 단계 anchore/sbom-action이 만든 sbom.cdx.json은 어디에서도 사용되지 않습니다.
  제안: run 단계 전에 anchore/sbom-action/download-syft@v0으로 syft를 설치하거나, 생성해 둔 sbom.cdx.json을 jq로 파싱하도록 라이선스 추출을 바꿉니다.
- [P0|agents-core] agents/04-process-designer/.claude/settings.local.json:4 — 사용자명이 포함된 절대경로 권한 규칙이 git에 커밋되어 있어 다른 사용자 환경에서는 동작하지 않고 경로 규칙을 위반한다.
  제안: settings.local.json을 git 추적에서 제거(.gitignore 추가)하고, 필요한 권한은 상대 패턴으로 settings.json(커밋 가능)에 옮긴다.
- [P0|agents-06-07] agents/06-training-manager/CLAUDE.md:44 — 무료 교육 리소스에서 LFD106x를 '오픈소스 개발 기초'로 표기했으나 LFD106x는 Secure Software Development(Verification and More Specialized Topics) 과정으로, 오픈소스 개발 기초 과정은 LFD102다.
  제안: LFD106x를 LFD102로 바꾸거나, 코드를 유지하려면 설명을 '보안 소프트웨어 개발(검증 심화)'로 정정한다.
- [P0|agents-devtools] agents/secret-analyst/CLAUDE.md:19 — 입력 파일 생성 안내 명령 `gitleaks git . --report-format json` 은 `--report-path` 가 없어 리포트 파일을 만들지 않으므로, 따라 하면 agent에 넘길 결과 파일이 생성되지 않습니다.
  제안: `gitleaks git . --report-format json --report-path gitleaks-report.json` 으로 수정합니다.
- [P0|web-aicoding] website/ai-coding/cicd-quick.mdx:136 — GitLab CI 예시가 ubuntu:22.04 이미지에서 바로 curl을 실행하지만 해당 이미지에는 curl이 없어 파이프라인이 첫 줄에서 실패한다.
  제안: script 앞에 `apt-get update && apt-get install -y curl ca-certificates`를 추가하거나 curl이 포함된 이미지를 사용하도록 예시를 수정한다.
- [P0|web-devsecops] website/devsecops/iac-security.mdx:174 — CKV_AWS_25를 'SSH 포트 전체 개방 금지'로 설명하지만 실제 CKV_AWS_25는 RDP(3389) 포트 개방 검사이고 SSH(22)는 CKV_AWS_24입니다.
  제안: SSH 검사는 CKV_AWS_24로 바꾸거나 설명을 RDP로 수정합니다.
- [P0|web-devsecops] website/devsecops/iac-security.mdx:177 — CKV_K8S_35를 '지원 종료 API 버전 사용 금지'로 설명하지만 실제 CKV_K8S_35는 '시크릿을 환경변수 대신 파일로 사용' 검사입니다.
  제안: 항목 설명을 실제 검사 내용으로 고치거나 올바른 검사 ID로 교체합니다.
- [P0|web-devsecops] website/devsecops/sca.mdx:96 — GitLab CI 예시가 ubuntu:22.04 이미지에서 curl을 실행하지만 ubuntu 기본 이미지에는 curl이 없어 잡이 즉시 실패합니다.
  제안: script 앞에 'apt-get update && apt-get install -y curl ca-certificates'를 추가하거나 curl이 포함된 이미지를 사용합니다.
- [P0|web-devsecops] website/devsecops/pipeline-design.md:194 — GitLab 통합 파이프라인의 sca 잡도 ubuntu:22.04에서 curl을 호출해 sca.mdx와 동일하게 실패합니다.
  제안: curl 설치 단계를 추가하거나 curl 포함 이미지로 교체합니다.
- [P0|web-devsecops] website/devsecops/pipeline-design.md:218 — GitLab container-security 잡이 aquasec/trivy 이미지 안에서 docker build를 실행하는데, 이 이미지에는 docker CLI가 없고 dind 서비스도 선언돼 있지 않아 실패합니다.
  제안: dind 서비스 선언과 docker CLI가 있는 이미지(또는 별도 빌드 잡 분리) 구성으로 수정합니다.
- [P0|web-devsecops] website/devsecops/pipeline-design.md:228 — GitLab dast 잡이 zaproxy 이미지 안에서 docker compose up을 실행하는데, 해당 이미지에는 docker/compose가 없고 dind 서비스도 없어 실패합니다.
  제안: 앱 기동을 services: 또는 별도 잡/environment로 분리하고 zap-baseline.py는 접근 가능한 URL만 대상으로 하도록 구성합니다.
- [P0|web-devsecops] website/devsecops/container-security.md:117 — GitLab CI 예시가 aquasec/trivy 이미지에서 docker build를 실행하지만 trivy 이미지에는 docker CLI가 없어 실패하고, DOCKER_HOST가 TLS 포트(2376)인데 TLS 인증서 설정이 없습니다.
  제안: docker CLI가 있는 이미지에서 빌드하는 잡과 trivy 스캔 잡을 분리하거나, docker 설치·DOCKER_TLS_CERTDIR 설정을 추가합니다.
- [P0|web-devsecops] website/devsecops/secret-detection.mdx:75 — GitLab CI의 'gitleaks git . --source .' 명령은 v8.19+에서 제거된 --source 플래그를 새 git 서브커맨드(위치 인자 방식)와 섞어 써서 unknown flag 오류로 실패합니다.
  제안: 'gitleaks git . --config .gitleaks.toml --exit-code 1'처럼 --source를 제거합니다.
- [P0|web-reference] website/reference/samples/conformance.md:33 — 갭 분석 요약·소계의 18974 집계(충족 17 / 부분충족 8)가 같은 페이지 표의 실제 집계(충족 18 / 부분충족 7)와 다릅니다.
  제안: 표 기준으로 요약·소계를 ✅ 18개 / 🔶 7개로 고치고, 원본 output-sample 갭 분석도 함께 수정합니다.
- [P0|web-design] website/docusaurus.config.ts:98 — docs preset의 editUrl이 문자열 베이스라서 모든 문서의 '이 페이지 편집' 링크가 `edit/main/../docs/...` 형태로 생성되어 404가 됩니다.
  제안: editUrl을 함수형(`({docPath}) => \`https://github.com/trustedoss/trustedoss.github.io/edit/main/docs/${docPath}\``)으로 바꿔 올바른 저장소 경로를 생성합니다.
- [P0|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/vulnerability/tools-setup.md:103 — 트러블슈팅 표의 진단 명령이 번역 과정에서 깨져 `curl -I https://Check connection with api.osv.dev` 라는 실행 불가능한 문자열이 됐다.
  제안: 명령을 `curl -I https://api.osv.dev`로 복원하고 'to check connectivity' 설명은 코드 스팬 밖으로 뺀다.
- [P0|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/sbom.md:8 — 본문 첫 줄의 챕터 링크가 기계번역 과정에서 마크다운 문법이 쪼개져 하이퍼링크로 렌더되지 않고 원시 텍스트로 노출된다.
  제안: "[05 Tools Chapter](/docs/tools/sbom-generation)" 형태로 링크 문법을 복원한다.
- [P0|templates] output-sample/organization/role-definition.md:38 — 가상 기업 '테크유니콘' 샘플 산출물 전반에 실제 기업 SK텔레콤의 도메인(opensource@sktelecom.com, security@sktelecom.com, https://www.sktelecom.com)이 연락처로 기재되어 있다.
  제안: 샘플 전체의 sktelecom.com을 가상 도메인(예: opensource@techunicorn.example)으로 일괄 교체하고 update-reference-samples로 공개 페이지를 재생성한다.
- [P0|samples] samples/nodejs-unlicensed/README.md:22 — 샘플의 핵심 전제가 사실과 다릅니다 — nightmare@3.0.2 패키지는 실제로 MIT 라이선스이므로 '라이선스 미명시(UNLICENSED)' 실습 결과가 재현되지 않습니다.
  제안: 실제로 license 필드가 없는 패키지(또는 저장소 내 로컬 path 의존성으로 license 없는 가짜 패키지)로 교체하거나, 프로젝트 자체 package.json의 license 누락(NOASSERTION)만을 학습 포인트로 삼도록 샘플과 README·index.js를 재구성해야 합니다.

## 확정 P1

- [P1|docs-00] docs/00-overview/checklist-mapping.md:579 — 요약 통계의 '두 표준 공통 항목 수 11'이 실제 [공통] 태그 개수(12개)와 맞지 않습니다.
  제안: 공통 항목 수를 12로 고치고, 이에 연동되는 '약 35% 절약' 문구(12/31≈39%)와 index.md의 공통 항목 개수도 함께 갱신합니다.
- [P1|docs-00] docs/00-overview/checklist-mapping.md:602 — 다음 단계의 에이전트 실행 순서가 '취약점 분석(6) → SBOM 관리 계획(7)'로 되어 있어, 취약점 분석 에이전트의 전제 조건과 모순됩니다.
  제안: 6번과 7번 순서를 바꿔 'SBOM 관리 계획 → 취약점 분석'으로 수정합니다.
- [P1|docs-00] docs/00-overview/checklist-mapping.md:178 — G1.7, G3S.5, G3S.6, G4.5의 '담당 Agent'가 해당 에이전트의 충족 체크리스트 선언과 불일치합니다.
  제안: 매핑의 담당 Agent 필드와 각 agent CLAUDE.md의 충족 체크리스트 선언을 양방향으로 동기화합니다(G3L.6처럼 복수 기재 허용).
- [P1|docs-00] docs/00-overview/index.md:27 — '23개 산출물' 주장과 산출물 표가 실제 필수 산출물(24개)과 맞지 않습니다. 프로세스 행에서 필수 산출물 inquiry-response.md가 빠져 있습니다.
  제안: 프로세스 행에 inquiry-response.md를 추가하고 총 개수를 24개로 수정합니다.
- [P1|docs-00] docs/00-overview/index.md:129 — 완료 확인 체크리스트의 '공통 항목 10개'가 같은 문서 108행의 '공통 항목이 11개'와 모순되며, 매핑 문서의 실제 태그 개수(12개)와도 다릅니다.
  제안: checklist-mapping.md의 확정 수치(12개)로 두 곳을 통일합니다.
- [P1|docs-00] docs/00-overview/agents.md:23 — 4 프로세스 에이전트의 생성 산출물 목록에서 항상 생성되는 process-diagram.md가 누락되었습니다.
  제안: 표의 4 프로세스 행에 process-diagram을 추가합니다.
- [P1|docs-00] docs/00-overview/sbom-101.md:95 — 포맷 비교 표의 '최신 버전 SPDX 2.3 / CycloneDX 1.5'가 낡은 정보이고, 같은 문서의 AI SBOM 섹션(SPDX 3.0, CycloneDX 1.6)과 모순됩니다.
  제안: 최신 버전 행을 SPDX 3.0(또는 3.0.1), CycloneDX 1.6으로 갱신하거나 '이 키트에서 사용하는 버전'으로 표현을 바꿉니다.
- [P1|docs-01-02] docs/02-organization/index.md:8 — frontmatter 충족 체크리스트가 G-ID만 나열해 STYLEGUIDE §5 형식(3.x.x/4.x.x)과 다른 챕터 관례에서 벗어납니다.
  제안: 다른 챕터처럼 'G1.3 (3.1.2)' 병기 또는 '[3.1.2, 3.2.1, 3.2.2]'/'[4.1.2, 4.2.1, 4.2.2]' 형식으로 통일합니다.
- [P1|docs-01-02] docs/02-organization/index.md:145 — 대화 예시의 질문 번호 표기가 '질문 1/5~5/5' 후 '질문 6/6'으로 총 개수와 모순됩니다.
  제안: 예시 라벨을 '질문 1/6'~'질문 6/6'으로 수정합니다.
- [P1|docs-01-02] docs/02-organization/index.md:222 — ISO/IEC 5230 표의 3.2.2 행에서 요구사항 라벨(역할·책임 매트릭스)과 자체인증 질문(미준수 검토·시정 프로세스)이 서로 다른 하위 항목을 가리킵니다.
  제안: 라벨에 맞춰 질문을 역할·담당자 문서화 여부를 묻는 문장으로 바꾸거나, 질문에 맞춰 라벨을 '미준수 검토·시정 절차'로 수정합니다.
- [P1|docs-01-02] docs/01-setup/index.md:140 — 일반 안내 문장에 마크다운 인용(>)을 사용해 프로젝트 규칙(인용 대신 admonition)을 위반합니다.
  제안: :::info 또는 :::tip admonition으로 변환합니다.
- [P1|docs-01-02] docs/02-organization/index.md:140 — details 내부의 agent 안내 메시지를 마크다운 인용(>)으로 표기해 인용 금지 규칙을 위반합니다.
  제안: agent 출력 예시이므로 코드펜스(```text)로 감싸는 형태로 변환합니다.
- [P1|docs-03-04] docs/04-process/index.md:322 — contribution-process.md·project-publication-process.md 생성 조건이 문서 내에서 모순됩니다: 예상 결과물 표는 Q5/Q6 '예' 시에만 생성이라 하고, 완료 확인 체크리스트는 계획 여부와 무관하게 생성됨을 요구합니다.
  제안: 정본을 하나로 정하세요: agent가 '아니오' 답변 시에도 선언적 문서를 생성하도록 스펙·표를 바꾸거나, 체크리스트를 '기여/공개 계획이 있는 경우' 조건부로 수정.
- [P1|docs-03-04] docs/04-process/index.md:180 — '#### 3-6. 외부 문의 대응 프로세스'가 '### CI/CD 통합 포인트' 섹션 뒤에 배치되어 핵심 프로세스 6가지(3-1~3-5) 그룹에서 분리되고, 헤딩 계층상 CI/CD 통합 포인트의 하위 항목으로 렌더링됩니다.
  제안: 3-6을 3-5 바로 뒤로 옮기고 CI/CD 통합 포인트를 그 뒤에 배치.
- [P1|docs-03-04] docs/04-process/index.md:100 — onot을 'SBOM(SPDX 문서)을 입력받아' 고지문을 생성한다고 서술했으나, onot은 SPDX 외에 CycloneDX(JSON/XML)와 Excel도 입력으로 지원합니다.
  제안: 'SBOM(SPDX·CycloneDX 문서)을 입력받아'로 수정해 앞 단계 CycloneDX 산출물이 그대로 쓰임을 명확히.
- [P1|docs-03-04] docs/03-policy/index.md:218 — `open output/policy/oss-policy.md` (228행 `open .../license-allowlist.md` 포함)는 macOS 전용 명령이라 Linux·Windows 독자는 따라 하면 실패하며, 다른 챕터에서는 쓰지 않는 방식입니다.
  제안: `cat` 또는 '편집기로 output/policy/oss-policy.md 를 엽니다' 같은 OS 중립 안내로 교체.
- [P1|docs-05-sbom] docs/05-tools/sbom-management/index.md:232 — ISO/IEC 18974 4.3.1의 자체인증 체크리스트 영문 문구가 sbom-generation 챕터와 서로 다르게 인용되어, 같은 조항에 두 가지 '공식' 질문이 존재하는 것처럼 보인다.
  제안: 두 챕터의 4.3.1 체크리스트 문구를 정본 스펙 기준 단일 문구로 통일한다.
- [P1|docs-05-sbom] docs/05-tools/sbom-generation/index.md:221 — 생성되는 SBOM 파일명이 문서 내에서 sbom.cdx.json과 [project].cdx.json으로 혼용되어 독자가 산출물 확인 시 혼란을 겪는다.
  제안: agent 정본 규칙인 [project].cdx.json으로 문서 전체 파일명을 통일한다.
- [P1|docs-05-sbom] docs/05-tools/sbom-generation/docker-cicd.md:90 — 샘플 프로젝트가 '두 가지 제공된다'고 쓰고 2개만 나열했으나 실제 samples/에는 3개가 있고 상위 index.md도 3개를 안내해 서로 어긋난다.
  제안: nodejs-unlicensed를 추가해 3개로 맞추고 문장을 '제공됩니다'로 고친다.
- [P1|docs-05-vuln-ai] docs/05-tools/vulnerability/index.md:194 — 본문 충족 표는 ISO/IEC 18974 4.1.5와 4.3.2 두 항목을 충족한다고 안내하지만 frontmatter 충족 체크리스트에는 4.3.2만 있어 두 곳이 불일치한다.
  제안: frontmatter에 4.1.5를 추가하거나 본문 표에서 4.1.5를 제거해 두 곳을 일치시키고, 4.1.5를 유지한다면 스펙 명칭(표준 관행 구현)과 정합하게 표기한다.
- [P1|docs-05-vuln-ai] docs/05-tools/vulnerability/index.md:41 — '두 가지 도구를 사용합니다'라고 쓰고 바로 아래 표에는 도구 3개(OSV, Dependency Track, NVD)가 나열되어 숫자가 맞지 않는다.
  제안: NVD를 표에서 분리해 참조 데이터로 별도 문장 처리하거나, 본문을 '도구 두 가지와 참조 데이터베이스 하나'로 고쳐 숫자를 일치시킨다.
- [P1|docs-05-vuln-ai] docs/05-tools/vulnerability/index.md:29 — 프로젝트 규칙이 금지하는 마크다운 인용(>)을 장식용 인용문에 사용했고, 인용문 안에서 존댓말과 반말이 섞여 있다.
  제안: 인용 블록을 admonition(:::note 등)이나 평문으로 바꾸고 문장 종결을 존댓말로 통일한다.
- [P1|docs-05-vuln-ai] docs/05-tools/vulnerability/tools-setup.md:10 — 권장 순서 안내에 금지된 마크다운 인용(>)을 사용했다.
  제안: :::tip 권장 순서 형태의 admonition으로 바꾼다 (index.md 49행과 중복 안내이므로 문장 통일도 함께 검토).
- [P1|docs-06-07] docs/06-training/index.md:174 — :::tip 예상 결과 블록(158행 시작)의 닫는 펜스가 blockquote 안("> :::")에 들어가 admonition이 닫히지 않고 이후 렌더링이 깨진다.
  제안: 173행 인용을 평문으로 바꾸고 :::를 독립된 행으로 분리한다.
- [P1|docs-06-07] docs/07-conformance/index.md:149 — §6의 항목 수(공통 10개, 5230 전용 6개, 18974 전용 9개 = 총 25개)가 정본 매핑 문서의 수치(공통 11개, 5230 20개, 18974 23개, 전체 31개)와 모순된다.
  제안: checklist-mapping.md 요약 통계 기준(공통 11, 5230 전용 9, 18974 전용 12)으로 수치를 통일한다.
- [P1|docs-06-07] docs/06-training/index.md:5 — front matter 충족 체크리스트에 G1.7이 빠져 있다 — 정본 매핑과 validate-checklist 모두 교육 산출물(completion-tracker.md)을 G1.7(§3.1.3/§4.1.3)에 배정하는데, 어느 챕터도 G1.7을 선언하지 않는다.
  제안: 06 front matter와 본문 충족 표에 G1.7 (5230 3.1.3 / 18974 4.1.3)을 추가한다.
- [P1|docs-06-07] docs/07-conformance/index.md:87 — validate-checklist가 초기 인증 시 부분충족으로 처리하는 시간 기반 항목 3개(18974 §4.1.2.5, §4.1.2.6, §4.1.4.3) 중 §4.1.4.3만 설명하고 나머지 둘의 처리 방법이 누락됐다.
  제안: §4에 나머지 두 항목의 초기 인증 처리 방법(gap-analysis.md 검토 주기 기록, role-definition.md 담당자 명시)을 함께 안내한다.
- [P1|docs-08] docs/08-developer-guide/method2-skill.md:9 — 도입 admonition이 '한 번 정의하면 모든 프로젝트에서 /oss-policy-check으로 즉시 호출할 수 있습니다'라고 안내하지만, 문서가 만들게 하는 것은 프로젝트 로컬 .claude/skills/ 스킬이라 해당 프로젝트에서만 호출됩니다.
  제안: 문구를 '이 프로젝트 어디서나 호출'로 고치거나, 모든 프로젝트에서 쓰려면 ~/.claude/skills/에 두라는 스코프 구분 안내를 추가합니다.
- [P1|agents-core] agents/03-policy-generator/.claude/settings.local.json:1 — settings.local.json이 git에 커밋되어 프로젝트 규칙('로컬 전용, 커밋 금지')을 위반한다.
  제안: 추적 해제 후 공용으로 필요한 권한만 settings.json으로 이전한다.
- [P1|agents-core] agents/04-process-designer/CLAUDE.md:8 — "4~7개의 프로세스 문서가 생성된다"는 범위가 실제 최소 생성 수(5개)와 맞지 않는다.
  제안: "5~7개"로 수정한다.
- [P1|agents-core] agents/04-process-designer/CLAUDE.md:21 — 충족 체크리스트의 ISO/IEC 18974 섹션 매핑이 정본(docs/00-overview/checklist-mapping.md)과 어긋난다: G3S.1~G3S.4에 4.2.1을 붙이고, G2.2 행에서는 4.2.1을 누락했다.
  제안: G2.2 행의 18974 칸에 4.2.1을 넣고, G3S 행은 정본에 맞춰 4.1.5(필요 시 4.3.2 절차 부분)로 정리한다.
- [P1|agents-core] .claude/scripts/validate-output.py:34 — process 챕터 필수 파일 목록에 process-diagram.md가 없어, agent 선언·validate-chain.py·test-agent-specs.py와 검증 기준이 어긋난다.
  제안: CHAPTER_FILES['process']에 process-diagram.md를 추가해 세 검증 기준을 일치시킨다.
- [P1|agents-core] agents/02-organization-designer/CLAUDE.md:49 — agent 세션 cwd는 agents/02-organization-designer인데 output/·templates/ 경로가 어느 디렉토리 기준인지 명시가 없어, 상대 해석 시 산출물이 레포 루트 output/(체인·검증 스크립트의 기대 위치)이 아닌 agent 폴더 아래에 생성될 수 있다.
  제안: 각 agent CLAUDE.md에 '모든 경로는 레포 루트 기준이며 산출물은 ../../output/에 쓴다' 같은 기준 문장을 추가한다.
- [P1|agents-core] agents/02-organization-designer/CLAUDE.md:66 — '다음 단계'의 `cd agents/03-policy-generator`는 독자가 실제로 위치한 agents/02-organization-designer 디렉토리에서 실행하면 실패한다 (03·04의 다음 단계 블록도 동일 패턴).
  제안: `cd ../03-policy-generator` 형태로 바꾸거나 '레포 루트에서 실행' 전제를 명시한다.
- [P1|agents-05] agents/05-sbom-guide/.claude/settings.local.json:4 — settings.local.json이 git에 커밋돼 있고 내부에 사용자명 포함 절대경로(/Users/1112821/...)가 노출된다. 같은 문제가 스코프 내 4개 agent(05-sbom-analyst, 05-sbom-management, 05-vulnerability-analyst) 전부에 있다.
  제안: git rm --cached로 4개 파일의 추적을 해제하고, 공용으로 필요한 권한은 사용자명 없는 형태로 settings.json에 옮긴다.
- [P1|agents-05] agents/05-sbom-guide/CLAUDE.md:63 — Q2 선택지에 Go와 '기타'를 제시하면서 처리 방식 명령어 매핑 표에는 Java(Maven/Gradle)·Python·Node.js 4행만 있어 Go·기타 선택 시 분기가 정의되지 않는다.
  제안: 표에 Go(syft 등) 행과 '기타' 언어 처리 규칙(예: syft 범용 스캔으로 대응)을 추가하거나 선택지를 표와 일치시킨다.
- [P1|agents-05] agents/05-sbom-guide/CLAUDE.md:32 — 'Docker 없이 진행' 샘플 명령 블록과 '완료 후 확인'의 상대 경로(output/, output-sample/)가 레포 루트 기준인데, 이 agent의 실행 위치는 agents/05-sbom-guide여서 그대로 실행하면 잘못된 위치에 output/이 생기거나 cp가 실패한다.
  제안: 블록 앞에 '레포 루트에서 실행' 안내를 넣거나 경로를 ../../output-sample, ../../output 형태 또는 루트 기준임을 명시하는 문구로 고정한다.
- [P1|agents-06-07] agents/06-training-manager/CLAUDE.md:14 — 충족 체크리스트 표에 이 agent가 담당하는 G1.7(프로그램 참여자 인식 기록)이 누락되어 마스터 매핑·validate-checklist와 불일치한다.
  제안: 충족 체크리스트 표에 G1.7 (5230 3.1.3 / 18974 4.1.3, completion-tracker.md) 행을 추가한다.
- [P1|agents-06-07] agents/07-conformance-preparer/CLAUDE.md:15 — 충족 체크리스트 표가 G4.1~G4.4만 나열하고, 마스터 매핑과 템플릿이 이 agent 담당으로 지정한 G4.5(배포 소프트웨어 알려진 취약점 없음 확인)를 누락했다.
  제안: 충족 체크리스트 표에 G4.5 (18974 4.4.1·4.3.2) 행을 추가한다.
- [P1|agents-06-07] agents/07-conformance-preparer/CLAUDE.md:50 — '25개 체크리스트 항목 전체 대조'·'gap-analysis.md (25개 항목 대조)'·'모든 25개 항목이 충족되면'의 25개가 표준별 수치임을 밝히지 않아, 템플릿의 31개 G항목 및 '표준별 25개(총 50개)' 공식 표기와 충돌한다.
  제안: '표준별 25개 입증자료(둘 다 선택 시 총 50개)'로 통일하고, 갭 분석 대조 단위(G항목 31개)와 입증자료 수(표준별 25개)를 구분해 서술한다.
- [P1|agents-devtools] website/devsecops/monitoring.md:235 — issue-tracker agent의 산출물·기능 설명이 실제 agent 스펙과 전혀 일치하지 않습니다 (파일명 3개 모두 불일치, Dependabot 분석 기능은 agent에 없음).
  제안: monitoring.md의 설명·산출물 목록을 agent 스펙에 맞추거나, Dependabot 분석·정기 스캔 워크플로우를 실제로 생성하도록 agent 스펙을 확장해 양쪽을 일치시킵니다.
- [P1|agents-devtools] website/devsecops/iac-security.mdx:230 — agent 소개에 "Checkov / tfsec / Trivy IaC 결과 자동 감지"라고 쓰여 있지만 iac-fixer agent 스펙은 Checkov 결과 파일만 입력으로 받습니다.
  제안: 문서 문구를 "Checkov 결과 자동 파싱"으로 고치거나, agent 스펙에 tfsec·Trivy(trivy config) 결과 형식 지원을 추가해 일치시킵니다.
- [P1|agents-devtools] website/devsecops/strategy.md:84 — admonition은 agent들이 "전략 페이지의 1~4단계"를 구현한다고 안내하지만 바로 아래 표는 2단계~5단계를 나열해 단계 범위가 서로 맞지 않습니다.
  제안: "1~4단계"를 "2~5단계"로 수정합니다.
- [P1|web-aicoding] website/ai-coding/strategy.md:54 — 3단계 설명 본문은 '아래 6개 영역'이라고 하지만 바로 아래 표에는 5개 영역만 있다.
  제안: '6개'를 '5개'로 고치거나(의도가 6개라면 누락된 영역을 표에 추가) 본문과 표의 개수를 일치시킨다.
- [P1|web-aicoding] website/ai-coding/iso-mapping.md:28 — 매핑 표의 ISO/IEC 5230 조항 라벨이 표준의 실제 조항 제목과 다르다 — §3.3.2를 '라이선스 식별·분류', §3.4.1을 '컴플라이언스 검증'으로 표기.
  제안: 조항 라벨을 표준 제목대로 '라이선스 컴플라이언스'·'컴플라이언스 산출물'로 고치고, CI 라이선스 게이트의 매핑 대상 조항이 적절한지(예: §3.3.2) 재검토한다.
- [P1|web-aicoding] website/ai-coding/iso-mapping.md:34 — 마크다운 인용(>)을 사용해 프로젝트 공통 규칙(인용 대신 admonition/코드펜스)을 위반한다.
  제안: :::note 또는 :::info admonition으로 바꾼다.
- [P1|web-devsecops] website/devsecops/secret-detection.mdx:93 — .gitleaks.toml 예시는 v8.21+에서 도입된 [[allowlists]] 배열 문법을 쓰는데, 같은 페이지의 pre-commit 예시는 이를 지원하지 않는 v8.18.0으로 고정돼 있어 예외 규칙이 적용되지 않습니다.
  제안: pre-commit rev를 [[allowlists]]를 지원하는 버전(v8.21 이상)으로 올리거나 config 문법을 rev에 맞춥니다.
- [P1|web-devsecops] website/devsecops/iac-security.mdx:99 — GitLab CI 예시의 'checkov -d . ... --soft-fail false'에서 --soft-fail은 값을 받지 않는 불리언 플래그라서 'false'가 인식되지 않거나, 플래그가 파싱되면 의도(하드 실패)와 반대로 soft fail이 켜집니다.
  제안: --soft-fail false를 삭제합니다(하드 실패가 기본 동작).
- [P1|web-devsecops] website/devsecops/iac-security.mdx:175 — CKV_K8S_6은 PodSecurityPolicy 리소스 대상 검사라서 일반 Pod/Deployment 매니페스트의 루트 실행을 잡지 못합니다(해당 용도는 CKV_K8S_23).
  제안: CKV_K8S_23으로 교체합니다.
- [P1|web-devsecops] website/devsecops/sast.mdx:143 — 'CodeQL 설정' 섹션 하위의 '### GitLab CI' 소절 내용이 CodeQL이 아닌 Semgrep 잡이어서 독자가 CodeQL의 GitLab 설정으로 오해합니다.
  제안: GitLab CI 소절을 Semgrep 설정 섹션으로 옮기거나 CodeQL은 GitHub 전용임을 명시합니다.
- [P1|web-reference] website/reference/samples/sbom.md:239 — "CycloneDX → SPDX 변환 (cdxgen 사용)"이라는 주석의 명령이 실제로는 변환이 아니라 CycloneDX 생성 명령이며, cdxgen에는 CycloneDX↔SPDX 변환 기능이 없습니다.
  제안: 포맷 변환 도구를 cyclonedx-cli(convert) 등 실제 변환 도구로 교체하고 주석과 표를 실제 동작에 맞게 수정합니다.
- [P1|web-reference] website/reference/samples/sbom.md:419 — SPDX 검증 명령 `pyspdxtools validate <파일명>`이 spdx-tools의 문서화된 CLI 사용법(`pyspdxtools -i <파일>`)과 다르며 그대로 실행하면 인자 오류가 납니다.
  제안: `pyspdxtools -i <파일명>` 형식으로 수정하고 원본 템플릿도 함께 갱신합니다.
- [P1|web-reference] website/reference/samples/process.md:609 — 같은 회사 산출물 안에서 취약점 대응 기한이 충돌합니다: §2 표는 Critical 1주일·High 4주일(KWG 기준선)인데 흐름도(취약점 대응 프로세스)는 Critical 24시간·High 1주일을 확정 기한으로 표기합니다.
  제안: 흐름도의 기한을 §2 표(KWG 기준선)와 일치시키거나, 흐름도가 강화 SLA 예시임을 명시해 하나의 기준으로 통일합니다.
- [P1|web-reference] website/reference/samples/process.md:684 — "외부 문의 대응 절차" 섹션이 원본 산출물(output-sample/process/inquiry-response.md)과 내용이 크게 어긋나 있습니다(이메일 도메인, 문의 유형 정의, SLA 값이 모두 다름).
  제안: update-reference-samples 스킬로 이 섹션을 원본 기준으로 재생성해 동기화합니다.
- [P1|web-reference] website/reference/samples/organization.md:9 — "3개 산출물의 완성 예시"라고 안내하지만 페이지에는 role-definition·raci-matrix 2개만 있고 appointment-template(발령문)이 빠져 있습니다.
  제안: appointment-template.md 섹션을 페이지에 추가하거나 산출물 개수 안내를 실제 수록 내용과 일치시킵니다.
- [P1|web-reference] website/reference/samples/organization.md:63 — 가상 기업 '테크유니콘' 산출물 예시에 실제 SK텔레콤 도메인·자산(opensource@sktelecom.com, security@sktelecom.com, www.sktelecom.com, 'SKT-JIRA')이 쓰여 있어, 템플릿을 복사한 독자가 실제 회사로 문의하게 되고 페이지 간 도메인도 3종으로 혼재합니다.
  제안: 가상 기업용 도메인(techunicorn.com 또는 example.com) 하나로 전 산출물을 통일하고 실제 기업 도메인·시스템명을 제거합니다.
- [P1|web-reference] website/reference/samples/conformance.md:358 — 부분충족(🔶) 상태 항목까지 OpenChain 공식 제출 폼에서 "체크"하라고 안내하고, 선언문도 🔶 항목을 포함한 채 "25개 입증자료를 모두 충족함을 선언한다"고 적어 자체 인증 요건과 모순됩니다.
  제안: 부분충족 항목을 충족 완료로 전환한 뒤 제출하도록 절차 순서를 바꾸거나, '진행 중 상태로 체크' 안내를 삭제합니다.
- [P1|web-reference] website/reference/concepts/license-classification.md:47 — ISO/IEC 5230 3.3.2를 "라이선스 의무사항 식별·분류"로 설명했으나, 스펙에서 3.3.2는 '일반 라이선스 사용 사례 처리(라이선스 컴플라이언스)'이고 의무사항 식별·기록은 3.1.5입니다.
  제안: 매핑을 3.1.5(라이선스 의무)로 바꾸거나 3.3.2의 괄호 설명을 '라이선스 사용 사례 처리'로 정정합니다.
- [P1|web-reference] website/reference/samples/sbom.md:115 — 리포트 각주 두 곳에서 ISO/IEC 5230 §3.3.2를 "라이선스 식별"로 표기했으나 3.3.2는 라이선스 사용 사례 처리 절차이며 식별·검토는 3.1.5에 해당합니다.
  제안: 각주의 조항 설명을 스펙 명칭에 맞게 정정하거나 §3.1.5를 병기하고 원본 산출물도 함께 갱신합니다.
- [P1|web-reference] website/reference/intro.md:22 — 산출물 Best Practice 표의 SBOM 행이 실제 SBOM 페이지 구성과 어긋납니다: 페이지에 없는 sbom.cdx.json을 나열하고, 수록된 sbom-management-plan·sbom-sharing-template과 대응 agent(sbom-management)는 누락했습니다.
  제안: 표의 산출물 목록과 대응 Agent를 SBOM 페이지 실제 수록 내용에 맞게 갱신합니다.
- [P1|web-reference] website/reference/concepts/license-classification.md:10 — 프로젝트 규칙(마크다운 인용 `>` 대신 admonition/코드펜스 사용)에 어긋나는 blockquote가 reference 전반에 반복됩니다.
  제안: 정본 안내·바로가기·생성 agent 표기를 :::info 등 admonition으로 통일합니다.
- [P1|web-design] website/docusaurus.config.ts:92 — docs 플러그인에 exclude 설정이 없어 독자 비노출이어야 할 docs/ 하위 CLAUDE.md 14개가 /docs/CLAUDE 등 공개 페이지로 빌드·검색 인덱싱됩니다.
  제안: docs preset 옵션에 `exclude: ['**/CLAUDE.md']`를 추가해 내부 지침 파일을 빌드에서 제외합니다.
- [P1|web-design] website/docusaurus.config.ts:119 — gtag trackingID 'G-TRUSTEDOSS01'은 실제 GA4 측정 ID 형식이 아닌 플레이스홀더로 보여 방문 분석이 동작하지 않습니다.
  제안: 실제 발급받은 GA4 측정 ID로 교체하거나, 분석을 쓰지 않는다면 gtag 블록을 제거합니다.
- [P1|web-design] website/src/components/Home/Showcase/index.tsx:60 — 랜딩 Showcase의 적합성 선언문 미리보기가 ISO/IEC 5230 섹션 제목을 잘못 매핑합니다 — '3.3 역량 · 절차 확보'라고 표시하지만 역량(competence)은 3.1.2이고 3.3은 '오픈소스 콘텐츠 검토 및 승인'입니다.
  제안: 미리보기 항목을 실제 5230 목차(예: 3.1 프로그램 기반 / 3.2 관련 업무 지원 / 3.3 검토·승인)에 맞게 수정합니다.
- [P1|web-landing-ux] docs/00-overview/quick-start.md:44 — 실행 전 확인 admonition이 quick-start 문맥에 맞지 않아, 안내대로 새 터미널에서 실행하면 상대 경로 cd 명령이 실패한다.
  제안: quick-start에서는 admonition을 문맥에 맞게 조정하고 코드 블록에 `cd trustedoss-agents/agents/02-organization-designer`처럼 저장소 루트 기준 경로를 명시한다.
- [P1|web-landing-ux] website/src/components/Home/FinalCTA/index.tsx:24 — 랜딩 마지막 CTA가 "설치도, 비용도, 벤더 종속도 없습니다"라고 약속하지만 실제 여정은 Docker·Git·Claude Code 설치(01 환경 준비)와 Claude Code 사용 비용을 요구한다.
  제안: 무설치·무비용 주장을 데모 범위로 한정하거나 "가이드는 무료" 수준으로 표현을 낮춘다.
- [P1|web-landing-ux] docs/00-overview/index.md:129 — 완료 확인 체크리스트가 공통 항목을 "10개"라고 쓰는데, 같은 문서 본문(line 108)과 정본인 checklist-mapping.md 요약 통계는 모두 11개다.
  제안: line 129의 10개를 11개로 수정한다.
- [P1|web-landing-ux] docs/00-overview/quick-start.md:15 — 첫 진입 문단이 공식 명칭이 아닌 "OpenChain 2026"을 표준 이름처럼 사용한다.
  제안: "OpenChain(ISO/IEC 5230·18974)" 표기로 교체한다.
- [P1|web-landing-ux] docs/00-overview/quick-start.md:13 — 페이지가 "5분 빠른 시작"(front matter 소요시간 5분)을 약속하지만, 본문 2단계에 포함된 에이전트 실행만 해도 에이전트 스펙 기준 약 15분이 걸린다.
  제안: 5분 범위를 1단계(무설치 데모)로 한정해 명시하거나 2단계에 별도 예상 시간을 표기한다.
- [P1|web-landing-ux] website/src/pages/about.md:26 — 프로젝트 공통 규칙이 금지하는 마크다운 인용(>)을 출처 표기 예시에 사용한다.
  제안: :::info admonition 또는 평문으로 바꾼다.
- [P1|en-inventory] website/ai-coding/iso-mapping.md — website/ai-coding/iso-mapping.md의 영어 번역 파일이 website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/에 없어 영어 사이트에서 이 페이지가 한국어 원문으로 노출된다.
  제안: website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/iso-mapping.md 번역본을 추가한다.
- [P1|en-inventory] website/reference/glossary.md — website/reference/glossary.md의 영어 번역 파일이 website/i18n/en/docusaurus-plugin-content-docs-reference/current/에 없어 영어 사이트에서 용어집 페이지가 한국어 원문으로 노출된다.
  제안: website/i18n/en/docusaurus-plugin-content-docs-reference/current/glossary.md 번역본을 추가한다.
- [P1|en-inventory] website/i18n/en/docusaurus-plugin-content-docs/current/08-developer-guide/index.md:65 — 08장 개발자 가이드 영어 번역이 ko 원본 대비 43% 짧은 구버전 내용으로 남아 있다 (ko 208줄 vs en 118줄).
  제안: ko docs/08-developer-guide/index.md 최신 내용(특히 4절 방법별 상세 요약)을 en index.md에 반영해 재번역한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/supply-chain.md:160 — ko 원본의 '6. 내 조직의 공급망 위험 평가하기' 섹션(4가지 평가 축 표, 전이 의존 설명, 3단계 평가 절차) 전체가 en에 누락됐다.
  제안: ko 6절(위험 평가 틀)과 완료 체크리스트 5번째 항목을 번역해 en에 추가하고 이후 섹션 번호를 재정렬한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/index.md:32 — 빠른 시작의 git clone 대상이 ko 정본(trustedoss-agents)과 다른 낡은 저장소(trustedoss.github.io)를 가리켜 en 문서 간에도 서로 모순된다.
  제안: ko 정본에 맞춰 trustedoss-agents 저장소 URL과 디렉토리명으로 갱신한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/03-policy/index.md:103 — 실습 전 확인 admonition의 클론 대상 저장소가 ko 정본과 달리 낡은 trustedoss.github.io URL로 남아 있다.
  제안: ko와 동일하게 trustedoss-agents로 교체한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/sbom-generation/docker-cicd.md:8 — 문서 전반이 교정되지 않은 기계번역으로, 문장이 쉼표·마침표로 뒤엉켜 독해가 어렵다.
  제안: 파일 전체를 ko 원본 기준으로 재번역·교정한다 (같은 챕터의 sbom-generation/index.md 수준의 품질로).
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/vulnerability/tools-setup.md:8 — P0 명령 오류 외에도 문서 전반이 기계번역 상태로 문장이 붙거나 끊겨 있다.
  제안: 파일 전체를 재번역·교정한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/08-developer-guide/index.md:67 — ko 4절의 방법 1~4 핵심 요약(코드 예시 포함)과 '상황별 적용 조합 권장' 표가 en에 통째로 없고 링크 표만 남아 있다.
  제안: ko 최신본 기준으로 4절 요약·조합 표와 두 admonition을 번역해 추가한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/08-developer-guide/index.md:14 — 제목부터 본문까지 기계번역 잔재(콜론 뒤 공백 누락, 어순 붕괴)가 남아 독자를 혼란시킨다.
  제안: 제목·front matter title 포함 전체를 재번역·교정한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/04-process/index.md:6 — front matter의 ISO/IEC 18974 충족 목록에 ko 정본에서 제거된 4.3.2가 남아 있어 챕터의 표준 커버리지 주장(정합성)이 어긋난다.
  제안: en front matter를 ko와 동일하게 [4.1.5, 4.2.1]로 갱신한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/04-process/index.md:25 — en에만 낡은 '### Why you need processes' 섹션이 남아 있고, ko가 admonition으로 재구성한 용어집 tip과 KWG 참조 tip, Prerequisite 배너가 en에는 반영되지 않았다.
  제안: en 2절 도입부를 ko 최신 구조(Prerequisite + 두 tip admonition)로 동기화하고 낡은 소절을 제거한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/index.md:63 — ko에 있는 7단계 진행 추적 컴포넌트 <JourneyProgress />와 안내 문장이 en에 누락됐다.
  제안: 안내 문장을 번역하고 <JourneyProgress />를 같은 위치에 추가한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/index.md:14 — ko의 선행 조건 배너 <Prerequisite>(4. 오픈소스 프로세스 + Docker 환경)가 en에 누락됐다.
  제안: en에도 Prerequisite 배너를 추가하고, 같은 누락이 있는 02·03·04·06·07 챕터 en index에도 일괄 반영한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/intro.md:7 — H1이 "#Reference"로 #과 제목 사이 공백이 없어 헤딩으로 렌더되지 않고 본문에 '#Reference' 문자 그대로 노출된다.
  제안: "# Reference"로 공백을 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/intro.md:25 — en 레퍼런스 인트로가 구버전 그대로다: ko가 삭제한 "수록 예정(in preparation)" 섹션이 남아 있고, ko의 개념 심화·용어집·에이전트 선택 가이드·도구와 규제 섹션이 없으며, 산출물 표에서 SBOM·취약점 2개 행이 빠졌다.
  제안: ko 최신 intro.md 기준으로 en 페이지를 재번역한다.
- [P1|en-web] website/ai-coding/iso-mapping.md — ai-coding 사이드바에 노출되는 iso-mapping 문서의 en 번역 파일이 없어 영어 사이트에서 이 페이지가 한국어 원문으로 표시된다.
  제안: ko 원본을 번역해 en current/ 폴더에 iso-mapping.md를 추가한다.
- [P1|en-web] website/reference/glossary.md — reference 사이드바 두 번째 항목인 용어집(glossary)의 en 번역 파일이 없어 영어 사이트에서 한국어 원문으로 표시된다.
  제안: glossary.md를 번역해 en current/에 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-theme-classic/footer.json — footer 번역 키 2개가 누락되고 1개가 낡은 키라서 영어 사이트 푸터에 '오픈소스 관리'와 '기여 가이드'가 한국어로 노출된다.
  제안: "link.item.label.오픈소스 관리"와 "link.item.label.기여 가이드" 키를 추가하고 체계구축 키를 제거한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current.json — reference 사이드바 카테고리 번역 키가 실제 라벨과 불일치해 영어 사이트 사이드바에 '산출물 Best Practice'가 한국어로 노출된다.
  제안: 키를 "sidebar.reference.category.산출물 Best Practice"로 바꾼다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/sast.mdx:10 — ko devsecops 8개 페이지 전부에 추가된 ':::tip 아래 설정은 예시입니다 — 작동하는 전체 구현은 참조 저장소에' admonition(Best Practice 저장소 링크)이 en 8개 페이지 모두에서 빠져 있다.
  제안: 8개 en 페이지에 해당 tip admonition을 번역해 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/sast.mdx:171 — 브라우저 분석기 데모 개편이 en에 미반영: sast·sca·secret-detection·iac-security 4개 en 페이지에 '먼저 샘플로 미리보기'(sample-demo iframe)와 '내 결과로 실제 분석하기' 하위 섹션 및 Anthropic API 키 안내 :::info admonition(과금·전송 고지)이 없다.
  제안: 샘플 미리보기 iframe 섹션과 API 키·과금 고지 admonition을 en 4개(+cicd-quick) 페이지에 반영한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/rules-template.mdx:12 — en rules-template에 ko의 Anthropic API 키 안내 :::info, '이 템플릿 vs 개발자 가이드' :::note, 그리고 문서 마지막 '## 다음 단계' 섹션이 모두 빠져 있다.
  제안: 세 블록을 번역해 en 파일에 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-ai-coding/current/intro.md:9 — en ai-coding 인트로에 ko의 ':::note 선택 단계 — 개발팀이 있다면' admonition(체계구축 가이드와의 선후 관계 안내)이 빠져 있다.
  제안: 해당 note를 번역해 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/iso-mapping.md:8 — en 18974 매핑 페이지에 ko의 ':::note 표준 충족 매핑의 정본'(체크리스트 매핑이 정본이라는 안내)이 빠져 있어 정본 문서로의 연결이 끊긴다.
  제안: 해당 note를 번역해 추가한다.
- [P1|harness] .claude/scripts/verify.sh:129 — [5/12] 로컬 경로 노출 검사가 CLAUDE.md가 금지하는 Windows 경로(C:\Users\...)를 전혀 탐지하지 못하고, 검사 대상 확장자에서 _.py, _.js, _.mdx, _.tsx, \*.scss가 빠져 있다.
  제안: grep 패턴에 [Cc]:\\Users 계열을 추가하고 ls-files 확장자 목록에 py/js/mdx/tsx/scss를 포함한다.
- [P1|harness] .claude/scripts/verify.sh:155 — [6/12] 섹션 번호 검사가 '18974를 3.x.x로 표기'한 방향만 잡고, 반대 방향인 '5230을 4.x.x로 표기'한 혼용은 전혀 검사하지 않으며, 스캔 범위도 docs/·agents/뿐이라 templates/(18974 참조 파일 15개)·output-sample/·website/\*.md는 대상에서 빠진다.
  제안: 5230+4.x.x 역방향 패턴을 추가하고 스캔 범위에 templates/, output-sample/, website/ai-coding/, website/devsecops/를 포함한다.
- [P1|harness] .claude/scripts/verify.sh:39 — [2/12] 링크 검사 범위가 docs/·README.md·workshop/뿐이고 /로 시작하는 절대 경로 링크는 건너뛰는데, Docusaurus 빌드는 onBrokenLinks: 'warn'이라 website/ai-coding·devsecops·reference의 깨진 링크와 잘못된 /reference/... 절대 경로 링크가 어느 검사에서도 FAIL이 되지 않는다.
  제안: onBrokenLinks를 'throw'로 올리거나(빌드가 잡게), 링크 검사에 website md 스캔과 /reference/... 경로의 실제 파일 매칭을 추가한다.
- [P1|harness] .claude/scripts/validate-output.py:24 — CHAPTER_FILES 기대 목록이 validate-chain.py CHAIN_SPEC·output-sample 실물과 어긋난다: process/process-diagram.md, training/resources.md, conformance/declaration-draft.md, conformance/submission-guide.md 4개 파일이 빠져 있어 사용자의 output/에서 이 파일들이 누락돼도 verify.sh [9/12]가 PASS한다.
  제안: CHAPTER_FILES에 누락된 4개 파일을 추가해 CHAIN_SPEC과 단일 기준으로 맞춘다.
- [P1|harness] .claude/scripts/check-admonition.js:13 — PostToolUse 훅이 CLAUDE_TOOL_OUTPUT 환경변수에서 파일 경로를 읽지만 Claude Code 훅은 페이로드를 stdin JSON으로 전달하므로 이 변수는 항상 비어 있고, 훅은 매번 조용히 exit 0 하여 admonition 경고 기능이 동작하지 않는다.
  제안: stdin으로 들어오는 훅 JSON(tool_input.file_path)을 파싱하도록 check-admonition.js와 settings.json 인라인 훅을 함께 수정한다.
- [P1|harness] .claude/scripts/sync-kwg-reference.sh:28 — TARGET_DIR(.claude/reference/kwg)와 check-kwg-drift.py 호출 경로가 모두 cwd 기준 상대 경로라, 레포 루트가 아닌 곳에서 실행하면 엉뚱한 위치에 .claude/reference/kwg를 만들고 드리프트 검사는 'python3 없음'이라는 오해를 부르는 메시지와 함께 건너뛴다.
  제안: sync-output-samples.sh처럼 스크립트 위치 기준으로 ROOT를 계산해 모든 경로를 절대화한다.
- [P1|templates] templates/conformance/gap-analysis.md:25 — 갭 분석 템플릿은 G1.1~G4.5 31개 G항목 체크리스트 구조인데, 같은 산출물의 output-sample은 G항목 없이 표준별 ISO 조항 ID(3.x.x/4.x.x) 50행 구조로 되어 있어 정본 구조가 이원화되어 있다.
  제안: 둘 중 하나(G항목 31개 체계 권장)를 정본으로 정해 템플릿과 샘플의 표 구조를 통일한다.
- [P1|templates] templates/conformance/declaration-draft.md:39 — 자체 인증 선언문 템플릿의 충족 확인 표는 G항목(G1.1~G4.5) 기준인데 output-sample 선언문은 ISO 조항 ID 기준 표라서 같은 산출물의 두 표본이 서로 다른 체크리스트 체계를 쓴다.
  제안: gap-analysis와 함께 체크리스트 체계(G항목 또는 조항 ID)를 하나로 통일하고 제목·절 구성을 맞춘다.
- [P1|templates] templates/training/curriculum.md:36 — 교육 커리큘럼 템플릿은 법무/구매·보안 담당을 포함한 5개 직군 필수 과정(7절 구성)을 정의하지만, 06-training-manager 스펙과 output-sample은 개발자/관리자/운영·기타 3개 직군만 다루고 agent는 templates/training/을 참조 목록에 두지도 않아 템플릿이 표류 상태다.
  제안: 06 agent가 templates/training/을 참조하도록 명시하고, 템플릿 직군 구성을 agent 질문 체계(3직군 + 선택 직군)와 샘플 구조에 맞춰 재정렬한다.
- [P1|templates] output-sample/process/vulnerability-response.md:110 — 취약점 대응 절차 샘플에 CVD(조정된 취약점 공개) 절차 섹션이 없어, 템플릿(§8 CVD, 8.1~8.5)과 04-process-designer 스펙('CVD §8 포함' 상시 생성)이 모두 요구하는 내용이 빠진 구버전 구조다.
  제안: 샘플을 재생성해 CVD 절차 섹션을 추가하고 절 번호를 템플릿과 정렬한다.
- [P1|templates] output-sample/organization/appointment-template.md:33 — 임명장 샘플에 '주기적 검토' 섹션과 검토 이력 테이블이 없어, 템플릿과 02-organization-designer 스펙이 명시한 18974 §4.1.2.5 입증자료 요소가 샘플에서 빠져 있다.
  제안: 샘플에 주기적 검토·검토 이력 섹션을 추가해 템플릿·agent 스펙과 일치시킨다.
- [P1|templates] templates/policy/oss-policy.md:102 — 정책 템플릿의 '## 5. AI 생성 코드 정책' 절은 03-policy-generator 스펙과 output-sample 어디에도 없고, 이 절 때문에 절 번호가 밀려 agent가 '항상 포함'한다고 명시한 '정책 변경 요청 및 운영' 절이 템플릿에선 §11, 샘플에선 §10으로 어긋난다.
  제안: AI 생성 코드 절의 정본 여부를 결정해 agent 스펙·샘플과 맞추고, 상호 참조는 절 번호 대신 절 이름 기준으로 바꾼다.
- [P1|samples] samples/README.md:9 — nodejs-unlicensed의 잘못된 학습 포인트('라이선스 미명시(UNLICENSED) 패키지 처리')가 학습 메타 표와 docs 실습 표에 그대로 전파되어 있습니다.
  제안: P0(nightmare MIT) 수정 시 samples/README.md 표와 docs/05-tools/sbom-generation/index.md 143행의 학습 포인트 문구를 함께 갱신해야 합니다.
- [P1|samples] docs/05-tools/sbom-generation/docker-cicd.md:90 — '실습용 샘플 프로젝트가 두 가지 제공된다'고 안내하지만 실제 samples/에는 세 개(nodejs-unlicensed 포함)가 있어 다른 문서와 불일치합니다.
  제안: 세 개 샘플을 모두 나열하고(또는 index.md 표로 링크) 문장을 존댓말로 통일합니다.
- [P1|samples] samples/java-vulnerable/README.md:58 — 샘플 README의 'SBOM 생성 명령어'는 출력 디렉터리 생성 단계 없이 `> ../../output/sbom/...`로 리다이렉트하므로 fresh clone에서 그대로 실행하면 'No such file or directory'로 실패합니다.
  제안: 세 샘플 README의 명령 블록 첫 줄에 `mkdir -p ../../output/sbom`을 추가하거나 선행 조건에 출력 폴더 생성을 명시합니다.

## 미검증 P0/P1 (상한 초과)

- [P1|web-devsecops] website/devsecops/strategy.md:84 — 셀프 스터디 admonition은 '전략 페이지의 1~4단계를 구현'한다고 하지만 아래 표의 단계 번호(2~5단계)는 AI 코딩 가이드의 다른 체계를 따라, 같은 페이지의 로드맵 1~4단계와 어긋나 독자를 혼란시킵니다.
  제안: admonition 문구에서 '1~4단계' 표현을 제거하거나 표의 단계 열 이름을 'AI 코딩 가이드 단계'로 구분해 표기합니다.
- [P1|web-devsecops] website/devsecops/monitoring.md:84 — 'Dependabot Security Alerts를 활성화하면 별도 설정 없이 PR을 생성한다'는 설명은 부정확합니다 — 알림(alerts)과 보안 업데이트 PR(security updates)은 별개 설정입니다.
  제안: alerts(알림)와 security updates(자동 PR)를 구분해 두 설정 모두 활성화하도록 안내합니다.
- [P1|web-devsecops] website/devsecops/container-security.md:172 — 6개 도구 페이지 중 컨테이너 보안과 DAST 두 페이지만 표준 동선(샘플 데모 iframe → API 키 callout → 실제 분석 iframe → 셀프 스터디 agent)이 없어 페이지 간 구성이 일관되지 않습니다.
  제안: 두 페이지에도 동일한 데모·분석기 동선을 추가하거나, 의도적 차이라면 다음 단계 안내에 그 이유를 한 줄 밝힙니다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/sbom-generation/index.md:17 — ko에 추가된 'SBOM · 취약점 분석 · SCA의 관계' note와 용어집 안내 tip 두 admonition이 en에 누락됐다.
  제안: 두 admonition을 번역해 같은 위치에 추가한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/vulnerability/index.md:17 — ko의 ':::note 이 단계의 위치'(SBOM 생성=입력, 취약점 분석=산출, DevSecOps SCA 링크) admonition이 en에 누락됐다.
  제안: 해당 note admonition을 번역해 1절 끝에 추가한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/checklist-mapping.md:50 — ko가 admonition으로 쓴 '핵심 통찰'과 '참고' 블록을 en이 마크다운 인용(>)으로 격하해 프로젝트 규칙(인용 대신 admonition)을 위반한다.
  제안: 두 블록을 :::info admonition으로 복원한다 (sbom-generation/index.md 57행의 KWG tip 블록도 동일 패턴).
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/sbom-101.md:9 — sidebar_label이 'SBOM Default'로 오역돼('SBOM 기본'의 기계번역) 사이드바 내비게이션에서 의미가 통하지 않는다.
  제안: sidebar_label을 'SBOM Basics'로 수정한다.
- [P1|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/index.md:124 — 같은 문서 안에서 공통 항목 수가 11개(2절)와 10개(완료 체크리스트)로 엇갈린다.
  제안: 완료 체크리스트의 10을 11로 고치고 ko 원본도 함께 수정한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/sast.mdx:192 — 셀프 스터디 사전 조건의 저장소 링크가 en 7개 파일에서 낡은 trustedoss.github.io를 가리킨다 — ko는 전부 trustedoss/trustedoss-agents로 갱신됨.
  제안: 7개 en 파일의 저장소 URL을 trustedoss/trustedoss-agents로 갱신한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/policy.md:243 — en 정책 샘플에 ko의 '### 10. 정책 변경 요청 및 운영' 섹션(18974 §4.1.1.1·5230 §3.1.5.1 대응, 변경 요청 5단계 절차와 규제 모니터링)이 통째로 빠져 §9에서 바로 부록 A로 건너뛴다.
  제안: 섹션 10을 번역해 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/organization.md:36 — en 조직 샘플의 역할 목록 표에서 ko에 있는 '팀별 챔피언' 행이 빠져 있다.
  제안: 해당 행을 번역해 표에 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/sbom.md:10 — en SBOM 샘플에 ko의 ':::tip 샘플 SBOM 내려받기'(fixture-sample.cdx.json 다운로드 링크와 SCA 분석기 연계 안내)가 빠져 있다.
  제안: 다운로드 tip 블록을 번역해 추가한다.
- [P1|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/training.md:4 — reference 샘플 7개의 en sidebar_label이 같은 ko 용어 '산출물'을 deliverables/output/artifacts로 제각각 번역하고 대소문자도 불일치해 사이드바 항목이 뒤죽박죽으로 보인다.
  제안: 'Organization Output'처럼 용어(Output)와 대문자 표기를 통일한다.

## P2 backlog

- [P2|docs-00] docs/00-overview/supply-chain.md:47 — 오픈소스 구성 비율이 index.md(70~80%)와 이 문서(70~90%)에서 서로 다르게 표기됩니다.
  제안: 한 가지 수치 범위로 통일합니다.
- [P2|docs-00] docs/00-overview/supply-chain.md:16 — 존댓말 평서형 기준을 어기고 반말과 존댓말이 한 문단 안에서도 혼용됩니다.
  제안: 본문 서술을 존댓말 평서형('~합니다')으로 통일합니다.
- [P2|docs-00] docs/00-overview/checklist-mapping.md:593 — admonition 안내문이 명령형 반말('시작하라')이고, 문서 읽는 방법 목록(라인 31~34)도 반말이라 존댓말 평서형 기준과 어긋납니다.
  제안: '시작하세요' 등 존댓말 평서형으로 통일합니다.
- [P2|docs-00] docs/00-overview/supply-chain.md:126 — NTIA의 한국어 풀이가 STYLEGUIDE 정본 용어와 다릅니다.
  제안: STYLEGUIDE 정본인 '미국 통신정보관리청'으로 통일합니다.
- [P2|docs-00] docs/00-overview/sbom-101.md:6 — front matter 충족 체크리스트에 ISO 섹션 번호(4.x.x) 대신 내부 G항목 ID('G3B.1 배경')를 사용해 문서화된 형식과 다릅니다.
  제안: 빈 배열로 두거나 해당 섹션 번호(예: 4.3.1) 표기로 바꾸고, G항목 언급은 본문에 둡니다.
- [P2|docs-00] docs/00-overview/sbom-101.md:12 — 제목의 SBOM 풀이 '소프트웨어 구성 명세서'가 STYLEGUIDE 정본 풀이 '소프트웨어 부품 명세서'와 다릅니다.
  제안: 정본 풀이로 통일하거나 STYLEGUIDE 표를 먼저 개정한 뒤 사용합니다.
- [P2|docs-00] docs/00-overview/checklist-mapping.md:607 — 체크리스트 참조 관용 패턴이 아닌 일반 강조·인용 목적에 마크다운 인용(>)을 사용합니다.
  제안: :::info 등 admonition으로 전환합니다.
- [P2|docs-01-02] docs/02-organization/index.md:157 — 질문 4(법무 자문)의 선택지가 agent 스펙과 다릅니다.
  제안: agent 스펙의 선택지 4개에 맞춰 문서의 두 곳을 갱신합니다.
- [P2|docs-01-02] docs/02-organization/index.md:186 — 셀프스터디 5번 항목이 바로 위 details 대화 예시와 같은 6개 질문을 그대로 반복합니다.
  제안: 5번 항목을 '위 예시의 6개 질문에 자사 상황으로 답변' 한 줄로 압축합니다.
- [P2|docs-01-02] docs/01-setup/index.md:16 — 본문 일부가 반말 평서형('~하다')으로 작성되어 존댓말 기준과 혼재합니다.
  제안: 해당 불릿·번호 항목을 존댓말 평서형으로 통일합니다.
- [P2|docs-01-02] docs/02-organization/index.md:274 — admonition 제목 표기가 같은 문서 안에서 두 가지 문법으로 혼재합니다.
  제안: 레포 관례인 공백 문법(:::tip 산출물 예시)으로 통일합니다.
- [P2|docs-01-02] docs/02-organization/index.md:15 — Prerequisite가 링크 없는 평문으로만 작성되어 다른 챕터와 형식이 다르고 개요 챕터로 이동할 수 없습니다.
  제안: items prop으로 '0. 개요' 링크(href: /docs/)를 추가합니다.
- [P2|docs-03-04] docs/04-process/index.md:152 — cron '0 9 \* _ 1' 주석이 '매주 월요일 오전 9시'인데 GitHub Actions cron은 UTC 기준이라 한국 독자 기준 실제 실행은 월요일 18시입니다.
  제안: 주석을 '매주 월요일 09:00 UTC (KST 18:00)'로 수정하거나 KST 오전 실행이 의도면 '0 0 _ \* 1'로 변경.
- [P2|docs-03-04] docs/04-process/index.md:21 — '4~7개 산출물을 생성합니다'가 본문 예상 결과물 표와 맞지 않습니다: 표 기준 무조건 생성 5개 + 조건부 2개이므로 5~7개입니다.
  제안: '5~7개'로 수정하고 agents/04-process-designer/CLAUDE.md의 동일 표기(4~7개)도 함께 정리.
- [P2|docs-03-04] docs/04-process/index.md:56 — '이 세 지점에 아래 핵심 프로세스가 대응합니다' 직후 6가지 프로세스가 나와 세 지점과 6개의 대응 관계가 불명확하고, '핵심 프로세스 6가지' 도입부(60행)도 결론 대신 §3.5 기여·공개 부연으로 시작합니다.
  제안: 도입 문장을 '여섯 가지 프로세스'로 맞추고 §3.5 설명 문단은 3-4 앞으로 이동.
- [P2|docs-03-04] docs/04-process/index.md:1 — 본문이 369줄로 STYLEGUIDE 권장 밴드(200~350줄)를 초과합니다.
  제안: 3-4~3-6 상세나 CI/CD 예시 일부를 하위 문서·reference 페이지로 분리.
- [P2|docs-03-04] docs/03-policy/index.md:34 — Artifex vs Hancom 서술에서 '소각하 신청을 기각했습니다'는 신청 주체(한컴)가 생략되어 있고 '소각하'가 붙여 쓰여 오독('소각') 여지가 있습니다.
  제안: '한컴이 낸 소 각하 신청(사건을 심리 없이 종료해 달라는 신청)을 기각했습니다'처럼 주체와 풀이를 붙여 쓰기.
- [P2|docs-03-04] docs/03-policy/index.md:174 — Agent 대화 예시의 안내 메시지를 마크다운 인용(>)으로 표기했습니다. 프로젝트 규칙은 표준 체크리스트 문구('> 이 단계는...') 외의 인용을 admonition·코드펜스로 대체하도록 합니다.
  제안: agent 메시지 예시는 코드펜스나 평문으로 전환.
- [P2|docs-05-sbom] docs/05-tools/sbom-management/index.md:143 — GitHub Actions cron은 UTC 기준인데 주석이 '매주 월요일 오전 9시'라고만 적어 한국 독자는 KST 오전 9시로 오해할 수 있다.
  제안: 주석을 '매주 월요일 09:00 UTC(KST 18:00)'로 명시한다.
- [P2|docs-05-sbom] docs/05-tools/index.md:17 — '아래 세 단계 흐름으로 진행합니다'라고 안내한 직후 번호 목록이 4개 항목(4번째는 선택인 AI SBOM)이라 문구와 목록이 맞지 않는다.
  제안: '세 단계 + 선택 단계 하나'로 문구를 고치거나 AI SBOM 항목을 번호 목록 밖으로 뺀다.
- [P2|docs-05-sbom] docs/05-tools/sbom-management/index.md:111 — 'SBOM 을'처럼 조사를 띄어 쓴 오류가 반복되고, '받은 SBOM 을 수입해'의 '수입'은 통용되지 않는 번역투 용어다.
  제안: 조사를 붙여 쓰고 '수입해'는 '받아들여(ingest)' 등 통용 표현으로 바꾼다.
- [P2|docs-05-sbom] docs/05-tools/sbom-management/index.md:285 — 같은 목적의 산출물 예시 안내 admonition이 챕터마다 타입·문법이 다르다(:::tip[산출물 예시] vs :::note 산출물 예시).
  제안: 두 챕터의 산출물 예시 안내를 동일한 admonition 타입·제목 문법으로 통일한다.
- [P2|docs-05-sbom] docs/05-tools/sbom-generation/index.md:145 — ISO 충족 표기 관례가 아닌 일반 안내('권장: java-vulnerable 샘플')에 마크다운 인용(>)을 사용했다.
  제안: :::tip admonition으로 바꾼다.
- [P2|docs-05-sbom] docs/05-tools/sbom-generation/docker-cicd.md:1 — docker-cicd.md의 front matter에 STYLEGUIDE §5가 요구하는 4개 필수 필드(작성일·버전·충족 체크리스트·셀프스터디 소요시간)가 없다.
  제안: 4개 필드를 추가하거나, 하위 실행 가이드 예외를 STYLEGUIDE에 명문화한다.
- [P2|docs-05-vuln-ai] docs/05-tools/ai-sbom/index.md:54 — BomLens 저장소 URL이 옛 이름(github.com/sktelecom/sbom-tools)으로 표기되어 있으며 실제 저장소는 github.com/sktelecom/bomlens로 이전(rename)되었다.
  제안: 저장소 정식 URL(github.com/sktelecom/bomlens)로 갱신하고 clone 후 cd 경로도 새 디렉토리명 기준으로 맞춘다.
- [P2|docs-05-vuln-ai] docs/05-tools/vulnerability/tools-setup.md:16 — 존댓말 문서 안에서 반말 종결('오픈소스 도구다', '데이터베이스다')이 섞여 문체가 일관되지 않는다.
  제안: '오픈소스 도구입니다', '취약점 데이터베이스입니다'로 존댓말 평서형으로 통일한다.
- [P2|docs-05-vuln-ai] docs/05-tools/vulnerability/index.md:83 — 섹션 3 제목이 '셀프 스터디'로, 문서 템플릿과 ai-sbom 챕터가 쓰는 '셀프스터디 경로'와 표기가 다르다.
  제안: 05-tools 하위 챕터의 섹션 3 제목을 '셀프스터디 경로'(또는 최소한 붙여쓴 '셀프스터디')로 통일한다.
- [P2|docs-06-07] docs/06-training/index.md:24 — 존댓말 문서에 반말 평서형이 반복 혼용된다 (18행 "이루어지지 않는다", 24행 "~하나다", 72행 "기록 자체다", 99·152행 "읽는다/한다", 197행 "생성된다", 217행 "차례다").
  제안: 본문 전체를 존댓말 평서형(~합니다/~입니다)으로 통일한다.
- [P2|docs-06-07] docs/06-training/index.md:64 — 무료 교육 리소스 표의 "링크" 열에 실제 링크가 아닌 텍스트만 있는 행이 4개다 (LFC193, NIPA, SPDX, CycloneDX).
  제안: 각 행에 실제 URL을 마크다운 링크로 넣거나 열 이름을 바꾼다.
- [P2|docs-06-07] docs/06-training/index.md:78 — 표준 충족 표기 형식이 아닌 일반 안내문에 마크다운 인용(>)을 사용했다 (78행, 118~120행 agent 대화 예시, 173행).
  제안: 78행은 :::info 또는 평문으로, 118~120행 대화 예시는 코드펜스로 전환한다.
- [P2|docs-06-07] docs/06-training/index.md:152 — 셀프스터디 4번 단계가 바로 위 details 블록(124~134행)에 이미 나온 agent 질문 3개를 그대로 반복한다.
  제안: 4번 단계는 "agent의 3가지 질문에 답합니다(위 대화 예시 참조)" 한 줄로 축약한다.
- [P2|docs-06-07] docs/07-conformance/index.md:104 — 정형 충족 표기가 아닌 일반 보충 설명에 마크다운 인용(>)을 사용했다.
  제안: :::info admonition 또는 평문으로 전환한다.
- [P2|docs-08] docs/08-developer-guide/method1-claude-md.md:1 — method1~method4 네 문서 모두 STYLEGUIDE §5가 docs/ 하위 문서 필수로 규정한 front matter 4개 필드(작성일·버전·충족 체크리스트·셀프스터디 소요시간)가 없습니다.
  제안: 네 method 파일에 작성일·버전·충족 체크리스트·셀프스터디 소요시간 필드를 추가해 다른 하위 문서와 형식을 맞춥니다.
- [P2|docs-08] docs/08-developer-guide/index.md:24 — 본문에서 마크다운 인용(>)으로 목표 문장을 강조하고 있어, 인용 대신 admonition을 쓰는 프로젝트 규칙과 어긋납니다.
  제안: :::info 또는 :::tip admonition으로 바꿉니다.
- [P2|docs-08] docs/08-developer-guide/method4-cicd.md:97 — method1~3은 문서 끝에 '→ 다음' 이동 링크가 있지만 method4는 아무 연결 없이 끝나, 독자가 index의 완료 확인·다음 단계 섹션으로 돌아갈 경로가 없습니다.
  제안: 문서 끝에 index.md의 '6. 완료 확인'으로 돌아가는 링크를 추가해 네 문서의 내비게이션을 일관되게 맞춥니다.
- [P2|agents-core] agents/02-organization-designer/CLAUDE.md:31 — 질문 5 선택지의 '외부 보안 컨실팅'은 '컨설팅'의 오타다.
  제안: '외부 보안 컨설팅 활용'으로 수정한다.
- [P2|agents-core] agents/02-organization-designer/CLAUDE.md:44 — 확장 옵션 분기 조건 '5인 미만이면 생략'이 선택지 '2인~5인'(5인 포함)과 경계가 어긋나 5인 팀의 처리 방향이 모호하다.
  제안: "'5인 이상' 선택 시 포함, 그 외 선택지는 생략"처럼 선택지 기준으로 조건을 쓴다.
- [P2|agents-core] tests/fixtures/02-organization-designer.json:5 — 픽스처 입력 '겸직'이 agent 선택지 표기 '겸무'와 일치하지 않는다.
  제안: 픽스처 입력을 '겸무'로 맞추거나 선택지 표기를 통일한다.
- [P2|agents-core] tests/fixtures/03-policy-generator.json:5 — 03 픽스처(그리고 04 branch-A/B)에 prerequisite_files가 없어 agent가 선언한 전제조건(output/organization/role-definition.md) 없이 테스트된다.
  제안: openwave 픽스처처럼 prerequisite_files로 전제 산출물을 복사해 실제 체인 조건에서 테스트한다.
- [P2|agents-core] .claude/scripts/validate-chain.py:58 — 04의 조건부 산출물 중 project-publication-process.md(Q6=예)가 CHAIN_SPEC에 전혀 반영되지 않아 contribution-process.md만 조건부로 모델링된다.
  제안: conditional_outputs에 project-publication-process.md(조건: 공개 계획 있음, Q6=예)를 추가한다.
- [P2|agents-05] agents/05-sbom-management/CLAUDE.md:23 — 처리 방식(37행)과 e2e fixture는 copyleft-risk.md를 입력으로 사용하는데 전제 조건 목록과 validate-chain.py inputs에는 license-report.md만 있다.
  제안: 전제 조건과 validate-chain.py inputs에 sbom/copyleft-risk.md를 추가해 처리 방식·fixture와 일치시킨다.
- [P2|agents-05] agents/05-vulnerability-analyst/CLAUDE.md:42 — CVSS 심각도 분류에 이모지 불릿(🔴🟠🟡🟢)을 사용해, 생성 리포트에도 그대로 전파된다(ko-style 이모지 장식 금지 규칙 위반).
  제안: 이모지를 제거하고 Critical/High/Medium/Low 텍스트 라벨만 쓰도록 스펙과 output-sample을 함께 정리한다.
- [P2|agents-05] agents/05-vulnerability-analyst/CLAUDE.md:40 — 제품명 'Dependency Track'은 정식 명칭 'Dependency-Track'(OWASP, 하이픈 포함)과 다르게 표기됐다(40행·73행).
  제안: 두 곳 모두 'Dependency-Track'으로 수정한다.
- [P2|agents-05] agents/05-vulnerability-analyst/CLAUDE.md:92 — '다음 단계' 뒤의 "Claude 프롬프트가 열리면 `시작`을 입력한다" 안내가 이 agent에만 있고, 같은 체인의 05-sbom-guide·05-sbom-analyst·05-sbom-management 다음 단계에는 없다.
  제안: 네 agent의 다음 단계 안내 문구를 동일한 형식으로 통일한다.
- [P2|agents-06-07] agents/07-conformance-preparer/CLAUDE.md:26 — 전제 조건의 폴더별 G항목 주석이 마스터 매핑과 어긋난다 — training/에 G1.7, sbom/에 G3S.5, vulnerability/에 G3S.6이 빠져 있고, sbom/의 'G3B.1~G3B.4'는 validate-checklist의 '(G3B.1, G3B.2, G3L.1, G3L.3)'과 다르다.
  제안: 폴더별 G항목 주석을 checklist-mapping.md 기준으로 재산정해 validate-checklist.md와 동일하게 맞춘다.
- [P2|agents-06-07] agents/CLAUDE.md:50 — '전체 Agent 목록'이라는 제목과 달리 agents/ 디렉토리의 16개 중 셀프스터디 9개만 나열해 '전체'라는 표현이 실제와 다르다.
  제안: 제목을 '셀프스터디 Agent 목록'으로 바꾸거나, 나머지 agent가 별도 트랙(DevSecOps·AI 코딩)임을 한 줄로 안내한다.
- [P2|agents-06-07] tests/fixtures/07-conformance-preparer.json:8 — 07 fixture의 prerequisite_files에 process/process-diagram.md가 없어 validate-chain.py의 07 입력 스펙(및 output-sample 실상)과 어긋난다.
  제안: fixture prerequisite_files에 process/process-diagram.md를 추가해 체인 스펙과 테스트 환경을 일치시킨다.
- [P2|agents-devtools] agents/devsecops-setup/CLAUDE.md:84 — 출력 산출물 트리에서 devsecops-merge.yml 주석이 "(GitHub 선택 시)"로 되어 있어, 컨테이너·DAST 미선택 시 생성하지 않는다는 처리 방식 설명(68행)과 조건이 어긋납니다.
  제안: 주석을 "(GitHub + 컨테이너/DAST 선택 시)"로 바꿔 생성 조건을 한 곳으로 통일합니다.
- [P2|agents-devtools] agents/ai-coding-setup/CLAUDE.md:13 — 충족 체크리스트가 SBOM 정책·저작권 헤더 규칙을 항상 포함한다고 단정하지만, 질문 5에서 이 규칙들은 선택 사항("없음" 가능)이라 분기가 모순됩니다.
  제안: 체크리스트 두 항목에 "(질문 5 선택 시)" 조건을 명시하거나 기본 포함 규칙으로 승격해 질문 5와 일치시킵니다.
- [P2|agents-devtools] agents/level2-automation/issue-tracker/CLAUDE.md:1 — 스코프의 독립 도구 agent 7종은 체인 agent(02~07)와 달리 스펙 구조 검증·골든 픽스처가 전혀 없어 회귀를 잡을 수단이 없습니다.
  제안: 체인 밖 agent에도 최소한 필수 섹션(세션 시작 동작·입력 질문·출력 산출물) 구조 검증을 test-agent-specs.py에 추가하는 것을 검토합니다.
- [P2|web-aicoding] website/ai-coding/intro.md:22 — SBOM·SCA 약어가 문서 첫 등장에서 풀이 없이 사용되어 STYLEGUIDE의 쉬운 용어 규칙(첫 등장 괄호 풀이)에 어긋난다.
  제안: 첫 등장 위치에 STYLEGUIDE 약어 풀이 표의 표준 풀이를 괄호로 추가한다.
- [P2|web-aicoding] website/ai-coding/cicd-quick.mdx:37 — '설치 없이 GitHub Actions / GitLab CI에서 바로 사용 가능'이라는 서술이 같은 문서의 GitLab 파이프라인(도구를 curl로 직접 설치)과 모순된다.
  제안: 'GitHub Actions에서는 마켓플레이스 Action으로 설치 없이, GitLab CI에서는 스크립트 한 줄로 설치해' 정도로 플랫폼별 차이를 정확히 서술한다.
- [P2|web-aicoding] website/ai-coding/ai-security-review.md:136 — 워크플로우 코드 주석의 '상위 10개로 제한'이 실제 코드(Semgrep 8개 + grype 5개 = 13개) 및 본문·다이어그램의 '13개' 표기와 불일치한다.
  제안: 주석을 '상위 13개(Semgrep 8 + grype 5)로 제한'으로 수정한다.
- [P2|web-devsecops] website/devsecops/sast.mdx:189 — 분석기 iframe의 border 색상이 페이지마다 다르게 하드코딩돼 있고(다크 고정 #30363d, #2a2f45, #2a2a2a vs 라이트 고정 #e0e5ec) 라이트/다크 테마를 따라가지 못합니다.
  제안: 공용 CSS 변수(예: var(--ifm-color-emphasis-300))로 통일합니다.
- [P2|web-devsecops] website/devsecops/monitoring.md:98 — renovate.json 예시가 폐기 예정 프리셋 config:base를 사용합니다(현행 권장은 config:recommended).
  제안: config:recommended로 교체합니다.
- [P2|web-devsecops] website/devsecops/iso-mapping.md:96 — 'Trusted OSS의 기업 오픈소스 거버넌스 가이드를 참고하세요'가 링크 없이 끝나고, 다른 페이지에서 쓰는 명칭(체계구축/오픈소스 관리 가이드)과도 다릅니다.
  제안: '[체계구축 가이드](/docs)를 참고하세요'처럼 통일 명칭과 링크를 붙입니다.
- [P2|web-devsecops] website/devsecops/intro.md:16 — SBOM이 문서 첫 등장인데 STYLEGUIDE의 '첫 등장 시 괄호 풀이' 규칙(소프트웨어 부품 명세서)이 적용되지 않았습니다.
  제안: 첫 등장 시 'SBOM(소프트웨어 부품 명세서 — ...)' 형태의 표준 풀이를 붙입니다.
- [P2|web-devsecops] website/devsecops/iac-security.mdx:176 — CKV_K8S_11은 CPU limits 검사만 담당하는데 설명이 'CPU·메모리 limits 설정'으로 메모리(CKV_K8S_13)까지 포괄하는 것처럼 적혀 있습니다.
  제안: 설명을 'CPU limits 설정'으로 좁히거나 CKV_K8S_13을 함께 표기합니다.
- [P2|web-reference] website/reference/concepts/vulnerability-response.md:18 — "대응 기한 (KWG 기준선)" 열이 4개 행 전체를 KWG 출처로 표기하지만 KWG 가이드는 Critical 1주·High 4주만 정의하며, Medium(1개월)은 High(4주일)와 사실상 같은 기한이라 심각도 차등이 무의미해 보입니다.
  제안: Medium·Low 행은 trustedoss 권고임을 구분 표기하고, High(4주)와 Medium(1개월)의 기한 차이를 명확히 벌립니다.
- [P2|web-reference] website/reference/concepts/license-classification.md:44 — 허용 매트릭스의 기호 의미가 혼란스럽습니다: '✗ 검토 필요'는 금지 기호에 검토 라벨을 붙였고 '△ 조건부'와의 차이가 설명되지 않으며, 정책 샘플 페이지는 ✅/⚠️/❌ 다른 체계를 씁니다.
  제안: 정본 페이지에 기호 범례를 추가하고 정책 샘플과 같은 3단계 표기 체계로 통일합니다.
- [P2|web-reference] website/reference/samples/organization.md:46 — §1 역할 목록에는 '팀별 챔피언'이 있으나 §2 역할별 필요 역량 표에는 해당 행이 없어, 역할별 역량 문서(5230 3.1.2.2·18974 4.1.2.2) 예시로서 불완전합니다.
  제안: 역량 표에 팀별 챔피언 행을 추가하고 원본 산출물도 함께 갱신합니다.
- [P2|web-reference] website/reference/samples/training.md:182 — 이수 추적 시트에서 샘플 레코드는 '완료'(홍길동·이영희·박지수)로 표시돼 있는데 바로 아래 이수 현황 요약은 완료 0명·이수율 0%로 집계돼 서로 모순돼 보입니다.
  제안: 샘플 레코드 행에 '집계 제외 예시' 표시를 하거나 요약 수치를 샘플 포함 기준으로 맞춥니다.
- [P2|web-reference] website/reference/samples/sbom.md:369 — 준거 표준 표에 4.3.1이 두 행으로 중복 기재되고 두 번째 행의 "SBOM 공유 (공급망 파트너)"는 4.3.1 입증자료 정의에 없는 내용입니다.
  제안: 중복 행을 합치고 요구사항 요약을 스펙 문구(수명주기 지속 기록)에 맞게 정정합니다.
- [P2|web-reference] website/reference/samples/sbom.md:399 — 같은 페이지에서 SBOM 포맷 버전이 혼재합니다: 리포트·픽스처는 CycloneDX 1.6인데 제출 템플릿 예시는 CycloneDX 1.5를 기준으로 안내합니다.
  제안: 템플릿 예시의 CycloneDX 버전을 1.6으로 통일합니다.
- [P2|web-reference] website/reference/glossary.md:64 — 용어집에 있는 cdxgen·OSV·onot·BomLens가 정본 출처인 STYLEGUIDE 약어 표에 없어, '표에 먼저 추가 후 용어집과 동기화'라는 유지보수 규칙과 어긋납니다.
  제안: STYLEGUIDE 약어 표에 4개 용어를 추가해 두 문서를 동기화합니다.
- [P2|web-design] website/src/css/customTheme.scss:361 — @font-face의 폰트 URL이 `/static/fonts/...`로 되어 있으나 빌드 산출물은 `/fonts/...`에 배치되어 요청 시 404가 나며, 'Optimistic Display' 선언 자체가 Roboto 수렴(POSITIONING §6) 이후 어디서도 사용되지 않는 잔재입니다.
  제안: 미사용 Optimistic Display @font-face를 제거하고, Source Code Pro를 유지하려면 경로를 `/fonts/...`로 고칩니다.
- [P2|web-design] website/src/css/customTheme.scss:11 — --toss-cyan-_ 팔레트(주석: '색의 값은 여기에만 존재한다. 모든 의미 토큰은 이 변수를 참조한다')가 실제로는 어떤 규칙에서도 참조되지 않아 주석이 현재 상태(Google 블루 --g-blue-_ 단일 소스)와 모순됩니다.
  제안: 미사용 --toss-cyan-_ 정의와 낡은 '단일 소스' 주석을 제거하거나 --g-blue-_ 기준으로 주석을 갱신합니다.
- [P2|web-design] website/src/components/releases/\_releases-table.md:8 — React Native 웹사이트 포크 잔재가 src에 남아 있습니다 — React Native 릴리스 표 데이터(ReleasesTable)와 어디서도 import되지 않는 showcase.scss·versions.scss.
  제안: components/releases/ 디렉토리와 미사용 showcase.scss·versions.scss를 삭제합니다.
- [P2|web-design] website/src/components/Home/Hero/index.tsx:87 — Hero 터미널 목업의 텍스트('회사 상황 5개 질문에 답하는 중…', 칩 '정책/SBOM/취약점/선언문')가 Translate로 감싸져 있지 않아 영어 로케일 랜딩에도 한국어로 노출됩니다.
  제안: 목업 문자열과 aria-label을 translate()로 감싸 en 로케일에서 번역되게 합니다.
- [P2|web-design] website/docusaurus.config.ts:48 — onBrokenLinks가 'warn'이라 빌드 시 깨진 내부 링크가 경고로만 지나가고 배포를 막지 못합니다.
  제안: onBrokenLinks(및 onBrokenMarkdownLinks)를 'throw'로 올려 빌드에서 차단합니다.
- [P2|web-design] website/src/components/Home/Features/index.tsx:86 — 세 트랙 카드 제목이 'AI코딩'(붙여쓰기)인데 navbar·footer·사이드바는 'AI 코딩 거버넌스'(띄어쓰기)를 써서 같은 화면 안에서 표기가 갈립니다.
  제안: 카드 제목을 'AI 코딩' 또는 'AI 코딩 거버넌스'로 통일합니다.
- [P2|web-design] website/docusaurus.config.ts:2 — 파일 헤더 주석들이 사이트 도메인을 'trustedoss.dev'로 표기하지만 실제 사이트는 trustedoss.github.io입니다.
  제안: 헤더 주석의 도메인 표기를 trustedoss.github.io로 정정합니다.
- [P2|web-landing-ux] docs/00-overview/start-path.md:21 — "빠른 시작"이라는 같은 라벨이 5분짜리 quick-start 페이지와 1~2시간짜리 축약 코스라는 두 가지 다른 의미로 쓰여 혼동을 준다.
  제안: 1~2시간 코스는 "축약 코스" 등 다른 이름으로 구분한다.
- [P2|web-landing-ux] docs/00-overview/index.md:47 — 전체 챕터 표의 "05 도구" 행이 선택 챕터인 5.4 AI SBOM을 누락한다 (같은 선택 챕터인 08은 표에 포함).
  제안: 05 도구 행에 AI SBOM(선택) 링크를 추가한다.
- [P2|web-landing-ux] website/src/components/Home/Hero/index.tsx:80 — Hero의 터미널 연출이 03-policy-generator를 첫 실행처럼 보여주지만, 모든 안내(quick-start·Roadmap·상태 감지)는 02-organization-designer를 첫 에이전트로 안내한다.
  제안: 연출을 02-organization-designer 실행 장면으로 바꾸거나 유지 사유를 남긴다.
- [P2|web-landing-ux] docs/00-overview/index.md:138 — 다음 단계 안내 섹션이 화살표(→) 산문으로 작성되어 문체 규칙(화살표 산문 지양)과 어긋난다.
  제안: 화살표를 빼고 평서형 문장으로 잇는다.
- [P2|web-landing-ux] website/devsecops/intro.md:49 — "어디서 시작할까?" admonition이 6개 항목 모두 화살표(→) 산문으로 나열되어 문체 규칙과 어긋난다.
  제안: 표(상황 | 시작점)로 압축하거나 평서형 문장으로 바꾼다.
- [P2|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/checklist-mapping.md:45 — '인증 방식'을 'Authentication Method'로, 'G1: 프로그램 기반'을 'G1: Program-based'로 오역해 스타일가이드 용어(Self-Certification, Program foundation)와 어긋난다.
  제안: 'Certification method', 'G1: Program foundation'으로 통일하고 태그 표기를 규칙 표와 일치시킨다.
- [P2|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/agents.md:51 — 에이전트 시작 입력어를 이 문서만 `start`로 안내해, `시작`으로 안내하는 다른 en 문서들과 불일치한다.
  제안: 다른 문서와 같이 'type `시작` ("start")' 표기로 통일한다.
- [P2|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/sbom-generation/index.md:161 — Step 5 안내문이 주어가 뒤집힌 번역('Executes when the agent generates...')으로 어색하고 오해 소지가 있다.
  제안: 'When the agent has generated `output/sbom/sbom-commands.sh`, run it:'로 고친다.
- [P2|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/index.md:39 — en 페이지의 루트 절대 경로 링크(/devsecops/intro, /reference/... 등)가 locale 접두사 없이 ko 페이지로 이동해 en 독자의 언어 맥락이 끊긴다.
  제안: en 번역 파일에서는 /en/ 접두사를 붙이거나 빌드 검증에서 locale-aware 링크 처리를 도입한다.
- [P2|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/quick-start.md:14 — ko가 쓰는 용어 툴팁 컴포넌트 <Term>(openchain, self-certification, sbom)이 en에서 모두 평문으로 대체돼 용어집 연동이 사라졌다.
  제안: en에도 동일 위치에 <Term> 컴포넌트를 적용한다 (00-overview/index.md 등 다른 파일 포함).
- [P2|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/00-overview/index.md:2 — ko 원본에 있는 front matter description(SEO·미리보기용)이 en 번역본에는 거의 전부 누락됐다.
  제안: ko description을 번역해 해당 en 파일들의 front matter에 추가한다.
- [P2|en-docs] website/i18n/en/docusaurus-plugin-content-docs/current/05-tools/sbom-management/index.md:270 — 예시 산출물 코드블록 내 섹션 제목의 대소문자가 뒤죽박죽이라(1번만 Title Case, 2~4번 소문자) 견본 품질이 떨어진다.
  제안: 예시 블록 제목을 일관된 표기(문장 첫 글자 대문자 이상)로 통일한다.
- [P2|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/process.md:433 — ko가 admonition(:::info[참고], :::note[조건부 생성])으로 승격한 블록들이 en에서는 옛 blockquote(>) 형태로 남아 있다 (process 3곳, policy 1곳, sbom 1곳).
  제안: ko와 같은 admonition 문법으로 교체한다.
- [P2|en-web] website/i18n/en/docusaurus-plugin-content-docs-devsecops/current/sca.mdx:24 — 섹션 헤딩이 소문자로 시작해 다른 헤딩과 표기가 불일치한다: '## vulnerability Scanning — grype', '## vulnerability Policy Design'.
  제안: 'Vulnerability Scanning — grype', 'Vulnerability Policy Design'으로 통일한다.
- [P2|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/training.md:9 — 기계번역 어순 오류로 문장이 어색하다: 코드 식별자가 주어 앞에 고립되어 있다.
  제안: "A complete example of the three outputs generated by the `training-manager` agent."로 다듬는다.
- [P2|en-web] website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/policy.md:239 — 기계번역 잔재인 zero-width space(U+200B)가 reference en 7개 파일(intro 및 samples 전체)에 산재한다.
  제안: U+200B 문자를 일괄 제거한다.
- [P2|harness] .claude/scripts/test-output-fixtures.py:91 — check_fixture_completeness()의 CHAPTER_FILES 복제본이 'validate-output.py CHAPTER_FILES 기준'이라는 주석과 달리 실제 목록과 다르다(sbom이 1개 vs 4개).
  제안: 복제 상수를 제거하고 validate-output.py에서 CHAPTER_FILES를 import해 단일 소스로 쓴다.
- [P2|harness] .claude/scripts/validate-output.py:8 — 스크립트 docstring·메시지의 verify.sh 항목 번호가 현재 12항목 체계와 어긋난 옛 번호로 남아 있다.
  제안: 네 파일의 항목 번호 표기를 현재 12항목 체계로 갱신하거나 번호 대신 검사 이름으로 표기한다.
- [P2|harness] .claude/skills/kwg-check/skill.md:69 — 반영 절차의 검증 단계가 'verify.sh # 8/8 PASS 확인'으로 옛 항목 수를 안내한다(현재 12항목).
  제안: 8/8을 12/12로 갱신하거나 '전 항목 PASS'로 표기한다.
- [P2|harness] .claude/skills/update-reference-samples.md:213 — 완료 조건이 'verify.sh를 실행하여 7개 항목 PASS를 확인한다'로 옛 항목 수를 안내한다(현재 12항목).
  제안: 7개를 12개로 갱신하거나 '전 항목 PASS'로 표기한다.
- [P2|harness] .claude/scripts/sync-kwg-reference.sh:34 — AUTH_HEADER 변수를 만들어 놓고 어디에서도 사용하지 않는다(실제 인증은 api_get 함수가 별도로 처리).
  제안: AUTH_HEADER 조립 코드를 삭제한다.
- [P2|harness] .claude/scripts/verify.sh:35 — [2/12] 링크 존재 확인의 보조 조건 [ ! -e "$filepath" ]가 레포 루트 기준으로도 존재를 인정해, 문서 기준으로는 깨진 상대 링크가 루트의 동명 파일과 우연히 일치하면 통과한다.
  제안: 루트 기준 fallback 조건을 제거하고 문서 디렉토리 기준으로만 판정한다.
- [P2|harness] .claude/scripts/verify.sh:206 — [7/12] admonition 검사가 코드펜스를 정확히 '`bash'일 때만 인식해 '`bash title="..."' 또는 '`sh' 블록 안의 cd agents/는 검사를 우회한다.
제안: startswith('`bash') 및 '```sh' 계열까지 매칭하도록 조건을 완화한다.
- [P2|templates] templates/process/usage-approval.md:13 — 04-process-designer가 상시 포함한다고 명시한 CI/CD 자동화 워크플로우 절이 사용 승인 템플릿에는 없어, 샘플(§2 CI/CD 자동화 통합)과 절 번호가 한 칸씩 밀린다.
  제안: 템플릿에 CI/CD 자동화 절 자리(placeholder)를 추가해 샘플과 절 번호를 정렬한다.
- [P2|templates] output-sample/organization/role-definition.md:7 — 역할 정의 샘플의 §6이 '모범 사례 일치 검증 담당자' 한 절로 축소되어, 템플릿이 갖춘 '주기적 검토 방법'·'검토 이력' 하위 절(18974 §4.1.2.5 갱신 시 이력 기록처)이 없다.
  제안: 샘플 §6에 주기적 검토 방법과 검토 이력 표를 추가해 템플릿 구조와 맞춘다.
- [P2|samples] samples/python-mixed-license/README.md:29 — 'SBOM 생성 시 mysql-connector-python GPL-2.0 컴포넌트 탐지'라고 기술하지만 실제 syft 출력의 licenses 필드는 비어 있어 GPL-2.0 표시는 이후 분석 단계에서만 나타납니다.
  제안: 예상 결과를 '컴포넌트 탐지'와 'GPL-2.0 식별(라이선스 분석 단계)'로 분리해 java 샘플과 같은 방식으로 안내합니다.
- [P2|samples] samples/java-vulnerable/README.md:35 — 같은 README 안에서 업그레이드 권고 버전이 35행 '2.15.0 이상'과 45행 '2.17.1 이상'으로 엇갈립니다.
  제안: 예상 결과 문구를 '도구는 수정 버전으로 2.15.0을 보고하지만 실제 조치는 2.17.1 이상 권장'으로 통일합니다.
- [P2|samples] samples/java-vulnerable/README.md:24 — 샘플 README 세 개 모두 존댓말과 반말이 혼재합니다(대표 사례).
  제안: STYLEGUIDE의 독자용 문서 기준에 맞춰 샘플 README 본문을 존댓말 평서형으로 통일합니다.
- [P2|samples] docs/05-tools/sbom-generation/index.md:145 — 샘플 권장 안내에 프로젝트에서 금지한 마크다운 인용(>) 블록을 사용했습니다.
  제안: :::tip 권장 ::: admonition으로 전환합니다.

## 검증에서 반박된 발견 (수정 불필요)

- [P1|agents-05] agents/05-sbom-guide/CLAUDE.md:98 — '다음 단계'의 `cd agents/05-sbom-analyst`는 세션 종료 직후 셸 cwd(agents/05-sbom-guide)에서 실행하면 실패한다. 같은 패턴이 05-sbom-analyst(72행), 05-sbom-management(70행), 05-vulnerability-analyst(88행)에도 있다.
  제안: `cd ../05-sbom-analyst`로 바꾸거나 '레포 루트로 이동 후 실행' 안내 문구를 다음 단계 블록에 추가한다(4개 agent 공통).
  반박: 대상 4개 파일은 모두 폴더 CLAUDE.md로 감사 규칙상 스코프 제외(독자 비노출)이며, Claude가 소비하는 에이전트 지침이라 코드 블록이 그대로 사용자 셸에서 실행돼 실패한다는 전제가 확정적이지 않다. 또한 `cd agents/...` 표기는 같은 파일의 output/ 경로, 루트 CLAUDE.md 상태 감지 테이블, agents/CLAUDE.md 실행 명령과 동일한 레포 루트 기준 관례여서 해당 행만 결함으로 볼 수 없다.
- [P1|web-design] website/src/css/customTheme.scss:474 — .table-wrapper가 overflow: hidden이고 996px 이하에서 .markdown table이 display: block으로 바뀌지만 overflow-x: auto가 없어, 좁은 화면에서 넓은 표가 스크롤 불가 상태로 잘립니다.
  제안: .table-wrapper 또는 모바일 .markdown table에 `overflow-x: auto`를 주어 넓은 표를 가로 스크롤로 볼 수 있게 합니다.
  반박: Infima 기본 규칙(table{display:block;overflow:auto})이 빌드된 CSS에 그대로 포함되고 .markdown table 오버라이드는 overflow를 건드리지 않으므로, 996px 이하에서 표 자체가 overflow:auto로 가로 스크롤됩니다. .table-wrapper의 overflow:hidden은 border-radius 클리핑용일 뿐 표 내용을 잘라내지 않아 결함이 실재하지 않습니다.
- [P1|web-landing-ux] docs/00-overview/start-path.md:27 — 경로 2(개발팀과 함께)가 02 조직 단계를 건너뛰고 03 정책으로 직행하도록 안내하지만, 정책 에이전트는 output/organization/role-definition.md를 전제 조건으로 요구한다.
  제안: 경로 2 안내를 "02 조직 → 03 정책" 순서로 고치거나 정책 챕터의 전제 조건을 명시한다.
  반박: start-path.md 경로 2가 03 정책으로 직행 안내하는 것은 사실이나, 링크 대상인 docs/03-policy/index.md 13행에 Prerequisite 컴포넌트('2. 조직 구성' 링크)가 이미 있어 독자가 챕터 진입 즉시 02 선행 조건을 안내받는다. 발견이 제안한 시정(정책 챕터에 전제 조건 명시)이 이미 구현되어 있으므로 독자가 실패하는 결함은 실재하지 않는다.
- [P1|templates] templates/policy/license-allowlist.md:1 — 허용 라이선스 목록 템플릿(Permissive/Weak/Strong Copyleft/금지 4분류 + 분류학 절)과 output-sample(채널별 허용 원칙 + Network Copyleft 별도 분류 + 호환성 절)이 제목부터 분류 체계까지 전면 상이해 어느 쪽이 표준 구조인지 알 수 없다.
  제안: 채널별 구성(샘플 방식)을 정본으로 삼아 템플릿 골격을 재작성하거나, 템플릿 구조 유지 시 샘플을 재생성해 한쪽으로 통일한다.
  반박: 구조 차이는 실재하나 결함이 아니다. 템플릿은 {배포방식} 자리표시자와 "배포방식에 따라 조정 필요" 주석을 가진 적응용 골격이고, agent 03 스펙이 배포 방식별 재구성을 명시하며, 샘플은 복합 배포(4채널) 인스턴스다. 독자용 챕터(docs/03-policy/index.md:301)가 채널 매트릭스 구조를 기대 산출물로 문서화해 표준 구조가 명확하고, 템플릿 자체는 docs/website 어디에서도 독자에게 노출되지 않아 혼동 시나리오가 성립하지 않는다.
