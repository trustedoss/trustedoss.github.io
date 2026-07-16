---
작성일: 2026-07-09
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: [G3B.1 확장 — AI 컴포넌트까지 SBOM 범위 확대]'
셀프스터디 소요시간: 1시간
sidebar_label: '5.4 AI SBOM (선택)'
---

# AI SBOM: 모델과 데이터셋의 SBOM 만들기 (선택)

## 1. 이 챕터에서 하는 일

AI 시스템(모델을 개발하거나 도입해 운영)을 다루는 조직을 위한 **선택 챕터**입니다.
HuggingFace 모델 하나를 대상으로 CycloneDX **ML-BOM** 을 직접 생성하고, 모델 라이선스와
데이터셋 항목을 읽는 법을 실습합니다. AI 시스템이 없는 조직은 건너뛰어도 인증 여정에 영향이 없습니다.

전제 조건: [5.1 SBOM 생성](../sbom-generation/index.md)을 먼저 진행해 SBOM 개념과 도구 사용에
익숙한 상태여야 합니다. 실습에는 Docker 와 네트워크 연결이 필요합니다.

## 2. 배경 지식

### 왜 일반 SBOM으로 부족한가

코드 의존성만 담는 SBOM 은 AI 시스템의 두 가지 구성 요소를 놓칩니다.

- **사전 훈련 모델** — 표준화되지 않은 커스텀 라이선스(상업적 사용 조건, MAU 제한, 파생 모델 의무)가 많습니다.
- **학습 데이터셋** — CC 계열 오픈 데이터 라이선스의 저작자 표시, 동일 조건 의무가 따라옵니다.

이 둘을 SBOM 에 기록하는 확장이 AI SBOM 이고, 사실상의 표준 형식은
**CycloneDX ML-BOM**(모델 카드 메타데이터가 풍부)과 **SPDX 3.0 AI Profile**(라이선스 표현이 정밀) 두 가지입니다.

### 표준 요구사항과의 관계

ISO/IEC 5230과 18974의 SBOM 요구(G3B 계열)는 "공급 소프트웨어의 오픈소스 컴포넌트"가 대상이라,
AI SBOM 자체가 필수 요구는 아닙니다. 다만 모델·데이터셋을 제품에 포함해 공급한다면 그것도
오픈소스 컴포넌트이므로, 같은 원칙을 확장 적용하는 것이 이 챕터의 취지입니다.
개념 배경은 [SBOM 기본의 AI SBOM 절](../../00-overview/sbom-101.md)과
[AI 시스템 컴플라이언스](/ai-coding/iso42001)를 참조하세요.

:::tip 바로 보기 — 완성 예시 먼저
어떤 결과가 나오는지 먼저 보려면 [KWG AI SBOM 컴플라이언스 가이드](https://openchain-project.github.io/OpenChain-KWG/guide/ai-sbom_guide/)의
조항 체크리스트와 도구 실행 결과 화면을 훑어보세요. cdxgen 실행 결과로 AI 컴포넌트의
라이선스 정보 공백을 실증한 사례도 실려 있습니다.
:::

## 3. 셀프 스터디

:::info 셀프스터디 모드 (약 1시간)
실습에는 Docker 실행 환경과 네트워크 연결이 필요합니다.
:::

실습 도구는 [BomLens](https://github.com/sktelecom/bomlens)를 사용합니다. HuggingFace 모델
식별자를 입력하면 CycloneDX 1.7 ML-BOM 과 고지문, 위험 리포트를 로컬(Docker)에서 생성합니다.

### 1단계 — BomLens 준비

```bash
git clone https://github.com/sktelecom/bomlens.git
cd bomlens
docker pull ghcr.io/sktelecom/bomlens:latest
```

:::warning macOS/Windows 는 Docker 파일 공유 경로에서 실행하세요
`/tmp` 처럼 Docker Desktop 파일 공유 밖 경로에서 실행하면 스캔은 성공해도 산출물이 호스트로
복사되지 않습니다(도구가 안내 메시지를 출력합니다). 홈 디렉토리 아래에서 클론해 실행하세요.
:::

### 2단계 — 모델 스캔으로 ML-BOM 생성

```bash
./scripts/scan-sbom.sh --project bert-base --version 1.0.0 \
  --model "google-bert/bert-base-uncased" --generate-only
```

- `--model` 에 HuggingFace 모델 식별자를 넣습니다. 자신이 검토할 모델로 바꿔 실행하세요.
- 모델 스캔용 전용 이미지(`ghcr.io/sktelecom/bomlens-aibom`)가 자동으로 내려받아집니다.
- 산출물은 `bert-base_1.0.0/` 하위 폴더에 생성됩니다: `bert-base_1.0.0_bom.json`(CycloneDX 1.7 ML-BOM),
  고지문(notice), 위험 리포트(risk-report), 보안(security) 리포트, NTIA 최소 요소 적합성 점검 결과.
  모델에는 패키지 CVE 가 없으므로 보안 리포트는 취약점 0건으로 나오는 것이 정상입니다.

### 3단계 — ML-BOM 읽기

생성된 `bom.json` 에서 아래를 확인합니다.

- **모델 라이선스**: 모델 컴포넌트의 라이선스 항목이 커스텀 라이선스(예: Llama Community License)인지,
  표준 라이선스(Apache-2.0 등)인지 확인하고 [5.1의 라이선스 검토 절차](../sbom-generation/index.md)와
  동일하게 허용 목록과 대조합니다.
- **모델 카드 메타데이터**: 용도, 제한 사항 등 모델 카드에서 온 항목을 확인합니다.
- **정보 공백**: 라이선스나 데이터셋 항목이 비어 있으면 그 자체가 발견입니다 — HuggingFace 모델
  카드에서 직접 확인해 보완 기록을 남깁니다 (KWG 가이드의 "라이선스 공백 실증"과 같은 상황).

### 대안 도구 — OWASP AIBOM Generator

표준 중립 대안으로는 OWASP AIBOM Generator 가 있습니다. HuggingFace 모델을 대상으로 AI SBOM 을
생성하며, 설치와 실행 방법은 [KWG AI SBOM 가이드 — 도구](https://openchain-project.github.io/OpenChain-KWG/guide/ai-sbom_guide/)를 참조하세요.

### 코드 SBOM과의 관계

AI 서비스의 전체 그림은 두 SBOM 의 결합입니다: 코드 의존성 SBOM([5.1](../sbom-generation/index.md),
syft/cdxgen)과 이 챕터의 모델 ML-BOM. 배포 단위별로 두 문서를 함께 보관하면
[5.2 SBOM 관리](../sbom-management/index.md)의 보관·공유 절차를 그대로 적용할 수 있습니다.

### 자동화로 잇기

모델 버전이 바뀔 때마다 ML-BOM 을 재생성하도록 CI 에 넣을 수 있습니다. 위 스캔 명령을
[DevSecOps — SCA](/devsecops/sca)의 SBOM 생성 잡과 같은 방식으로 워크플로에 추가하면 됩니다.

## 4. 완료 확인 체크리스트

- [ ] 일반 SBOM 과 AI SBOM 의 차이(모델, 데이터셋 라이선스)를 설명할 수 있다
- [ ] HuggingFace 모델 하나의 ML-BOM 을 생성했다
- [ ] 생성된 ML-BOM 에서 모델 라이선스를 확인하고 허용 목록과 대조했다
- [ ] 라이선스·데이터셋 정보 공백이 있으면 모델 카드로 보완 확인했다

## 5. 다음 단계

- SBOM 보관과 공급망 공유: [5.2 SBOM 관리](../sbom-management/index.md)
- 취약점 대응(코드 의존성 대상): [5.3 취약점 분석과 대응](../vulnerability/index.md)
- AI 시스템 전반의 컴플라이언스: [AI 시스템 컴플라이언스](/ai-coding/iso42001)
