"""
Stamp the PowerFlow templates into a project.

    python stamp.py --target <repo> --answers <init.json> [--mcp uvx|python] [--force] [--dry-run]

Copies every file listed in TEMPLATES from PowerFlow/templates into the target,
fills `{{placeholders}}` from the answers file, picks the .mcp.json variant
that resolves on this machine, and refuses to leave a placeholder behind.
Existing files are kept unless --force. PLAN.md is never written here: the
plan is created through powerplan so the single-writer rule holds from the
first byte (PowerFlow D2, D11).

Answers (JSON object). Required:
  project, one_liner, stack, platform, dev_command, smoke_command,
  test_command, typecheck_command, e2e_command, verify_command, version_source
Optional (default):
  github (""), showcase ("optional"), license ("MIT"), author (""),
  date (today), dev_port (omit -> no .claude/launch.json)
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import sys
from datetime import date
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve()
PACK_ROOT = HERE.parents[3]                 # PowerFlow/
TEMPLATES = PACK_ROOT / "templates"

REQUIRED = [
    "project", "one_liner", "stack", "platform", "dev_command", "smoke_command",
    "test_command", "typecheck_command", "e2e_command", "verify_command",
    "version_source",
]
DEFAULTS = {"github": "", "showcase": "optional", "license": "MIT", "author": ""}
PLACEHOLDER = re.compile(r"\{\{([a-z0-9_]+)\}\}")
HEADER_LINE = re.compile(r"^(?:<!-- placeholders: [^>]*-->|# placeholders: .*|// placeholders: .*)\r?\n")

# (template path, target path). Order is the report order.
FILES = [
    ("PRD.md", "PRD.md"),
    ("AGENTS.md", "AGENTS.md"),
    ("CLAUDE.md", "CLAUDE.md"),
    ("README.md", "README.md"),
    (".gitignore", ".gitignore"),
    ("docs/srs/README.md", "docs/srs/README.md"),
    ("docs/decisions/README.md", "docs/decisions/README.md"),
    ("docs/agents/README.md", "docs/agents/README.md"),
    (".claude/settings.local.json", ".claude/settings.local.json"),
    (".github/workflows/ci.yml", ".github/workflows/ci.yml"),
    ("scripts/check-plan.mjs", "scripts/check-plan.mjs"),
    ("scripts/check-req-ids.mjs", "scripts/check-req-ids.mjs"),
    ("scripts/check-version.mjs", "scripts/check-version.mjs"),
]
EMPTY_DIRS = ["docs/agents/memories", "docs/agents/context"]


def load_answers(path: Path) -> dict:
    answers = json.loads(path.read_text(encoding="utf-8"))
    if "answers" in answers and isinstance(answers["answers"], dict):
        answers = dict(answers["answers"])  # a previous stamp's provenance file — re-stamp from it
    missing = [k for k in REQUIRED if not str(answers.get(k, "")).strip()]
    if missing:
        sys.exit(f"answers missing required keys: {', '.join(missing)}")
    for k, v in DEFAULTS.items():
        answers.setdefault(k, v)
    answers.setdefault("date", date.today().isoformat())
    if not answers["github"]:
        answers["github"] = "not published yet"
    if "dev_port" in answers and answers["dev_port"]:
        parts = shlex.split(str(answers["dev_command"]))
        answers["dev_command_exe"] = parts[0]
        answers["dev_command_args"] = json.dumps(parts[1:])
        answers["dev_port"] = int(answers["dev_port"])  # rendered via str(); stays numeric in provenance
    return answers


def render(text: str, answers: dict, name: str) -> str:
    text = HEADER_LINE.sub("", text, count=1)
    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in answers:
            sys.exit(f"{name}: no answer for {{{{{key}}}}}")
        return str(answers[key])
    out = PLACEHOLDER.sub(sub, text)
    left = PLACEHOLDER.findall(out)
    if left:
        sys.exit(f"{name}: placeholders left after rendering: {left}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=True, type=Path)
    ap.add_argument("--answers", required=True, type=Path)
    ap.add_argument("--mcp", choices=["uvx", "python", "auto"], default="auto")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    target = args.target.resolve()
    if not target.is_dir():
        sys.exit(f"target is not a directory: {target}")
    if not TEMPLATES.is_dir():
        sys.exit(f"templates not found at {TEMPLATES}")
    answers = load_answers(args.answers)

    files = list(FILES)
    mcp = args.mcp
    if mcp == "auto":
        mcp = "uvx" if shutil.which("uvx") else "python"
    files.append((".mcp.json" if mcp == "uvx" else ".mcp.python.json", ".mcp.json"))
    if answers.get("dev_port"):
        files.append((".claude/launch.json", ".claude/launch.json"))

    written, kept = [], []
    for src_rel, dst_rel in files:
        src = TEMPLATES / src_rel
        dst = target / dst_rel
        if not src.is_file():
            sys.exit(f"template missing: {src}")
        content = render(src.read_text(encoding="utf-8"), answers, src_rel)
        if dst.exists() and not args.force:
            kept.append(dst_rel)
            continue
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(content, encoding="utf-8", newline="\n")
        written.append(dst_rel)
    for d in EMPTY_DIRS:
        p = target / d
        if not args.dry_run:
            p.mkdir(parents=True, exist_ok=True)
            (p / ".gitkeep").touch()

    # Provenance for powerflow-audit: what was stamped, from which pack version.
    pack_version = "unknown"
    plugin = PACK_ROOT / ".claude-plugin" / "plugin.json"
    if plugin.is_file():
        pack_version = json.loads(plugin.read_text(encoding="utf-8")).get("version", pack_version)
    stamp = {
        "powerflow": pack_version,
        "stamped": date.today().isoformat(),
        "mcp": mcp,
        "answers": {k: answers[k] for k in REQUIRED + list(DEFAULTS) + ["date", "dev_port"] if k in answers},
        "files": written,
    }
    if not args.dry_run:
        (target / ".powerflow").mkdir(exist_ok=True)
        (target / ".powerflow" / "init.json").write_text(json.dumps(stamp, indent=2) + "\n", encoding="utf-8")

    verb = "would write" if args.dry_run else "wrote"
    print(f"stamp: {verb} {len(written)} file(s) into {target} (mcp: {mcp})")
    for f in written:
        print(f"  + {f}")
    for f in kept:
        print(f"  = {f} (exists, kept; --force to overwrite)")
    print("stamp: PLAN.md is not written here -- create it through powerplan (see SKILL.md step 4)")


if __name__ == "__main__":
    main()
