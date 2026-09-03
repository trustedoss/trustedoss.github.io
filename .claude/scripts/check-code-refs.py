#!/usr/bin/env python3
"""문서가 인용하는 외부 참조가 실재하는지 확인한다 (L3).

actionlint 는 워크플로 문법만 본다. `uses:` 가 가리키는 태그가 실제로 있는지는
확인하지 않는다. 2026-09 진단에서 `aquasecurity/trivy-action@0.36.0` 이 7곳에
있었는데 실제 태그는 `v0.36.0` 이었고, 문법 검사는 전부 통과했다. 복사하면 액션
해석 단계에서 바로 실패한다. 그래서 참조 실재를 따로 확인한다.

문서를 고치지 않아도 깨질 수 있는 검사라는 점이 앞의 계층과 다르다. 태그가 삭제
되거나 설치 URL 이 옮겨 가면 우리 잘못 없이 빨간불이 된다. 그래서 PR 게이트에서는
변경된 파일만 보고, 전량 확인은 주간 예약으로 돌린다.

사용법:
    python3 .claude/scripts/check-code-refs.py                 # 전량
    python3 .claude/scripts/check-code-refs.py --changed BASE  # BASE 이후 변경분만
    python3 .claude/scripts/check-code-refs.py -v
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TARGETS = [
    "docs",
    "website/ai-coding",
    "website/devsecops",
    "website/reference",
    "website/i18n",
    "samples",
    "agents",
    "templates",
    "output-sample",
]
EXCLUDE_DIRS = {"build", "node_modules", "_plan", ".claude", ".docusaurus"}
DERIVED_PREFIXES = (
    "website/reference/samples/",
    "website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/",
)
EXTS = {".md", ".mdx"}

# 자리표시자는 실재를 확인할 수 없다. 문서가 일부러 비워 둔 자리다.
PLACEHOLDER = re.compile(r"[<>{}\[\]]|커밋 SHA|commit SHA")

# "독자가 자기 것으로 바꿔 쓰라"는 뜻의 가상 소유자. 실재하지 않는 것이 정상이다.
PLACEHOLDER_OWNERS = {
    "owner", "your-org", "your-organization", "myorg", "my-org",
    "example", "example-org", "ORG", "org",
}

USES = re.compile(
    r"uses:\s*([A-Za-z0-9._-]+/[A-Za-z0-9._-]+(?:/[A-Za-z0-9._/-]+)?)@([A-Za-z0-9._-]+)"
)
# 설치 스크립트로 널리 쓰이는 형태만 본다. 문서 안의 일반 링크는 대상이 아니다.
INSTALL_URL = re.compile(
    r"(https://(?:get\.anchore\.io/[a-z]+|raw\.githubusercontent\.com/[^\s'\"`)]+\.sh))"
)


def iter_files(changed=None):
    if changed is not None:
        for rel in changed:
            path = ROOT / rel
            if path.suffix in EXTS and path.is_file():
                yield rel, path
        return
    for target in TARGETS:
        base = ROOT / target
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.suffix not in EXTS:
                continue
            rel = path.relative_to(ROOT)
            if EXCLUDE_DIRS & set(rel.parts):
                continue
            if rel.as_posix().startswith(DERIVED_PREFIXES):
                continue
            yield rel.as_posix(), path


def changed_files(base):
    proc = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if proc.returncode:
        print(f"  경고: git diff 실패({base}). 전량 검사로 전환한다.")
        return None
    out = []
    for rel in proc.stdout.split():
        if EXCLUDE_DIRS & set(Path(rel).parts):
            continue
        if rel.startswith(DERIVED_PREFIXES):
            continue
        out.append(rel)
    return out


def collect(files):
    refs, urls = {}, {}
    for rel, path in files:
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.split("\n"), 1):
            for m in USES.finditer(line):
                repo, tag = m.group(1), m.group(2)
                if PLACEHOLDER.search(tag) or PLACEHOLDER.search(repo):
                    continue
                if repo.split("/")[0] in PLACEHOLDER_OWNERS:
                    continue
                refs.setdefault((repo, tag), []).append(f"{rel}:{i}")
            for m in INSTALL_URL.finditer(line):
                urls.setdefault(m.group(1), []).append(f"{rel}:{i}")
    return refs, urls


def ref_exists(repo, tag):
    """git ls-remote 로 확인한다.

    GitHub tags API 는 페이지네이션 때문에 태그가 많은 저장소에서 조용히 놓친다.
    진단 때 checkov-action@v12 를 그렇게 없는 것으로 잘못 판정했다. ls-remote 는
    전체 ref 를 한 번에 주므로 그런 착오가 없다.
    """
    base = "/".join(repo.split("/")[:2])
    try:
        proc = subprocess.run(
            ["git", "ls-remote", f"https://github.com/{base}"],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        # 조회 자체가 안 된 것과 태그가 없는 것은 다르다. 없다고 단정하지 않는다.
        return None
    if proc.returncode:
        return None
    pat = re.compile(rf"refs/(?:tags|heads)/{re.escape(tag)}$", re.M)
    return bool(pat.search(proc.stdout))


def url_ok(url):
    proc = subprocess.run(
        ["curl", "-sSL", "-o", "/dev/null", "-w", "%{http_code}",
         "--max-time", "30", url],
        capture_output=True, text=True,
    )
    return proc.stdout.strip() == "200"


def main():
    ap = argparse.ArgumentParser(description="외부 참조 실재 확인 (L3)")
    ap.add_argument("--changed", metavar="BASE",
                    help="BASE 이후 변경된 파일만 검사한다")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    changed = changed_files(args.changed) if args.changed else None
    if args.changed and changed is not None and not changed:
        print("[외부 참조 확인] 변경된 문서가 없다")
        return 0

    files = list(iter_files(changed))
    refs, urls = collect(files)
    scope = f"변경분 {len(files)}개 파일" if changed is not None else f"{len(files)}개 파일"
    print(f"[외부 참조 확인] {scope} 에서 액션 참조 {len(refs)}종, 설치 URL {len(urls)}종")

    failures = []
    for (repo, tag), where in sorted(refs.items()):
        result = ref_exists(repo, tag)
        if result is None:
            print(f"    조회 실패(네트워크): {repo}@{tag}")
            continue
        if result:
            if args.verbose:
                print(f"    OK  {repo}@{tag} ({len(where)}곳)")
        else:
            failures.append(
                (f"{repo}@{tag}", "해결되는 태그·브랜치가 없다", where)
            )

    for url, where in sorted(urls.items()):
        if url_ok(url):
            if args.verbose:
                print(f"    OK  {url} ({len(where)}곳)")
        else:
            failures.append((url, "HTTP 200 이 아니다", where))

    if failures:
        print(f"  FAIL: {len(failures)}건")
        for what, why, where in failures:
            print(f"    {what}: {why}")
            for w in where[:5]:
                print(f"        {w}")
            if len(where) > 5:
                print(f"        (외 {len(where) - 5}곳)")
        return 1

    if not refs and not urls:
        print("  확인할 외부 참조가 없다")
        return 0
    print("  PASS: 모든 외부 참조가 실재한다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
