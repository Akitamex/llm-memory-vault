#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-frontmatter>=1.1"]
# ///
"""Backlink table for the vault.

Usage:
    uv run tools/backlinks.py                  # full table
    uv run tools/backlinks.py --for "Title"    # one page only
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import frontmatter

VAULT = Path(__file__).resolve().parent.parent
WIKI = VAULT / "wiki"
EXCLUDE = {"index.md", "log.md"}

RE_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]")


def build():
    pages: dict[str, Path] = {}
    aliases: dict[str, str] = {}
    for md in WIKI.rglob("*.md"):
        if md.name in EXCLUDE:
            continue
        try:
            post = frontmatter.load(md)
        except Exception:
            continue
        title = (post.get("title") or md.stem).strip()
        pages[title] = md
        aliases[title.lower()] = title
        for a in post.get("aliases") or []:
            if isinstance(a, str):
                aliases[a.strip().lower()] = title

    incoming: dict[str, set[str]] = {t: set() for t in pages}
    for src_title, src_path in pages.items():
        text = src_path.read_text(encoding="utf-8")
        for m in RE_WIKILINK.finditer(text):
            target = aliases.get(m.group(1).strip().lower())
            if target and target != src_title:
                incoming[target].add(src_title)
    return incoming


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--for", dest="target", help="Show backlinks for one page only.")
    args = ap.parse_args()

    incoming = build()
    if args.target:
        refs = sorted(incoming.get(args.target, set()))
        if not refs:
            print(f"No backlinks to [[{args.target}]].")
            return
        print(f"# Backlinks → [[{args.target}]] ({len(refs)})\n")
        for r in refs:
            print(f"- [[{r}]]")
        return

    print("# Backlink table\n")
    print("| Page | ← from |")
    print("|---|---|")
    for t in sorted(incoming):
        refs = sorted(incoming[t])
        cell = ", ".join(f"[[{r}]]" for r in refs) if refs else "_(orphan)_"
        print(f"| [[{t}]] | {cell} |")


if __name__ == "__main__":
    main()
