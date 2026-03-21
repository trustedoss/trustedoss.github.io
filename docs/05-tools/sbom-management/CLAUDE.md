# 챕터 05-2 — SBOM 관리

## 현재 위치: 5-2단계 - SBOM 관리 (5.2/7단계)

## 이 챕터의 목표

생성한 SBOM을 지속적으로 관리하고, 릴리즈 시마다 갱신하며,
외부 고객이나 납품처에 공유하는 체계를 수립한다.

SBOM은 한 번 만들고 끝이 아니다. 소프트웨어가 업데이트될 때마다 갱신해야 하며,
신규 CVE 발생 시 영향 범위를 빠르게 파악할 수 있어야 한다.

## 충족되는 체크리스트 항목

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G3B.2 | SBOM 관리 및 유지보수 | — | 3.3.1 |
| G3B.3 | SBOM 공유 (공급망 파트너) | — | 3.3.1 |
| G3B.4 | 공급망 취약점 지속 모니터링 | — | 3.3.3 |

> 이 단계는 ISO/IEC 18974 3.3.1, 3.3.3 요구사항을 충족합니다.

## 전제 조건

- `output/sbom/*.cdx.json` 완료 (챕터 05-1)

## 완료 기준

- [ ] `output/sbom/sbom-management-plan.md` 생성됨
- [ ] `output/sbom/sbom-sharing-template.md` 생성됨
- [ ] SBOM 갱신 주기가 정의됨
- [ ] 외부 공유 절차가 문서화됨

## agent 실행 안내

```bash
cd agents/05-sbom-management
claude
```

agent가 아래 질문을 순서대로 한다:
1. SBOM을 외부(고객/납품처)에 제공해야 하는지 여부
2. 납품처가 요구하는 SBOM 포맷 (CycloneDX/SPDX/무관)
3. 소프트웨어 릴리즈 주기

## 납품처 SBOM 제공 시나리오

납품처가 SBOM을 요구하는 경우가 증가하고 있다. 특히:
- 공공기관 납품 (EO 14028 영향으로 SBOM 요구 증가)
- 대기업 공급망 관리 프로그램 (삼성, 현대차 등)
- EU 시장 출시 소프트웨어 (EU CRA 2027년 시행)

`sbom-sharing-template.md` 는 납품처에게 SBOM을 전달할 때 함께 제출하는 설명 문서다.

## 셀프스터디 경로

:::info 셀프스터디 모드 (약 45분)
agent와 대화하며 관리 계획을 생성합니다.
:::

1. `docs/05-tools/sbom-management/index.md` 읽기
2. `cd agents/05-sbom-management && claude` 실행
3. 3개 질문에 답변
4. `output/sbom/sbom-management-plan.md` 확인

## 워크숍 경로

:::tip 워크숍 모드 (M4 - 45분)
납품처 SBOM 요구사항을 미리 파악해오면 빠르게 진행됩니다.
:::

1. (10분) SBOM 관리 중요성 설명
2. (25분) agent 실행 및 계획 문서 생성
3. (10분) 공유 템플릿 검토

## 자주 발생하는 문제

**Q: SBOM을 언제 갱신해야 하나요?**
A: 새로운 의존성 추가, 기존 의존성 업데이트, 릴리즈 시점마다 갱신 권장.
CI/CD에 통합하면 자동화 가능하다 (챕터 04 참조).

**Q: SPDX와 CycloneDX 중 어느 포맷으로 공유해야 하나요?**
A: 납품처가 지정하지 않으면 CycloneDX JSON 권장 (도구 지원 범위가 넓음).

## 다음 단계

완료 후:
```bash
cd agents/05-vulnerability-analyst
claude
```
또는 `docs/05-tools/vulnerability/` 로 이동.
