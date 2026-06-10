#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Atomically append an entry to wiki/log.md.

Usage:
    uv run tools/log_append.py --op ingest --title "Source X" --body "Created [[A]]\\nUpdated [[B]]"

Body lines starting with '-' are kept; otherwise each line is prefixed with '- '.
"""
from __future__ import annotations

import argparse
import os
import tempfile
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
LOG = VAULT / "wiki" / "log.md"

ALLOWED_OPS = {"init", "ingest", "query", "lint", "merge", "deprecate", "human-edit", "schema", "save", "scoop", "stage2"}


def format_body(raw: str) -> str:
    if not raw:
        return ""
    lines = raw.replace("\\n", "\n").splitlines()
    out = []
    for line in lines:
        s = line.rstrip()
        if not s:
            continue
        if s.startswith("- ") or s.startswith("* "):
            out.append(s)
        else:
            out.append(f"- {s}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--op", required=True, choices=sorted(ALLOWED_OPS))
    ap.add_argument("--title", required=True)
    ap.add_argument("--body", default="")
    ap.add_argument("--date", default=None, help="Override date (YYYY-MM-DD); defaults to today.")
    args = ap.parse_args()

    today = args.date or date.today().isoformat()
    body = format_body(args.body)
    entry = f"## [{today}] {args.op} | {args.title}\n"
    if body:
        entry += body + "\n"
    entry += "\n"

    existing = LOG.read_text(encoding="utf-8") if LOG.exists() else "# Log\n\n"
    new = existing.rstrip() + "\n\n" + entry

    fd, tmp = tempfile.mkstemp(prefix=".log-", dir=str(LOG.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(new)
        os.replace(tmp, LOG)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    print(f"log appended: [{today}] {args.op} | {args.title}")


if __name__ == "__main__":
    main()
