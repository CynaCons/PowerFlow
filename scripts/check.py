"""
PowerFlow verify — the one proof command. Exit 1 on any failure.

  1. powerplan check_plan is green on PLAN.md.
  2. .claude-plugin/plugin.json, package.json and the CHANGELOG top section agree on the version.
  3. The opt-in guards' tests pass (node --test extras/guards/tests).
  4. skills/powerflow/SKILL.md has frontmatter, name `powerflow`, and stays under 300 lines (D15).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAIL: list[str] = []


def check_plan() -> None:
    from powerplan import mutations as mut

    report = mut.check_plan(mut.load_plan_for_mutation(ROOT / "PLAN.md"))
    for issue in report["issues"]:
        FAIL.append(f"PLAN.md: {issue['message']}")
    print(f"check_plan ok={report['ok']} current={report['current']} tasks={report['task_progress']['done']}/{report['task_progress']['total']}")


def check_versions() -> None:
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    top = re.search(r"^## (\d+\.\d+\.\d+)", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), flags=re.M)
    if pkg != plugin:
        FAIL.append(f"package.json {pkg} != plugin.json {plugin}")
    if not top or top.group(1) != plugin:
        FAIL.append(f"CHANGELOG top section {top.group(1) if top else 'missing'} != plugin.json {plugin}")
    print(f"versions: plugin {plugin} / package {pkg} / changelog {top.group(1) if top else '-'}")


def check_guard_tests() -> None:
    # Direct call, no shell: a list + shell=True runs only the first element on POSIX.
    r = subprocess.run(["node", "--test", "extras/guards/tests/**/*.test.mjs"], cwd=ROOT, capture_output=True, text=True)
    passed = re.search(r"^# pass (\d+)", r.stdout, flags=re.M)
    failed = re.search(r"^# fail (\d+)", r.stdout, flags=re.M)
    print(f"guard tests: pass {passed.group(1) if passed else '?'} fail {failed.group(1) if failed else '?'}")
    if r.returncode != 0:
        FAIL.append("guard tests failed")


def check_skill() -> None:
    text = (ROOT / "skills" / "powerflow" / "SKILL.md").read_text(encoding="utf-8")
    fm = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
    if not fm or not re.search(r"^name: powerflow\s*$", fm.group(1), flags=re.M):
        FAIL.append("skills/powerflow/SKILL.md: frontmatter missing or name != powerflow")
    lines = text.count("\n")
    if lines > 300:
        FAIL.append(f"skills/powerflow/SKILL.md is {lines} lines; D15 says ~300 — split by procedure, not by rule")
    others = [p.name for p in (ROOT / "skills").iterdir() if p.is_dir() and p.name != "powerflow"]
    if others:
        FAIL.append(f"extra skill directories: {others} (D15: one skill)")
    print(f"skill: powerflow, {lines} lines")


def main() -> int:
    for fn in (check_plan, check_versions, check_guard_tests, check_skill):
        fn()
    for f in FAIL:
        print(f"FAIL {f}")
    print("check: OK" if not FAIL else f"check: {len(FAIL)} failure(s)")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
