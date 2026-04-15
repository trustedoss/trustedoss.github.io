#!/bin/bash
# trustedoss 자체 검증 스크립트
# Claude Code가 작업 완료 후 반드시 실행

PASS=0
FAIL=0
WARNINGS=()

echo "===== trustedoss 자체 검증 시작 ====="

# 검증 1: Docusaurus 빌드
echo "[1/11] Docusaurus 빌드 확인..."
if npm run build --silent 2>/dev/null; then
  echo "  PASS: 빌드 성공"
  PASS=$((PASS+1))
else
  echo "  FAIL: 빌드 실패"
  FAIL=$((FAIL+1))
fi

# 검증 2: 내부 링크 확인
echo "[2/11] 내부 링크 확인..."
BROKEN=0
while IFS= read -r file; do
  while IFS= read -r link; do
    # 앵커(#) 제거 후 파일 경로만 추출
    filepath=$(echo "$link" | sed 's/#.*//')
    [ -z "$filepath" ] && continue
    # 상대 경로 기준 실제 파일 존재 여부 확인
    dir=$(dirname "$file")
    if [ ! -e "$dir/$filepath" ] && \
       [ ! -e "$filepath" ]; then
      WARNINGS+=("깨진 링크: $file → $link")
      BROKEN=$((BROKEN+1))
    fi
  done < <(grep -Eo '\]\([^)]+\)' "$file" | sed 's/\](\(.*\))/\1/' | grep -v "^http" | grep -v "^/")
done < <(find docs README.md workshop -name "*.md" \
         2>/dev/null)

if [ $BROKEN -eq 0 ]; then
  echo "  PASS: 내부 링크 이상 없음"
  PASS=$((PASS+1))
else
  echo "  WARN: 깨진 내부 링크 ${BROKEN}개 발견"
  FAIL=$((FAIL+1))
fi

# 검증 3: YAML front matter 콜론 확인
echo "[3/11] Front matter YAML 형식 확인..."
FM_ERRORS=0
while IFS= read -r file; do
  # front matter 추출 후 콜론 포함 값 따옴표 여부 확인
  in_fm=0
  fm_count=0
  while IFS= read -r line; do
    if [ "$line" = "---" ]; then
      fm_count=$((fm_count+1))
      [ $fm_count -eq 1 ] && in_fm=1
      [ $fm_count -eq 2 ] && in_fm=0
      continue
    fi
    if [ $in_fm -eq 1 ]; then
      # 키: 값 형태에서 값에 콜론이 있고 따옴표 없는 경우 감지
      if echo "$line" | grep -qE '^[a-zA-Z가-힣_-]+: .*:' && \
         ! echo "$line" | grep -qE '^[a-zA-Z가-힣_-]+: "'; then
        WARNINGS+=("따옴표 누락: $file → $line")
        FM_ERRORS=$((FM_ERRORS+1))
      fi
    fi
  done < "$file"
done < <(find docs -name "*.md" 2>/dev/null)

if [ $FM_ERRORS -eq 0 ]; then
  echo "  PASS: Front matter 형식 이상 없음"
  PASS=$((PASS+1))
else
  echo "  WARN: Front matter 오류 ${FM_ERRORS}개"
  FAIL=$((FAIL+1))
fi

# 검증 4: 필수 파일 존재 확인
echo "[4/11] 필수 파일 존재 확인..."
REQUIRED_FILES=(
  "CLAUDE.md"
  "README.md"
  "website/docusaurus.config.ts"
  ".github/workflows/deploy.yml"
  ".claude/settings.json"
  ".claude/skills/create-doc.md"
  ".claude/skills/validate-checklist.md"
  ".claude/skills/generate-report.md"
  ".claude/skills/update-reference-samples.md"
  "templates/process/contribution-process.md"
  "templates/process/inquiry-response.md"
  "templates/process/project-publication-process.md"
  "templates/organization/appointment-template.md"
)
MISSING=0
for f in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    WARNINGS+=("누락 파일: $f")
    MISSING=$((MISSING+1))
  fi
done

if [ $MISSING -eq 0 ]; then
  echo "  PASS: 필수 파일 모두 존재"
  PASS=$((PASS+1))
else
  echo "  FAIL: 누락 파일 ${MISSING}개"
  FAIL=$((FAIL+1))
fi

# 검증 5: 로컬 경로 노출 확인
# (git ls-files 기준 — gitignore 된 파일 제외, verify.sh 자신 제외)
echo "[5/11] 로컬 경로 노출 확인..."
LOCAL_PATH_HITS=$(git ls-files \
  -- '*.md' '*.sh' '*.yml' '*.yaml' '*.json' '*.ts' \
  2>/dev/null | \
  grep -v "^\.claude/scripts/verify\.sh$" | \
  grep -v "settings\.local\.json$" | \
  grep -v "^\.claude/reference/kwg/" | \
  xargs grep -ln "/Users/[^/]*/\|/home/[^/]*/" 2>/dev/null || true)

LOCAL_PATH_COUNT=$(echo "$LOCAL_PATH_HITS" | grep -c . || true)

if [ "$LOCAL_PATH_COUNT" -eq 0 ] || [ -z "$LOCAL_PATH_HITS" ]; then
  echo "  PASS: 로컬 경로 노출 없음"
  PASS=$((PASS+1))
else
  echo "  FAIL: 로컬 경로가 포함된 파일 ${LOCAL_PATH_COUNT}개 발견"
  echo "$LOCAL_PATH_HITS" | while IFS= read -r f; do
    grep -n "/Users/[^/]*/\|/home/[^/]*/" "$f" 2>/dev/null | \
      sed "s|^|  $f:|"
  done
  FAIL=$((FAIL+1))
fi

# 검증 6: ISO/IEC 18974 섹션 번호 형식 확인
# 18974는 §4.x.x 체계 — 아래 2가지 패턴으로 §3.x.x 오표기 탐지
echo "[6/11] ISO/IEC 18974 섹션 번호 형식 확인..."
SPEC_ERRORS=0

# 패턴 1: 본문 텍스트 "18974 3.x.x" 형식 (괄호·숫자 이전까지만 탐색)
# [^(0-9]*: ( 와 숫자 이전까지만 허용 — "4.3.2.1" 안의 "3.2.1"을 오탐하지 않음
while IFS= read -r match; do
  WARNINGS+=("18974 번호 오류 (§4.x.x 이어야 함): $match")
  SPEC_ERRORS=$((SPEC_ERRORS+1))
done < <(grep -rn "18974[^(0-9]*3\.[1-9]\.[0-9]" \
    docs/ agents/ \
    --include="*.md" \
    2>/dev/null | \
    grep -v "\.claude/reference/")

# 패턴 2: 괄호/대괄호 안 "18974 G?.? (3.x.x)" 또는 "[3.x.x]" 형식
# [\[(]3\.: [ 또는 ( 바로 뒤에 3.이 오는 경우만 탐지 — "§4.3.1" 형태는 오탐 없음
while IFS= read -r match; do
  WARNINGS+=("18974 번호 오류 (§4.x.x 이어야 함): $match")
  SPEC_ERRORS=$((SPEC_ERRORS+1))
done < <(grep -rn "18974[^)]*[\[(]3\.[1-9]" \
    docs/ agents/ \
    --include="*.md" \
    2>/dev/null | \
    grep -v "\.claude/reference/")

if [ $SPEC_ERRORS -eq 0 ]; then
  echo "  PASS: 18974 섹션 번호 형식 이상 없음"
  PASS=$((PASS+1))
else
  echo "  FAIL: 18974 섹션 번호 오류 ${SPEC_ERRORS}개 (§3.x.x → §4.x.x 로 수정 필요)"
  FAIL=$((FAIL+1))
fi

# 검증 7: agent 실행 블록 admonition 누락 확인
# docs/ 내 bash 블록에 'cd agents/'가 있으면 직전 10줄에 ':::tip 실행 전 확인'이 있어야 함
echo "[7/11] agent 실행 admonition 누락 확인..."
ADMON_ERRORS=0
while IFS= read -r result; do
  WARNINGS+=("admonition 누락: $result")
  ADMON_ERRORS=$((ADMON_ERRORS+1))
done < <(python3 - <<'PYEOF'
import os, sys

docs_dir = 'docs'
violations = []

for root, dirs, files in os.walk(docs_dir):
    for fname in files:
        if not fname.endswith('.md'):
            continue
            # CLAUDE.md 는 내부 지침 파일 — admonition 검사 제외
        if fname == 'CLAUDE.md':
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, encoding='utf-8') as f:
            lines = f.readlines()
        i = 0
        while i < len(lines):
            # bash 블록 시작 탐지
            if lines[i].strip() == '```bash':
                block_start = i
                block_lines = []
                j = i + 1
                while j < len(lines) and lines[j].strip() != '```':
                    block_lines.append(lines[j])
                    j += 1
                # cd agents/ 포함 여부 확인
                if any('cd agents/' in bl for bl in block_lines):
                    # 직전 10줄에 admonition 있는지 확인
                    preceding = lines[max(0, block_start - 10):block_start]
                    if not any(':::tip 실행 전 확인' in pl for pl in preceding):
                        # 위반 위치와 명령어 출력
                        cmd = next((bl.strip() for bl in block_lines if 'cd agents/' in bl), '')
                        violations.append(f'{fpath}:{block_start + 1} — {cmd}')
                i = j
            i += 1

for v in violations:
    print(v)
PYEOF
)

if [ $ADMON_ERRORS -eq 0 ]; then
  echo "  PASS: agent 실행 admonition 이상 없음"
  PASS=$((PASS+1))
else
  echo "  FAIL: admonition 누락 ${ADMON_ERRORS}곳 발견"
  FAIL=$((FAIL+1))
fi

# 검증 8: ISO 커버리지 정합성 (test-coverage.py)
echo "[8/11] ISO 커버리지 정합성 확인..."
if python3 "$(dirname "$0")/test-coverage.py" 2>/dev/null; then
  echo "  PASS: ISO 커버리지 정합성 이상 없음"
  PASS=$((PASS+1))
else
  echo "  FAIL: ISO 커버리지 갭 발견 — python3 .claude/scripts/test-coverage.py 실행하여 상세 확인"
  FAIL=$((FAIL+1))
fi

# 검증 9: output/ 산출물 완전성 (validate-output.py)
echo "[9/11] output/ 산출물 완전성 확인..."
if python3 "$(dirname "$0")/validate-output.py" 2>/dev/null; then
  echo "  PASS: output/ 산출물 완전성 이상 없음"
  PASS=$((PASS+1))
else
  echo "  FAIL: output/ 산출물 미완료 항목 발견 — python3 .claude/scripts/validate-output.py 실행하여 상세 확인"
  FAIL=$((FAIL+1))
fi

# 검증 10: Agent CLAUDE.md 스펙 구조 검증 (test-agent-specs.py)
echo "[10/11] Agent 스펙 구조 확인..."
if python3 "$(dirname "$0")/test-agent-specs.py" 2>/dev/null; then
  echo "  PASS: Agent 스펙 구조 이상 없음"
  PASS=$((PASS+1))
else
  echo "  FAIL: Agent 스펙 구조 오류 발견 — python3 .claude/scripts/test-agent-specs.py 실행하여 상세 확인"
  FAIL=$((FAIL+1))
fi

# 검증 11: 골든 픽스처 회귀 테스트 (test-output-fixtures.py)
echo "[11/11] 골든 픽스처 회귀 테스트..."
if python3 "$(dirname "$0")/test-output-fixtures.py" 2>/dev/null; then
  echo "  PASS: output-sample/ 골든 픽스처 유효"
  PASS=$((PASS+1))
else
  echo "  FAIL: 골든 픽스처 검증 실패 — python3 .claude/scripts/test-output-fixtures.py 실행하여 상세 확인"
  FAIL=$((FAIL+1))
fi

# 최종 결과 출력
echo ""
echo "===== 검증 결과 ====="
echo "PASS: ${PASS}개 / FAIL: ${FAIL}개"

if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo ""
  echo "--- 경고 목록 ---"
  for w in "${WARNINGS[@]}"; do
    echo "  ! $w"
  done
fi

if [ $FAIL -eq 0 ]; then
  echo ""
  echo "모든 검증 통과. 푸시해도 좋습니다."
  exit 0
else
  echo ""
  echo "검증 실패 항목이 있습니다. 수정 후 재실행하세요."
  exit 1
fi
