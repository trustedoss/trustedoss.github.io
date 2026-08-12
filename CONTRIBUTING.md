[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# 기여 가이드

trustedoss에 기여해주셔서 감사합니다.

---

## 작업 범위

이 프로젝트는 **콘텐츠 작업만** 합니다.

| 작업 대상 (O)               | 작업 금지 (X)                             |
| --------------------------- | ----------------------------------------- |
| `docs/`                     | `website/src/` (CSS 예외 제외)            |
| `agents/`                   | `website/static/`                         |
| `templates/`                | `website/src/**/*.ts`, `*.tsx`            |
| `.claude/`                  | `*.js`, `*.css`, `*.scss` (CSS 예외 제외) |
| `CLAUDE.md`                 | 설정 파일 전체                            |
| `website/ai-coding/` (md만) |                                           |
| `website/devsecops/` (md만) |                                           |

디자인/코드 수정이 필요해 보이면 작업을 멈추고 이슈로 논의하세요.

---

## Push 전 필수 5단계

```
Step 1   /qa changed                               # 품질 검증 (Claude 세션 필요)
Step 2   bash .claude/scripts/verify.sh            # 13/13 PASS 확인
Step 3   진행 기록 갱신                            # 로컬 작업 노트 (저장소에는 올리지 않는다)
Step 4   git add -p && git commit -m "..."         # 변경 파일 선택적 스테이징
Step 5   git push                                  # 모든 검증 통과 후에만
```

> **주의**: `git add -A` 또는 `git add .` 대신 `git add -p`로 파일을 선택하여 스테이징하세요.
> `.env`, 로컬 설정 파일, 불필요한 바이너리가 함께 커밋되는 것을 방지합니다.

---

## 검증 명령어 빠른 참조

| 명령어                                       | 역할                           | 소요시간 |
| -------------------------------------------- | ------------------------------ | -------- |
| `/qa changed`                                | 변경 파일 품질 자동 검사·수정  | ~2분     |
| `bash .claude/scripts/verify.sh`             | 정적 검증 13항목 일괄 실행     | ~30초    |
| `python3 .claude/scripts/test-coverage.py`   | ISO G항목 커버리지 정합성 확인 | ~5초     |
| `python3 .claude/scripts/validate-output.py` | output/ 산출물 완전성 확인     | ~5초     |
| `/kwg-check`                                 | KWG 원본 싱크 상태 확인        | ~1분     |

---

## verify.sh FAIL 시 자주 발생하는 오류

### [1/12] Docusaurus 빌드 실패

```
FAIL: Docusaurus 빌드 실패
```

**원인**: 잘못된 Markdown 문법, 깨진 import, front matter YAML 오류  
**해결**: 빌드 로그에서 오류 파일·줄 번호 확인 → 해당 파일 수정

---

### [2/12] 내부 링크 오류

```
FAIL: 깨진 링크 발견
```

**원인**: 파일 이동·삭제 후 링크 미갱신, 오타  
**해결**: 링크 대상 파일 경로 확인, 상대 경로 수정

---

### [3/12] front matter YAML 오류

```
FAIL: front matter YAML 오류
```

**원인**: `작성일:`, `버전:`, `충족 체크리스트:`, `셀프스터디 소요시간:` 중 누락 또는 잘못된 들여쓰기  
**해결**: docs/ 파일의 front matter 4개 필드 존재 여부 확인

---

### [5/12] 로컬 경로 노출

```
FAIL: 로컬 사용자 경로 노출
```

**원인**: `/Users/사용자명` 또는 `C:\Users\사용자명` 형태의 절대 경로 포함  
**해결**: 상대 경로(`./`) 또는 일반화 경로(`/path/to/trustedoss`)로 교체

---

### [6/12] ISO 섹션 번호 형식 오류

```
FAIL: 18974 섹션 번호 형식 오류
```

**원인**: ISO/IEC 18974 섹션 번호에 `3.x.x` 체계 사용 (5230 체계와 혼용)  
**해결**: 18974는 반드시 `4.x.x` 체계 사용

| 표준          | 올바른 형식 | 잘못된 형식 |
| ------------- | ----------- | ----------- |
| ISO/IEC 5230  | `3.1.1`     | —           |
| ISO/IEC 18974 | `4.1.1`     | ~~`3.1.1`~~ |

---

### [7/12] agent 실행 admonition 누락

```
FAIL: agent 실행 admonition 누락
```

**원인**: `cd agents/...` bash 코드블록 직전에 세션 종료 안내 admonition이 없음  
**해결**: 코드블록 바로 위에 아래 admonition 추가:

```
:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::
```

---

## 처음 기여하신다면

1. 저장소를 fork 하고 브랜치를 만듭니다.
2. 위 "작업 범위"의 O 항목이면 바로 고치셔도 됩니다.
3. `-s` 옵션으로 커밋하고 Pull Request를 엽니다.

`/qa changed` 같은 하네스 명령은 메인테이너용입니다. 실행 환경이 없어도 Pull Request는 여실 수
있습니다. 검증은 CI와 메인테이너가 맡습니다.

---

## 라이선스와 저작권

기여하신 내용의 저작권은 기여자 본인이 그대로 보유합니다. 프로젝트는 그 기여를 문서는
[CC BY 4.0](./LICENSE-docs), 코드는 [MIT](./LICENSE)로 배포합니다.

모든 커밋에는 DCO(Developer Certificate of Origin) 사인오프가 필요합니다. 커밋할 때 `-s`를
붙이면 됩니다.

```bash
git commit -s -m "docs: 정책 템플릿에 예시 추가"
```

커밋 메시지 끝에 아래 한 줄이 남습니다. 그 기여를 프로젝트 라이선스로 제출할 권리가 본인에게
있다는 확인이며, 전문은 [developercertificate.org](https://developercertificate.org/)에 있습니다.

```
Signed-off-by: Your Name <your.email@example.com>
```

이미 만든 커밋에서 빠뜨렸다면 `git commit --amend -s`로, 여러 커밋이면
`git rebase --signoff origin/main`으로 채울 수 있습니다.

프로젝트 운영 방식은 [`GOVERNANCE.md`](./GOVERNANCE.md), 메인테이너 목록은
[`MAINTAINERS.md`](./MAINTAINERS.md)에 있습니다.

---

## 참고 문서

| 문서                             | 내용                                     |
| -------------------------------- | ---------------------------------------- |
| `CLAUDE.md`                      | 작업 범위, 경로 규칙, 스킬·에이전트 목록 |
| `.claude/harness-guide.md`       | QA 하네스 슬래시 커맨드 상세 사용법      |
| `.claude/scripts/verify.sh`      | 검증 항목 전체 소스                      |
| `.claude/reference/iso-5230.md`  | ISO/IEC 5230 스펙 전문                   |
| `.claude/reference/iso-18974.md` | ISO/IEC 18974 스펙 전문                  |

---

<a id="english"></a>

# Contributing Guide

Thank you for contributing to trustedoss.

---

## Scope of Work

This project handles **content work only**.

| Allowed (O)                    | Not Allowed (X)                                   |
| ------------------------------ | ------------------------------------------------- |
| `docs/`                        | `website/src/` (except CSS exceptions)            |
| `agents/`                      | `website/static/`                                 |
| `templates/`                   | `website/src/**/*.ts`, `*.tsx`                    |
| `.claude/`                     | `*.js`, `*.css`, `*.scss` (except CSS exceptions) |
| `CLAUDE.md`                    | All configuration files                           |
| `website/ai-coding/` (md only) |                                                   |
| `website/devsecops/` (md only) |                                                   |

If design or code changes appear necessary, stop work and open an issue for discussion.

---

## 5 Required Steps Before Push

```
Step 1   /qa changed                               # Quality check (requires Claude session)
Step 2   bash .claude/scripts/verify.sh            # Confirm 13/13 PASS
Step 3   Update your progress notes               # Local working notes, not tracked in the repository
Step 4   git add -p && git commit -m "..."         # Stage files selectively
Step 5   git push                                  # Only after all checks pass
```

> **Note**: Use `git add -p` instead of `git add -A` or `git add .` to stage files selectively.
> This prevents accidentally committing `.env`, local config files, or unnecessary binaries.

---

## Verification Command Reference

| Command                                      | Role                                    | Time    |
| -------------------------------------------- | --------------------------------------- | ------- |
| `/qa changed`                                | Auto-check and fix changed file quality | ~2 min  |
| `bash .claude/scripts/verify.sh`             | Run all 13 static validation checks     | ~30 sec |
| `python3 .claude/scripts/test-coverage.py`   | Verify ISO requirement coverage         | ~5 sec  |
| `python3 .claude/scripts/validate-output.py` | Verify output/ deliverable completeness | ~5 sec  |
| `/kwg-check`                                 | Check sync status with KWG source       | ~1 min  |

---

## Common verify.sh FAIL Errors

### [1/12] Docusaurus Build Failure

```
FAIL: Docusaurus 빌드 실패
```

**Cause**: Invalid Markdown syntax, broken imports, or front matter YAML errors  
**Fix**: Check the build log for the error file and line number → fix the file

---

### [2/12] Broken Internal Links

```
FAIL: 깨진 링크 발견
```

**Cause**: Links not updated after file moves or deletions, or typos  
**Fix**: Verify the target file path and correct the relative path

---

### [3/12] Front Matter YAML Error

```
FAIL: front matter YAML 오류
```

**Cause**: Missing or incorrectly indented fields among `작성일:`, `버전:`, `충족 체크리스트:`, `셀프스터디 소요시간:`  
**Fix**: Confirm all 4 front matter fields exist in docs/ files

---

### [5/12] Local Path Exposed

```
FAIL: 로컬 사용자 경로 노출
```

**Cause**: Absolute paths containing `/Users/username` or `C:\Users\username`  
**Fix**: Replace with relative paths (`./`) or generalized paths (`/path/to/trustedoss`)

---

### [6/12] ISO Section Number Format Error

```
FAIL: 18974 섹션 번호 형식 오류
```

**Cause**: ISO/IEC 18974 section numbers using `3.x.x` (mixing with the 5230 scheme)  
**Fix**: ISO/IEC 18974 must always use the `4.x.x` scheme

| Standard      | Correct Format | Incorrect Format |
| ------------- | -------------- | ---------------- |
| ISO/IEC 5230  | `3.1.1`        | —                |
| ISO/IEC 18974 | `4.1.1`        | ~~`3.1.1`~~      |

---

### [7/12] Missing Agent Execution Admonition

```
FAIL: agent 실행 admonition 누락
```

**Cause**: No session-exit admonition immediately before a `cd agents/...` bash code block  
**Fix**: Add the following admonition directly above the code block:

```
:::tip Before Running
First exit the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::
```

---

## Your first contribution

1. Fork the repository and create a branch.
2. If your change falls under the allowed paths above, go ahead and edit.
3. Commit with `-s` and open a pull request.

Harness commands such as `/qa changed` are for maintainers. You can open a pull request without
that setup; CI and the maintainers handle verification.

---

## License and copyright

You keep the copyright in what you contribute. The project distributes contributions as
[CC BY 4.0](./LICENSE-docs) for documentation and [MIT](./LICENSE) for code.

Every commit needs a DCO (Developer Certificate of Origin) sign-off. Add `-s` when you commit.

```bash
git commit -s -m "docs: add an example to the policy template"
```

That appends the line below to your commit message. It certifies that you have the right to
submit the contribution under the project license; the full text is at
[developercertificate.org](https://developercertificate.org/).

```
Signed-off-by: Your Name <your.email@example.com>
```

If you forgot on a commit you already made, use `git commit --amend -s`, or
`git rebase --signoff origin/main` for several commits.

How the project is run is described in [`GOVERNANCE.md`](./GOVERNANCE.md), and the maintainer
list is in [`MAINTAINERS.md`](./MAINTAINERS.md).

---

## Reference Documents

| Document                         | Content                                 |
| -------------------------------- | --------------------------------------- |
| `CLAUDE.md`                      | Scope, path rules, skills & agent list  |
| `.claude/harness-guide.md`       | QA harness slash command detailed usage |
| `.claude/scripts/verify.sh`      | Full source for all validation checks   |
| `.claude/reference/iso-5230.md`  | ISO/IEC 5230 full specification         |
| `.claude/reference/iso-18974.md` | ISO/IEC 18974 full specification        |
