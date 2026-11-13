---
id: best-practice-repo
title: Best Practice 저장소
sidebar_label: Best Practice 저장소
sidebar_position: 10
---

# Best Practice 저장소

[5단계 전략](./strategy)과 [테스트 환경](./testing)·[협업](./collaboration) 통제를 CI 워크플로와 설정 파일로 구현한 참조 GitHub 저장소입니다.
fork해서 즉시 사용하거나, 설정 파일을 복사해 기존 프로젝트에 적용할 수 있습니다.

4c(에이전트·MCP 도구 거버넌스)는 CI 가 아니라 개발자 워크스테이션의 에이전트를 대상으로
하므로 워크플로가 아닌 설정 파일(`.mcp.json`, `.claude/settings.json`)로 들어 있습니다.
조직 전체에 강제하는 방법은 [에이전트와 MCP 도구 거버넌스](./agent-governance)를 참고하세요.

:::info 저장소
**[github.com/trustedoss/ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice)**
:::

---

## 저장소 구성

```
ai-coding-best-practice/
├── README.md                          # 배지 + 단계별 설명 + 가이드 링크
├── src/
│   └── app.py                         # 샘플 Python 웹 앱 (의존성 포함)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml                 # DAST·AI 퍼징용 앱 기동
│
├── CLAUDE.md                          # 2단계: AI 규칙 내재화 + 4c: MCP 서버 추가 절차 + 테스트 정책
├── pyproject.toml                     # 테스트: pytest·mutmut 설정
├── requirements-dev.txt               # 테스트: pytest·pytest-cov·mutmut (버전 고정)
├── .cursorrules                       # 2단계: Cursor 규칙
│
├── .mcp.json                          # 4c: 승인한 MCP 서버 (현재 비어 있음)
├── .claude/
│   └── settings.json                  # 4c: 에이전트 권한 (읽기 차단·승인 필요 명령·tests/ 수정 승인)
│
├── .gitleaks.toml                     # 3단계: 시크릿 탐지 설정
├── .grype.yaml                        # 3단계: SCA 임계값 설정
├── .semgrep.yml                       # 3단계: SAST 룰셋
│
├── renovate.json                      # 5단계: Renovate 자동 업데이트
│
├── k8s/
│   └── deployment.yaml                # IaC 보안 스캔 대상 샘플 (Checkov)
│
├── tests/
│   └── test_app.py                    # 테스트: 동작 테스트 (에이전트 작업의 완료 기준)
│
├── scripts/
│   ├── ai-fuzz.py                     # AI 퍼징 실행 스크립트
│   └── check-test-integrity.py        # 테스트: PR 의 테스트 약화 탐지
│
└── .github/
    ├── CODEOWNERS                     # 협업: tests/·에이전트 규칙·CI 담당자 리뷰
    ├── pull_request_template.md       # 협업: AI 사용·사람의 결정·테스트 확인 기록
    ├── dependabot.yml                 # 5단계: Dependabot 설정
    └── workflows/
        ├── secret-detection.yml       # 3단계: Gitleaks
        ├── sast.yml                   # 3단계: Semgrep
        ├── codeql.yml                 # 3단계: CodeQL (PR + 주 1회)
        ├── oss-policy.yml             # 3단계: syft + grype + 라이선스
        ├── iac-security.yml           # 3단계: Checkov (Dockerfile·K8s)
        ├── container-security.yml     # 3단계: Trivy
        ├── ai-review.yml              # 4단계: findings-driven AI 리뷰 (ANTHROPIC_API_KEY 등록 시 자동 활성화)
        ├── ai-fuzzing.yml             # 4단계: AI 퍼징 (주 1회 + Push)
        ├── dast.yml                   # 5단계: ZAP (Push to main)
        ├── tests.yml                  # 테스트: pytest + 커버리지 하한 90% (차단)
        ├── test-integrity.yml         # 테스트: 테스트 약화 탐지 (차단, 라벨로 해제)
        ├── mutation.yml               # 테스트: mutmut 변이 테스트 (주 1회, 권고)
        └── pr-size.yml                # 협업: 400줄 초과 PR 분할 권고
```

---

## 단계별 구현 내용

### 3단계: CI/CD 자동 차단

| 영역          | 구현 파일                | 설명                                           |
| ------------- | ------------------------ | ---------------------------------------------- |
| 시크릿 탐지   | `secret-detection.yml`   | Gitleaks: PR마다 API 키·토큰 하드코딩 탐지     |
| SAST          | `sast.yml`               | Semgrep: OWASP Top 10 룰셋 + 커스텀 룰         |
| SAST (심층)   | `codeql.yml`             | CodeQL: PR 및 주 1회 스케줄 정적 분석          |
| SCA           | `oss-policy.yml`         | syft + grype: SBOM 생성·CVE 스캔·라이선스 검사 |
| IaC 보안      | `iac-security.yml`       | Checkov: Dockerfile·Kubernetes 설정 오류 탐지  |
| 컨테이너 보안 | `container-security.yml` | Trivy: Docker 이미지 취약점 스캔               |

### 4단계: AI 방어 레이어

| 항목              | 구현 파일                            | 설명                                                                     |
| ----------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| AI 코드 리뷰 (4a) | `ai-review.yml`                      | Semgrep·grype findings → Claude 검증·심층 해석 → PR 코멘트               |
| AI 퍼징 (4b)      | `ai-fuzzing.yml`                     | Claude가 엣지케이스 생성 → 앱 실행 → 5xx 탐지 (Push to main)             |
| MCP 거버넌스 (4c) | `.mcp.json`, `.claude/settings.json` | MCP 서버 자동 승인 차단, 시크릿 읽기 차단, 외부 통신·배포 명령 사람 승인 |

### 5단계: 지속적 모니터링·자동 교정

| 항목                 | 구현 파일        | 설명                                          |
| -------------------- | ---------------- | --------------------------------------------- |
| 의존성 자동 업데이트 | `dependabot.yml` | 주간 의존성 업데이트 PR 자동 생성             |
| 패치 자동 병합       | `renovate.json`  | Critical 패치 자동 병합, Major는 검토 알림    |
| DAST                 | `dast.yml`       | ZAP Baseline: Push to main 시 동적 스캔 |

### 협업과 테스트

| 항목             | 구현 파일                                               | 설명                                                                                 |
| ---------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 동작 테스트      | `tests/`, `tests.yml`                                   | pytest 와 커버리지 하한 90%. PR 차단                                                 |
| 테스트 약화 탐지 | `test-integrity.yml`, `scripts/check-test-integrity.py` | 테스트 삭제, skip·xfail 추가, assert 감소를 탐지. `test-change-approved` 라벨로 해제 |
| 변이 테스트      | `mutation.yml`                                          | mutmut 로 assert 가 잘못된 동작을 잡는지 측정. 주 1회 권고                           |
| PR 크기          | `pr-size.yml`                                           | 400줄 초과 시 분할 권고. 빌드는 실패시키지 않음                                      |
| 담당자 리뷰      | `.github/CODEOWNERS`                                    | `tests/`, 규칙 파일, 에이전트 권한, CI 변경에 담당자 리뷰 요청                       |
| 변경 기록        | `.github/pull_request_template.md`                      | AI 사용 여부, 사람이 내린 결정, 테스트 확인                                          |
| 에이전트 권한    | `.claude/settings.json`                                 | 에이전트가 `tests/` 를 고칠 때 사람 승인(`Edit(./tests/**)`)                         |

설계 배경은 [테스트 환경](./testing)과 [생산성과 협업](./collaboration)에 있습니다.

---

## 시작하기

**1. 저장소 fork**

```bash
git clone https://github.com/YOUR-ORG/ai-coding-best-practice.git
cd ai-coding-best-practice
```

**2. GitHub Secrets 등록**

| Secret 이름         | 용도                  | 필수 여부 |
| ------------------- | --------------------- | --------- |
| `ANTHROPIC_API_KEY` | AI 코드 리뷰, AI 퍼징 | 선택      |

**3. PR을 열어 파이프라인 확인**

```bash
git checkout -b test/pipeline-check
echo "# test" >> README.md
git commit -am "test: pipeline check"
git push origin test/pipeline-check
```

PR 생성 시 3단계 워크플로우 6개가 자동 실행됩니다.
4단계 AI 리뷰는 `ANTHROPIC_API_KEY` 등록 시 자동 활성화됩니다.
AI 퍼징과 DAST는 Push to main 또는 주간 스케줄에서 실행됩니다.

---

## 커스터마이징 포인트

| 파일                 | 수정 포인트                                           |
| -------------------- | ----------------------------------------------------- |
| `CLAUDE.md`          | 팀 라이선스 정책, 금지 패키지 목록 반영               |
| `.grype.yaml`        | 취약점 임계값 조정 (`high` ↔ `critical`)              |
| `.gitleaks.toml`     | 조직 내부 패턴 예외 처리 추가                         |
| `.semgrep.yml`       | 언어·프레임워크별 룰셋 추가                           |
| `renovate.json`      | 자동 병합 범위, 업데이트 주기 조정                    |
| `dast.yml`           | 안정화 후 `fail_action: true`로 변경해 Hard fail 전환 |
| `tests.yml`          | 커버리지 하한 `--cov-fail-under` 를 현재 수준에 맞춤  |
| `pr-size.yml`        | 권고 기준 `MAX_LINES`                                 |
| `.github/CODEOWNERS` | 계정을 팀(`@your-org/maintainers`)으로 교체           |

---

## 관련 가이드

- [5단계 전략](./strategy): 각 단계의 목적과 도입 순서
- [30분 완성 Quick CI/CD](./cicd-quick): SCA 중심 최소 시작점
- [AI 보안 코드 리뷰](./ai-security-review): AI를 활용한 의미론적 취약점 탐지
- [테스트 환경](./testing): 테스트 우선 작업, 테스트 약화 방어, 변이 테스트
- [생산성과 협업](./collaboration): PR 크기, 리뷰 부담 분산, 병렬 에이전트 작업
- [DevSecOps: 전사 파이프라인 설계](/devsecops/pipeline-design): 멀티 저장소·정책 거버넌스
