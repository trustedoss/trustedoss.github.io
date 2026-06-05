---
id: intro
title: 레퍼런스
slug: intro
description: '산출물 Best Practice, 정본 개념 페이지(라이선스 분류, 취약점 대응 기한), 용어집, 에이전트 선택 가이드를 모은 레퍼런스.'
---

# 레퍼런스

오픈소스 관리 체계 구축에 필요한 참조 자료를 모아둔 섹션입니다.

## 산출물 Best Practice

각 단계별 agent가 생성하는 산출물의 완성 예시입니다.
규모별(스타트업 / 중소기업 / 대기업) 3가지 프로필을 제공합니다.
자신의 `output/` 폴더 결과물과 비교하여 빠진 항목을 확인하세요.

| 산출물                                                                    | 대응 Agent            | 바로가기                                 |
| ------------------------------------------------------------------------- | --------------------- | ---------------------------------------- |
| 조직 (role-definition, raci-matrix, appointment-template)                 | organization-designer | [조직 산출물](./samples/organization)    |
| 정책 (oss-policy, license-allowlist)                                      | policy-generator      | [정책 산출물](./samples/policy)          |
| 프로세스 (usage-approval, distribution-checklist, vulnerability-response) | process-designer      | [프로세스 산출물](./samples/process)     |
| SBOM (sbom.cdx.json, license-report, copyleft-risk)                       | sbom-guide / analyst  | [SBOM 산출물](./samples/sbom)            |
| 취약점 (cve-report, remediation-plan)                                     | vulnerability-analyst | [취약점 산출물](./samples/vulnerability) |
| 교육 (curriculum, completion-tracker, resources)                          | training-manager      | [교육 산출물](./samples/training)        |
| 인증 (gap-analysis, declaration-draft, submission-guide)                  | conformance-preparer  | [인증 산출물](./samples/conformance)     |

## 개념 심화

본문에서 링크하는 정본 개념 페이지입니다. 정책·프로세스·도구 챕터는 여기를 기준으로 합니다.

| 문서                                                        | 내용                                                 |
| ----------------------------------------------------------- | ---------------------------------------------------- |
| [라이선스 분류](./concepts/license-classification)          | 분류 기준, 배포 방식별 영향, 배포 채널 허용 매트릭스 |
| [취약점 대응 기한과 VEX](./concepts/vulnerability-response) | CVSS 심각도별 대응 기한(KWG 기준선·조직 SLA), VEX    |
| [용어집](./glossary)                                        | 라이선스·SBOM·보안·조직 용어 풀이                    |

## 에이전트 선택 가이드

어느 상황에 어느 에이전트를 쓰는지, 에이전트와 챕터와 산출물의 매핑은 [AI 에이전트로 산출물 만들기](/docs/overview/agents)에 정리돼 있습니다.

## 도구와 규제 더 알아보기

| 주제                  | 바로가기                                                                                                                                              |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| SBOM 생성 도구 심화   | [SBOM 생성](/docs/tools/sbom-generation) (syft, cdxgen)                                                                                               |
| 취약점 관리 도구 심화 | [취약점 분석과 대응](/docs/tools/vulnerability) (grype, OSV)                                                                                          |
| KWG 생태계 도구       | [KWG 오픈소스 가이드 — 도구](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/4-tool/) (FOSSLight, SW360, FOSSology) |
| 규제 동향             | [소프트웨어 공급망 보안](/docs/overview/supply-chain) (EU CRA, EO 14028, 국내 SBOM 동향)                                                              |
| SKT 오픈소스 가이드   | [바로가기](https://sktelecom.github.io)                                                                                                               |
