"""
docs/ 하위 본문 .md 파일의 한다체 → 합니다체 일괄 치환.
제외 대상:
  - 파일명이 CLAUDE.md인 파일
  - 코드블록(``` ~ ```) 내부
  - front matter(--- ~ ---) 내부
"""

import re
import os
from pathlib import Path

# 치환 규칙 (순서 중요 — 긴 패턴 먼저)
REPLACEMENTS = [
    # 복합 패턴 (먼저 처리)
    (r'해야 한다\.', '해야 합니다.'),
    (r'해야 한다 ', '해야 합니다 '),
    (r'할 수 있다\.', '할 수 있습니다.'),
    (r'할 수 없다\.', '할 수 없습니다.'),
    (r'알 수 없다\.', '알 수 없습니다.'),
    (r'될 수 있다\.', '될 수 있습니다.'),
    (r'볼 수 있다\.', '볼 수 있습니다.'),
    (r'써도 된다\.', '써도 됩니다.'),
    (r'선택해도 된다\.', '선택해도 됩니다.'),
    # 단순 패턴
    (r'한다\.', '합니다.'),
    (r'된다\.', '됩니다.'),
    (r'있다\.', '있습니다.'),
    (r'없다\.', '없습니다.'),
    (r'이다\.', '입니다.'),
    (r'한다 ', '합니다 '),
    (r'된다 ', '됩니다 '),
]

def is_excluded_file(path: Path) -> bool:
    return path.name == 'CLAUDE.md'

def transform(text: str) -> tuple[str, int]:
    """코드블록·front matter 제외 후 치환. 변경 횟수 반환."""
    count = 0
    result = []
    in_code = False
    in_front_matter = False
    front_matter_done = False
    lines = text.split('\n')

    for i, line in enumerate(lines):
        # front matter 처리 (파일 첫 번째 --- 블록)
        if i == 0 and line.strip() == '---':
            in_front_matter = True
            result.append(line)
            continue
        if in_front_matter and line.strip() == '---':
            in_front_matter = False
            front_matter_done = True
            result.append(line)
            continue
        if in_front_matter:
            result.append(line)
            continue

        # 코드블록 토글
        if line.strip().startswith('```'):
            in_code = not in_code
            result.append(line)
            continue

        if in_code:
            result.append(line)
            continue

        # 본문 치환
        new_line = line
        for pattern, replacement in REPLACEMENTS:
            new_line, n = re.subn(pattern, replacement, new_line)
            count += n
        result.append(new_line)

    return '\n'.join(result), count

def main():
    docs_path = Path('docs')
    total_files = 0
    total_changes = 0
    changed_files = []

    for md_file in sorted(docs_path.rglob('*.md')):
        if is_excluded_file(md_file):
            continue
        original = md_file.read_text(encoding='utf-8')
        transformed, count = transform(original)
        if count > 0:
            md_file.write_text(transformed, encoding='utf-8')
            changed_files.append((str(md_file), count))
            total_changes += count
            total_files += 1

    print(f"\n치환 완료")
    print(f"변경 파일: {total_files}개")
    print(f"총 치환 횟수: {total_changes}건\n")
    print("파일별 치환 횟수:")
    for f, c in changed_files:
        print(f"  {c:3d}건  {f}")

if __name__ == '__main__':
    main()
