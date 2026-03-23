# 챕터 01 — 환경 준비

## 현재 위치: 1단계 - 환경 준비 (1/7단계)

이 챕터는 이후 모든 실습에서 사용할 도구들을 설치하고 검증하는 단계다.
실습 환경이 완성되어야 이후 단계를 진행할 수 있다.

## 이 챕터의 목표

Docker, Git, Claude Code, Node.js 등 이 키트에서 사용하는 모든 도구가
정상적으로 설치되어 있음을 확인하고, 저장소를 클론하여 실습 환경을 완성한다.

## 충족되는 체크리스트 항목

이 챕터 자체는 체크리스트 항목을 직접 충족하지 않는다 (환경 준비 단계).
그러나 이 단계 없이는 이후 모든 실습이 불가능하다.

## 전제 조건

- macOS, Linux, 또는 Windows (WSL2 권장) 환경
- 인터넷 연결
- 관리자(sudo) 권한

## 설치 확인 명령어

아래 명령어를 실행하여 각 도구의 설치 상태를 확인한다:

```bash
# Docker 확인
docker --version
# 예상: Docker version 24.x.x 이상

# Git 확인
git --version
# 예상: git version 2.x.x

# Claude Code 확인
claude --version
# 예상: 버전 번호 출력

# Node.js 확인
node --version
# 예상: v18.x.x 이상
```

## 설치가 안 된 도구 발견 시

| 도구 | 설치 방법 |
|------|---------|
| Docker Desktop | https://www.docker.com/products/docker-desktop |
| Git | https://git-scm.com/downloads |
| Claude Code | `npm install -g @anthropic-ai/claude-code` |
| Node.js | https://nodejs.org (LTS 버전 권장) |

## 저장소 클론

```bash
git clone https://github.com/haksungjang/trustedoss.git
cd trustedoss
```

## 완료 기준

- [ ] `docker --version` 정상 출력
- [ ] `git --version` 정상 출력
- [ ] `claude --version` 정상 출력
- [ ] `node --version` 정상 출력
- [ ] 저장소 클론 완료
- [ ] `output/` 디렉토리 생성 확인 (없으면 `mkdir output`)

## 셀프스터디 경로

:::info 셀프스터디 모드 (약 30분~1시간)
도구 설치 상황에 따라 소요 시간이 달라집니다.
:::

1. 위의 설치 확인 명령어 4개 실행
2. 오류가 있는 도구 설치
3. 저장소 클론 (이미 있다면 `git pull`)
4. `output/` 디렉토리 생성
5. `claude` 실행하여 정상 동작 확인


## 자주 발생하는 문제

**Q: Docker Desktop이 시작되지 않아요.**
A: macOS에서 보안 경고 시 시스템 환경설정 > 개인 정보 보호 및 보안 > 허용 클릭.

**Q: `claude` 명령이 not found 오류가 나와요.**
A: `npm install -g @anthropic-ai/claude-code` 실행 후 터미널 재시작.

**Q: Node.js 버전이 낮아요.**
A: nvm 사용 권장: `nvm install --lts && nvm use --lts`

**Q: Windows에서 Docker가 느려요.**
A: WSL2 백엔드 사용 권장. Docker Desktop 설정 > General > Use WSL2 based engine 활성화.

## 다음 단계

환경 준비 완료 후:
```bash
cd agents/02-organization-designer
claude
```
또는 `docs/02-organization/` 으로 이동하여 조직 설계 챕터를 읽은 뒤 진행.
