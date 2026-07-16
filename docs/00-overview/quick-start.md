---
description: '5분 만에 시작하는 기업 오픈소스 관리. 무설치 데모로 결과를 먼저 보고 AI 에이전트로 첫 산출물을 만듭니다.'
작성일: 2026-06-05
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
셀프스터디 소요시간: 5분
sidebar_position: 1
sidebar_label: 5분 빠른 시작
---

# 5분 빠른 시작

TrustedOSS는 AI 에이전트로 <Term k="openchain">OpenChain</Term>(ISO/IEC 5230·18974) 기업 오픈소스 관리 산출물을 회사 맞춤으로 자동 생성해, <Term k="self-certification">자체 인증</Term> 선언까지 가장 빠르게 도달하도록 돕습니다. 오픈소스 관리를 처음 맡으셨어도 단계별로 따라오면 됩니다.

## 언제 쓰나요

- 기업 오픈소스 관리를 처음 맡아 무엇부터 할지 막막할 때
- 자체 인증에 필요한 정책, 프로세스, <Term k="sbom">SBOM</Term> 등 산출물을 빠르게 만들어야 할 때
- 만든 정책을 CI 파이프라인과 AI 코딩 도구에 자동으로 적용하고 싶을 때

## 지금 해보기

### 1. 결과부터 보기 (무설치·무API키, 5분)

설치 없이 브라우저에서 SBOM 분석 결과를 바로 확인해 보세요.

- [SBOM 샘플 체험 열기](pathname:///tools/sbom-sample-demo.html)

생성되는 산출물의 실제 형태가 궁금하면 [정책 산출물 Best Practice](/reference/samples/policy)도 참고하세요.

### 2. 내 산출물 만들기 (AI 에이전트, 약 15분)

가장 먼저 만드는 산출물은 조직의 역할과 책임 정의입니다. 에이전트가 질문하고 회사 맞춤 문서를 생성합니다.

저장소를 아직 클론하지 않았다면 먼저 받아 두세요. [환경 준비: 실습에 필요한 도구 설치](../01-setup/index.md)를 이미 마쳤다면 이 단계는 건너뜁니다.

```bash
git clone https://github.com/trustedoss/trustedoss-agents.git
cd trustedoss-agents
```

:::tip 실행 전 확인
Claude 세션이 열려 있다면 먼저 종료(`/exit` 또는 `Ctrl+C`)하세요. 아래 명령은 위에서 이동해 둔 `trustedoss-agents` 저장소 루트에서 실행합니다. (새 터미널을 열었다면 먼저 `cd trustedoss-agents`)
:::

```bash
cd agents/02-organization-designer
claude
```

에이전트가 끝나면 산출물을 확인하세요: `ls output/organization/` — 파일 3개가 보이면 성공입니다.

## 다음 단계

- 내 상황에 맞는 진행 경로를 고르려면 [내게 맞는 시작 경로](./start-path.md)를 보세요.
- 전체 여정을 보려면 [개요: 두 표준과 전체 여정](./index.md)으로 가세요.
- 환경부터 준비하려면 [환경 준비](../01-setup/index.md) 챕터로 가세요.
