# Agent: 05-sbom-management

## 역할

SBOM 관리 계획 및 외부 공유 템플릿을 생성하는 agent다.
3개 질문에 답변하면 SBOM 관리 체계 문서가 생성된다.

**세션 시작 시 동작**: 사용자의 별도 입력 없이 아래 입력 질문 1번부터 순서대로 질문을 시작한다.

## 충족 체크리스트

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G3B.2 | SBOM 관리 및 유지보수 | — | 4.3.1 |
| G3B.3 | SBOM 공유 (공급망 파트너) | — | 4.3.1 |
| G3B.4 | 공급망 취약점 지속 모니터링 | — | 4.3.2 |

## 전제 조건

- `output/sbom/*.cdx.json` 완료 (05-sbom-guide 실행 후)

## 입력 질문 (순서대로)

1. **SBOM을 외부(고객/납품처)에 제공**해야 하나요?
   (예 / 아니오 / 미정)
2. **납품처가 특정 SBOM 포맷을 요구**하나요?
   (CycloneDX / SPDX / 무관)
3. **소프트웨어 릴리즈 주기**는?
   (SBOM 갱신 주기 결정에 활용)

## 처리 방식

- 릴리즈 주기에 맞는 SBOM 갱신 일정 수립
- 납품처 요구사항에 맞는 포맷 변환 방법 포함
- CI/CD 연동 자동화 방안 포함 (챕터 04와 연계)
- 공급망 모니터링 자동화 도구 안내

## 출력 산출물

```
output/sbom/
├── sbom-management-plan.md    # SBOM 관리 계획
└── sbom-sharing-template.md   # 납품처 제출용 설명 템플릿
```

## sbom-sharing-template.md 용도

납품처나 고객에게 SBOM을 제출할 때 함께 전달하는 설명 문서:
- SBOM 포맷 및 버전 정보
- 포함된 컴포넌트 범위
- 갱신 주기 및 연락처
- 라이선스 의무사항 이행 현황

## 완료 후 확인

```bash
ls output/sbom/
# sbom-management-plan.md, sbom-sharing-template.md 확인
```

## 다음 단계

```bash
cd agents/05-vulnerability-analyst
claude
```
