# 챕터 04 — 프로세스 설계

## 현재 위치: 4단계 - 프로세스 설계 (4/7단계)

## 이 챕터의 목표

오픈소스 사용 승인, 배포 전 체크리스트, 취약점 대응 절차를 문서화한다.
정책이 "무엇을 해야 하는가"를 정의한다면, 프로세스는 "어떻게 실행하는가"를 정의한다.

CI/CD 파이프라인과 통합하는 방법도 다룬다. 프로세스가 개발 흐름에 자연스럽게
내장되어야 지속 가능한 컴플라이언스 체계가 된다.

## 충족되는 체크리스트 항목

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G1.6 | 라이선스 의무사항 검토 절차 수립 | 3.1.5 | — |
| G3L.2 | 라이선스 의무사항 이행 | 3.3.2 | — |

> 이 단계는 ISO/IEC 5230 3.1.5, 3.3.2 요구사항을 충족합니다.

## 전제 조건

- `output/policy/oss-policy.md` 완료 (챕터 03)

## 완료 기준

- [ ] `output/process/usage-approval.md` 생성됨
- [ ] `output/process/distribution-checklist.md` 생성됨
- [ ] `output/process/vulnerability-response.md` 생성됨
- [ ] `output/process/process-diagram.md` 생성됨 (Mermaid 흐름도 포함)

## agent 실행 안내

```bash
cd agents/04-process-designer
claude
```

agent가 아래 질문을 순서대로 한다:
1. 현재 사용 중인 CI/CD 도구 (GitHub Actions/Jenkins/GitLab CI/없음/기타)
2. 소프트웨어 배포 주기 (매일/주간/월간/비정기)
3. 이슈 트래커 사용 여부 (GitHub Issues/Jira/없음/기타)
4. 오픈소스 사용 승인 결재 단계 (담당자 단독/팀장 승인/위원회 승인)

## CI/CD 통합 포인트

프로세스가 CI/CD에 통합되는 주요 지점:

- **PR 단계**: 새 의존성 추가 시 라이선스 자동 확인
- **빌드 단계**: SBOM 자동 생성
- **배포 전**: 배포 체크리스트 자동 실행
- **주기적 스캔**: 알려진 CVE 모니터링

GitHub Actions 기반 예시 워크플로우는 agent가 생성한다.

## 셀프스터디 경로

:::info 셀프스터디 모드 (약 1~2시간)
프로세스는 회사 환경에 맞게 상당한 커스터마이징이 필요합니다.
:::

1. `docs/04-process/index.md` 읽기
2. `cd agents/04-process-designer && claude` 실행
3. 4개 질문에 답변
4. 생성된 Mermaid 흐름도 검토
5. CI/CD 통합 계획 수립

## 워크숍 경로

:::tip 워크숍 모드 (M2 - 1시간)
CI/CD 도구와 배포 주기를 미리 확인해오세요.
:::

1. (10분) 프로세스의 중요성 설명 + 사례
2. (40분) agent 실행 및 문서 생성
3. (10분) Mermaid 흐름도 리뷰

## 자주 발생하는 문제

**Q: CI/CD가 없는데 어떻게 하나요?**
A: agent가 수동 체크리스트 기반의 프로세스를 생성한다. 나중에 CI/CD 도입 시 업그레이드 가능.

**Q: 결재 단계가 너무 많으면 개발 속도가 느려지지 않나요?**
A: 사전 승인된 라이선스 목록(allowlist)에 있는 오픈소스는 별도 승인 없이 사용 가능하도록 설계한다.

**Q: Mermaid 흐름도를 어디서 볼 수 있나요?**
A: GitHub에서 마크다운 파일을 열면 자동으로 렌더링된다. 또는 mermaid.live 사이트 활용.

## 다음 단계

완료 후:
```bash
cd agents/05-sbom-guide
claude
```
또는 `docs/05-tools/` 로 이동.
