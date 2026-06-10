# /lint

Run the lint workflow from CLAUDE.md section 4.3 on: $ARGUMENTS

**Key invariants:**
- Run `tools/orphans.py` and `tools/backlinks.py`; fix every orphan and broken wikilink before committing.
- Fix stale `modified:` dates and missing frontmatter fields. Surface unresolved contradictions as `[!warning] Contradiction` blocks.
- Run `tools/build_index.py` after fixes. Log with `tools/log_append.py --op lint --title "health check"`. Commit: `lint: health check`.
