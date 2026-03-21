---
id: intro
title: DevSecOps
slug: intro
---

# DevSecOps

개발 파이프라인에 보안을 통합하는 실전 가이드입니다.

:::info 준비 중
이 섹션은 현재 준비 중입니다.
곧 아래 내용으로 찾아뵙겠습니다.
:::

## 다룰 내용

| 챕터 | 내용 | 상태 |
|---|---|---|
| SAST | 정적 분석 (Semgrep, CodeQL) | 준비 중 |
| SCA | 소프트웨어 구성 분석 (syft + grype) | 준비 중 |
| 시크릿 관리 | git-secrets, GitHub Secret Scanning | 준비 중 |
| 컨테이너 보안 | Trivy 기반 이미지 스캔 | 준비 중 |
| CI/CD 통합 | GitHub Actions 완성 워크플로우 | 준비 중 |

## 체계구축과의 연계

DevSecOps 는 [체계구축](/docs) 섹션에서
구축한 오픈소스 관리 체계를
개발 파이프라인에 자동화하는 다음 단계입니다.

```
오픈소스 관리 체계 구축
        ↓
DevSecOps 파이프라인 통합
        ↓
Trusted AI Coding 정책 자동 준수
```

## AI코딩과의 연계

[AI코딩](/ai-coding/intro) 섹션의
CI/CD 자동화는 이 섹션의 내용을 기반으로 합니다.

## 업데이트 알림

진행 상황은
[GitHub](https://github.com/haksungjang/trustedoss)
에서 확인하실 수 있습니다.
