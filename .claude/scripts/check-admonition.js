/**
 * check-admonition.js
 * PostToolUse hook: Write/Edit 직후 실행.
 * docs/ 파일에 cd agents/ 블록이 있으나 직전 admonition이 없으면 경고 출력.
 *
 * 입력: Claude Code 훅 페이로드는 stdin으로 JSON이 전달된다.
 *       (tool_input.file_path 에 수정된 파일 경로가 담긴다)
 */

import fs from 'fs';
import path from 'path';

// stdin에서 훅 페이로드 읽어 파일 경로 추출
let filePath = '';
try {
  const payload = JSON.parse(fs.readFileSync(0, 'utf8'));
  filePath =
    (payload.tool_input && payload.tool_input.file_path) ||
    (payload.tool_response && payload.tool_response.filePath) ||
    '';
} catch {
  // stdin이 비었거나 JSON이 아니면 검사할 대상 없음
  process.exit(0);
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
      `   verify.sh [7/12] FAIL 원인이 됩니다. doc-fixer 또는 수동으로 admonition을 추가하세요.\n`
  );
}
