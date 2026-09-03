#!/usr/bin/env python3
"""문서의 코드블록을 문법(L1)과 스키마(L2) 수준에서 검사한다.

독자가 그대로 복사해 실행하는 예시가 깨져 있으면 가이드 전체의 신뢰가 무너진다.
2026-09 진단에서 워크플로 하나가 YAML 로 파싱조차 되지 않는 상태로 발행돼 있었고,
액션 태그 하나는 실존하지 않는 참조였다. 사람이 매번 확인할 수 없으니 상시 검사한다.

검사 계층
    L1 문법  yaml / json / xml / toml 을 파서에 넣는다.
    L2 스키마 GitHub Actions 는 actionlint, GitLab CI 는 구조 검사,
             bash 는 `bash -n` 과 shellcheck 를 돌린다.

외부 참조(액션 태그 실재, 설치 URL 응답)는 네트워크가 필요하므로
check-code-refs.py 가 따로 맡는다.

사용법:
    python3 .claude/scripts/check-code-blocks.py            # 전체 검사
    python3 .claude/scripts/check-code-blocks.py -v         # 블록별 집계까지
    python3 .claude/scripts/check-code-blocks.py --stats    # 인벤토리만 출력
    python3 .claude/scripts/check-code-blocks.py --selftest # 검사기가 실제로 도는지 확인

검사에서 빼는 방법:
    펜스에 validate=skip 을 단다. 예: ```yaml validate=skip
    안티패턴 예시나 자리표시자가 든 블록처럼 통과할 수 없는 것에만 쓴다.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

# PyYAML 이 없는 채로 진행하면 yaml 블록을 한 건도 보지 않고 통과한다.
# check-kwg-drift.py 와 같은 방식으로 즉시 멈춘다. CI 는 static-verify 에서 미리 넣는다.
try:
    import yaml
except ImportError:
    print("PyYAML 이 없다. 의존성을 갖춘 뒤 다시 실행하라 (pyyaml).")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]

# 검사 대상 경로. 셸 변수로 넘기면 zsh 가 단어 분리를 하지 않아 통째로 한 인자가 되고
# 결과가 조용히 0건이 된다(2026-09 K17 에서 실제로 겪었다). 파이썬 리스트로 고정한다.
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

# 어느 깊이에 있든 제외한다.
#   build, node_modules  빌드 산출물. 원본을 고쳐도 여기 사본은 남아 이중 보고가 된다.
#   _plan                로컬 작업 노트. 문서가 아니다.
#   .claude              세션 기록.
EXCLUDE_DIRS = {"build", "node_modules", "_plan", ".claude", ".docusaurus"}

# 파생물. output-sample/ 이 원본이고 update-reference-samples 스킬이 이걸 만든다.
# 스킬은 코드블록 내부를 바꾸지 않으므로(변환 규칙 4) 원본만 검사하면 충분하다.
# 여기서 위반을 고치면 다음 재생성에서 원복돼 CI 가 같은 위반을 되풀이 보고한다.
DERIVED_PREFIXES = (
    "website/reference/samples/",
    "website/i18n/en/docusaurus-plugin-content-docs-reference/current/samples/",
)

EXTS = {".md", ".mdx"}

# 문서 안내용이라 결함이 아닌 shellcheck 규칙
#   SC2164  `cd foo` 뒤에 `|| exit` 이 없다. 독자 안내 블록에는 붙이지 않는다.
#   SC2148  셔뱅이 없다. 블록을 떼어냈으니 당연하다.
#   SC1083  중괄호. GitHub Actions 표현식이 섞이면 오탐이다.
#   SC2034  변수를 쓰지 않았다. 앞뒤 문맥이 잘린 발췌에서는 늘 뜬다.
#   SC2154  변수에 값이 없다. 위와 같은 이유다.
# SC2046(인용 없는 명령 치환)은 실제 결함이라 남긴다. `$(pwd)` 미인용이 여기서 잡힌다.
SHELLCHECK_EXCLUDE = "SC2164,SC2148,SC1083,SC2034,SC2154"


class Block:
    __slots__ = ("path", "line", "lang", "meta", "code")

    def __init__(self, path, line, lang, meta, code):
        self.path = path
        self.line = line
        self.lang = lang
        self.meta = meta
        self.code = code

    @property
    def where(self):
        return f"{self.path}:{self.line}"

    @property
    def skipped(self):
        return "validate=skip" in self.meta


def iter_files():
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
            posix = rel.as_posix()
            if posix.startswith(DERIVED_PREFIXES):
                continue
            yield rel, path


def extract(rel, path):
    """중첩 펜스를 스택으로 처리해 바깥 블록만 센다.

    4-백틱 안에 3-백틱이 든 예시가 문서에 있어서, 단순 짝 맞추기로는 어긋난다.
    """
    lines = path.read_text(encoding="utf-8").split("\n")
    stack = []
    out = []
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)(`{3,})\s*([A-Za-z0-9_+-]*)\s*(.*)$", line)
        if not m:
            continue
        _, ticks, lang, meta = m.groups()
        if stack and len(ticks) >= len(stack[-1][1]) and not lang and not meta.strip():
            start, _, slang, smeta = stack.pop()
            if not stack:
                out.append(
                    Block(rel.as_posix(), start + 1, slang, smeta,
                          "\n".join(lines[start + 1:i]))
                )
        else:
            stack.append((i, ticks, lang, meta))
    return out


def is_gha(code):
    return bool(re.search(r'^\s*(on|"on"):', code, re.M)) and bool(
        re.search(r"^\s*jobs:", code, re.M)
    )


def is_compose(data):
    """docker-compose 를 GitLab CI 로 오분류하지 않는다.

    tools-setup.md 의 Dependency-Track compose 파일이 services 아래 image 를 갖는데,
    stages 없는 GitLab 잡과 모양이 비슷해 진단 때 실제로 오분류됐다.
    """
    if not isinstance(data, dict) or "services" not in data:
        return False
    services = data["services"]
    if not isinstance(services, dict):
        return False
    return any(isinstance(v, dict) and "image" in v for v in services.values())


def is_gitlab(code, data):
    if is_compose(data):
        return False
    return bool(re.search(r"^\s*stages:", code, re.M)) or bool(
        re.search(r"^\s*(image|script):", code, re.M)
    )


def strip_json_comments(code):
    """선두의 `// 파일명` 주석 줄을 걷어낸다.

    renovate.json 은 JSON5 주석을 실제로 허용하고, SARIF·grype 발췌 블록도
    파일명을 주석으로 붙여 둔다. 엄격 파서에 그대로 넣으면 전부 실패한다.
    """
    out = []
    for line in code.split("\n"):
        if not out and line.strip().startswith("//"):
            continue
        out.append(line)
    return "\n".join(out)


def check_yaml(block, findings):
    try:
        data = yaml.safe_load(block.code)
    except Exception as exc:
        findings.append((block.where, "yaml", str(exc).split("\n")[0]))
        return None
    return data


def check_json(block, findings):
    try:
        json.loads(strip_json_comments(block.code))
    except Exception as exc:
        findings.append((block.where, "json", str(exc)))


def check_xml(block, findings):
    """조각을 가짜 루트로 감싼다.

    pom.xml 발췌는 <dependency> 가 여럿이라 루트가 하나가 아니다. 조각인 것이
    정상이므로 감싼 뒤 파싱한다. 그래도 실패하면 진짜 문법 오류다.
    """
    try:
        ET.fromstring(f"<root>{block.code}</root>")
    except Exception as exc:
        findings.append((block.where, "xml", str(exc)))


def check_toml(block, findings, skips):
    try:
        import tomllib
    except ImportError:
        skips.add("toml 검사 (tomllib 없음, Python 3.11 이상 필요)")
        return
    try:
        tomllib.loads(block.code)
    except Exception as exc:
        findings.append((block.where, "toml", str(exc)))


def check_gitlab(block, data, findings):
    reserved = {
        "stages", "variables", "default", "include", "workflow",
        "image", "services", "before_script", "after_script", "cache",
    }
    if not isinstance(data, dict):
        return
    stages = data.get("stages")
    for name, job in data.items():
        if name in reserved or not isinstance(job, dict):
            continue
        if not {"script", "trigger", "extends"} & set(job):
            findings.append((block.where, "gitlab", f'잡 "{name}" 에 script 가 없다'))
        stage = job.get("stage")
        if stages is not None and stage is not None and stage not in stages:
            findings.append(
                (block.where, "gitlab",
                 f'잡 "{name}" 의 stage "{stage}" 가 stages 목록에 없다 {stages}')
            )


def run_actionlint(blocks, findings, verbose, skips):
    if not shutil.which("actionlint"):
        skips.add("GitHub Actions 스키마 검사 (actionlint 없음)")
        return False
    with tempfile.TemporaryDirectory() as tmp:
        wf = Path(tmp) / ".github" / "workflows"
        wf.mkdir(parents=True)
        index = {}
        for n, block in enumerate(blocks, 1):
            name = f"wf{n:03d}.yml"
            (wf / name).write_text(block.code + "\n", encoding="utf-8")
            index[name] = block.where
        # actionlint 는 git 저장소 안에서만 워크플로 디렉터리를 찾는다
        subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True)
        proc = subprocess.run(
            ["actionlint", "-no-color", "-oneline",
             "-shellcheck=", "-pyflakes="],
            cwd=tmp, capture_output=True, text=True,
        )
        for line in proc.stdout.strip().split("\n"):
            if not line:
                continue
            m = re.match(r"^\.github/workflows/(wf\d+\.yml):(\d+):\d+: (.*)$", line)
            if m:
                findings.append((index[m.group(1)], "actionlint", m.group(3)))
            else:
                findings.append(("(actionlint)", "actionlint", line))
    if verbose:
        print(f"  actionlint: GitHub Actions 블록 {len(blocks)}개 검사")
    return True


def run_bash(blocks, findings, verbose, skips):
    have_shellcheck = shutil.which("shellcheck") is not None
    if not have_shellcheck:
        skips.add("bash 정적 분석 (shellcheck 없음)")
    with tempfile.TemporaryDirectory() as tmp:
        index = {}
        paths = []
        for n, block in enumerate(blocks, 1):
            p = Path(tmp) / f"b{n:04d}.sh"
            p.write_text("#!/bin/bash\n" + block.code + "\n", encoding="utf-8")
            index[p.name] = block.where
            paths.append(p)
            proc = subprocess.run(["bash", "-n", str(p)], capture_output=True, text=True)
            if proc.returncode:
                first = proc.stderr.strip().split("\n")[0]
                findings.append((block.where, "bash -n", first.split(": ", 1)[-1]))
        if have_shellcheck and paths:
            proc = subprocess.run(
                ["shellcheck", "-f", "gcc", "-S", "warning",
                 "-e", SHELLCHECK_EXCLUDE] + [str(p) for p in paths],
                capture_output=True, text=True,
            )
            for line in proc.stdout.strip().split("\n"):
                m = re.match(r"^(.*?/)?(b\d+\.sh):(\d+):\d+: \w+: (.*)$", line)
                if m and m.group(2) in index:
                    findings.append((index[m.group(2)], "shellcheck", m.group(4)))
    if verbose:
        print(f"  bash: {len(blocks)}개 블록에 bash -n"
              f"{' 과 shellcheck' if have_shellcheck else ''} 실행")


def collect_blocks():
    blocks = []
    for rel, path in iter_files():
        blocks.extend(extract(rel, path))
    return blocks


def analyse(blocks, findings, verbose, skips):
    counts = {}
    gha, gitlab_pairs, bash_blocks = [], [], []
    for block in blocks:
        counts[block.lang or "(표기없음)"] = counts.get(block.lang or "(표기없음)", 0) + 1
        if block.skipped:
            continue
        lang = block.lang
        if lang == "yaml":
            data = check_yaml(block, findings)
            if data is None:
                continue
            if is_gha(block.code):
                gha.append(block)
            elif is_gitlab(block.code, data):
                gitlab_pairs.append((block, data))
        elif lang == "json":
            check_json(block, findings)
        elif lang == "xml":
            check_xml(block, findings)
        elif lang == "toml":
            check_toml(block, findings, skips)
        elif lang == "bash":
            bash_blocks.append(block)

    for block, data in gitlab_pairs:
        check_gitlab(block, data, findings)
    if gha:
        run_actionlint(gha, findings, verbose, skips)
    if bash_blocks:
        run_bash(bash_blocks, findings, verbose, skips)
    return counts, len(gha), len(gitlab_pairs), len(bash_blocks)


def selftest():
    """검사기가 실제로 도는지 확인한다.

    결과가 0건일 때 그것이 진짜 0인지 검사기가 아무것도 안 본 것인지 구분되지
    않으면 검사가 무의미하다. 일부러 깨뜨린 블록을 넣어 잡히는지 본다.
    """
    cases = [
        ("yaml", "a:\n  b: c\n bad-indent: x", "yaml"),
        ("json", '{"a": 1,}', "json"),
        ("bash", 'if [ -z "$x" ]; then\necho hi', "bash -n"),
        # SC2046 은 제외 목록에 넣지 않았다는 것을 고정한다.
        # K17 이 고친 `$(pwd)` 미인용이 다시 들어오면 여기서 막힌다.
        ("bash", "docker run --rm -v $(pwd):/x img", "shellcheck"),
    ]
    ok = True
    print("[셀프테스트] 일부러 깨뜨린 블록이 잡히는지 확인한다")
    for lang, code, kind in cases:
        findings = []
        block = Block("<selftest>", 1, lang, "", code)
        analyse([block], findings, False, set())
        hit = any(f[1] == kind for f in findings)
        print(f"  {'OK  ' if hit else 'FAIL'} {lang} 위반 -> {kind} 검출 "
              f"{'됨' if hit else '안 됨'}")
        ok &= hit

    findings = []
    block = Block("<selftest>", 1, "yaml", "validate=skip", "a:\n  b: c\n bad: x")
    analyse([block], findings, False, set())
    skipped_ok = not findings
    print(f"  {'OK  ' if skipped_ok else 'FAIL'} validate=skip 블록은 건너뛴다")
    ok &= skipped_ok
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="코드블록 문법·스키마 검사 (L1·L2)")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--stats", action="store_true", help="인벤토리만 출력한다")
    ap.add_argument("--selftest", action="store_true", help="검사기 자체를 확인한다")
    ap.add_argument("--allow-missing-tools", action="store_true",
                    help="도구가 없어 돌지 못한 검사를 실패로 세지 않는다 (로컬 전용)")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    blocks = collect_blocks()
    if not blocks:
        print("FAIL: 코드블록을 하나도 찾지 못했다. 대상 경로 설정을 확인하라.")
        return 1

    skipped = [b for b in blocks if b.skipped]
    findings = []
    skips = set()
    counts, n_gha, n_gitlab, n_bash = analyse(blocks, findings, args.verbose, skips)

    print(f"[코드블록 검사] 파일에서 블록 {len(blocks)}개 수집 "
          f"(validate=skip {len(skipped)}개 제외)")
    if args.verbose or args.stats:
        for lang, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"    {lang:14} {n}")
        print(f"    GitHub Actions {n_gha} / GitLab CI {n_gitlab} / bash {n_bash}")
        for block in skipped:
            print(f"    skip: {block.where} ({block.lang})")
    if args.stats:
        return 0

    if findings:
        print(f"  FAIL: {len(findings)}건")
        for where, kind, msg in findings:
            print(f"    {where} [{kind}] {msg}")
        return 1

    # 도구가 없어 돌지 못한 검사가 있으면 통과로 세지 않는다. 검사기가 아무것도 보지
    # 않고 초록을 내는 것이 이 스크립트가 막으려는 실패 유형이다.
    if skips and not args.allow_missing_tools:
        print(f"  FAIL: 돌지 못한 검사 {len(skips)}종")
        for item in sorted(skips):
            print(f"    {item}")
        print("    도구를 갖추고 다시 실행하라. 로컬에서 일부러 건너뛰려면"
              " --allow-missing-tools 를 준다.")
        return 1

    print("  PASS: 코드블록 문법·스키마 이상 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
