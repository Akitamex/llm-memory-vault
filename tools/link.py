#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-frontmatter>=1.1", "rapidfuzz>=3", "spacy>=3.7"]
# ///
"""Auto-wikilink: convert plaintext mentions of existing page titles/aliases into [[Wikilinks]].

Usage:
    uv run tools/link.py [files...]        # Tier 1 only (exact + fuzzy match)
    uv run tools/link.py --ner [files...]  # + Tier 2 (spaCy NER on named entities)

Without files: scans all wiki pages.
Skips: code blocks, inline code, headings, URLs, existing wikilinks, HTML comments,
frontmatter, and pages with `human_edited: true`.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import frontmatter
from rapidfuzz import fuzz, process

VAULT = Path(__file__).resolve().parent.parent
WIKI = VAULT / "wiki"

EXCLUDE_NAMES = {"index.md", "log.md"}

# Patterns for safe-zone detection
RE_FENCED = re.compile(r"```[\s\S]*?```", re.MULTILINE)
RE_INLINE = re.compile(r"`[^`\n]+`")
RE_URL = re.compile(r"https?://\S+")
RE_WIKILINK = re.compile(r"\[\[[^\]]+\]\]")
RE_MDLINK = re.compile(r"\[[^\]]+\]\([^)]+\)")
RE_HTML_COMMENT = re.compile(r"<!--[\s\S]*?-->")
RE_HEADING = re.compile(r"^#+ .+$", re.MULTILINE)


def build_alias_map() -> dict[str, str]:
    """Map lowercased surface form → canonical title."""
    m: dict[str, str] = {}
    for md in WIKI.rglob("*.md"):
        if md.name in EXCLUDE_NAMES:
            continue
        try:
            post = frontmatter.load(md)
        except Exception:
            continue
        title = post.get("title")
        if not title:
            continue
        m.setdefault(title.lower(), title)
        for a in post.get("aliases") or []:
            if isinstance(a, str):
                m.setdefault(a.lower(), title)
    return m


def safe_zones(text: str) -> list[tuple[int, int]]:
    """Return list of (start, end) byte ranges where we MUST NOT linkify."""
    zones: list[tuple[int, int]] = []
    for pat in (RE_FENCED, RE_INLINE, RE_URL, RE_WIKILINK, RE_MDLINK, RE_HTML_COMMENT, RE_HEADING):
        for m in pat.finditer(text):
            zones.append(m.span())
    zones.sort()
    return zones


def is_safe(pos: int, length: int, zones: list[tuple[int, int]]) -> bool:
    end = pos + length
    for s, e in zones:
        if s >= end:
            break
        if not (end <= s or pos >= e):
            return False
    return True


def linkify_tier1(body: str, alias_map: dict[str, str], current_title: str) -> tuple[str, int]:
    """Replace first occurrence of each alias with [[Title|surface]]. Skips current page's own title."""
    if not alias_map:
        return body, 0

    surfaces = sorted(alias_map.keys(), key=len, reverse=True)
    new_body = body
    replaced = 0
    used: set[str] = set()  # canonical titles already linked once

    for surface in surfaces:
        canonical = alias_map[surface]
        if canonical == current_title or canonical in used:
            continue
        zones = safe_zones(new_body)
        pat = re.compile(r"\b" + re.escape(surface) + r"\b", re.IGNORECASE)
        for m in pat.finditer(new_body):
            if not is_safe(m.start(), len(m.group(0)), zones):
                continue
            original = m.group(0)
            link = f"[[{canonical}|{original}]]" if original.lower() != canonical.lower() else f"[[{canonical}]]"
            new_body = new_body[: m.start()] + link + new_body[m.end():]
            used.add(canonical)
            replaced += 1
            break
    return new_body, replaced


def linkify_tier2_ner(body: str, alias_map: dict[str, str], current_title: str, nlp) -> tuple[str, int]:
    """spaCy NER → fuzzy match to existing pages → wikilink. Threshold 85."""
    titles = list({v for v in alias_map.values()})
    if not titles:
        return body, 0
    used: set[str] = set()
    new_body = body
    replaced = 0
    doc = nlp(body)
    spans = sorted(
        [(ent.start_char, ent.end_char, ent.text) for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "PRODUCT", "WORK_OF_ART", "EVENT", "FAC", "LOC", "NORP"}],
        key=lambda s: -s[0],
    )
    for start, end, text in spans:
        if text.lower() in alias_map:
            continue  # tier 1 already handled
        match = process.extractOne(text, titles, scorer=fuzz.WRatio, score_cutoff=85)
        if not match:
            continue
        canonical, _score, _ = match
        if canonical == current_title or canonical in used:
            continue
        zones = safe_zones(new_body)
        if not is_safe(start, end - start, zones):
            continue
        new_body = new_body[:start] + f"[[{canonical}|{text}]]" + new_body[end:]
        used.add(canonical)
        replaced += 1
    return new_body, replaced


def collect_targets(args_paths: list[str]) -> list[Path]:
    if args_paths:
        targets = []
        for p in args_paths:
            path = (VAULT / p) if not Path(p).is_absolute() else Path(p)
            if path.is_file():
                targets.append(path)
            elif path.is_dir():
                targets.extend(path.rglob("*.md"))
        return [t for t in targets if t.suffix == ".md" and t.name not in EXCLUDE_NAMES]
    return [t for t in WIKI.rglob("*.md") if t.name not in EXCLUDE_NAMES]


def main():
    ap = argparse.ArgumentParser(description="Auto-wikilink vault pages.")
    ap.add_argument("paths", nargs="*", help="Files or dirs to process (default: all wiki pages).")
    ap.add_argument("--ner", action="store_true", help="Enable spaCy NER tier 2 matching.")
    args = ap.parse_args()

    alias_map = build_alias_map()
    if not alias_map:
        print("link.py: no pages with titles found, nothing to link", file=sys.stderr)
        return

    nlp = None
    if args.ner:
        try:
            import spacy
            try:
                nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("link.py: spaCy model 'en_core_web_sm' not installed.", file=sys.stderr)
                print("Run: uv run --with spacy python -m spacy download en_core_web_sm", file=sys.stderr)
                return
        except ImportError:
            print("link.py: --ner requires spacy", file=sys.stderr)
            return

    total = 0
    for md in collect_targets(args.paths):
        try:
            post = frontmatter.load(md)
        except Exception as e:
            print(f"warn: skip {md.name}: {e}", file=sys.stderr)
            continue
        if post.get("human_edited"):
            continue
        title = post.get("title") or md.stem
        body = post.content
        body, n1 = linkify_tier1(body, alias_map, title)
        n2 = 0
        if nlp is not None:
            body, n2 = linkify_tier2_ner(body, alias_map, title, nlp)
        if n1 + n2 > 0:
            post.content = body
            md.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")
            print(f"  {md.relative_to(VAULT)}: +{n1} tier1{f', +{n2} tier2' if nlp else ''} link(s)")
            total += n1 + n2
    print(f"link.py: {total} new wikilink(s) inserted")


if __name__ == "__main__":
    main()
