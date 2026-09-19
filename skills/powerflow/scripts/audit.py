"""
Audit a repository against the PowerFlow method (lean, D15).

    python audit.py --root <repo> [--json] [--tasks]

Read-only. Prints findings grouped by area with the canonical fix; --tasks
prints them as `- [ ] audit: …` lines ready for powerplan add_tasks; --json
for tooling. Exit code: 0 no findings, 1 findings, 2 not a repo we can read.

What it looks at:
  root      PRD.md, PLAN.md, AGENTS.md, CLAUDE.md (shim?), README.md
  plan      Current Status header (D2), achievements lists, non-checkbox bullets
            inside iterations, more than one current, complete-with-open
  srs       location (docs/srs vs docs/SRS_* vs spec/srs), ID scheme, first
            table's columns vs canon, a docs/srs/README.md tag index,
            Test rows with an empty Trace
  decisions DECISIONS.md or docs/decisions/
  agents    docs/agents/memories/ present
  mcp       powerplan registered, variant (uvx / python -m / submodule /
            absolute path), settings.local.json enables it
  ci        guards present — informational only (they are opt-in, extras/guards)
  tests     NN-topic.spec.* share among spec files
  pack      .powerflow/init.json (stamped version)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

CANON_COLUMNS = ["ID", "Requirement", "Rationale", "Verification", "Trace"]
SCHEMES = [
    ("SRS-<FEAT>-NNN (canon, D1)", re.compile(r"^\|\s*SRS-[A-Z][A-Z0-9]*-\d{3,}\s*\|", re.M)),
    ("CC-REQ-… (powertimelines)", re.compile(r"^\|\s*CC-REQ-[A-Z0-9-]+\s*\|", re.M)),
    ("REQ-XXX-NNN (PowerNote)", re.compile(r"^\|\s*REQ-[A-Z]+-\d{3}\s*\|", re.M)),
    ("XX-NNN two-letter prefix (RadEAU)", re.compile(r"^\|\s*[A-Z]{2}-\d{3}\s*\|", re.M)),
    ("SR-XXX-NN (powerplanner native)", re.compile(r"^\|\s*SR-[A-Z]+-\d+\s*\|", re.M)),
    ("R<n> per document (A2L-Forge)", re.compile(r"^\|\s*R\d+\s*\|", re.M)),
]

findings: list[dict] = []


def add(area: str, severity: str, what: str, fix: str) -> None:
    findings.append({"area": area, "severity": severity, "what": what, "fix": fix})


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def audit_root(root: Path) -> None:
    for name in ["PRD.md", "PLAN.md", "AGENTS.md"]:
        if not (root / name).is_file():
            add("root", "high", f"{name} missing", f"stamp.py writes {name}; PLAN.md is created through powerplan create_plan")
    claude = root / "CLAUDE.md"
    if not claude.is_file():
        add("root", "medium", "CLAUDE.md missing", "stamp the shim (templates/CLAUDE.md) so Claude reads AGENTS.md")
    else:
        text = read(claude)
        if "AGENTS.md" not in text or len(text) > 1500:
            add("root", "medium", f"CLAUDE.md is not a shim ({len(text)} chars{'; no AGENTS.md pointer' if 'AGENTS.md' not in text else ''})",
                "move shared guidance to AGENTS.md, keep CLAUDE.md as a pointer (D3)")
    if (root / "GEMINI.md").is_file() and not (root / "AGENTS.md").is_file():
        add("root", "low", "GEMINI.md present without AGENTS.md", "AGENTS.md is the shared source; other harness files point to it")


def audit_plan(root: Path) -> None:
    p = root / "PLAN.md"
    if not p.is_file():
        return
    text = read(p)
    if not re.search(r"^## Current Status\s*$", text, re.M):
        add("plan", "medium", "no stale-proof `## Current Status` header (D2)",
            "powerplan append_prose: 'The current iteration is the last heading below that is not marked COMPLETE'")
    if re.search(r"^#+ .*(Recent Achievements|Key Metrics|Quick Summary)", text, re.M):
        add("plan", "medium", "maintained summary/achievements section in the plan header",
            "drop it; history is the closed iterations, metrics come from powerflow-status (D2)")
    # non-checkbox bullets inside iterations
    in_iter, in_backlog, bad = False, False, 0
    for line in text.splitlines():
        if re.match(r"^## (Backlog|Future \(Backlog\))", line):
            in_backlog = True; in_iter = False; continue
        if in_backlog:
            continue
        if re.match(r"^### v\d+\.\d+\.\d+", line):
            in_iter = True; continue
        if re.match(r"^##? ", line):
            in_iter = False; continue
        if in_iter and re.match(r"^\s*- (?!\[[ xX]\] )", line):
            bad += 1
    if bad:
        add("plan", "low", f"{bad} non-checkbox bullet(s) inside iterations",
            "iterations hold `- [ ]` tasks only; move prose to the Goal line or the SRS (METHODOLOGY §2.4)")
    currents = re.findall(r"^### (v\d+\.\d+\.\d+)[^\n]*\((current|ACTIVE|IN PROGRESS|WIP)\)", text, re.M | re.I)
    if len(currents) > 1:
        add("plan", "high", f"{len(currents)} iterations marked current/active", "exactly one active iteration; powerplan start_iteration clears the others")
    heads = re.findall(r"^### (v\d+\.\d+\.\d+)\b", text, re.M)
    if len(heads) != len(set(heads)):
        add("plan", "high", "duplicate iteration versions", "versions are monotonic and unique; renumber the newer one")


def audit_srs(root: Path) -> None:
    locs = {
        "docs/srs (canon)": list((root / "docs" / "srs").glob("SRS-*.md")) if (root / "docs" / "srs").is_dir() else [],
        "docs/SRS_*.md": list((root / "docs").glob("SRS_*.md")) if (root / "docs").is_dir() else [],
        "spec/srs*": [p for d in root.glob("spec/srs*") if d.is_dir() for p in d.glob("SRS-*.md")],
        "docs/srs/SRS-R<n>": [],
    }
    files = [p for v in locs.values() for p in v]
    if not files:
        if (root / "docs" / "srs" / "README.md").is_file():
            add("srs", "low", "no SRS files yet (index present)", "the first feature gets docs/srs/SRS-<feature>.md before its code")
        else:
            add("srs", "high", "no docs/srs/ at all", "one docs/srs/SRS-<feature>.md per feature area, rows before code; docs/srs/README.md lists the tags")
        return
    used = [k for k, v in locs.items() if v]
    if used != ["docs/srs (canon)"]:
        add("srs", "medium", f"SRS location: {', '.join(used)}", "canon is docs/srs/SRS-<feature>.md with docs/srs/README.md as the index (D1)")
    corpus = "\n".join(read(p) for p in files)
    schemes = [name for name, rx in SCHEMES if rx.search(corpus)]
    if schemes != ["SRS-<FEAT>-NNN (canon, D1)"]:
        add("srs", "medium", f"requirement ID scheme(s): {', '.join(schemes) or 'none detected'}",
            "canon is SRS-<FEAT>-NNN; a migration is a project decision (D1) — record it or keep the scheme and note it in AGENTS.md")
    # first table's header columns
    m = re.search(r"^\|\s*ID\s*\|([^\n]*)\|\s*$", corpus, re.M)
    if m:
        cols = ["ID"] + [c.strip().strip("*") for c in m.group(1).split("|") if c.strip()]
        if cols != CANON_COLUMNS:
            add("srs", "low", f"table columns {cols}", f"canon columns {CANON_COLUMNS}; status lives in Trace, priority in PLAN.md")
    index = root / "docs" / "srs" / "README.md"
    if not index.is_file() or not re.search(r"^\|\s*Tag\s*\|\s*File", read(index), re.M | re.I):
        alt = root / "docs" / "REQUIREMENT_IDS.md"
        if alt.is_file():
            add("srs", "low", "tag index is docs/REQUIREMENT_IDS.md", "docs/srs/README.md with a `| Tag | File | Feature |` table is the canon location; either works with the guards")
        else:
            add("srs", "low", "no docs/srs/README.md tag index", "one table: which file owns which tag (templates/docs/srs/README.md)")
    # Test rows with empty trace (canon columns only)
    unverified = len(re.findall(r"^\|\s*SRS-[A-Z0-9]+-\d+\s*\|[^\n]*\|\s*Test\s*\|\s*\|\s*$", corpus, re.M))
    if unverified:
        add("srs", "low", f"{unverified} row(s) with Verification=Test and empty Trace", "fill the test path in the same change as the test, or change Verification honestly")


def audit_docs(root: Path) -> None:
    d = root / "docs" / "decisions"
    if not (root / "DECISIONS.md").is_file() and not (d.is_dir() and any(d.glob("D*.md"))):
        add("decisions", "low", "no decision log (DECISIONS.md or docs/decisions/)", "record choices between alternatives with what would reopen them (SKILL.md section 8)")
    m = root / "docs" / "agents" / "memories"
    if not m.is_dir():
        add("agents", "medium", "no docs/agents/memories/", "create it; write the first landmine as a memory — agents get smarter by writing markdown")
    elif not any(m.glob("*.md")):
        add("agents", "low", "docs/agents/memories/ is empty", "write the first landmine as a memory")


def audit_mcp(root: Path) -> None:
    p = root / ".mcp.json"
    if not p.is_file():
        add("mcp", "high", "no .mcp.json", "stamp templates/.mcp.json (uvx powerplan-mcp) — PLAN.md needs its single writer")
        return
    try:
        cfg = json.loads(read(p))
    except json.JSONDecodeError:
        add("mcp", "high", ".mcp.json is not valid JSON", "fix or re-stamp it"); return
    servers = cfg.get("mcpServers", {})
    pp = servers.get("powerplan")
    if not pp:
        add("mcp", "high", "powerplan not registered in .mcp.json", "add the powerplan entry (D4); PLAN.md is written only through it")
    else:
        blob = json.dumps(pp)
        if re.search(r"[A-Za-z]:[\\/]|^/", " ".join(pp.get("args", [])) + " " + json.dumps(pp.get("env", {}))):
            add("mcp", "medium", "powerplan registered by absolute path", "use `uvx powerplan-mcp` or `python -m powerplan` (D4); absolute paths break on every other machine")
        elif "powerplan_server.py" in blob:
            add("mcp", "low", "powerplan registered via the PowerSpawn submodule path", "fine for repos that develop powerplan/PowerSpawn; otherwise `uvx powerplan-mcp` (D4)")
    if "agents" in servers and "powerspawn" not in servers:
        add("mcp", "low", "PowerSpawn registered under the legacy name `agents`", "rename to `powerspawn` so skills and AGENTS.md match")
    s = root / ".claude" / "settings.local.json"
    if s.is_file():
        try:
            cfg_local = json.loads(read(s))
            enabled = cfg_local.get("enabledMcpjsonServers", [])
            disabled = cfg_local.get("disabledMcpjsonServers", [])
            plugin_provides = "powerflow" in read(Path.home() / ".claude" / "plugins" / "installed_plugins.json")
            if pp and "powerplan" in disabled and not plugin_provides:
                add("mcp", "medium", "project powerplan disabled in settings.local.json but the powerflow plugin is not installed here", "enable it (D14: the plugin-disabled variant is only for machines with the plugin)")
            elif pp and "powerplan" not in enabled and "powerplan" not in disabled and not cfg_local.get("enableAllProjectMcpServers"):
                add("mcp", "medium", "powerplan not enabled in .claude/settings.local.json", "add it to enabledMcpjsonServers")
        except (json.JSONDecodeError, OSError):
            pass


def audit_ci(root: Path) -> None:
    wf = root / ".github" / "workflows"
    text = "\n".join(read(p) for p in wf.glob("*.yml")) if wf.is_dir() else ""
    if not text:
        return  # CI is the project's choice; the guards are opt-in (extras/guards)
    # Projects that predate the pack run equivalent guards under other names.
    aliases = {
        "check-plan": ["check-plan", "plan-normalize", "check_plan", "lint:plan"],
        "check-req-ids": ["check-req-ids", "lint:ids", "check_req_ids", "req-ids", "requirement-id"],
        "check-version": ["check-version", "check_version", "lint:version", "version-check"],
    }
    missing = [g for g, names in aliases.items() if not any(n in text for n in names)]
    if missing and len(missing) < 3:
        add("ci", "low", f"some guards in CI, not all: missing {', '.join(missing)}", "extras/guards has the others (opt-in)")


def audit_tests(root: Path) -> None:
    specs = [p for p in root.rglob("*.spec.*") if "node_modules" not in p.parts and ".git" not in p.parts]
    if not specs:
        return
    numbered = [p for p in specs if re.match(r"^\d{2,3}-", p.name)]
    if len(numbered) < len(specs) * 0.8:
        add("tests", "low", f"{len(specs) - len(numbered)}/{len(specs)} spec files not numbered NN-topic", "number E2E files from the SRS allocator (METHODOLOGY §6)")


def audit_pack(root: Path) -> None:
    p = root / ".powerflow" / "init.json"
    if p.is_file():
        try:
            v = json.loads(read(p)).get("powerflow", "unknown")
            print(f"pack: stamped with PowerFlow {v} on {json.loads(read(p)).get('stamped', '?')}")
        except json.JSONDecodeError:
            add("pack", "low", ".powerflow/init.json unreadable", "re-run stamp.py")
    else:
        add("pack", "low", "not stamped (no .powerflow/init.json)", "retrofit: stamp.py adds only missing files, then fix the findings above")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--tasks", action="store_true", help="print findings as PLAN tasks")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}"); return 2
    print(f"audit: {root.name}")
    for fn in (audit_root, audit_plan, audit_srs, audit_docs, audit_mcp, audit_ci, audit_tests, audit_pack):
        fn(root)
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["area"]))
    if args.json:
        print(json.dumps(findings, indent=2))
    elif args.tasks:
        for f in findings:
            print(f"- [ ] audit ({f['area']}, {f['severity']}): {f['what']} -> {f['fix']}")
    else:
        for f in findings:
            print(f"[{f['severity']:<6}] {f['area']:<9} {f['what']}\n         fix: {f['fix']}")
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in order}
    print(f"findings: {len(findings)} (high {counts['high']}, medium {counts['medium']}, low {counts['low']})")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
