"""
SRS bookkeeping for a PowerFlow project (D1). Two subcommands:

  python srs.py new --tag CANVAS --feature "Infinite canvas" --prd-section 4.2 [--file SRS-canvas.md]
      Registers the tag in docs/srs/README.md's allocator table and creates
      docs/srs/<file> from the PowerFlow SRS template. Refuses a tag that is
      already owned by another file.

  python srs.py allocate --tag CANVAS --count 3
      Prints the next <count> IDs for the tag (one per line) and bumps the
      allocator's "Allocated" and "Next free" cells. IDs are never reused:
      the script only moves forward.

Both take --root <repo> (default: walk up from cwd to the dir holding docs/srs)
and --dry-run. The allocator table is the single source of tags and numbers;
scripts/check-req-ids.mjs in the project fails CI when an SRS file defines an
ID this table has not handed out.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve()
PACK_ROOT = HERE.parents[3]
TEMPLATE = PACK_ROOT / "templates" / "docs" / "srs" / "SRS-template.md"

HEADER = re.compile(r"^\|\s*Tag\s*\|\s*File\s*\|\s*Feature\s*\|\s*Allocated\s*\|\s*Next free\s*\|\s*$", re.I)
ROW = re.compile(r"^\|\s*([A-Z][A-Z0-9]*)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*(\d{3,})\s*\|\s*$")
EMPTY_ROW = re.compile(r"^\|\s*\|\s*\|\s*\|\s*[—-]?\s*\|\s*(\d{3,})\s*\|\s*$")


def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "docs" / "srs" / "README.md").is_file():
            return p
    sys.exit("no docs/srs/README.md found walking up from cwd — run powerflow-init first or pass --root")


def load_table(readme: Path):
    lines = readme.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if HEADER.match(l.rstrip("\r\n"))), None)
    if start is None:
        sys.exit(f"{readme}: no allocator table (| Tag | File | Feature | Allocated | Next free |)")
    i = start + 2  # header + separator
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        rows.append(i)
        i += 1
    return lines, start, rows


def fmt_row(tag: str, file: str, feature: str, allocated: str, next_free: int, nl: str) -> str:
    return f"| {tag} | {file} | {feature} | {allocated} | {next_free:03d} |{nl}"


def cmd_new(args) -> None:
    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    readme = root / "docs" / "srs" / "README.md"
    tag = args.tag.upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9]*", tag):
        sys.exit("tag must be uppercase letters/digits, e.g. CANVAS")
    file = args.file or f"SRS-{args.feature.lower().replace(' ', '-')}.md"
    lines, start, rows = load_table(readme)
    nl = "\r\n" if lines[0].endswith("\r\n") else "\n"
    for i in rows:
        m = ROW.match(lines[i].rstrip("\r\n"))
        if m and m.group(1) == tag:
            sys.exit(f"tag {tag} is already owned by {m.group(2)} — extend that file with `allocate` instead")
        if m and m.group(2).strip("`") == file:
            sys.exit(f"{file} already owns tag {m.group(1)} — one tag per file")
    new_row = fmt_row(tag, file, args.feature, "—", 1, nl)
    empties = [i for i in rows if EMPTY_ROW.match(lines[i].rstrip("\r\n"))]
    if empties:
        lines[empties[0]] = new_row
    else:
        insert_at = (rows[-1] + 1) if rows else start + 2
        lines.insert(insert_at, new_row)
    target = root / "docs" / "srs" / file
    if target.exists():
        sys.exit(f"{target} already exists")
    body = TEMPLATE.read_text(encoding="utf-8")
    body = re.sub(r"^<!-- placeholders:[^\n]*\n", "", body, count=1)
    body = body.replace("{{feature}}", args.feature).replace("{{FEAT}}", tag).replace("{{prd_section}}", args.prd_section)
    if args.dry_run:
        print(f"would register {tag} → {file} and create {target}")
        return
    readme.write_text("".join(lines), encoding="utf-8")
    target.write_text(body, encoding="utf-8", newline="\n")
    print(f"registered {tag} -> docs/srs/{file} (next free 001); created {target.relative_to(root)}")
    print(f"the template's first row uses SRS-{tag}-001 — allocate it: python srs.py allocate --tag {tag} --count 1")


def cmd_allocate(args) -> None:
    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    readme = root / "docs" / "srs" / "README.md"
    tag = args.tag.upper()
    lines, start, rows = load_table(readme)
    nl = "\r\n" if lines[0].endswith("\r\n") else "\n"
    for i in rows:
        m = ROW.match(lines[i].rstrip("\r\n"))
        if not m or m.group(1) != tag:
            continue
        file, feature, allocated, next_free = m.group(2), m.group(3), m.group(4), int(m.group(5))
        ids = [f"SRS-{tag}-{n:03d}" for n in range(next_free, next_free + args.count)]
        first = re.match(r"(\d{3,})", allocated)
        low = int(first.group(1)) if first else next_free
        new_alloc = f"{low:03d}–{next_free + args.count - 1:03d}" if (next_free + args.count - 1) > low else f"{low:03d}"
        lines[i] = fmt_row(tag, file, feature, new_alloc, next_free + args.count, nl)
        for id_ in ids:
            print(id_)
        if not args.dry_run:
            readme.write_text("".join(lines), encoding="utf-8")
        return
    sys.exit(f"tag {tag} is not registered — run `srs.py new --tag {tag} --feature … --prd-section …` first")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    ap.add_argument("--dry-run", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("--tag", required=True)
    n.add_argument("--feature", required=True)
    n.add_argument("--prd-section", required=True)
    n.add_argument("--file")
    a = sub.add_parser("allocate")
    a.add_argument("--tag", required=True)
    a.add_argument("--count", type=int, default=1)
    args = ap.parse_args()
    if args.cmd == "new":
        cmd_new(args)
    else:
        if args.count < 1:
            sys.exit("--count must be >= 1")
        cmd_allocate(args)


if __name__ == "__main__":
    main()
