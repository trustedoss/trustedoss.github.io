---
id: monitoring
title: 지속적 모니터링 · 자동 교정
sidebar_label: 모니터링 · 자동 교정
sidebar_position: 11
---

# 지속적 모니터링 · 자동 교정

CI/CD 게이트는 배포 시점의 코드 상태를 검사하지만, 배포 이후 발생하는 신규 취약점에는 대응할 수 없습니다.
Dependabot·Renovate·정기 스캔을 조합하면 프로덕션 환경의 취약점을 지속적으로 탐지하고 자동으로 패치 PR을 생성할 수 있습니다.

:::tip 아래 설정은 예시입니다 — 작동하는 전체 구현은 참조 저장소에
이 페이지의 YAML·명령은 핵심을 보여주는 예시입니다. 복사해 바로 쓸 수 있는 전체 파이프라인(정책 파일·샘플 앱 포함)은 [Best Practice 저장소](/ai-coding/best-practice-repo)에서 확인하세요.
:::

:::note 예시의 태그 표기와 실제 운영 설정
아래 예시는 읽기 쉽도록 `@v7` 같은 태그를 그대로 썼습니다. 태그는 나중에 다른 커밋을 가리키도록 바뀔 수 있으므로, 실제 운영 워크플로에서는 액션을 커밋 SHA로 고정하고 `permissions:` 로 잡마다 필요한 권한만 부여하세요. 이유와 방법은 [파이프라인 자체 보안](/devsecops/pipeline-security)에서 다룹니다.
:::

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
      time: '09:00'
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

GitHub의 Dependabot은 두 가지 설정을 구분해 활성화합니다. **Security Alerts**는 GitHub
Advisory Database 기반으로 취약한 의존성을 알림으로 알려주고, 수정 PR까지 자동으로 만들려면
**Dependabot security updates**를 추가로 켜야 합니다. 둘 다 저장소 Settings의
Code security 메뉴에서 활성화합니다.

---

## Renovate 설정

Renovate는 Dependabot보다 세밀한 정책 설정이 가능하며 GitHub·GitLab·Bitbucket 모두 지원합니다.
self-hosted 방식으로 GitLab에서도 동일하게 사용 가능합니다.

```json
// renovate.json

{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
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

| 항목        | Dependabot  | Renovate                |
| ----------- | ----------- | ----------------------- |
| 플랫폼      | GitHub 전용 | GitHub·GitLab·Bitbucket |
| 설정 복잡도 | 낮음        | 높음 (유연성 높음)      |
| 자동 병합   | 제한적      | 세밀한 정책 설정 가능   |
| 그룹 PR     | 가능        | 가능 (더 세밀)          |
| 비용        | 무료        | 무료 (self-hosted)      |

---

## 두 도구가 보지 못하는 것

Dependabot과 Renovate는 매니페스트에 선언된 패키지를 갱신합니다. `requirements.txt`,
`package.json`, `go.mod` 에 이름이 적혀 있어야 대상이 됩니다. 선언되지 않은 것은 두 도구의
시야 밖에 있습니다.

실행 환경에는 선언되지 않은 패키지가 함께 들어갑니다. 베이스 이미지에 미리 설치된 것,
그리고 설치한 도구가 자기 안에 번들한 것입니다.

**실제 사례.** [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice)
저장소의 컨테이너 스캔이 HIGH 2건으로 실패한 적이 있습니다.

| 패키지     | 취약점              | 설치 버전 | 수정 버전 |
| ---------- | ------------------- | --------- | --------- |
| msgpack    | GHSA-6v7p-g79w-8964 | 1.1.2     | 1.2.1     |
| setuptools | CVE-2025-47273      | 70.3.0    | 78.1.1    |

둘 다 `requirements.txt` 에 없었습니다. `site-packages/pip/_vendor/` 안, 즉 pip 자체에 들어
있는 라이브러리였습니다. Dependabot과 Renovate는 이 둘을 보지 못했고, 게이트가 3개월 넘게
빨간 상태로 남아 있었습니다.

이 저장소는 Dependabot에 docker 생태계도 등록해 두었지만 도움이 되지 않았습니다. docker
생태계는 `FROM` 의 태그를 갱신합니다. `python:3.14-slim` 처럼 패치 버전이 고정되지 않은
태그에는 올릴 버전이 없고, 이미지 안에 설치된 패키지는 어느 경우에도 대상이 아닙니다.

### 무엇으로 메우는가

| 대응                   | 내용                                                                          |
| ---------------------- | ----------------------------------------------------------------------------- |
| 이미지 스캔을 게이트로 | 매니페스트가 아니라 빌드된 이미지를 스캔해야 이 영역이 보입니다 (Trivy·grype) |
| 정기 실행              | PR 때만 돌리면 새 취약점이 공개된 뒤 다음 PR까지 발견되지 않습니다            |
| 런타임에서 도구 제거   | 컨테이너에 패키지 관리자를 남기지 않으면 그것이 번들한 트리도 함께 사라집니다 |
| 억제는 근거와 함께     | 억제 자체가 문제는 아닙니다. 근거 없는 억제가 문제입니다 (아래 참고)          |

위 사례는 `pip install` 직후 pip을 제거하는 것으로 해결했습니다. 런타임 컨테이너에는 패키지
관리자가 필요하지 않습니다. 같은 원리가 빌드 도구, 컴파일러, 셸 유틸리티에도 적용됩니다.

### 억제 파일을 쓸 때의 기준

업스트림이 아직 고치지 않았거나, 취약한 코드 경로를 실제로 호출하지 않는 경우가 있습니다.
이때 `.trivyignore` 로 항목을 제외하는 것은 정당합니다. 다만 무엇을 왜 제외했는지 남지 않으면
그냥 게이트를 끈 것과 구분되지 않습니다.

[TRUSCA](https://github.com/trustedoss/trusca)의 `.trivyignore` 는 항목마다 아래를 요구합니다.

- CVE 식별자와 해당 아티팩트, 그리고 스캐너가 보고한 경로
- 업스트림 수정 상태 (미수정인지, 수정됐지만 번들에 아직 안 들어왔는지)
- 도달 분석. 취약한 진입점을 이 프로젝트가 실제로 호출하지 않는다는 근거를 코드 위치와 함께 적습니다

도달 가능한 취약점은 억제 대상이 아니며 고칠 때까지 병합을 막습니다. 전체 항목은 180일마다,
또는 해당 도구가 새 릴리스를 내면 그때 다시 판단합니다. 이 정도가 갖춰지면 억제 파일은
숨기는 수단이 아니라 판단 기록이 됩니다.

---

## 정기 스캔 자동화

PR 단계 외에도 배포된 코드를 주기적으로 스캔하는 스케줄 워크플로우를 별도로 운영합니다.

```yaml
# .github/workflows/scheduled-scan.yml

name: Scheduled Security Scan

on:
  schedule:
    - cron: '0 2 * * *' # 매일 새벽 2시
  workflow_dispatch: # 수동 실행 가능

jobs:
  sca-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v7

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: Scan for new CVEs
        uses: anchore/scan-action@v7
        with:
          sbom: sbom.cdx.json
          fail-build: true
          severity-cutoff: critical

      - name: Upload SBOM
        uses: actions/upload-artifact@v7
        with:
          name: sbom-scheduled-${{ github.run_id }}
          path: sbom.cdx.json
          retention-days: 365 # 연간 보관

  container-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Scan production image
        uses: aquasecurity/trivy-action@0.36.0
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

## 실제 운영 사례

TRUSCA 는 이 층을 세 갈래로 운영합니다.

- [dependabot.yml](https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml) — npm, pip, docker, github-actions 네 생태계의 여섯 항목을 덮습니다
- [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml) — 매일 07:00 UTC 에 SBOM 을 다시 만들고 취약점을 재스캔합니다
- [dogfood-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml) — 자사 SCA 로 자기 저장소를 스캔합니다

마지막 워크플로우는 기본값이 advisory(비차단)이고 `fail_on_gate` 입력으로 차단을 켜도록
설계돼 있습니다. 관측부터 시작해 차단으로 올리는 순서를 그대로 구현한 예입니다.

## 셀프 스터디 — 레벨 2 자동화

:::tip Claude Code로 자동화 워크플로우 생성
아래 agent들은 CI/CD 파이프라인과 연동해서
보안 분석을 완전히 자동화하는 워크플로우 파일을 생성합니다.
:::

**사전 조건**: [Trusted OSS Agent 저장소](https://github.com/trustedoss/trustedoss-agents) 클론 필요

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

보안 스캔 결과(grype, Semgrep, 라이선스 위반)에서 설정한 심각도 이상을
GitHub·GitLab Issues로 자동 등록하는 워크플로우를 생성합니다.
CVE ID 기준 중복 방지 로직을 포함합니다.

```bash
cd agents/level2-automation/issue-tracker
claude
```

생성 산출물:

- `.github/workflows/security-issue-tracker.yml`
- `gitlab-issue-tracker.yml` (GitLab CI 변환 버전)
- `ISSUE-TRACKER-SETUP.md` (토큰 권한·라벨·비용 설정 가이드)

:::info GitHub Actions vs GitLab CI
GitHub Actions는 실제 동작 검증된 YAML을 제공합니다.
GitLab CI는 동일 기능의 변환 패턴과 주석을 포함합니다.
두 플랫폼 모두 ANTHROPIC_API_KEY를 Secret/Variable로 등록해야 합니다.
:::

---

## 다음 단계

- ISO/IEC 18974 요구사항과 구현 매핑: [ISO 표준 연계](./iso-mapping)
