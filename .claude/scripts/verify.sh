#!/bin/bash
# trustedoss 자체 검증 스크립트
# Claude Code가 작업 완료 후 반드시 실행

PASS=0
FAIL=0
WARNINGS=()

echo "===== trustedoss 자체 검증 시작 ====="

# 검증 1: Docusaurus 빌드
echo "[1/6] Docusaurus 빌드 확인..."
if npm run build --silent 2>/dev/null; then
  echo "  PASS: 빌드 성공"
  PASS=$((PASS+1))
else
  echo "  FAIL: 빌드 실패"
  FAIL=$((FAIL+1))
fi

# 검증 2: 내부 링크 확인
echo "[2/6] 내부 링크 확인..."
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
  done < <(grep -Eo '\]\([^)]+\)' "$file" | sed 's/\](\(.*\))/\1/' | grep -v "^http")
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
echo "[3/6] Front matter YAML 형식 확인..."
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
echo "[4/6] 필수 파일 존재 확인..."
REQUIRED_FILES=(
  "CLAUDE.md"
  "README.md"
  "website/docusaurus.config.ts"
  ".github/workflows/deploy.yml"
  ".claude/settings.json"
  ".claude/skills/create-doc.md"
  ".claude/skills/validate-checklist.md"
  ".claude/skills/generate-report.md"
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
echo "[5/6] 로컬 경로 노출 확인..."
LOCAL_PATH_HITS=$(git ls-files \
  -- '*.md' '*.sh' '*.yml' '*.yaml' '*.json' '*.ts' \
  2>/dev/null | \
  grep -v "^\.claude/scripts/verify\.sh$" | \
  grep -v "^\.claude/settings\.local\.json$" | \
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
# 18974는 §4.x.x 체계 — §3.x.x 형식이 같은 줄에 있으면 오류
echo "[6/6] ISO/IEC 18974 섹션 번호 형식 확인..."
SPEC_ERRORS=0
while IFS= read -r match; do
  WARNINGS+=("18974 번호 오류 (§4.x.x 이어야 함): $match")
  SPEC_ERRORS=$((SPEC_ERRORS+1))
done < <(grep -rn "18974[^(0-9]*3\.[1-9]\.[0-9]" \
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
