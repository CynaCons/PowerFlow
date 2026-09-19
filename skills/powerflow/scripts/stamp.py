"""
Stamp the PowerFlow templates into a project (the lean set, D15).

    python stamp.py --target <repo> --answers <init.json> [--mcp uvx|python] [--plugin yes|no] [--force] [--dry-run]

Writes PRD.md (skeleton), AGENTS.md, CLAUDE.md (shim), docs/srs/README.md,
.mcp.json (powerplan), .claude/settings.local.json, .gitignore, and creates
docs/agents/memories/ + context/. Fills {{placeholders}} from the answers and
refuses to leave one behind. Existing files are kept unless --force; PRD,
AGENTS and the SRS index are kept even then unless --force-all. PLAN.md is
never written here: it is created through powerplan (SKILL.md section 2).

Answers (JSON). Required: project, one_liner, stack, platform, dev_command,
smoke_command, test_command. Optional (default): typecheck_command and
e2e_command ('echo "none yet"'), version_source (package.json if present),
showcase ("optional"), github (""), license ("MIT"), date (today).
"""

from __future__ import annotations

import argparse
import json
import re
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

REQUIRED = ["project", "one_liner", "stack", "platform", "dev_command", "smoke_command", "test_command"]
DEFAULTS = {
    "typecheck_command": 'echo "no typecheck yet"', "e2e_command": 'echo "no e2e yet"',
    "showcase": "optional", "github": "", "license": "MIT",
}
PLACEHOLDER = re.compile(r"\{\{([a-z0-9_]+)\}\}")
HEADER_LINE = re.compile(r"^(?:<!-- placeholders: [^>]*-->|# placeholders: .*|// placeholders: .*)\r?\n")

# (template path, target path). Order is the report order.
FILES = [
    ("PRD.md", "PRD.md"),
    ("AGENTS.md", "AGENTS.md"),
    ("CLAUDE.md", "CLAUDE.md"),
    (".gitignore", ".gitignore"),
    ("docs/srs/README.md", "docs/srs/README.md"),
]
EMPTY_DIRS = ["docs/agents/memories", "docs/agents/context"]
# Files that carry project state once the project lives: --force never
# overwrites them (a re-stamp wiped a live SRS index on 2026-09-19).
STATEFUL = {"docs/srs/README.md", "PRD.md", "AGENTS.md"}


def _powerflow_plugin_installed() -> bool:
    """True when Claude Code has the powerflow plugin at user scope (D14)."""
    reg = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        return "powerflow" in json.loads(reg.read_text(encoding="utf-8")).get("plugins", {}) or                '"powerflow@' in reg.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError):
        return False


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
    ap.add_argument("--plugin", choices=["yes", "no", "auto"], default="auto",
                    help="is the powerflow Claude Code plugin installed on this machine? (D14)")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--force-all", action="store_true", help="also overwrite stateful files (SRS/decisions indexes, PRD, AGENTS, README)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    target = args.target.resolve()
    if not target.is_dir():
        sys.exit(f"target is not a directory: {target}")
    if not TEMPLATES.is_dir():
        sys.exit(f"templates not found at {TEMPLATES}")
    answers = load_answers(args.answers)
    if not answers.get("version_source"):
        answers["version_source"] = next((f for f in ("package.json", "pyproject.toml", "Cargo.toml") if (target / f).is_file()), "package.json")

    files = list(FILES)
    mcp = args.mcp
    if mcp == "auto":
        mcp = "uvx" if shutil.which("uvx") else "python"
    files.append((".mcp.json" if mcp == "uvx" else ".mcp.python.json", ".mcp.json"))
    # D14: when the powerflow plugin is installed, Claude Code already loads
    # powerplan from the plugin; disable the project copy locally (git-ignored)
    # so the server is not loaded twice. Clones without the plugin enable it.
    plugin = args.plugin
    if plugin == "auto":
        plugin = "yes" if _powerflow_plugin_installed() else "no"
    files.append((".claude/settings.local.plugin.json" if plugin == "yes" else ".claude/settings.local.json",
                  ".claude/settings.local.json"))

    written, kept = [], []
    for src_rel, dst_rel in files:
        src = TEMPLATES / src_rel
        dst = target / dst_rel
        if not src.is_file():
            sys.exit(f"template missing: {src}")
        content = render(src.read_text(encoding="utf-8"), answers, src_rel)
        if dst.exists() and (not args.force or (dst_rel in STATEFUL and not args.force_all)):
            kept.append(dst_rel + (" [stateful: --force-all to overwrite]" if args.force and dst_rel in STATEFUL else ""))
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
    manifest = PACK_ROOT / ".claude-plugin" / "plugin.json"
    if manifest.is_file():
        pack_version = json.loads(manifest.read_text(encoding="utf-8")).get("version", pack_version)
    stamp = {
        "powerflow": pack_version,
        "stamped": date.today().isoformat(),
        "mcp": mcp,
        "plugin": plugin,
        "answers": {k: answers[k] for k in REQUIRED + list(DEFAULTS) + ["date", "version_source"] if k in answers},
        "files": written,
    }
    if not args.dry_run:
        (target / ".powerflow").mkdir(exist_ok=True)
        (target / ".powerflow" / "init.json").write_text(json.dumps(stamp, indent=2) + "\n", encoding="utf-8")

    verb = "would write" if args.dry_run else "wrote"
    print(f"stamp: {verb} {len(written)} file(s) into {target} (mcp: {mcp}, plugin: {plugin})")
    for f in written:
        print(f"  + {f}")
    for f in kept:
        print(f"  = {f} (exists, kept; --force to overwrite)")
    print("stamp: PLAN.md is not written here -- create it through powerplan (SKILL.md section 2)")


if __name__ == "__main__":
    main()
