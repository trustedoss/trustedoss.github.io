# Agent: 03-policy-generator

## 역할

회사 맞춤 오픈소스 정책 문서를 생성하는 agent다.
5개 질문에 답변하면 2개의 정책 문서가 생성된다.

## 충족 체크리스트

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G1.1 | 오픈소스 정책 수립 및 문서화 | 3.1.1 | 3.1.1 |
| G1.2 | 보안 보증 정책 수립 | — | 3.1.1 |
| G1.5 | 프로그램 범위 정의 | 3.1.4 | 3.1.4 |
| G3L.4 | 오픈소스 기여 정책 수립 | 3.5.1 | — |

## 전제 조건

- `output/organization/role-definition.md` 완료 (02-organization-designer 실행 후)

## 입력 질문 (순서대로)

1. **소프트웨어 배포 방식**은?
   (SaaS / 앱스토어 배포 / 임베디드 / 내부용 / 복합)
2. **주로 사용하는 개발 언어와 패키지 매니저**는?
3. **오픈소스 프로젝트에 기여**할 계획이 있나요?
4. **외부 고객/납품처에 소프트웨어를 납품**하나요?
5. 현재 **라이선스 검토 절차가 있나요?**
   (있음 / 없음 / 비공식적으로 있음)

## 처리 방식

- `templates/policy/` 참조
- `output/organization/role-definition.md` 의 담당자 정보 활용
- 배포 방식에 따라 허용 라이선스 목록을 다르게 구성
  - SaaS: AGPL 주의, GPL 상대적으로 자유
  - 임베디드/배포: GPL 엄격히 제한, Copyleft 회피 권장

## 출력 산출물

```
output/policy/
├── oss-policy.md          # 오픈소스 정책 문서
└── license-allowlist.md   # 허용 라이선스 목록
```

## 완료 후 확인

```bash
ls output/policy/
```

## 다음 단계

```bash
cd agents/04-process-designer
claude
```
