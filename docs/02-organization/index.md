---
id: index
title: 조직 구성
sidebar_label: 조직 구성
sidebar_position: 1
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - "ISO/IEC 5230: [G1.3, G2.1, G2.2]"
  - "ISO/IEC 18974: [G1.3, G2.1, G2.2]"
셀프스터디 소요시간: 1시간
---

# 조직 구성: 오픈소스 담당자 지정과 역할 정의

## 1. 이 챕터에서 하는 일

이 챕터에서는 오픈소스 관리 담당자를 지정하고, 역할과 책임을 문서화한다.
`organization-designer` agent를 실행하면 아래 3개의 산출물이 자동으로 생성된다.

- `output/organization/role-definition.md` — 담당자별 역할 정의서
- `output/organization/raci-matrix.md` — 활동별 책임 매트릭스
- `output/organization/appointment-template.md` — 담당자 임명 템플릿

> 이 단계는 ISO/IEC 5230 G1.3 (3.1.2), G2.1 (3.2.2), G2.2 (3.2.1) 및 ISO/IEC 18974 동일 항목 요구사항을 충족합니다.

---

## 2. 왜 담당자 지정이 첫 번째인가

오픈소스 관리는 의사결정이 필요한 활동이다. "이 라이브러리를 써도 되는가?", "이 취약점에 어떻게 대응할 것인가?" — 이런 질문에 누군가는 답해야 한다. 책임 소재가 없으면 정책도, 프로세스도 실제로는 작동하지 않는다.

표준이 담당자 지정을 첫 번째로 요구하는 이유도 여기에 있다. 조직이 없으면 이후의 모든 활동이 흐지부지된다.

실제 오픈소스 분쟁 사례에서 담당자 부재가 야기하는 결과는 구체적이다.

- **GPL 라이선스 위반 발생 시**: 대응 주체가 없어 소송 리스크를 그대로 떠안게 된다. 누가 소스 코드를 공개할지, 누가 법무 대응을 할지 결정되지 않아 골든타임을 놓친다.
- **CVE 취약점 발표 시**: 자사 제품에 영향을 받는 컴포넌트를 파악하지 못해 대응이 수 주씩 늦어진다. SBOM이 없고 담당자도 없으면 뒤늦게 이슈를 인지하게 된다.
- **납품처 SBOM 요구 시**: 계약서에 SBOM 제출 조항이 들어오는 경우가 늘고 있다. 담당자와 프로세스가 없으면 제출 자체가 불가능해 계약 차질이 생긴다.

---

## 3. 표준이 요구하는 역할

ISO/IEC 5230과 ISO/IEC 18974는 공통적으로 다음 두 가지를 요구한다.

1. **담당자 지정** (G1.3 / 3.1.2): 오픈소스 프로그램 관리를 책임지는 사람 또는 그룹이 명확히 지정되어야 한다.
2. **외부 문의 수신 채널** (G2.2 / 3.2.1): 라이선스 의무 이행 요청 및 취약점 신고를 받을 수 있는 공식 채널이 있어야 한다.

아래는 두 표준을 모두 충족하기 위해 공통적으로 필요한 역할이다.

| 역할 | 영문명 | 주요 책임 | 최소 자격 |
|------|--------|-----------|-----------|
| 오픈소스 프로그램 관리자 | OSPO Manager / OSPM | 전체 오픈소스 정책 관리, 대외 창구, 최종 승인 | 오픈소스 기본 지식, 내부 조정 능력 |
| 법무 담당 | Legal Officer | 라이선스 검토, 법적 의무사항 확인, 분쟁 대응 | 라이선스 기본 지식 (외부 자문 활용 가능) |
| 보안 담당 | Security Officer | CVE 모니터링, 취약점 대응, SBOM 관리 | 보안 기본 지식, CVE 스캔 도구 사용 |
| 개발 대표 | Developer Representative | 현장 오픈소스 사용 현황 파악, 개발팀 교육, SBOM 생성 | 개발 경험 |

### 외부 문의 수신 채널 (G2.2 요구사항)

라이선스 의무 이행 요청 및 취약점 신고를 받는 공식 이메일 또는 채널을 반드시 지정해야 한다. 이것은 표준의 명시적 요구사항이며, 담당자를 지정하는 것만큼 중요하다.

예시:
- `opensource@company.com` — 라이선스 관련 외부 문의
- `security@company.com` — 취약점 신고 수신

두 채널을 통합하여 단일 주소로 운영하는 것도 소규모 조직에서는 현실적인 방법이다.

---

## 4. 회사 규모별 현실적인 구성 방안

| 규모 | 구성 방안 | 최소 인원 | 권장 |
|------|-----------|-----------|------|
| 스타트업/소규모 (개발자 10명 이하) | 1인이 OSPM + 법무 + 보안 겸직 가능 | 1명 | CTO 또는 시니어 개발자가 담당 |
| 중소기업 (10~100명) | OSPM 전담 1명, 법무·보안 겸직 | 2~3명 | 법무는 외부 자문 활용 |
| 중견/대기업 (100명 이상) | 전담팀 구성 권장, 역할별 분리 | 4명 이상 | OSPO 공식 설립 |

**중요**: 소규모 조직에서 역할이 겹쳐도 괜찮다. 중요한 것은 누가 책임지는지가 명확한 것이다.

---

## 5. 셀프스터디 경로

:::info 셀프스터디 모드 (약 1시간)
agent와 대화하며 조직 산출물을 생성합니다.
:::

1. 이 문서 읽기 — 역할 개념 이해
2. 자사 규모와 상황에 맞는 구성 방안 결정 (섹션 4 참고)
3. agent 실행:

   :::tip 실행 전 확인
   현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
   :::

   ```bash
   cd agents/02-organization-designer
   claude
   ```

   :::details Agent 대화 예시 (클릭해서 펼치기)
   아래는 실제 agent와의 대화 흐름 예시입니다. 실행 시 이런 형태로 진행됩니다.

   **Agent 안내 메시지:**
   > 안녕하세요! 조직/담당자 산출물을 생성하는 agent입니다.
   > 5개 질문에 답변하시면 3개의 산출물 파일이 자동으로 생성됩니다.

   ---

   **질문 1/5** — 회사명과 담당 부서명을 알려주세요.

   `예시 답변: (주)테크스타트, 개발팀`

   **질문 2/5** — 전체 개발자 수는 몇 명인가요?

   `예시 답변: 50명`

   **질문 3/5** — 오픈소스 업무를 전담할 수 있는 인원이 있나요? (전담 / 겸직 / 1인 담당)

   `예시 답변: 겸직`

   **질문 4/5** — 법무팀이 있나요? (있음 / 없음 / 외부 법무 활용)

   `예시 답변: 외부 법무 활용`

   **질문 5/5** — 보안팀이 있나요? (있음 / 없음 / 겸직)

   `예시 답변: 겸직`

   ---

   **생성 완료 시 출력 예시:**

   | 파일 | 내용 |
   |------|------|
   | `output/organization/role-definition.md` | 역할과 책임 정의, 외부 문의 채널 |
   | `output/organization/raci-matrix.md` | RACI 매트릭스, 역할별 담당자 |
   | `output/organization/appointment-template.md` | 담당자 임명장 템플릿 |

   **직접 기입이 필요한 항목:**
   - 담당자 실제 성명
   - 개발팀 대표 이메일
   - 오픈소스 도구·교육 예산 현황
   :::

4. Claude 프롬프트가 열리면 **`시작`** 을 입력하세요. agent가 5개 질문을 순서대로 진행합니다.
5. agent의 5개 질문에 답변:
   - 회사명과 담당 부서명
   - 전체 개발자 수
   - 전담/겸직/1인 담당 중 선택
   - 법무팀 유무
   - 보안팀 유무
6. `output/organization/` 생성 확인

:::tip 예상 결과
실습을 완료하면 아래 3개 파일이 생성됩니다.

**생성 파일:**
- `output/organization/role-definition.md`
- `output/organization/raci-matrix.md`
- `output/organization/appointment-template.md`

**파일 내 반드시 포함되어야 할 항목:**
- 오픈소스 담당자 이름과 연락처
- 역할별 책임(R/A/C/I) 정의
- 외부 라이선스 문의 및 취약점 신고 채널(이메일)

생성된 파일에서 `{담당자 이름}`, `{이메일 주소}` 등 플레이스홀더가 실제 값으로 채워졌는지 확인하세요.
:::

:::info 충족되는 표준 요구사항
이 실습을 완료하면 아래 요구사항이 충족됩니다.

**ISO/IEC 5230**

| 항목 ID | 요구사항 | 자체인증 체크리스트 |
|---|---|---|
| 3.1.2 | 담당자 및 역할 정의 | Do you have documented roles and responsibilities for your open source program? |
| 3.2.1 | 외부 문의 수신 채널 | Do you have a publicly visible contact method for open source compliance inquiries? |
| 3.2.2 | 역할·책임 매트릭스 | Do you have a process for reviewing and remediating open source license obligations? |

**ISO/IEC 18974**

| 항목 ID | 요구사항 | 자체인증 체크리스트 |
|---|---|---|
| 4.1.2 | 보안 담당자 및 역할 정의 | Do you have documented roles and responsibilities for your open source security assurance program? |
| 4.2.1 | 외부 취약점 신고 채널 | Do you have a publicly visible contact method for open source vulnerability reporting? |
| 4.2.2 | 보안 역할·책임 매트릭스 | Do you have a process for assigning responsibilities for handling open source security vulnerabilities? |
:::

---

## 6. 생성되는 산출물 예시

### role-definition.md 샘플

```markdown
## 오픈소스 프로그램 관리자 (OSPM)

**담당자**: 홍길동 (개발팀 시니어 엔지니어)
**연락처**: opensource@example.com

### 주요 책임
- 오픈소스 사용 승인 및 검토
- 정책 문서 유지 관리
- 외부 문의 수신 및 대응
```

### raci-matrix.md 샘플

| 활동 | OSPM | 법무 | 보안 | 개발 |
|------|------|------|------|------|
| 오픈소스 사용 승인 | R, A | C | C | I |
| 라이선스 검토 | A | R | I | C |
| CVE 취약점 대응 | A | I | R | C |
| SBOM 생성 | A | I | C | R |

*(R=실행, A=최종책임, C=협의, I=정보공유)*

---

## 7. 완료 확인 체크리스트

- [ ] `output/organization/role-definition.md` 생성됨
- [ ] `output/organization/raci-matrix.md` 생성됨
- [ ] `output/organization/appointment-template.md` 생성됨
- [ ] 오픈소스 담당자 이름과 연락처가 정의됨
- [ ] 외부 문의 이메일/채널이 지정됨

---

## 8. 다음 단계

조직 구성이 완료되면 오픈소스 정책 수립으로 이동한다.

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/03-policy-generator
claude
```

또는 [오픈소스 정책 수립: 법적 보호의 첫걸음](../03-policy/index.md)으로 이동하여 정책 챕터를 먼저 읽은 뒤 진행할 수 있다.
