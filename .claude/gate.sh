#!/usr/bin/env bash
# quality-gate 커밋 게이트 — trustedoss
#
# quality-gate 플러그인이 커밋 전에 이 스크립트를 실행한다.
# 프로젝트의 단일 진실 검증인 verify.sh 를 그대로 위임 호출한다.
# (Docusaurus 빌드 / 내부 링크 / front matter / ISO 섹션 번호 /
#  로컬 경로 노출 / agent 체인 등 11개 항목)
set -euo pipefail

# 레포 루트로 이동 (.claude/ 의 부모)
cd "$(dirname "$0")/.."

bash .claude/scripts/verify.sh
