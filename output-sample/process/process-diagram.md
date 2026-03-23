# 오픈소스 프로세스 흐름도
<!-- 5230 §3.1.5.1, §3.3.1.1, §3.4.1.1 -->

**회사명**: 테크유니콘
**작성일**: 2026-03-23

---

## 1. 오픈소스 사용 승인 프로세스

```mermaid
graph TD
    A[오픈소스 사용 요청\nJira 티켓 생성] --> B{허용 라이선스 목록\n확인}
    B -->|허용 목록 내| C{리스크 수준 판정}
    B -->|허용 목록 외| D[위원회 승인 + 법무 검토]
    C -->|낮음\nPermissive + CVE 없음| E[담당자 단독 승인]
    C -->|중간\nWeak Copyleft or Medium CVE| F[팀장 승인]
    C -->|높음\nStrong Copyleft or High/Critical CVE| D
    D -->|승인| G[취약점 스캔\nGitHub Actions / Jenkins / GitLab CI]
    E --> G
    F --> G
    G -->|Critical/High CVE 없음| H[승인 완료\nJira 티켓 Done]
    G -->|Critical/High CVE 발견| I[패치 버전 변경\n또는 대안 검색]
    I --> G
    D -->|거부| J[도입 취소]
    H --> K[SBOM 업데이트]
    K --> L[배포 전 체크리스트 완료]
```

---

## 2. 배포 파이프라인 프로세스

```mermaid
graph TD
    A[코드 커밋] --> B{브랜치 구분}
    B -->|개발 브랜치\n매일 배포| C[GitHub Actions / GitLab CI\n자동 스캔]
    B -->|상용 브랜치\n주간 배포| D[Jenkins 전체 파이프라인]
    C --> E{Critical/High CVE?}
    E -->|없음| F[개발 배포 승인]
    E -->|있음| G[PR/커밋 머지 차단\nJira 티켓 자동 생성]
    G --> H[패치 적용]
    H --> C
    D --> I[SBOM 재생성]
    I --> J[라이선스 검사]
    J --> K{의무사항 이행\n완료?}
    K -->|완료| L[취약점 스캔]
    K -->|미완료| M[담당자 조치]
    M --> J
    L --> N{Critical/High CVE?}
    N -->|없음| O[배포 체크리스트\n완료]
    N -->|있음| P[Jira 티켓 Blocker 등록\n핫픽스 또는 배포 연기]
    P --> L
    O --> Q[팀장 승인]
    Q --> R[상용 배포]
```

---

## 3. 취약점 대응 프로세스

```mermaid
graph TD
    A[취약점 탐지\nCI/CD 스캔 / 외부 신고] --> B[Jira 티켓 생성\nOSS-SEC 프로젝트]
    B --> C{CVSS 심각도}
    C -->|Critical 9.0+| D[24시간 이내 대응\nJira Blocker]
    C -->|High 7.0~8.9| E[1주일 이내 대응\nJira Critical]
    C -->|Medium 4.0~6.9| F[1개월 이내 대응\nJira Major]
    C -->|Low ~3.9| G[다음 릴리즈 반영\nJira Minor]
    D --> H{배포 소프트웨어\n영향?}
    E --> H
    H -->|영향 있음| I[고객/파트너 통보\nsecurity@sktelecom.com]
    H -->|영향 없음| J[패치 적용]
    I --> J
    F --> J
    G --> J
    J --> K[재스캔으로\n취약점 해소 확인]
    K --> L[remediation-plan.md\n기록 갱신]
    L --> M[Jira 티켓 Done]
```

---

## 4. 전체 오픈소스 관리 사이클

```mermaid
graph LR
    A[사용 요청] --> B[라이선스 검토]
    B --> C[취약점 스캔]
    C --> D[리스크 기반 승인\n담당자/팀장/위원회]
    D --> E[SBOM 업데이트]
    E --> F[개발 배포\n매일]
    F --> G[상용 배포\n주간]
    G --> H[출시 후 모니터링\n월 1회 재스캔]
    H --> I{신규 취약점?}
    I -->|있음| J[취약점 대응 절차]
    J --> K[패치 릴리즈]
    K --> G
    I -->|없음| H
```

---

## 참조 문서

| 프로세스 | 상세 절차 문서 |
|---------|-------------|
| 사용 승인 | `output/process/usage-approval.md` |
| 배포 체크리스트 | `output/process/distribution-checklist.md` |
| 취약점 대응 | `output/process/vulnerability-response.md` |
| 라이선스 정책 | `output/policy/oss-policy.md` |
| 허용 라이선스 | `output/policy/license-allowlist.md` |
