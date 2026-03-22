---
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - "ISO/IEC 5230: []"
  - "ISO/IEC 18974: [4.3.1, 4.3.2]"
셀프스터디 소요시간: 1시간
---

# SBOM 관리: 만들고 끝이 아니라 관리가 시작이다

## 1. 이 챕터에서 하는 일

SBOM을 한 번 생성하는 것만으로는 부족하다. 소프트웨어는 지속적으로 변경되고, 새로운 취약점이 매일 공개된다. 이 챕터에서는 생성한 SBOM을 릴리즈 주기에 맞춰 갱신하고, 버전별로 보관하며, 외부 고객이나 납품처에 체계적으로 공유하는 프로세스를 수립한다.

`agents/05-sbom-management` agent를 실행하면 두 가지 산출물이 생성된다: 갱신 주기와 책임자를 정의한 `output/sbom/sbom-management-plan.md`와 납품처 제공용 커버 문서인 `output/sbom/sbom-sharing-template.md`. 이 두 문서가 완성되면 SBOM 관리 체계의 기초가 갖춰진다.

---

## 2. 배경 지식

### SBOM은 한 번 만들고 끝이 아니다

소프트웨어가 변경될 때마다 SBOM도 변경되어야 한다. 관리되지 않는 오래된 SBOM은 없는 것보다 위험할 수 있다. 최신 상태가 아닌 SBOM을 신뢰하면 실제 구성 요소와 문서 사이의 불일치로 인해 보안 사각지대가 생긴다.

**실제 사례:** 6개월 전 생성한 SBOM을 그대로 신뢰했다가, 그사이 추가된 취약한 라이브러리를 발견하지 못한 경우가 있다. 해당 라이브러리에서 CVE가 공개된 후에도 조직은 자신이 영향받는다는 사실을 인지하지 못했고, 고객사에서 먼저 문제를 발견하여 신뢰를 잃었다.

---

### SBOM 갱신 트리거

아래 이벤트가 발생할 때마다 SBOM을 반드시 갱신해야 한다.

| 이벤트 | 갱신 시점 | 비고 |
|--------|-----------|------|
| 새 오픈소스 컴포넌트 추가 | 즉시 (PR 병합 시) | CI/CD 자동화 권장 |
| 기존 컴포넌트 버전 변경 | 즉시 (PR 병합 시) | 특히 보안 패치 시 |
| 소프트웨어 릴리즈 | 릴리즈 직전 | 릴리즈 SBOM은 별도 보관 |
| 보안 취약점 패치 | 패치 완료 시 | 대응 증빙 목적 |

이 중 가장 중요한 시점은 **소프트웨어 릴리즈 직전**이다. 릴리즈 시점의 SBOM은 해당 버전의 구성 요소를 공식적으로 기록한 문서이므로, 별도로 보관하고 버전 태그를 명확히 달아야 한다.

---

### SBOM 버전 관리 전략

Git 기반 SBOM 버전 관리를 위한 파일 명명 규칙:

```
output/sbom/[project]-[version]-[date].cdx.json
```

예시:
```
output/sbom/myapp-v1.2.0-20260320.cdx.json
output/sbom/myapp-v1.1.0-20260101.cdx.json
output/sbom/myapp-latest.cdx.json  ← 항상 최신본 링크
```

`myapp-latest.cdx.json`은 항상 가장 최근에 생성된 SBOM을 가리키도록 유지하고, 릴리즈별 파일은 보관 정책에 따라 별도 디렉토리나 태그로 관리한다.

**릴리즈별 SBOM을 보관해야 하는 이유:**
- 규제 대응 시 특정 시점의 구성 요소를 증명할 수 있다
- 취약점 발견 시 영향받는 버전의 범위를 신속하게 파악할 수 있다
- EU CRA, EO 14028 등 신흥 규제의 요구사항에 대응할 수 있다

보관 기간 권장 기준: 해당 소프트웨어 릴리즈의 유지 기간 + 1년 이상

---

### 납품처/고객사에 SBOM 제공하기

**언제 SBOM을 제공해야 하는가:**
- 납품처가 명시적으로 요구할 때
- 계약서에 SBOM 제공 조항이 포함되어 있을 때
- EO 14028 적용 대상 (미국 연방정부 납품 시)
- EU CRA 적용 대상 (EU 시장 출시 예정, 2027년 시행)
- 대기업 공급망 관리 프로그램 참여 시 (삼성, 현대차 등 증가 추세)

**제공 방법별 장단점:**

| 방법 | 적합한 상황 | 주의사항 |
|------|-------------|---------|
| 이메일 첨부 | 소규모, 비정기 제공 | 버전 관리가 어렵고 분실 위험 있음 |
| 보안 파일 공유 (Google Drive, Box) | 중규모, 정기 제공 | 접근 권한 관리가 필요 |
| API 제공 | 대규모, 자동화 필요 | 초기 개발 비용이 필요 |
| 포털/웹 | 다수의 고객사에 동시 제공 | 인프라 구축 및 유지 비용 필요 |

**SBOM 제공 시 포함할 정보** (`sbom-sharing-template.md`에 포함):
- SBOM 파일 본체 (CycloneDX JSON 또는 SPDX 형식)
- SBOM 생성 도구 이름 및 버전
- 생성 일시 (ISO 8601 형식 권장)
- 적용된 소프트웨어 버전
- 담당자 이름 및 연락처

---

### 공급망 취약점 지속 모니터링

신규 CVE가 공개되었을 때 자신의 소프트웨어가 영향받는지 즉시 파악하려면 SBOM이 항상 최신 상태여야 한다. SBOM이 outdated 상태라면 모니터링 도구가 올바른 알림을 생성하지 못한다.

**모니터링 방법:**
- **Dependency Track 알림:** 취약점 임계치(CVSS 점수 등)를 초과하면 이메일 또는 웹훅으로 알림
- **GitHub Dependabot:** GitHub 기반 프로젝트에서 의존성 취약점을 자동으로 PR로 알림
- **OSV.dev 구독:** Google이 운영하는 오픈소스 취약점 데이터베이스 알림 구독

**CI/CD 자동 모니터링 예시 (주간 스캔):**

```yaml
# .github/workflows/vuln-scan.yml
name: Weekly Vulnerability Scan
on:
  schedule:
    - cron: '0 9 * * 1'  # 매주 월요일 오전 9시
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate fresh SBOM
        run: |
          syft . -o cyclonedx-json > output/sbom/myapp-latest.cdx.json
      - name: Check SBOM for new CVEs
        run: |
          # Dependency Track API 또는 grype 등으로 스캔
          grype sbom:output/sbom/myapp-latest.cdx.json --fail-on high
```

이 워크플로우를 통해 매주 최신 SBOM을 기반으로 취약점을 자동 스캔하고, 심각도 높은 취약점 발견 시 CI 빌드를 실패로 처리하여 팀에 알릴 수 있다.

---

## 3. 셀프스터디 경로

:::info 셀프스터디 모드 (약 45분)
agent와 대화하며 SBOM 관리 계획과 납품처 공유 템플릿을 생성합니다. agent가 3개의 질문을 순서대로 묻고, 답변에 맞춰 문서를 자동으로 작성합니다.
:::

**사전 준비 — 아래 3가지를 미리 파악해두면 빠르게 진행됩니다:**

1. SBOM을 외부(고객사/납품처)에 제공해야 하는지 여부
2. 납품처가 요구하는 SBOM 포맷 (CycloneDX / SPDX / 무관)
3. 소프트웨어 릴리즈 주기 (예: 월 1회, 분기 1회, 비정기)

**단계별 실습:**

**Step 1.** 위 3개 질문에 대한 자신의 상황을 간략히 메모한다.

**Step 2.** agent를 실행한다.
```bash
cd agents/05-sbom-management
claude
```

**Step 3.** agent가 묻는 3개 질문에 순서대로 답변한다.

| 질문 | 예시 답변 |
|------|-----------|
| SBOM을 외부에 제공해야 하나요? | "네, 납품처 A사가 요구합니다" 또는 "아니오, 내부 관리만" |
| 납품처가 요구하는 포맷은? | "CycloneDX JSON" 또는 "무관" |
| 릴리즈 주기는? | "분기 1회" 또는 "기능 완료 시 비정기" |

**Step 4.** 생성된 문서를 검토한다.
```bash
cat output/sbom/sbom-management-plan.md
```

**Step 5.** 공유 템플릿에 회사 정보를 실제 내용으로 채운다.
```bash
# 텍스트 에디터로 열어 [회사명], [담당자명] 등 플레이스홀더 교체
open output/sbom/sbom-sharing-template.md
```

**Step 6.** SBOM 파일 명명 규칙을 기존 파일에 적용한다.
```bash
# 예: 기존 파일 이름 변경
mv output/sbom/myapp.cdx.json output/sbom/myapp-v1.0.0-20260320.cdx.json
cp output/sbom/myapp-v1.0.0-20260320.cdx.json output/sbom/myapp-latest.cdx.json
```

**막혔을 때:** 납품처가 없거나 요구사항이 불명확한 경우 "외부 제공 없음"으로 답변한다. agent가 내부 관리 중심의 계획을 생성한다.

**예상 결과:**
- `output/sbom/sbom-management-plan.md`: 갱신 트리거, 갱신 주기, 책임자, 보관 정책, 모니터링 계획 포함
- `output/sbom/sbom-sharing-template.md`: 납품처 제공용 커버 문서 (회사 정보 플레이스홀더 포함)

---

## 4. 완료 확인 체크리스트

아래 항목을 모두 확인하면 이 챕터가 완료된다.

- [ ] `output/sbom/sbom-management-plan.md` 파일이 생성됨
- [ ] `output/sbom/sbom-sharing-template.md` 파일이 생성됨
- [ ] SBOM 갱신 트리거 목록이 management-plan에 명시됨
- [ ] SBOM 갱신 주기가 릴리즈 주기와 연동되어 정의됨
- [ ] 책임자 이름과 연락처가 management-plan에 명시됨
- [ ] 외부 제공 절차가 문서화됨 (납품처가 없는 경우 "해당 없음"으로 명시)
- [ ] 파일 명명 규칙 (`[project]-[version]-[date].cdx.json`)이 정의됨
- [ ] 보관 기간 정책이 정의됨

**sbom-management-plan.md 주요 섹션 예시:**

```markdown
# SBOM 관리 계획

## 1. SBOM 생성 및 갱신 정책
- **갱신 트리거 목록:** 신규 컴포넌트 추가, 버전 변경, 릴리즈, 보안 패치
- **갱신 담당자:** [이름], [역할]
- **갱신 절차:** PR 병합 시 CI/CD 자동 생성 → 담당자 검토 → 보관

## 2. 버전 관리 전략
- **파일 명명 규칙:** `[project]-[version]-[date].cdx.json`
- **보관 위치:** `output/sbom/` (Git 관리)
- **보관 기간:** 릴리즈 유지 기간 + 1년

## 3. 외부 공유 절차
- **공유 대상 및 조건:** [납품처명], 계약서 제X조 요건
- **제공 포맷:** CycloneDX JSON
- **제공 채널:** 보안 파일 공유 링크 (Box)
- **제공 주기:** 릴리즈 시마다, 납품처 요청 시

## 4. 모니터링 계획
- **신규 CVE 알림:** Dependency Track, CVSS 7.0 이상 즉시 알림
- **정기 검토 주기:** 월 1회 담당자 검토
- **자동 스캔:** 매주 월요일 GitHub Actions 실행
```

> 이 단계는 ISO/IEC 18974 4.3.1, 4.3.2 요구사항을 충족합니다.

---

## 5. 다음 단계

SBOM 관리 체계가 갖춰졌으면, 취약점 분석 단계로 이동한다. SBOM을 기반으로 현재 소프트웨어에 영향받는 CVE를 분석하고, 대응 계획을 수립하는 단계다.

```bash
cd agents/05-vulnerability-analyst
claude
```

또는 가이드 문서를 먼저 읽으려면:

```bash
cd docs/05-tools/vulnerability
```

취약점 분석 단계에서는 앞서 생성한 `output/sbom/[project].cdx.json`을 입력으로 사용하므로, SBOM 파일이 최신 상태인지 한 번 더 확인하고 진행하는 것을 권장한다.
