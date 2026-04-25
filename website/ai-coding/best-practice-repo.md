---
id: best-practice-repo
title: Best Practice 저장소
sidebar_label: Best Practice 저장소
sidebar_position: 8
---

# Best Practice 저장소

[4단계 전략](./strategy)의 1~4단계를 모두 구현한 참조 GitHub 저장소입니다.
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
└── .github/
    ├── dependabot.yml                 # 4단계: Dependabot 설정
    └── workflows/
        ├── secret-detection.yml       # 3단계: Gitleaks
        ├── sast.yml                   # 3단계: Semgrep
        ├── oss-policy.yml             # 3단계: syft + grype + 라이선스
        ├── container-security.yml     # 3단계: Trivy
        └── ai-review.yml             # 3단계 선택: AI 코드 리뷰 (기본 비활성화)
```

---

## 단계별 구현 내용

| 단계  | 구현 파일                                  | 설명                                            |
| ----- | ------------------------------------------ | ----------------------------------------------- |
| 2단계 | `CLAUDE.md`, `.cursorrules`                | 라이선스·보안 정책을 AI 도구에 내재화           |
| 3단계 | `.github/workflows/secret-detection.yml`   | Gitleaks — PR마다 시크릿 탐지                   |
| 3단계 | `.github/workflows/sast.yml`               | Semgrep — OWASP Top 10 룰셋 적용                |
| 3단계 | `.github/workflows/oss-policy.yml`         | syft + grype — SBOM 생성·CVE 스캔·라이선스 검사 |
| 3단계 | `.github/workflows/container-security.yml` | Trivy — Docker 이미지 취약점 스캔               |
| 3단계 | `.github/workflows/ai-review.yml`          | Claude API 코드 리뷰 (비활성화, 선택 적용)      |
| 4단계 | `.github/dependabot.yml`                   | 주간 의존성 업데이트 PR 자동 생성               |
| 4단계 | `renovate.json`                            | Critical 패치 자동 병합, Major 업데이트 알림    |

---

## 시작하기

**1. 저장소 fork**

```bash
# GitHub에서 fork 후 클론
git clone https://github.com/YOUR-ORG/ai-coding-best-practice.git
cd ai-coding-best-practice
```

**2. GitHub Secrets 등록**

| Secret 이름         | 용도         | 필수 여부                      |
| ------------------- | ------------ | ------------------------------ |
| `ANTHROPIC_API_KEY` | AI 코드 리뷰 | 선택 (`ai-review.yml` 사용 시) |

**3. PR을 열어 파이프라인 확인**

```bash
git checkout -b test/pipeline-check
echo "# test" >> README.md
git add README.md && git commit -m "test: pipeline check"
git push origin test/pipeline-check
```

GitHub에서 PR을 생성하면 3단계 워크플로우 전체가 자동 실행됩니다.

---

## 커스터마이징 포인트

| 파일             | 수정 내용                                                        |
| ---------------- | ---------------------------------------------------------------- |
| `CLAUDE.md`      | 팀 라이선스 정책·금지 패키지 목록 반영                           |
| `.grype.yaml`    | 취약점 임계값 조정 (`high` → `critical` 완화 또는 `medium` 강화) |
| `.gitleaks.toml` | 조직 내부 패턴 예외 처리 추가                                    |
| `.semgrep.yml`   | 언어·프레임워크에 맞는 룰셋으로 교체                             |
| `renovate.json`  | 자동 병합 범위, 업데이트 주기 조정                               |

---

## 관련 가이드

- [4단계 전략](./strategy) — 각 단계의 목적과 도입 순서
- [30분 완성 Quick CI/CD](./cicd-quick) — SCA 중심 최소 시작점
- [DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design) — 멀티 저장소·정책 거버넌스
