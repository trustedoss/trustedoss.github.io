# 워크숍 핸드아웃: 신뢰할 수 있는 오픈소스 사용을 위한 소프트웨어 공급망 관리 실전 워크숍

## 사전 준비 체크리스트 (강의 전날까지 완료)

- [ ] Docker Desktop 설치 및 실행 확인
- [ ] Git 설치 확인 (`git --version`)
- [ ] Claude Code 설치 및 로그인 확인 (`claude --version`)
- [ ] 저장소 클론 완료
  ```bash
  git clone https://github.com/haksungjang/trustedoss.git
  ```
- [ ] 본인 프로젝트 소스코드 준비
  (없으면 `samples/` 폴더의 샘플 프로젝트 사용 가능)
- [ ] 회사 정보 미리 파악
  - 개발자 수
  - 소프트웨어 배포 방식 (내부 배포 / 외부 배포 / SaaS 등)
  - 주요 개발 언어 (Java, Python, JavaScript 등)

---

## 오늘의 목표

워크숍 종료 시 `output/` 폴더에 아래 산출물이 모두 생성됩니다.

| 파일 | 설명 |
|------|------|
| `output/organization/role-definition.md` | 오픈소스 담당자 역할 정의 |
| `output/organization/raci-matrix.md` | 역할·책임 매트릭스 (RACI) |
| `output/organization/appointment-template.md` | 담당자 지정 공문 템플릿 |
| `output/policy/oss-policy.md` | 오픈소스 정책 문서 |
| `output/policy/license-allowlist.md` | 허용 라이선스 목록 |
| `output/process/usage-approval.md` | 오픈소스 사용 승인 절차 |
| `output/process/distribution-checklist.md` | 배포 전 체크리스트 |
| `output/process/vulnerability-response.md` | 취약점 대응 절차 |
| `output/process/process-diagram.md` | 전체 프로세스 다이어그램 |
| `output/sbom/[project].cdx.json` | SBOM (CycloneDX 형식) |
| `output/sbom/sbom-commands.sh` | SBOM 생성 명령어 스크립트 |
| `output/sbom/license-report.md` | 라이선스 분석 리포트 |
| `output/sbom/copyleft-risk.md` | Copyleft 위험 분석 |
| `output/sbom/sbom-management-plan.md` | SBOM 관리 계획 |
| `output/sbom/sbom-sharing-template.md` | SBOM 공유 템플릿 |
| `output/vulnerability/cve-report.md` | CVE 취약점 분석 리포트 |
| `output/vulnerability/remediation-plan.md` | 취약점 대응 계획 |
| `output/training/curriculum.md` | 교육 커리큘럼 |
| `output/training/completion-tracker.md` | 교육 이수 추적표 |
| `output/training/resources.md` | 교육 자료 목록 |
| `output/conformance/gap-analysis.md` | 갭 분석 보고서 |
| `output/conformance/declaration-draft.md` | 자체 인증 선언문 초안 |
| `output/conformance/submission-guide.md` | 인증 등록 안내 |

---

## 시간표

| 시간 | 내용 |
|------|------|
| 09:00–09:30 | 오리엔테이션 (환경 확인, 목표 공유) |
| 09:30–10:00 | **M0**: 공급망 보안 개요 |
| 10:00–11:00 | **M1**: 조직 + 정책 |
| 11:00–11:15 | 휴식 |
| 11:15–12:15 | **M2**: 프로세스 |
| 12:15–13:15 | 점심 |
| 13:15–14:45 | **M3**: SBOM 생성 + 분석 |
| 14:45–15:30 | **M4**: SBOM 관리 + 공유 |
| 15:30–16:15 | **M5**: 취약점 분석 |
| 16:15–16:30 | 휴식 |
| 16:30–17:00 | **M6**: 교육 + 인증 선언 |
| 17:00–17:30 | 마무리 + Q&A |

---

## 모듈별 실행 명령어 카드

### M1 조직 설계
```bash
cd agents/02-organization-designer && claude
```

### M1 정책 수립
```bash
cd agents/03-policy-generator && claude
```

### M2 프로세스 설계
```bash
cd agents/04-process-designer && claude
```

### M3 SBOM 생성
```bash
cd agents/05-sbom-guide && claude
```

### M3 SBOM 분석
```bash
cd agents/05-sbom-analyst && claude
```

### M4 SBOM 관리
```bash
cd agents/05-sbom-management && claude
```

### M5 취약점 분석
```bash
cd agents/05-vulnerability-analyst && claude
```

### M6 교육 체계
```bash
cd agents/06-training-manager && claude
```

### M6 인증 선언
```bash
cd agents/07-conformance-preparer && claude
```

---

## 막혔을 때 해결 순서

**1단계**: 해당 폴더에서 Claude Code에게 질문
```
"지금 [오류 내용]이 발생했어. 해결 방법은?"
```

**2단계**: `docs/` 해당 챕터의 트러블슈팅 섹션 확인

**3단계**: 옆 사람과 함께 확인

**4단계**: 강사 호출 (손을 들거나 채팅에 질문)

---

## 완성 체크리스트 (강의 끝에 스스로 확인)

워크숍 종료 후 `output/` 폴더에서 아래 파일들을 확인하세요.

**조직**
- [ ] `output/organization/role-definition.md`
- [ ] `output/organization/raci-matrix.md`
- [ ] `output/organization/appointment-template.md`

**정책**
- [ ] `output/policy/oss-policy.md`
- [ ] `output/policy/license-allowlist.md`

**프로세스**
- [ ] `output/process/usage-approval.md`
- [ ] `output/process/distribution-checklist.md`
- [ ] `output/process/vulnerability-response.md`
- [ ] `output/process/process-diagram.md`

**SBOM**
- [ ] `output/sbom/[project].cdx.json`
- [ ] `output/sbom/sbom-commands.sh`
- [ ] `output/sbom/license-report.md`
- [ ] `output/sbom/copyleft-risk.md`
- [ ] `output/sbom/sbom-management-plan.md`
- [ ] `output/sbom/sbom-sharing-template.md`

**취약점**
- [ ] `output/vulnerability/cve-report.md`
- [ ] `output/vulnerability/remediation-plan.md`

**교육**
- [ ] `output/training/curriculum.md`
- [ ] `output/training/completion-tracker.md`
- [ ] `output/training/resources.md`

**인증**
- [ ] `output/conformance/gap-analysis.md`
- [ ] `output/conformance/declaration-draft.md`
- [ ] `output/conformance/submission-guide.md`

모든 항목이 체크되었다면 **ISO/IEC 5230 & 18974 자체 인증 준비 완료**입니다.

> OpenChain 자체 인증 등록: https://www.openchainproject.org/conformance
