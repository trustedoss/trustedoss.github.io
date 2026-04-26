---
id: best-practice-repo
title: Best Practice 저장소
sidebar_label: Best Practice 저장소
sidebar_position: 8
---

# Best Practice 저장소

[5단계 전략](./strategy)의 1~5단계를 모두 구현한 참조 GitHub 저장소입니다.
fork해서 즉시 사용하거나, 설정 파일을 복사해 기존 프로젝트에 적용할 수 있습니다.

:::info 저장소
**[github.com/trustedoss/ai-coding-best-practice](http://github.com/trustedoss/ai-coding-best-practice)**
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
├── CLAUDE.md                          # 2단계: AI 규칙 내재화
├── .cursorrules                       # 2단계: Cursor 규칙
│
├── .gitleaks.toml                     # 3단계: 시크릿 탐지 설정
├── .grype.yaml                        # 3단계: SCA 임계값 설정
├── .semgrep.yml                       # 3단계: SAST 룰셋
│
├── renovate.json                      # 4단계: Renovate 자동 업데이트
│
├── k8s/
│   └── deployment.yaml                # IaC 보안 스캔 대상 샘플 (Checkov)
│
├── scripts/
│   └── ai-fuzz.py                     # AI 퍼징 실행 스크립트
│
└── .github/
    ├── dependabot.yml                 # 4단계: Dependabot 설정
    └── workflows/
        ├── secret-detection.yml       # 3단계: Gitleaks
        ├── sast.yml                   # 3단계: Semgrep
        ├── codeql.yml                 # 3단계: CodeQL (PR + 주 1회)
        ├── oss-policy.yml             # 3단계: syft + grype + 라이선스
        ├── iac-security.yml           # 3단계: Checkov (Dockerfile·K8s)
        ├── container-security.yml     # 3단계: Trivy
        ├── ai-review.yml              # 4단계: findings-driven AI 리뷰 (ANTHROPIC_API_KEY 등록 시 자동 활성화)
        ├── ai-fuzzing.yml             # 4단계: AI 퍼징 (주 1회 + Push)
        └── dast.yml                   # 5단계: OWASP ZAP (Push to main)
```

---

## 단계별 구현 내용

### 3단계 — CI/CD 자동 차단

| 영역          | 구현 파일                | 설명                                            |
| ------------- | ------------------------ | ----------------------------------------------- |
| 시크릿 탐지   | `secret-detection.yml`   | Gitleaks — PR마다 API 키·토큰 하드코딩 탐지     |
| SAST          | `sast.yml`               | Semgrep — OWASP Top 10 룰셋 + 커스텀 룰         |
| SAST (심층)   | `codeql.yml`             | CodeQL — PR 및 주 1회 스케줄 정적 분석          |
| SCA           | `oss-policy.yml`         | syft + grype — SBOM 생성·CVE 스캔·라이선스 검사 |
| IaC 보안      | `iac-security.yml`       | Checkov — Dockerfile·Kubernetes 설정 오류 탐지  |
| 컨테이너 보안 | `container-security.yml` | Trivy — Docker 이미지 취약점 스캔               |

### 4단계 — AI 방어 레이어

| 항목              | 구현 파일        | 설명                                                         |
| ----------------- | ---------------- | ------------------------------------------------------------ |
| AI 코드 리뷰 (4a) | `ai-review.yml`  | Semgrep·grype findings → Claude 검증·심층 해석 → PR 코멘트   |
| AI 퍼징 (4b)      | `ai-fuzzing.yml` | Claude가 엣지케이스 생성 → 앱 실행 → 5xx 탐지 (Push to main) |

### 5단계 — 지속적 모니터링·자동 교정

| 항목                 | 구현 파일        | 설명                                           |
| -------------------- | ---------------- | ---------------------------------------------- |
| 의존성 자동 업데이트 | `dependabot.yml` | 주간 의존성 업데이트 PR 자동 생성              |
| 패치 자동 병합       | `renovate.json`  | Critical 패치 자동 병합, Major는 검토 알림     |
| DAST                 | `dast.yml`       | OWASP ZAP Baseline — Push to main 시 동적 스캔 |

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

| 파일             | 수정 포인트                                           |
| ---------------- | ----------------------------------------------------- |
| `CLAUDE.md`      | 팀 라이선스 정책, 금지 패키지 목록 반영               |
| `.grype.yaml`    | 취약점 임계값 조정 (`high` ↔ `critical`)              |
| `.gitleaks.toml` | 조직 내부 패턴 예외 처리 추가                         |
| `.semgrep.yml`   | 언어·프레임워크별 룰셋 추가                           |
| `renovate.json`  | 자동 병합 범위, 업데이트 주기 조정                    |
| `dast.yml`       | 안정화 후 `fail_action: true`로 변경해 Hard fail 전환 |

---

## 관련 가이드

- [5단계 전략](./strategy) — 각 단계의 목적과 도입 순서
- [30분 완성 Quick CI/CD](./cicd-quick) — SCA 중심 최소 시작점
- [AI 보안 코드 리뷰](./ai-security-review) — AI를 활용한 의미론적 취약점 탐지
- [DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design) — 멀티 저장소·정책 거버넌스
