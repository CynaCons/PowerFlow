"""
Create a decision record (D<n>) in a PowerFlow project.

    python decide.py --title "Renderer memory strategy" [--slug renderer-memory] [--summary "…"] [--status Accepted] [--root <repo>] [--dry-run]

Deterministic bookkeeping around METHODOLOGY.md §2.2:
  * next free D number = max existing + 1 (numbers are never reused),
  * docs/decisions/D<n>-<slug>.md from the PowerFlow template (Status,
    Context, Decision, Consequences with the reopening gate),
  * one line appended to docs/decisions/README.md,
  * a row appended to the PRD's "Decisions to record" table when it exists.
The content of Context / Decision / Consequences is yours to write afterwards;
the script leaves the template's HTML comments as prompts.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve()
PACK_ROOT = HERE.parents[3]
TEMPLATE = PACK_ROOT / "templates" / "docs" / "decisions" / "D-template.md"


def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "docs" / "decisions").is_dir():
            return p
    sys.exit("no docs/decisions/ found walking up from cwd — run powerflow-init first or pass --root")


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:48].rstrip("-") or "decision"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--slug")
    ap.add_argument("--summary", default="", help="one line for the README index and the PRD table")
    ap.add_argument("--status", default="Accepted")
    ap.add_argument("--root")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    ddir = root / "docs" / "decisions"
    existing = sorted(int(m.group(1)) for p in ddir.glob("D*.md") if (m := re.match(r"D(\d+)-", p.name)))
    n = (existing[-1] + 1) if existing else 1
    slug = args.slug or slugify(args.title)
    target = ddir / f"D{n}-{slug}.md"
    today = date.today().isoformat()

    body = TEMPLATE.read_text(encoding="utf-8")
    body = re.sub(r"^<!-- placeholders:[^\n]*\n", "", body, count=1)
    body = body.replace("{{n}}", str(n)).replace("{{title}}", args.title).replace("{{date}}", today)
    body = body.replace("Status: Accepted", f"Status: {args.status}", 1)

    readme = ddir / "README.md"
    readme_line = f"- [D{n} — {args.title}](D{n}-{slug}.md) — {args.summary or '…'}\n"

    prd = root / "PRD.md"
    prd_text = prd.read_text(encoding="utf-8") if prd.is_file() else ""
    prd_row = f"| D{n} | {args.title} | {args.summary or ''} |\n"
    prd_new = None
    if prd_text:
        # append after the last row of the decisions table (rows start with "| D<k> |")
        rows = list(re.finditer(r"^\| D\d+ \|[^\n]*\n", prd_text, flags=re.M))
        if rows:
            end = rows[-1].end()
            prd_new = prd_text[:end] + prd_row + prd_text[end:]
        else:
            placeholder = re.search(r"^\| D1 \| \| \|\n", prd_text, flags=re.M)
            if placeholder:
                prd_new = prd_text.replace(placeholder.group(0), prd_row, 1)

    if args.dry_run:
        print(f"would create {target.relative_to(root)}, append to docs/decisions/README.md"
              + (", add a PRD §decisions row" if prd_new else ", PRD table not found (skipped)"))
        return
    target.write_text(body, encoding="utf-8", newline="\n")
    with readme.open("a", encoding="utf-8") as fh:
        fh.write(readme_line)
    if prd_new:
        prd.write_text(prd_new, encoding="utf-8")
    print(f"D{n} -> {target.relative_to(root)} ({args.status}, {today}); README linked"
          + ("; PRD row added" if prd_new else "; PRD table not found (add the row by hand)"))
    print("now write Context / Decision / Consequences — the consequences must name the reopening gate")


if __name__ == "__main__":
    main()
