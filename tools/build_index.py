#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-frontmatter>=1.1"]
# ///
"""Rebuild wiki/index.md from frontmatter of all wiki pages."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import frontmatter

VAULT = Path(__file__).resolve().parent.parent
WIKI = VAULT / "wiki"
INDEX = WIKI / "index.md"

# Order matters — controls section order in output
TYPE_FOLDERS = [
    ("entity", "entities", "Entities"),
    ("concept", "concepts", "Concepts"),
    ("source", "sources", "Sources"),
    ("synthesis", "syntheses", "Syntheses"),
    ("deprecated", "archive", "Archive"),
]

EXCLUDE = {"index.md", "log.md", ".gitkeep"}


def collect_pages():
    by_type: dict[str, list[tuple[str, str, str]]] = {t: [] for t, _, _ in TYPE_FOLDERS}
    untyped: list[tuple[str, str, str]] = []

    for md in sorted(WIKI.rglob("*.md")):
        if md.name in EXCLUDE:
            continue
        rel_dir = md.relative_to(WIKI).parts[0] if md.parent != WIKI else ""
        try:
            post = frontmatter.load(md)
        except Exception as e:
            print(f"warn: failed to parse {md.relative_to(VAULT)}: {e}", file=sys.stderr)
            continue
        title = post.get("title") or md.stem
        summary = post.get("summary") or ""
        ptype = post.get("type") or ""
        status = post.get("status") or "active"
        # Archive overrides type
        if status == "deprecated" or rel_dir == "archive":
            by_type["deprecated"].append((title, summary, str(md.relative_to(VAULT))))
            continue
        if ptype in by_type:
            by_type[ptype].append((title, summary, str(md.relative_to(VAULT))))
        else:
            untyped.append((title, summary, str(md.relative_to(VAULT))))

    return by_type, untyped


def render(by_type, untyped) -> str:
    lines = ["# Index", "", f"_Last rebuilt: {date.today().isoformat()}_", ""]
    total = sum(len(v) for v in by_type.values()) + len(untyped)
    lines.append(f"**Total pages:** {total}")
    lines.append("")

    for tkey, _folder, heading in TYPE_FOLDERS:
        items = sorted(by_type[tkey], key=lambda x: x[0].lower())
        lines.append(f"## {heading} ({len(items)})")
        lines.append("")
        if not items:
            lines.append("_(none yet)_")
        else:
            for title, summary, _path in items:
                tail = f" — {summary}" if summary else ""
                lines.append(f"- [[{title}]]{tail}")
        lines.append("")

    if untyped:
        lines.append(f"## Untyped ({len(untyped)})")
        lines.append("")
        lines.append("_Pages without a recognized `type` field — please fix:_")
        lines.append("")
        for title, summary, path in sorted(untyped, key=lambda x: x[0].lower()):
            lines.append(f"- [[{title}]] (`{path}`){' — ' + summary if summary else ''}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    by_type, untyped = collect_pages()
    INDEX.write_text(render(by_type, untyped), encoding="utf-8")
    total = sum(len(v) for v in by_type.values()) + len(untyped)
    print(f"index.md rebuilt: {total} page(s)")


if __name__ == "__main__":
    main()
