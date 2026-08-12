# 다음 세션 작업 지시 (fable)

작성 2026-08-12. 대상 저장소는 `trustedoss/trusca` 와 `trustedoss/trustedoss` 둘입니다.
발표에서 제시한 5단계를 TRUSCA에 실제로 적용하고, 가이드가 그 실제와 어긋나지 않게 만드는
작업입니다.

## 지금 상태

2026-08-12 기준으로 확인한 사실입니다. 착수 전에 다시 확인하세요. 특히 T0 은 하루 사이에
바뀔 수 있습니다.

| 항목                     | 상태                                                     |
| ------------------------ | -------------------------------------------------------- |
| TRUSCA `image-scan`      | main 에서 실패 중. worker 이미지 CRITICAL 9건 + HIGH 1건 |
| TRUSCA PR #57 (IaC 스캔) | 열려 있음. 새 job 은 통과, image-scan 만 빨강            |
| TRUSCA 4b·DAST           | 없음                                                     |
| IaC 미스컨피그           | HIGH 19건 (차트 15, Dockerfile 4). CRITICAL 0            |

TRUSCA에 이미 있는 것은 시크릿(gitleaks), SAST(bandit·semgrep·CodeQL), SCA(cdxgen+Trivy),
컨테이너 스캔, 4a(ai-review.yml), Dependabot, dogfood-scan 입니다.

## 손대지 말 것

- `trusca/CLAUDE.md` 는 비공개 유지입니다. `.gitignore:81` 에 있는 상태 그대로 둡니다.
  워크플로 경로 필터와 PR 템플릿이 이 파일을 가리키지만 그대로 둡니다. 사용자 결정입니다.
- `.trivyignore` 에 새 항목을 넣어 게이트를 통과시키지 마세요. 넣어야 한다면 기존 항목과 같은
  수준의 근거(CVE, 아티팩트 경로, 업스트림 상태, 도달 분석)를 갖추고, PR 본문에 이유를 씁니다.
- 발표 덱(`deck/index.html`)은 전달된 기록입니다. 수정하지 않습니다.

## 작업 단위

각 단위는 독립 PR 하나입니다. 순서는 T0 → T1 → 나머지입니다.

### T0. TRUSCA worker 이미지의 CRITICAL 9건 (최우선)

**왜 먼저인가.** main 이 빨간 상태라 모든 PR 이 그것을 물려받습니다. 새로 추가하는 게이트가
제대로 도는지 판단할 수 없고, 리뷰어가 빨강에 무뎌집니다.

**할 일.** 실패 로그에서 CRITICAL 9건의 패키지와 출처를 확인합니다. 대부분 worker 이미지에
번들된 다중 언어 툴체인(ORT, cdxgen, Gradle, Maven jar) 쪽일 가능성이 높습니다. 업스트림
버전을 올려 해결되는 것과 그렇지 않은 것을 나눕니다.

**완료 기준.** `image-scan (worker)` 가 main 에서 초록. 억제로 넘긴 항목이 있으면 각각 도달
분석이 붙어 있을 것.

**검증.**

```bash
gh run list --repo trustedoss/trusca --branch=main --workflow=ci.yml --limit 1
```

### T1. PR #57 머지 (IaC 스캔)

**배경.** `trivy config` 로 Helm 차트와 Dockerfile 을 스캔하는 워크플로입니다. 새 job 자체는
이미 통과했습니다. T0 이 끝나면 보드가 초록이 됩니다.

**주의.** `charts/trustedoss/ci/scan-values.yaml` 이 없으면 차트가 렌더되지 않고 Trivy 가
결과 0건으로 정상 종료합니다. 가드 스텝이 그것을 잡습니다. 이 구조를 리뷰에서 지우지 마세요.

**완료 기준.** 머지 완료. main 에서 `trivy config (helm chart + Dockerfiles)` 초록.

### T2. IaC HIGH 19건 처리

**할 일.** 두 덩어리로 나눠 별도 PR 로 진행합니다.

- Dockerfile 4건 (DS-0002, 컨테이너가 root 로 실행). `apps/backend/Dockerfile.prod` 는 이미
  해결되어 있으니 그 방식을 나머지 넷에 적용합니다. 볼륨 권한과 헬스체크가 깨지지 않는지
  확인이 필요합니다.
- 차트 15건. KSV-0118(security context 미지정) 9건, KSV-0014(root filesystem 쓰기 가능) 5건,
  KSV-0109(ConfigMap 에 secret) 1건. 마지막 것은 먼저 실제 시크릿인지 확인하세요.

**완료 기준.** HIGH 0건이 되면 `iac-security.yml` 의 `BLOCKING_SEVERITY` 를 `CRITICAL,HIGH`
로 올립니다. 이 승격이 T2 의 진짜 완료 조건입니다. 스캔만 있고 차단이 없으면 관측 단계에
머뭅니다.

**검증.**

```bash
trivy config --severity HIGH,CRITICAL \
  --helm-values charts/trustedoss/ci/scan-values.yaml charts/trustedoss
trivy config --severity HIGH,CRITICAL apps
```

### T3. DAST Baseline

**전제 확인.** 데모 호스트에서 `DEMO_READ_ONLY` 가 실제로 켜져 있는지 먼저 봅니다.
`DemoReadOnlyMiddleware` 가 GET·HEAD·OPTIONS 외를 기본 거부하므로, 켜져 있다면 능동 스캔의
위험 대부분이 이미 막혀 있습니다.

**할 일.** ZAP Baseline 을 데모 호스트에 겁니다. Baseline 은 트래픽을 관찰만 하고 공격
페이로드를 보내지 않습니다. Soft fail 로 시작합니다. `demo-health-canary.yml` 이 이미 같은
호스트를 주기적으로 두드리므로 붙일 자리가 있습니다.

**Full 은 이번 범위가 아닙니다.** 능동 스캔은 발견한 모든 파라미터에 실제 공격 페이로드를
보냅니다. 읽기 전용이라도 자원 고갈, 인증 경로 반복 시도로 인한 계정 잠금,
`demo_allow_sandbox_scans()` 가 켜졌을 때 열리는 스캔 인제스트 경로가 남습니다. 스캔 전용
인스턴스가 생긴 뒤에 다룹니다.

**완료 기준.** 워크플로가 돌고 리포트가 artifact 로 남을 것. 발견 항목은 이번에 고치지 않아도
됩니다.

### T4. 4b — 스키마 기반 퍼징

**핵심 판단.** Claude API 키 없이 진행합니다. `apps/backend/main.py:137` 의 `FastAPI()` 가
`openapi_url` 을 끄지 않았으므로 `/openapi.json` 이 그대로 나옵니다. schemathesis 가 그
스키마에서 타입·필수 여부·제약을 읽어 경계값을 만듭니다. 모델도 GPU 도 필요 없습니다.

**한계를 알고 시작하세요.** 스키마 기반은 타입과 제약만 압니다. 파라미터 이름이 경로처럼
보이니 경로 순회 문자열을 넣어본다는 식의 의미 기반 추론은 하지 못합니다. 비즈니스 로직
결함은 여전히 모델 쪽이 낫습니다. 이건 4b 전체가 아니라 4b 가 메우려는 공백의 일부입니다.

**기동은 재사용합니다.** `dogfood-scan.yml` 이 postgres, redis, backend, worker 를 띄우고
alembic 마이그레이션까지 돌립니다. 그 절차를 그대로 씁니다.

**먼저 정해야 하는 것.** 테스트 계정의 권한 범위입니다. 인증 없이 돌리면 전부 401 이 돌아와
아무것도 보지 못하고, 권한을 넓게 주면 위험한 경로까지 때립니다. RBAC 가 걸린 시스템이라
권한별로 결과가 달라집니다. 이건 기술 문제가 아니라 정책 결정이므로 사용자에게 확인하세요.

**완료 기준.** 주기 실행(주 1회 또는 main 푸시)으로 돌고, 결과가 artifact 로 남고, 차단
게이트가 아닐 것.

### G1~G3. 가이드 반영 (trustedoss 저장소)

| 번호 | 대상                     | 내용                                                            |
| ---- | ------------------------ | --------------------------------------------------------------- |
| G1   | `ai-coding/ai-fuzzing`   | 모델 없이 하는 방법 절 추가. 스키마 기반 퍼징과 그 한계         |
| G2   | `devsecops/dast`         | Baseline 과 Full 의 차이, 운영 중인 대상에 Full 을 걸 때의 위험 |
| G3   | `devsecops/iac-security` | TRUSCA 사례. 렌더 실패가 빈 게이트가 되는 문제와 가드           |

G3 의 교훈이 가장 값집니다. 필수 값 없이 Helm 차트를 스캔하면 Trivy 가 렌더 오류를 WARN 으로
남기고 결과 0건으로 정상 종료합니다. 검사 대상이 없는데 초록이 되는 형태이고, 이 프로젝트가
3단계에서 경계하는 바로 그 모양입니다. 일반적인 교훈이므로 IaC 페이지에 적습니다.

G1 과 G2 는 T4·T3 가 끝나기 전에도 쓸 수 있습니다. TRUSCA 사례를 넣는 부분만 나중에 채웁니다.

## 순서

```
T0 (main 복구)
 └→ T1 (PR #57 머지) ──→ G3
      ├→ T2 (HIGH 19건 → 차단 승격)
      ├→ T3 (DAST Baseline) ──→ G2 의 사례 부분
      └→ T4 (스키마 퍼징) ───→ G1 의 사례 부분

G1·G2 의 설명 부분은 언제든 착수 가능
```

## 품질 장치

**청크마다 같은 게이트를 통과시킵니다.** 작업 단위 하나가 끝날 때마다 아래를 전부 통과한
뒤에만 다음으로 넘어갑니다. 한 번에 여러 단위를 진행하지 마세요.

- trustedoss 저장소: `bash .claude/scripts/verify.sh` 13/13, `cd website && npm run build`
- trusca 저장소: 해당 PR 의 CI 전부 초록. 기존 실패는 T0 이 끝난 뒤에는 변명이 되지 않습니다

**독립 검증자를 역순으로 붙입니다.** 각 청크를 끝낸 뒤, 작업하지 않은 관점에서 결과를 다시
판정하세요. 특히 "이 게이트가 실제로 무언가를 검사하고 있는가"를 묻습니다. 이번 세션에서
Helm 렌더 실패가 그 질문으로 잡혔습니다. 초록 배지는 통과의 증거가 아닙니다.

**STATUS 를 먼저 커밋합니다.** 각 단위에 착수하기 전에 `docs/_plan/STATUS.md` 에 무엇을
시작하는지 적고 커밋하세요. 세션이 끊겨도 다음 세션이 이어받을 수 있습니다.

## 참고

이번 세션에서 만든 것입니다.

- trusca PR #57 — IaC 스캔 워크플로
- ai-coding-best-practice PR #33 (머지) — 4c 실물 `.mcp.json`, `.claude/settings.json`
- ai-coding-best-practice PR #34 (머지) — 런타임 이미지에서 pip 제거
- trustedoss `a70736f` — 억제 규칙 정정, 4a·4c 페이지를 실제 구현에 연결
