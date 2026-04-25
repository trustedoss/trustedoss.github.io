# AI 코딩 가이드 개선 계획

작성일: 2026-04-25  
목적: 세션 중단 시 작업 연속성 보장

---

## 개요

AI 코딩 가이드(`website/ai-coding/`)를 4가지 방향으로 개선하고, 연관 페이지 2개를 추가 조정한다.

| #   | 작업                                | 대상 파일                                        | 상태    |
| --- | ----------------------------------- | ------------------------------------------------ | ------- |
| A   | 3·4단계 정의 갱신                   | `website/ai-coding/strategy.md`                  | ✅ 완료 |
| B   | cicd-quick 포지셔닝 명확화          | `website/ai-coding/cicd-quick.mdx`               | ✅ 완료 |
| C   | AI 보안 검출 페이지 신규            | `website/ai-coding/ai-security-review.md` (신규) | ✅ 완료 |
| D   | Best Practice 저장소 페이지 신규    | `website/ai-coding/best-practice-repo.md` (신규) | ✅ 완료 |
| E   | intro 테이블 + cicd-quick 설명 갱신 | `website/ai-coding/intro.md`                     | ✅ 완료 |
| F   | DevSecOps 진입 경로 링크 수정       | `website/devsecops/intro.md`                     | ✅ 완료 |

완료 시 `⬜` → `✅` 로 변경한다.

---

## 작업 A — `strategy.md` 3·4단계 정의 갱신

**파일**: `website/ai-coding/strategy.md`

### A-1. 개요 테이블 — 3단계 행 수정

**현재**

```
| 3단계 | CI/CD 자동 차단 | syft · grype · ORT | 높음 | 팀·조직 |
```

**변경 후**

```
| 3단계 | CI/CD 자동 차단 | Gitleaks · Semgrep · syft · grype · Trivy · Checkov | 높음 | 팀·조직 |
```

### A-2. 개요 테이블 — 4단계 행 수정

**현재**

```
| 4단계 | 지속적 모니터링 | Dependabot · Renovate + AI | 매우 높음 | 조직·전사 |
```

**변경 후**

```
| 4단계 | 지속적 모니터링·자동 교정 | Dependabot · Renovate · OSS-Fuzz + AI | 매우 높음 | 조직·전사 |
```

### A-3. 3단계 설명 단락 전면 재작성

**현재 내용**: SCA(syft·grype·ORT) 중심 서술

**변경 후 구조**:

```
## 3단계: CI/CD 파이프라인 자동 차단 (Pipeline Enforcement)

:::warning 이 단계부터 진정한 Hard Block
:::

PR 또는 Merge 전 파이프라인에서 아래 6개 영역을 기계적으로 검증한다.
개발자나 AI의 실수와 무관하게 정책 위반 코드를 원천 차단할 수 있으며,
이 시점부터 진정한 의미의 게이트키퍼가 작동한다.

| 영역 | 대표 도구 | 파이프라인 위치 | 탐지 대상 |
|------|-----------|----------------|-----------|
| 시크릿 탐지 | Gitleaks | pre-commit · PR | API 키·토큰·비밀번호 하드코딩 |
| SAST | Semgrep · CodeQL | PR | SQL 인젝션·논리 버그·취약 패턴 |
| SCA | syft · grype | PR · 빌드 | 알려진 CVE·금지 라이선스 |
| 컨테이너 보안 | Trivy | 빌드 | 이미지 취약점 (컨테이너 사용 시) |
| IaC 보안 | Checkov | PR | 클라우드 인프라 설정 오류 (IaC 사용 시) |
| AI 코드 리뷰 | Claude · Semgrep AI | PR | 의미론적 취약점 (선택 옵션) |

특히 AI 코딩 도구는 하드코딩된 값을 코드에 삽입하는 경우가 잦으므로,
**시크릿 탐지는 3단계 도입 첫날부터 필수**다.
모든 영역을 한꺼번에 도입하려 하지 말고,
시크릿 탐지 → SAST → SCA 순서로 안정화한 뒤 다음으로 넘어간다.

- [30분 완성 Quick CI/CD](./cicd-quick) — SCA 중심 최소 시작점
- [AI 코드 리뷰 확장](./ai-security-review) — AI를 활용한 의미론적 취약점 탐지
- [전사 파이프라인 설계](/devsecops/pipeline-design) — 전 영역 통합 설계
```

### A-4. 4단계 설명 단락 — AI 퍼징 추가

기존 Dependabot·Renovate 설명 뒤에 아래 문단 추가:

```
AI 퍼징(Fuzz Testing) 또한 4단계의 확장 영역이다.
Claude 등 LLM에게 함수 시그니처를 분석시켜 fuzz target 코드를 자동 생성한 뒤,
AFL++·libFuzzer·OSS-Fuzz 인프라에서 실제 퍼징을 실행하는 방식이다.
C/C++·Rust 등 저수준 언어나 파서·프로토콜 구현부에 효과가 크다.
Python·JS 웹 애플리케이션은 DAST([동적 분석](/devsecops/dast))로 대체한다.
```

---

## 작업 B — `cicd-quick.mdx` 포지셔닝 명확화

**파일**: `website/ai-coding/cicd-quick.mdx`

### B-1. 페이지 상단 안내 admonition 추가

`## AI 규칙만으로는 부족한 이유` 섹션 **위에** 삽입:

```markdown
:::info 이 페이지의 범위
SCA(의존성 취약점 + 라이선스) 중심의 최소 시작점을 다룹니다.
시크릿 탐지·SAST·컨테이너 보안·IaC 보안까지 전 영역이 필요하다면
[DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design)를 참고하세요.
:::
```

### B-2. "다음 단계" 섹션 링크 확장

**현재**:

```
- [DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design)
- [DevSecOps — 지속적 모니터링·자동 교정](/devsecops/monitoring)
```

**변경 후**:

```
- [AI 코드 리뷰 확장](./ai-security-review) — AI를 활용한 의미론적 취약점 탐지 (선택 옵션)
- [DevSecOps — 시크릿 탐지](/devsecops/secret-detection) — Gitleaks pre-commit 설정
- [DevSecOps — SAST](/devsecops/sast) — Semgrep·CodeQL PR 게이트
- [DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design)
- [DevSecOps — 지속적 모니터링·자동 교정](/devsecops/monitoring)
```

---

## 작업 C — `ai-security-review.md` 신규 생성

**파일**: `website/ai-coding/ai-security-review.md` (신규)  
**sidebar_position**: 7

### 페이지 구성

```
---
id: ai-security-review
title: AI 보안 코드 리뷰
sidebar_label: AI 보안 리뷰
sidebar_position: 7
---
```

#### 섹션 구성

1. **개요** — SCA·SAST가 잡지 못하는 의미론적 취약점을 AI가 보완
2. **역할 분담** — 기존 도구 vs AI 리뷰 비교 테이블
   - Gitleaks: 하드코딩 시크릿
   - grype: 알려진 CVE
   - Semgrep: 정규 표현식 기반 패턴
   - AI 리뷰: 논리 흐름·비즈니스 규칙 위반 (위 도구의 보완)
3. **GitHub Actions 예시** — PR diff → Claude API 호출 패턴
   ```yaml
   # .github/workflows/ai-review.yml
   name: AI Security Review
   on:
     pull_request:
       branches: [main, develop]
   jobs:
     ai-review:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0
         - name: Get PR diff
           id: diff
           run: git diff origin/${{ github.base_ref }}...HEAD -- '*.py' '*.js' '*.ts' '*.go' > diff.txt
         - name: AI Security Review
           env:
             ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
           run: |
             python3 << 'EOF'
             import anthropic, pathlib
             diff = pathlib.Path("diff.txt").read_text()[:8000]  # 토큰 절약
             client = anthropic.Anthropic()
             response = client.messages.create(
               model="claude-opus-4-7",
               max_tokens=1024,
               messages=[{
                 "role": "user",
                 "content": f"아래 코드 변경에서 보안 취약점(SQL 인젝션, 인증 우회, 민감 정보 노출 등)을 탐지하라. 발견 없으면 'PASS'만 출력하라.\n\n{diff}"
               }]
             )
             print(response.content[0].text)
             EOF
   ```
4. **주의사항** 섹션
   - FP(오탐)율이 높으므로 빌드 차단이 아닌 PR 코멘트 또는 리포트 용도로만 사용
   - 컨텍스트 창 한계 → diff 단위(파일 전체 아님)로 분석
   - Anthropic API 비용 발생 → PR당 호출 횟수 제어 필요
   - 민감 코드의 외부 API 전송 리스크 — 사내 정책 확인 후 도입
5. **셀프 스터디** admonition — `cicd-quick` 적용 후 이 페이지로 확장 권장

---

## 작업 D — `best-practice-repo.md` 신규 생성

**파일**: `website/ai-coding/best-practice-repo.md` (신규)  
**sidebar_position**: 8

### 사전 작업 (문서 작성 전)

실제 GitHub 저장소를 먼저 생성해야 한다. 저장소 구성은 아래 참조.

**저장소명**: `trustedoss/ai-coding-best-practice` (가칭)  
**목적**: 1~4단계 모두 구현한 참조 저장소, 독자가 fork해서 즉시 사용

#### 저장소 내부 구성

```
ai-coding-best-practice/
├── README.md                          # 배지 + 단계별 설명 + 가이드 링크
├── src/
│   └── app.py                         # 샘플 Python 웹 앱 (의존성 포함)
├── requirements.txt                   # 의존성 파일 (취약점 스캔 대상)
├── Dockerfile                         # 컨테이너 보안(Trivy) 시연용
├── CLAUDE.md                          # 2단계: AI 규칙 내재화
├── .cursorrules                       # 2단계: Cursor 규칙
├── .gitleaks.toml                     # 3단계: 시크릿 탐지 설정
├── .grype.yaml                        # 3단계: SCA 임계값 설정
├── .semgrep.yml                       # 3단계: SAST 룰셋
├── renovate.json                      # 4단계: Renovate 자동 업데이트
├── .github/
│   ├── dependabot.yml                 # 4단계: Dependabot 설정
│   └── workflows/
│       ├── secret-detection.yml       # 3단계: Gitleaks
│       ├── sast.yml                   # 3단계: Semgrep
│       ├── oss-policy.yml             # 3단계: syft + grype + 라이선스
│       ├── container-security.yml     # 3단계: Trivy
│       └── ai-review.yml             # 3단계 선택: AI 코드 리뷰 (비활성화 상태)
└── docs/
    └── setup-guide.md                 # 각 단계 설정 방법 상세
```

#### README 배지 구성

```markdown
![Secret Detection](배지URL) ![SAST](배지URL) ![SCA](배지URL) ![Container Security](배지URL)
```

### 페이지 구성

```markdown
---
id: best-practice-repo
title: Best Practice 저장소
sidebar_label: Best Practice 저장소
sidebar_position: 8
---
```

#### 섹션 구성

1. **개요** — 4단계 모두 구현한 참조 저장소
2. **저장소 구조** — 위 트리 구조 표시
3. **단계별 구현 내용** — 각 단계가 어떤 파일로 구현됐는지
4. **시작하기** — fork → secrets 등록 → PR 열어서 검증 확인하는 3단계 안내
5. **커스터마이징 포인트** — 팀 정책에 맞게 수정할 파일 목록

---

## 작업 E — `ai-coding/intro.md` 테이블 갱신

**파일**: `website/ai-coding/intro.md`

### E-1. 페이지 목록 테이블 — cicd-quick 설명 수정

**현재**

```
| [30분 완성 Quick CI/CD](./cicd-quick) | AI 코딩과 SBOM/보안 스캔 자동화 최소 구성 |
```

**변경 후**

```
| [30분 완성 Quick CI/CD](./cicd-quick) | SCA·라이선스 중심 CI/CD 최소 시작점 |
```

### E-2. 페이지 목록 테이블 — 새 페이지 2개 추가

`cicd-quick` 행 아래에 추가:

```markdown
| [AI 보안 코드 리뷰](./ai-security-review) | AI를 활용한 의미론적 취약점 탐지 (선택 옵션) |
| [Best Practice 저장소](./best-practice-repo) | 1~4단계 모두 구현한 참조 GitHub 저장소 |
```

---

## 작업 F — `devsecops/intro.md` 진입 경로 링크 수정

**파일**: `website/devsecops/intro.md`

### F-1. "AI 코딩 가이드와의 관계" admonition 수정

**현재**

```
두 가이드는 독립적으로 사용 가능하지만, [AI 코딩 — Quick CI/CD](/ai-coding/cicd-quick) → DevSecOps 순서로 읽는 것을 권장합니다.
```

**변경 후**

```
두 가이드는 독립적으로 사용 가능하지만,
[AI 코딩 — 4단계 전략](/ai-coding/strategy) → [Quick CI/CD](/ai-coding/cicd-quick) → DevSecOps
순서로 읽는 것을 권장합니다.
```

---

## 검증 절차

각 작업 완료 후:

```bash
bash .claude/scripts/verify.sh
```

11/11 PASS 확인 후 다음 작업 진행.

---

## 완료 기준

- [x] A: `strategy.md` — 3단계 테이블·설명, 4단계 퍼징 추가
- [x] B: `cicd-quick.mdx` — 상단 admonition, 다음 단계 링크 확장
- [x] C: `ai-security-review.md` — 신규 페이지 생성 완료
- [ ] D-pre: GitHub 저장소(`trustedoss/ai-coding-best-practice`) 생성 완료 ← 사용자 직접 생성 필요
- [x] D: `best-practice-repo.md` — 신규 페이지 생성 완료
- [x] E: `ai-coding/intro.md` — 테이블 cicd-quick 설명 수정, 새 페이지 2개 추가
- [x] F: `devsecops/intro.md` — 진입 경로 링크 수정
- [x] 전체 verify.sh 11/11 PASS
- [ ] git commit

---

## 검토에서 수정 불필요로 확정된 파일

| 파일                           | 판단 근거                                           |
| ------------------------------ | --------------------------------------------------- |
| `ai-coding/iso42001.md`        | AI 코딩 단계 직접 참조 없음                         |
| `ai-coding/rules-template.mdx` | 도구 언급·링크 모두 개선 후에도 유효                |
| `ai-coding/tools/*.md` (5개)   | 도구별 설정 집중 페이지, 단계 참조 없음             |
| `devsecops/strategy.md`        | AI 코딩 가이드 단계 직접 참조 없음                  |
| `devsecops/pipeline-design.md` | AI 코딩 가이드 참조 없음                            |
| `devsecops/monitoring.md`      | AI 코딩 가이드 참조 없음                            |
| `docs/` 전체                   | "3단계/4단계"는 ISO 인증 절차·챕터 번호 (다른 맥락) |
