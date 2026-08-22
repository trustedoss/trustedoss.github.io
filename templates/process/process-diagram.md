# 오픈소스 프로세스 흐름도

<!-- 5230 §3.1.5.1, §3.3.2.1 · 18974 §4.1.5.1 -->

**회사명**: {회사명}
**작성일**: YYYY-MM-DD
**담당자**: {오픈소스 담당자 이름}

> 이 문서는 `usage-approval.md`, `distribution-checklist.md`, `vulnerability-response.md`에서
> 글로 정의한 절차를 Mermaid 흐름도로 시각화한 것이다. 절차 자체의 근거·예외 조건은 해당 문서를
> 따르고, 이 문서는 전체 흐름을 한눈에 보기 위한 참조 자료로 쓴다.

---

## 1. 오픈소스 사용 승인 흐름

<!-- usage-approval.md 절차와 동일해야 한다 -->

```mermaid
graph TD
    A[오픈소스 사용 요청] --> B{허용 라이선스 목록에 있는가?}
    B -->|Yes| C[취약점 스캔: Critical/High 없음 확인]
    B -->|No| D[법무 검토]
    D -->|승인| C
    D -->|거부| E[대안 컴포넌트 검토]
    C -->|이상 없음| F[담당자 승인]
    C -->|Critical/High 발견| G[패치 확인 또는 대안 검토]
    F --> H[SBOM 업데이트]
```

## 2. 배포 전 체크리스트 흐름

<!-- distribution-checklist.md 절차와 동일해야 한다 -->

```mermaid
graph TD
    A[배포 준비] --> B[SBOM 최신화 확인]
    B --> C[고지문 생성 및 확인]
    C --> D[Copyleft 의무 이행 확인]
    D --> E[최종 승인]
    E --> F[배포]
    F --> G[배포 후 최종 확인]
```

## 3. 취약점 대응 흐름

<!-- vulnerability-response.md 절차와 동일해야 한다 -->

```mermaid
graph TD
    A[CVE 탐지] --> B{심각도 분류}
    B -->|Critical| C[1주일 내 조치]
    B -->|High| D[4주일 내 조치]
    B -->|Medium| E[1개월 내 조치]
    B -->|Low| F[다음 릴리즈에 반영]
    C --> G[패치 또는 완화 조치]
    D --> G
    E --> G
    F --> G
    G --> H[remediation-plan.md 기록]
```

---

## 4. 참고

- 각 흐름도의 세부 조건과 예외 처리는 대응하는 프로세스 문서(§1의 안내 참조) 본문을 따른다.
- 프로세스 변경 시 이 문서와 대응 프로세스 문서를 함께 갱신한다.
