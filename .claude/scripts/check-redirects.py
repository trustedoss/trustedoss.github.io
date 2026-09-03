#!/usr/bin/env python3
"""기준선 라우트에서 사라진 URL이 전부 리다이렉트를 갖는지 검사한다.

@docusaurus/plugin-client-redirects 는 `to` 만 검증하고 `from` 은 검증하지 않는다.
따라서 "리다이렉트 파일이 생겼는가" 로는 누락을 잡지 못한다. 실제로 필요한 판정은
"기준선에 있었으나 지금 사이트맵에 없는 URL 전부가 리다이렉트를 갖는가" 이므로
이 스크립트가 그 방향으로 검사한다.

사용법:
    python3 .claude/scripts/check-redirects.py <기준선 파일> <build 디렉터리>

기준선 파일은 개편 착수 시점의 두 로케일 사이트맵 <loc> 합집합이다(K0 산출물).
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SITEMAP_NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
# 리다이렉트 HTML 의 meta refresh 에서 목적지를 뽑는다.
REFRESH_RE = re.compile(
    r'<meta\s+http-equiv="refresh"\s+content="0;\s*url=([^"]+)"', re.I
)


def read_baseline(path: Path) -> set[str]:
    urls = set()
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            urls.add(line)
    return urls


def read_sitemaps(build: Path) -> tuple[set[str], list[Path]]:
    """build 아래 모든 sitemap.xml 의 <loc> 합집합을 돌려준다."""
    found = sorted(build.glob('**/sitemap.xml'))
    urls = set()
    for sm in found:
        root = ET.fromstring(sm.read_text(encoding='utf-8'))
        for loc in root.iter(f'{SITEMAP_NS}loc'):
            if loc.text:
                urls.add(loc.text.strip())
    return urls, found


def url_to_path(url: str, site_root: str) -> str:
    """절대 URL 을 사이트 루트 기준 경로로 바꾼다. 예: https://x/y/z -> /y/z"""
    path = url[len(site_root):] if url.startswith(site_root) else url
    if not path.startswith('/'):
        path = '/' + path
    return path.rstrip('/') or '/'


def find_redirect_file(build: Path, path: str) -> Path | None:
    """리다이렉트 산출물 위치를 찾는다.

    trailingSlash: false 에서 플러그인은 <path>/index.html 로 만든다.
    설정에 따라 <path>.html 이 될 수도 있어 둘 다 본다.
    """
    rel = path.lstrip('/')
    for candidate in (build / rel / 'index.html', build / f'{rel}.html'):
        if candidate.is_file():
            return candidate
    return None


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    baseline_path, build = Path(sys.argv[1]), Path(sys.argv[2])
    if not baseline_path.is_file():
        print(f'FAIL: 기준선 파일이 없다: {baseline_path}')
        return 1
    if not build.is_dir():
        print(f'FAIL: build 디렉터리가 없다: {build}')
        return 1

    baseline = read_baseline(baseline_path)
    current, sitemaps = read_sitemaps(build)
    if not sitemaps:
        print(f'FAIL: {build} 아래에서 sitemap.xml 을 찾지 못했다.')
        return 1

    # 사이트 루트는 기준선 URL 에서 유추한다(가장 짧은 항목이 루트다).
    site_root = min(baseline, key=len).rstrip('/')

    removed = sorted(baseline - current)
    added = sorted(current - baseline)

    print(f'기준선 {len(baseline)} URL, 현재 사이트맵 {len(current)} URL')
    print(f'사이트맵 파일 {len(sitemaps)}개: ' +
          ', '.join(str(s.relative_to(build)) for s in sitemaps))
    print(f'사라진 URL {len(removed)}개, 새로 생긴 URL {len(added)}개')

    if not removed:
        print('\nPASS: 사라진 URL 이 없다. 검사할 리다이렉트가 없다.')
        return 0

    missing, dangling = [], []
    print('\n사라진 URL 의 리다이렉트 검사:')
    for url in removed:
        path = url_to_path(url, site_root)
        redirect_file = find_redirect_file(build, path)
        if redirect_file is None:
            missing.append(url)
            print(f'  [없음] {path}')
            continue

        html = redirect_file.read_text(encoding='utf-8')
        match = REFRESH_RE.search(html)
        if not match:
            missing.append(url)
            print(f'  [meta refresh 없음] {path} ({redirect_file.relative_to(build)})')
            continue

        target = match.group(1)
        target_url = site_root + target if target.startswith('/') else target
        target_url = target_url.rstrip('/') or site_root
        # 목적지가 현재 사이트맵에 실재하는 URL 인지 확인한다.
        if target_url in current or target_url + '/' in current:
            print(f'  [정상] {path} -> {target}')
        else:
            dangling.append((url, target))
            print(f'  [목적지 없음] {path} -> {target}')

    print()
    if missing or dangling:
        if missing:
            print(f'FAIL: 리다이렉트가 없는 URL {len(missing)}개')
            for url in missing:
                print(f'  {url}')
        if dangling:
            print(f'FAIL: 목적지가 사이트맵에 없는 리다이렉트 {len(dangling)}개')
            for url, target in dangling:
                print(f'  {url} -> {target}')
        return 1

    print(f'PASS: 사라진 URL {len(removed)}개 전부 리다이렉트가 있고 목적지가 실재한다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
