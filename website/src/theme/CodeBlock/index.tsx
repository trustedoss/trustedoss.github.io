/**
 * CodeBlock 스위즐 (wrapper)
 * 모든 코드블록에 언어 라벨 헤더 바를 띄운다 (Gemini docs 스타일).
 * Docusaurus의 `title` 메커니즘을 재사용 → 헤더 바 + 복사 버튼이 함께 렌더됨.
 * 명시적 title이 있으면 그대로 둔다.
 */
import React from 'react';
import OriginalCodeBlock from '@theme-original/CodeBlock';
import type CodeBlockType from '@theme/CodeBlock';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof CodeBlockType>;

const LABELS: Record<string, string> = {
  bash: 'Bash',
  sh: 'Shell',
  shell: 'Shell',
  json: 'JSON',
  yaml: 'YAML',
  yml: 'YAML',
  java: 'Java',
  kotlin: 'Kotlin',
  groovy: 'Groovy',
  diff: 'Diff',
  text: 'Text',
  md: 'Markdown',
  markdown: 'Markdown',
  ts: 'TypeScript',
  tsx: 'TSX',
  js: 'JavaScript',
  jsx: 'JSX',
  python: 'Python',
  py: 'Python',
  xml: 'XML',
  toml: 'TOML',
  dockerfile: 'Dockerfile',
};

function langLabel(className?: string): string | undefined {
  const m = /language-([\w-]+)/.exec(className ?? '');
  if (!m) {
    return undefined;
  }
  const key = m[1].toLowerCase();
  return LABELS[key] ?? key.charAt(0).toUpperCase() + key.slice(1);
}

export default function CodeBlock(props: Props): JSX.Element {
  const {className, title} = props as {className?: string; title?: string};
  const resolvedTitle = title ?? langLabel(className);
  return <OriginalCodeBlock {...props} title={resolvedTitle} />;
}
