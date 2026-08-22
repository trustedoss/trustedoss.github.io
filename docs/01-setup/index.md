---
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
셀프스터디 소요시간: 30분~1시간
---

# 환경 준비: 실습에 필요한 도구 설치

## 1. 이 챕터에서 하는 일

이 키트의 모든 실습에서 사용할 도구를 설치하고 검증합니다.

- 이 단계가 완료되어야 이후 agent 실행이 가능합니다
- 이 챕터 자체는 ISO/IEC 5230 또는 ISO/IEC 18974의 체크리스트 항목을 직접 충족하지 않습니다
- 그러나 이 단계 없이는 이후 모든 실습이 불가능하므로 반드시 완료해야 합니다

## 2. 터미널 열기

이 챕터부터는 **터미널**(글자로 명령을 입력해 컴퓨터를 조작하는 검은 화면의 프로그램)을 사용합니다.
아래 코드블록은 전부 이 터미널 안에 입력하는 명령어입니다.

**macOS에서 터미널 여는 법**

1. 키보드에서 `Cmd` 키와 `Space` 키를 동시에 누릅니다 (Spotlight 검색이 열립니다).
2. `터미널` 또는 영어로 `Terminal`이라고 입력합니다.
3. 검색 결과에 뜨는 "터미널" 앱을 클릭(또는 Enter)해서 엽니다.

**Windows에서 터미널 여는 법**

1. 시작 메뉴를 클릭하거나 키보드에서 `Windows` 키를 누릅니다.
2. `PowerShell`이라고 입력합니다.
3. "Windows PowerShell" 앱을 클릭해서 엽니다.

터미널을 열면 커서가 깜빡이는 빈 화면이 나옵니다. 이 화면에 이 문서의 코드블록 내용을 그대로
입력하거나 붙여넣고 Enter 키를 누르면 명령이 실행됩니다.

:::tip 코드블록 복사해서 붙여넣기
이 문서의 회색 코드블록에 마우스를 올리면 오른쪽 위에 복사 아이콘이 나타납니다. 이 아이콘을
클릭하면 블록 전체가 복사됩니다. 터미널 화면을 클릭한 뒤 macOS는 `Cmd+V`, Windows는
`Ctrl+V`(또는 마우스 오른쪽 버튼 클릭 → 붙여넣기)로 붙여넣고 Enter를 누르세요. 여러 줄로 된
블록도 한 번에 붙여넣고 Enter 한 번이면 순서대로 전부 실행됩니다.
:::

:::tip "새 터미널을 여세요"라는 안내를 만나면
이 가이드 곳곳에 "Claude 세션을 종료한 뒤 새 터미널에서 실행하세요"라는 안내가 나옵니다. "새
터미널을 연다"는 것은 지금 쓰던 터미널 창을 그대로 두고 위 방법으로 터미널 앱을 한 번 더 여는
것을 뜻합니다(같은 방법을 반복하면 됩니다). 기존 창을 닫아도 되고, 그대로 둔 채 새 창을 하나 더
열어도 됩니다.
:::

## 3. 필요한 도구 목록

| 도구           | 용도                                            | 설치 필요 여부                  | 버전 요구사항 |
| -------------- | ----------------------------------------------- | ------------------------------- | ------------- |
| Docker Desktop | 챕터 05 도구 실습(Dependency-Track 등) 실행     | 챕터 05만 사용 (대체 경로 있음) | 24.x 이상     |
| Git            | 저장소 관리 및 버전 관리                        | 필수                            | 2.x 이상      |
| Claude Code    | AI 기반 실습 보조, agent 실행                   | 필수                            | 최신 버전     |
| Node.js        | Docusaurus 문서 사이트를 직접 빌드하려는 경우만 | 선택 (아래 실습에는 불필요)     | v18 LTS 이상  |

:::info Node.js가 없어도 Claude Code를 설치할 수 있습니다
아래 4절의 Claude Code 설치 명령은 Node.js 없이 바로 실행됩니다. Node.js는 이 웹사이트를 직접
빌드해 보고 싶을 때만 필요하며, 이 키트의 실습(agent 실행, 산출물 생성)에는 전혀 쓰이지 않습니다.
:::

:::tip Docker를 설치할 수 없다면
Docker는 챕터 05(SBOM·취약점 도구 실습)에서만 사용합니다. 회사 정책 등으로 설치가 어렵다면, 챕터 05의 "Docker 없이 진행하는 경우" 경로에서 미리 만든 샘플 SBOM으로 실습을 이어갈 수 있습니다. 나머지 챕터(02 조직~04 프로세스, 06 교육~07 인증)는 Docker 없이 agent 대화만으로 진행됩니다.
:::

## 4. 설치 안내 (OS별)

### macOS

터미널에 아래 명령을 한 줄씩(또는 전체를 한 번에) 붙여넣고 실행합니다.

```bash
# Git — macOS는 별도 설치 프로그램이 필요 없습니다.
# 아래 명령을 실행하면, git이 없을 경우 "Command Line Tools를 설치하시겠습니까?"라는
# 팝업이 뜹니다. "설치"를 클릭하고 몇 분 기다리면 git이 함께 설치됩니다.
git --version

# Claude Code (Node.js 불필요, Homebrew 불필요)
curl https://claude.sh | bash

# Docker Desktop — 아래 명령은 브라우저에서 다운로드 페이지를 엽니다.
# 다운로드된 .dmg 파일을 더블클릭하고 안내에 따라 Applications 폴더로 끌어다 놓으세요.
open https://www.docker.com/products/docker-desktop
```

:::tip Node.js를 직접 설치하고 싶다면(선택)
문서 사이트를 직접 빌드해 보고 싶은 경우에만 필요합니다. [nodejs.org](https://nodejs.org)에서
"LTS" 버전 설치 프로그램(.pkg)을 내려받아 더블클릭하면 됩니다.
:::

### Windows

WSL2 사용을 권장합니다. Docker Desktop 설치 시 WSL2 백엔드를 활성화해야 합니다.

```powershell
# Git for Windows: https://git-scm.com/download/win 에서 설치 프로그램을 내려받아 실행

# Claude Code (Node.js 불필요)
curl https://claude.sh | bash

# 또는 winget이 있다면:
winget install Anthropic.Claude

# Docker Desktop: https://www.docker.com/products/docker-desktop 에서 다운로드
# 설치 중 "WSL2 사용" 옵션이 나오면 체크
```

### Linux (Ubuntu/Debian)

```bash
# Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER

# Git
sudo apt-get install git

# Claude Code (Node.js 불필요)
curl https://claude.sh | bash
```

## 5. 설치 확인 명령어 모음

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

## 6. 저장소 클론 및 첫 실행

**git clone이란?** 이 키트의 모든 파일(agent, 템플릿, 가이드 문서)은 GitHub라는 사이트에
저장돼 있습니다. `git clone` 명령은 그 파일 전체를 인터넷에서 내 컴퓨터로 통째로 내려받아
복사하는 명령입니다. 한 번만 실행하면 되고, 이후에는 내 컴퓨터에 생긴 `trustedoss-agents`라는
폴더 안에서 계속 작업합니다.

처음 시작하는 경우:

```bash
# 저장소 클론(파일 내려받기)
git clone https://github.com/trustedoss/trustedoss-agents.git
cd trustedoss-agents

# output 디렉토리 생성 (없는 경우)
mkdir -p output

# Claude Code 실행
claude
```

이미 클론한 경우(전에 한 번 내려받은 적이 있다면):

```bash
cd trustedoss-agents
git pull
claude
```

## 7. Claude Code 첫 실행 후 할 일

Claude Code가 실행되면:

1. **"어디서 시작해야 해?"** 입력 → 현재 상태 분석 후 다음 단계 자동 안내
2. 처음 실행이라면 `output/` 폴더가 비어있으므로 `02-organization-designer` agent 안내를 받게 됩니다
3. Claude Code는 `CLAUDE.md`를 자동으로 읽어 프로젝트 맥락을 이해합니다

:::info
Claude Code는 각 챕터 폴더의 `CLAUDE.md`도 함께 읽어 해당 단계의 맥락을 파악합니다.
:::

## 8. 트러블슈팅

### "Cannot connect to the Docker daemon" 오류가 뜰 때

이 메시지는 Docker Desktop 프로그램이 아직 켜지지 않았다는 뜻입니다(설치와 실행은 별개입니다).

- **macOS/Windows**: Launchpad(macOS) 또는 시작 메뉴(Windows)에서 "Docker Desktop" 앱을
  찾아 클릭해서 실행합니다. 화면 위쪽(macOS 메뉴바) 또는 트레이(Windows)에 고래 모양 아이콘이
  뜨고 움직임이 멈추면 준비된 것입니다. 그 후 다시 명령을 실행하세요.
- **Linux**: `sudo systemctl start docker` 실행 후 재시도

### Docker Desktop이 실행 안 될 때

- **macOS**: 시스템 환경설정 > 개인 정보 보호 및 보안 > 허용 클릭
- **Windows**: Hyper-V 및 WSL2 활성화 필요
- **Linux**: `sudo systemctl start docker` 실행 후 재시도

### "brew: command not found" 같은 오류가 뜰 때

이 가이드의 macOS 설치 명령은 Homebrew 없이 실행되도록 구성돼 있습니다. 이 오류가 뜬다면 이
문서의 다른 버전 안내를 따라 하고 있는 것일 수 있으니, 4절의 명령을 그대로 다시 붙여넣어
실행해 보세요.

### Claude Code 로그인 안 될 때

- `claude` 실행 후 세션 안에서 `/login` 을 입력하여 Anthropic 계정으로 인증
- 브라우저가 자동으로 열리지 않으면 터미널에 표시된 URL을 복사하여 수동 접속

### git clone 권한 오류

- HTTPS 방식으로 클론: `git clone https://github.com/trustedoss/trustedoss-agents.git`
- GitHub 인증 오류 시: `git config --global credential.helper store` 실행 후 재시도

### Node.js 버전이 너무 낮을 때 (v18 미만, 문서 사이트를 직접 빌드하는 경우만 해당)

- nvm 사용 권장: `nvm install --lts && nvm use --lts`

## 9. 셀프 스터디

:::info 셀프스터디 모드 (약 30분~1시간)
도구 설치 상황에 따라 소요 시간이 달라집니다.
:::

1. 필요한 도구 목록 확인
2. 각 도구 설치 (미설치된 경우)
3. 설치 확인 스크립트 실행
4. 저장소 클론 및 `output/` 생성
5. `claude` 실행 후 "어디서 시작해야 해?" 입력

## 10. 완료 확인 체크리스트

- [ ] `docker --version` 정상 출력 (Docker 미사용 경로 선택 시 생략)
- [ ] `git --version` 정상 출력
- [ ] `claude --version` 정상 출력
- [ ] 저장소 클론 완료 (또는 이미 존재)
- [ ] `output/` 디렉토리 존재
- [ ] `claude` 실행 후 정상 동작 확인

## 11. 다음 단계

환경 준비가 완료되면 조직 설계 단계로 진행합니다.

[조직 구성: 오픈소스 담당자 지정과 역할 정의](../02-organization/index.md) 챕터를 먼저 읽은 뒤 agent를 실행하거나, 바로 agent를 실행해도 됩니다.

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/02-organization-designer
claude
```

에이전트가 끝나면 레포 루트로 돌아와(`cd ../..`) 산출물을 확인하세요: `ls output/organization/` — 파일 3개(역할 정의, RACI 매트릭스, 임명장 템플릿)가 보이면 성공입니다.
