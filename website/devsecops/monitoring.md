---
id: monitoring
title: 지속적 모니터링 · 자동 교정
sidebar_label: 모니터링 · 자동 교정
sidebar_position: 10
---

# 지속적 모니터링 · 자동 교정

CI/CD 게이트는 배포 시점의 코드 상태를 검사하지만, 배포 이후 발생하는 신규 취약점에는 대응할 수 없습니다.
Dependabot·Renovate·정기 스캔을 조합하면 프로덕션 환경의 취약점을 지속적으로 탐지하고 자동으로 패치 PR을 생성할 수 있습니다.

## 왜 배포 후 모니터링이 필요한가

:::info CI/CD 게이트는 배포 시점의 스냅샷만 검사합니다
배포 후 발견된 신규 CVE는
파이프라인이 감지할 수 없습니다.
:::

**신규 CVE의 특성**: 오늘 배포한 코드가 내일 새로운 CVE로 취약해질 수 있습니다. Log4Shell처럼 수년간 사용된 라이브러리가 하루아침에 Critical 취약점이 된 사례가 대표적으로, 배포 시점의 스캔 결과는 시간이 지나면 의미를 잃습니다.

**모니터링 없는 파이프라인의 한계**: PR 단계에서 통과한 코드도 30일 후에는 취약점이 생길 수 있습니다. 지속적 스캔 없이는 프로덕션 환경의 위험을 인지하지 못한 채 서비스를 운영하게 됩니다.

**자동화의 필요성**: 수백 개의 의존성을 수동으로 추적하는 것은 현실적으로 불가능합니다. Dependabot·Renovate 같은 자동화 도구로 인간의 개입을 최소화하고 패치 속도를 높이는 것이 핵심입니다.

---

## Dependabot 설정

### 기본 설정

GitHub 저장소에 `.github/dependabot.yml`을 추가하면 의존성 업데이트·보안 패치 PR을 자동으로 생성합니다.

```yaml
# .github/dependabot.yml

version: 2
updates:
  # npm 의존성
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: "09:00"
    open-pull-requests-limit: 10
    groups:
      # 마이너·패치 업데이트는 그룹으로 묶어 PR 수 감소
      minor-and-patch:
        update-types:
          - minor
          - patch

  # Python 의존성
  - package-ecosystem: pip
    directory: /
    schedule:
      interval: weekly
    ignore:
      # 메이저 업데이트는 수동 검토
      - dependency-name: django
        update-types: [version-update:semver-major]

  # Docker 베이스 이미지
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly

  # GitHub Actions 자체 업데이트
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

### 보안 알림 자동 활성화

GitHub의 Dependabot Security Alerts는 저장소 설정에서 활성화하면 자동으로 작동합니다.
별도 설정 없이 GitHub Advisory Database 기반으로 Critical·High 취약점 발견 시 즉시 PR을 생성합니다.

---

## Renovate 설정

Renovate는 Dependabot보다 세밀한 정책 설정이 가능하며 GitHub·GitLab·Bitbucket 모두 지원합니다.
self-hosted 방식으로 GitLab에서도 동일하게 사용 가능합니다.

```json
// renovate.json

{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base"],
  "schedule": ["every weekend"],
  "vulnerabilityAlerts": {
    "enabled": true,
    "schedule": ["at any time"],
    "automerge": true,
    "automergeType": "pr"
  },
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "pr"
    },
    {
      "matchUpdateTypes": ["major"],
      "enabled": true,
      "automerge": false,
      "addLabels": ["major-update", "needs-review"]
    }
  ]
}
```

| 항목 | Dependabot | Renovate |
|------|-----------|----------|
| 플랫폼 | GitHub 전용 | GitHub·GitLab·Bitbucket |
| 설정 복잡도 | 낮음 | 높음 (유연성 높음) |
| 자동 병합 | 제한적 | 세밀한 정책 설정 가능 |
| 그룹 PR | 가능 | 가능 (더 세밀) |
| 비용 | 무료 | 무료 (self-hosted) |

---

## 정기 스캔 자동화

PR 단계 외에도 배포된 코드를 주기적으로 스캔하는 스케줄 워크플로우를 별도로 운영합니다.

```yaml
# .github/workflows/scheduled-scan.yml

name: Scheduled Security Scan

on:
  schedule:
    - cron: '0 2 * * *'  # 매일 새벽 2시
  workflow_dispatch:      # 수동 실행 가능

jobs:
  sca-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: Scan for new CVEs
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.cdx.json
          fail-build: true
          severity-cutoff: critical

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom-scheduled-${{ github.run_id }}
          path: sbom.cdx.json
          retention-days: 365  # 연간 보관

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Scan production image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ vars.PROD_IMAGE }}
          exit-code: 1
          severity: CRITICAL
          ignore-unfixed: true
```

---

## 알림 및 대응 체계

:::tip 알림은 담당자에게 즉시 전달되어야 합니다
:::

**GitHub Security 탭 활용**: Dependabot·코드 스캔 결과가 저장소 Security 탭에 자동 집계됩니다. Critical 발견 시 담당자에게 이메일·Slack 알림을 연동하면 대응 시간을 크게 단축할 수 있습니다.

**이슈 자동 생성**: 스케줄 스캔에서 신규 취약점 발견 시 GitHub Actions로 이슈를 자동 생성해 담당자 할당·SLA 추적이 가능합니다. 취약점이 이슈로 관리되면 패치 진행 상황을 팀 전체가 공유할 수 있습니다.

**SBOM 연도별 보관**: 정기 스캔에서 생성된 SBOM을 릴리즈 버전별로 영구 보관합니다. ISO/IEC 18974 감사 대응 증적으로 활용할 수 있으며, 특정 시점의 의존성 상태를 재현하는 데도 유용합니다.

---

## 셀프 스터디 — 레벨 2 자동화

:::tip Claude Code로 자동화 워크플로우 생성
아래 agent들은 CI/CD 파이프라인과 연동해서
보안 분석을 완전히 자동화하는 워크플로우 파일을 생성합니다.
:::

**사전 조건**: [Trusted OSS 저장소](https://github.com/trustedoss/trustedoss.github.io) 클론 필요

### PR 보안 분석 자동 코멘트

PR이 생성될 때마다 보안 스캔 결과를 Claude가 분석해서
PR에 자동으로 코멘트를 게시합니다.

```bash
cd agents/level2-automation/pr-comment
claude
```

생성 산출물:
- `.github/workflows/pr-security-comment.yml` (GitHub Actions)
- `gitlab-pr-comment.yml` (GitLab CI 변환 버전)

### 이슈 자동 등록 + Dependabot 분석

정기 스캔에서 High/Critical 취약점 발견 시 Issue를 자동 생성하고
Dependabot PR에 영향 분석 코멘트를 자동으로 게시합니다.

```bash
cd agents/level2-automation/issue-tracker
claude
```

생성 산출물:
- `.github/workflows/scheduled-security-scan.yml`
- `.github/workflows/dependabot-analysis.yml`
- `gitlab-scheduled-scan.yml` (GitLab CI 변환 버전)

:::info GitHub Actions vs GitLab CI
GitHub Actions는 실제 동작 검증된 YAML을 제공합니다.
GitLab CI는 동일 기능의 변환 패턴과 주석을 포함합니다.
두 플랫폼 모두 ANTHROPIC_API_KEY를 Secret/Variable로 등록해야 합니다.
:::

---

## 다음 단계

- ISO/IEC 18974 요구사항과 구현 매핑: [ISO 표준 연계](./iso-mapping)
