---
id: intro
title: trustedoss 소개
sidebar_label: 소개
sidebar_position: 1
slug: /
---

# trustedoss

**소프트웨어 공급망 보안과 오픈소스 관리 체계를 처음부터 완성까지**
ISO/IEC 5230 & 18974 기반 기업 오픈소스 관리 체계 구축 실전 키트

---

## 이 키트로 무엇을 할 수 있나요?

오픈소스 관리 경험이 전혀 없는 신규 담당자도 이 키트를 따라가면 **ISO/IEC 5230**(라이선스 컴플라이언스)과 **ISO/IEC 18974**(보안 보증) 자체 인증 선언까지 완성할 수 있습니다.

- Agent가 회사 상황에 맞는 **23개 산출물**을 자동으로 생성합니다
- **두 가지 표준을 동시에** 달성합니다 (공통 기반 40% 절약)
- **셀프스터디** 또는 **하루 워크숍** 두 가지 방식으로 활용 가능합니다

---

## 빠른 시작

### Claude Code 사용자 (권장)

```bash
git clone https://github.com/haksungjang/trustedoss.git
cd trustedoss && claude
# "어디서 시작해야 해?" 입력
```

### 문서만 읽으시는 분

왼쪽 사이드바에서 **00-overview → 00b-supply-chain → 01-setup** 순서로 읽어보세요.
각 챕터 하단의 **다음 단계** 링크를 따라가시면 됩니다.

---

## 전체 챕터

| 챕터 | 내용 | 워크숍 모듈 |
|------|------|-----------|
| [00 개요](./00-overview/index.md) | 두 표준 개요 및 체크리스트 매핑 | M0 |
| [00b 공급망](./00b-supply-chain/index.md) | 소프트웨어 공급망 보안 + SBOM 개념 | M0 |
| [01 환경 준비](./01-setup/index.md) | Docker, Git, Claude Code 설치 | 사전 준비 |
| [02 조직](./02-organization/index.md) | 조직 구성 및 담당자 지정 | M1 |
| [03 정책](./03-policy/index.md) | 오픈소스 정책 수립 | M1 |
| [04 프로세스](./04-process/index.md) | 오픈소스 프로세스 설계 | M2 |
| [05 SBOM 생성](./05-tools/sbom-generation/index.md) | SBOM 생성 및 라이선스 분석 | M3 |
| [05 SBOM 관리](./05-tools/sbom-management/index.md) | SBOM 관리 및 공급망 공유 | M4 |
| [05 취약점](./05-tools/vulnerability/index.md) | 취약점 분석 및 대응 | M5 |
| [06 교육](./06-training/index.md) | 교육 체계 구축 | M6 |
| [07 인증](./07-conformance/index.md) | 자체 인증 선언 | M6 |

---

## 두 가지 사용 경로

### 셀프스터디 (8–12시간)

혼자서 며칠에 걸쳐 진행합니다. 각 챕터의 **배경 지식** 섹션을 충분히 읽고 실습합니다.

→ `docs/00-overview/` 부터 시작하세요

### 워크숍 (7시간 30분)

강사와 함께 팀이 하루에 완성합니다. 핵심 단계에 집중하여 실습합니다.

→ [워크숍 핸드아웃](https://github.com/haksungjang/trustedoss/blob/main/workshop/student-handout.md)을 참고하세요

:::info 워크숍 신청 안내
OpenChain KWG 커뮤니티에서 정기 워크숍을 운영합니다. 일정은 추후 업데이트 예정입니다.
[OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/) 에서 소식을 확인하세요.
:::

---

## 관련 링크

- [OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/)
- [ISO/IEC 5230](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974](https://www.iso.org/standard/86450.html)
- [OpenChain 자체 인증 등록](https://www.openchainproject.org/conformance)
