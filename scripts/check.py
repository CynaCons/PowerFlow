"""
PowerFlow verify script — the one proof command named in PLAN.md.

Checks, exit 1 on any failure:
  1. powerplan check_plan is green on PLAN.md.
  2. Every docs/decisions/D*.md is linked from docs/decisions/README.md, and
     every D-number in PRD.md §9 has a file.
  3. Every skill named in PRD.md §5 (`powerflow-*`) has skills/<name>/SKILL.md,
     or is still an open PLAN task (reported as pending, not as a failure).
  4. Every decision file has Status / Context / Decision / Consequences.
  5. scripts/check-req-ids.mjs (the stamped guard) passes on docs/srs/.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAIL: list[str] = []
PEND: list[str] = []


def check_plan() -> None:
    from powerplan import mutations as mut

    plan = mut.load_plan_for_mutation(ROOT / "PLAN.md")
    report = mut.check_plan(plan)
    if not report["ok"]:
        for issue in report["issues"]:
            FAIL.append(f"PLAN.md: {issue['message']}")
    print(
        f"check_plan ok={report['ok']} current={report['current']} "
        f"tasks={report['task_progress']['done']}/{report['task_progress']['total']}"
    )


def check_decisions() -> None:
    ddir = ROOT / "docs" / "decisions"
    readme = (ddir / "README.md").read_text(encoding="utf-8")
    files = sorted(p for p in ddir.glob("D*.md"))
    for f in files:
        if f.name not in readme:
            FAIL.append(f"decisions/README.md does not link {f.name}")
        body = f.read_text(encoding="utf-8")
        for section in ("Status:", "## Context", "## Decision", "## Consequences"):
            if section not in body:
                FAIL.append(f"{f.name} lacks '{section}'")
    prd = (ROOT / "PRD.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"^\| (D\d+) \|", prd, flags=re.M))
    present = {re.match(r"(D\d+)", f.name).group(1) for f in files}
    for d in sorted(listed - present, key=lambda s: int(s[1:])):
        FAIL.append(f"PRD.md §9 lists {d} but docs/decisions has no {d}-*.md")
    for d in sorted(present - listed, key=lambda s: int(s[1:])):
        FAIL.append(f"docs/decisions has {d} but PRD.md §9 does not list it")
    print(f"decisions: {len(files)} files, {len(listed)} listed in PRD")


def check_skills() -> None:
    prd = (ROOT / "PRD.md").read_text(encoding="utf-8")
    names = sorted(set(re.findall(r"`(powerflow-[a-z]+)`", prd)))
    plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
    have = 0
    for name in names:
        skill = ROOT / "skills" / name / "SKILL.md"
        if skill.is_file():
            have += 1
            fm = re.match(r"---\n(.*?)\n---\n", skill.read_text(encoding="utf-8"), flags=re.S)
            if not fm:
                FAIL.append(f"skill {name}: SKILL.md has no YAML frontmatter")
                continue
            head = fm.group(1)
            if not re.search(rf"^name: {re.escape(name)}\s*$", head, flags=re.M):
                FAIL.append(f"skill {name}: frontmatter name does not match the directory")
            desc = re.search(r"^description: (.+)$", head, flags=re.M)
            if not desc or len(desc.group(1).strip()) < 80:
                FAIL.append(f"skill {name}: description missing or too short to trigger on")
            body_lines = skill.read_text(encoding="utf-8").count("\n")
            if body_lines > 500:
                FAIL.append(f"skill {name}: SKILL.md is {body_lines} lines; keep under 500 (move detail to references/)")
        elif re.search(rf"^- \[ \] .*\b{re.escape(name)}\b", plan, flags=re.M):
            PEND.append(f"skill {name}: not yet written (open PLAN task)")
        else:
            FAIL.append(f"skill {name}: no skills/{name}/SKILL.md and no open PLAN task")
    print(f"skills: {have}/{len(names)} present")


def check_req_ids() -> None:
    import subprocess
    r = subprocess.run(["node", "scripts/check-req-ids.mjs"], cwd=ROOT, capture_output=True, text=True)
    print((r.stdout.strip().splitlines() or ["check-req-ids: no output"])[0])
    if r.returncode != 0:
        FAIL.append("check-req-ids.mjs: " + (r.stderr.strip() or r.stdout.strip()))


def main() -> int:
    check_plan()
    check_decisions()
    check_req_ids()
    check_skills()
    for line in PEND:
        print(f"pending  {line}")
    for line in FAIL:
        print(f"FAIL     {line}")
    print("check: OK" if not FAIL else f"check: {len(FAIL)} failure(s)")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
