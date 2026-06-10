# /ingest

Run the ingest workflow from CLAUDE.md section 4.1 on: $ARGUMENTS

**Key invariants:**
- `raw/` is immutable: place the source there, never alter it afterward.
- Write exactly one source page in `wiki/sources/`, then extract entities and concepts into their own pages with wikilinks both ways.
- Run `tools/link.py`, `tools/build_index.py`, `tools/log_append.py --op ingest --title "<title>"` in that order. Commit: `ingest: <title>`.
