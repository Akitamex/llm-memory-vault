#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-frontmatter>=1.1"]
# ///
"""List wiki pages with zero incoming wikilinks. Used by /lint."""
from __future__ import annotations

import re
from pathlib import Path

import frontmatter

VAULT = Path(__file__).resolve().parent.parent
WIKI = VAULT / "wiki"
EXCLUDE = {"index.md", "log.md"}

RE_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]")


def main():
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
            target_raw = m.group(1).strip()
            target = aliases.get(target_raw.lower())
            if target and target != src_title:
                incoming[target].add(src_title)

    orphans = sorted([t for t, refs in incoming.items() if not refs])
    if not orphans:
        print("No orphan pages.")
        return
    print(f"# Orphans ({len(orphans)})")
    print()
    for t in orphans:
        rel = pages[t].relative_to(VAULT)
        print(f"- [[{t}]] (`{rel}`)")


if __name__ == "__main__":
    main()
