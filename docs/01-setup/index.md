---
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - "ISO/IEC 5230: []"
  - "ISO/IEC 18974: []"
셀프스터디 소요시간: 30분~1시간
---

# 환경 준비: 실습에 필요한 도구 설치

## 1. 이 챕터에서 하는 일

이 키트의 모든 실습에서 사용할 도구를 설치하고 검증합니다.

- 이 단계가 완료되어야 이후 agent 실행이 가능하다
- 이 챕터 자체는 ISO/IEC 5230 또는 ISO/IEC 18974의 체크리스트 항목을 직접 충족하지 않는다
- 그러나 이 단계 없이는 이후 모든 실습이 불가능하므로 반드시 완료해야 한다

## 2. 필요한 도구 목록

| 도구 | 용도 | 설치 필요 여부 | 버전 요구사항 |
|------|------|--------------|-------------|
| Docker Desktop | 모든 실습 도구(Dependency-Track 등) 실행 | 필수 | 24.x 이상 |
| Git | 저장소 관리 및 버전 관리 | 필수 | 2.x 이상 |
| Claude Code | AI 기반 실습 보조, agent 실행 | 필수 | 최신 버전 |
| Node.js | Docusaurus 문서 사이트 빌드 | 선택 (문서 사이트 필요 시) | v18 LTS 이상 |

## 3. 설치 안내 (OS별)

### macOS

```bash
# Docker Desktop
# https://www.docker.com/products/docker-desktop 에서 다운로드

# Git (Homebrew 사용)
brew install git

# Claude Code
npm install -g @anthropic-ai/claude-code

# Node.js (선택 - Homebrew)
brew install node
```

### Windows

WSL2 사용을 권장합니다. Docker Desktop 설치 시 WSL2 백엔드를 활성화해야 합니다.

```powershell
# Docker Desktop: https://www.docker.com/products/docker-desktop 에서 다운로드
# WSL2 활성화 필요

# Git for Windows: https://git-scm.com/download/win

# Claude Code (PowerShell)
npm install -g @anthropic-ai/claude-code
```

### Linux (Ubuntu/Debian)

```bash
# Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER

# Git
sudo apt-get install git

# Claude Code
npm install -g @anthropic-ai/claude-code

# Node.js (선택 - nvm 사용 권장)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

## 4. 설치 확인 명령어 모음

아래 스크립트를 실행하여 모든 필수 도구가 정상 설치되었는지 한 번에 확인합니다.

```bash
#!/bin/bash
echo "=== trustedoss 환경 확인 ==="

echo -n "Docker: "
docker --version 2>/dev/null || echo "❌ 미설치"

echo -n "Git: "
git --version 2>/dev/null || echo "❌ 미설치"

echo -n "Claude Code: "
claude --version 2>/dev/null || echo "❌ 미설치"

echo -n "Node.js (선택): "
node --version 2>/dev/null || echo "⚪ 미설치 (선택사항)"

echo ""
echo "모든 필수 도구가 설치되면 다음 단계로 진행하세요."
```

## 5. 저장소 클론 및 첫 실행

처음 시작하는 경우:

```bash
# 저장소 클론
git clone https://github.com/haksungjang/trustedoss.git
cd trustedoss

# output 디렉토리 생성 (없는 경우)
mkdir -p output

# Claude Code 실행
claude
```

이미 클론한 경우:

```bash
cd trustedoss
git pull
claude
```

## 6. Claude Code 첫 실행 후 할 일

Claude Code가 실행되면:

1. **"어디서 시작해야 해?"** 입력 → 현재 상태 분석 후 다음 단계 자동 안내
2. 처음 실행이라면 `output/` 폴더가 비어있으므로 `02-organization-designer` agent 안내를 받게 된다
3. Claude Code는 `CLAUDE.md`를 자동으로 읽어 프로젝트 맥락을 이해한다

> Claude Code는 각 챕터 폴더의 `CLAUDE.md`도 함께 읽어 해당 단계의 맥락을 파악합니다.

## 7. 트러블슈팅

### Docker Desktop이 실행 안 될 때

- **macOS**: 시스템 환경설정 > 개인 정보 보호 및 보안 > 허용 클릭
- **Windows**: Hyper-V 및 WSL2 활성화 필요
- **Linux**: `sudo systemctl start docker` 실행 후 재시도

### Claude Code 로그인 안 될 때

- `claude login` 실행하여 Anthropic 계정으로 인증
- 브라우저가 자동으로 열리지 않으면 터미널에 표시된 URL을 복사하여 수동 접속

### git clone 권한 오류

- HTTPS 방식으로 클론: `git clone https://github.com/haksungjang/trustedoss.git`
- GitHub 인증 오류 시: `git config --global credential.helper store` 실행 후 재시도

### Node.js 버전이 너무 낮을 때 (v18 미만)

- nvm 사용 권장: `nvm install --lts && nvm use --lts`

## 8. 셀프 스터디

:::info 셀프스터디 모드 (약 30분~1시간)
도구 설치 상황에 따라 소요 시간이 달라집니다.
:::

1. 필요한 도구 목록 확인
2. 각 도구 설치 (미설치된 경우)
3. 설치 확인 스크립트 실행
4. 저장소 클론 및 `output/` 생성
5. `claude` 실행 후 "어디서 시작해야 해?" 입력

## 9. 완료 확인 체크리스트

- [ ] `docker --version` 정상 출력
- [ ] `git --version` 정상 출력
- [ ] `claude --version` 정상 출력
- [ ] 저장소 클론 완료 (또는 이미 존재)
- [ ] `output/` 디렉토리 존재
- [ ] `claude` 실행 후 정상 동작 확인

## 10. 다음 단계

환경 준비가 완료되면 조직 설계 단계로 진행합니다.

[조직 구성: 오픈소스 담당자 지정과 역할 정의](../02-organization/index.md) 챕터를 먼저 읽은 뒤 agent를 실행하거나, 바로 agent를 실행해도 됩니다.

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/02-organization-designer
claude
```
