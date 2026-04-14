/**
 * check-admonition.js
 * PostToolUse hook: Write/Edit 직후 실행.
 * docs/ 파일에 cd agents/ 블록이 있으나 직전 admonition이 없으면 경고 출력.
 *
 * 환경변수: CLAUDE_TOOL_OUTPUT (수정된 파일 경로 포함 JSON 문자열)
 */

const fs = require('fs');
const path = require('path');

// 파일 경로 추출
const toolOutput = process.env.CLAUDE_TOOL_OUTPUT || '';
let filePath = '';

try {
  const parsed = JSON.parse(toolOutput);
  filePath = parsed.filePath || parsed.path || '';
} catch {
  // JSON이 아니면 문자열에서 경로 추출 시도
  const match = toolOutput.match(/docs\/[^\s"']+\.md/);
  if (match) filePath = match[0];
}

// docs/ 파일만 검사
if (!filePath || !filePath.includes('docs/') || !filePath.endsWith('.md')) {
  process.exit(0);
}

// CLAUDE.md 제외
if (path.basename(filePath) === 'CLAUDE.md') {
  process.exit(0);
}

// 파일 읽기
if (!fs.existsSync(filePath)) process.exit(0);

const content = fs.readFileSync(filePath, 'utf8');
const lines = content.split('\n');

// cd agents/ 패턴이 있는 줄 탐색
let hasViolation = false;
const violations = [];

for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('cd agents/')) {
    // 직전 10줄에 :::tip 실행 전 확인 있는지 확인
    const start = Math.max(0, i - 10);
    const context = lines.slice(start, i).join('\n');
    if (!context.includes(':::tip 실행 전 확인')) {
      hasViolation = true;
      violations.push(i + 1); // 1-based 라인 번호
    }
  }
}

if (hasViolation) {
  console.warn(
    `\n⚠️  [check-admonition] ${filePath}\n` +
      `   라인 ${violations.join(', ')}: cd agents/ 블록 직전에 :::tip 실행 전 확인 admonition 없음.\n` +
      `   verify.sh [7/8] FAIL 원인이 됩니다. doc-fixer 또는 수동으로 admonition을 추가하세요.\n`
  );
}
