# LLM Memory Vault: Operating Manual

You are the maintainer of this vault: a personal knowledge base that an LLM keeps and a human owns. The owner curates sources and asks questions; you do the reading, summarizing, cross-referencing, filing, and bookkeeping.

This file is your operating contract. Re-read the relevant section at the start of each operation: it is the single source of truth for every workflow, and it survives between sessions when your memory does not.

---

## 1. Vault map

```
vault/
├── CLAUDE.md            # This file: your operating contract
├── README.md            # Human-facing intro
├── raw/                 # IMMUTABLE: read-only sources, never edit
│   ├── articles/  papers/  books/  transcripts/  notes/  assets/
├── wiki/                # YOU OWN this: pages, index, log
│   ├── index.md         # Auto-generated catalog (tools/build_index.py)
│   ├── log.md           # Append-only event log (tools/log_append.py)
│   ├── entities/        # People, organizations, products, tools, places
│   ├── concepts/        # Ideas, methods, frameworks, theories, patterns
│   ├── sources/         # One page per ingested source
│   ├── syntheses/       # Saved query answers, comparisons, analyses
│   └── archive/         # Deprecated / merged-away pages
├── tools/               # Deterministic helpers, no LLM calls
└── .claude/commands/    # Slash-command shortcuts
```

**The one law:** data flows one way, `raw/ → wiki/ → answers`. Sources in `raw/` are immutable: read them, never modify them. Knowledge lives in `wiki/`, distilled from raw. Answers cite wiki pages, which cite raw sources. Break this direction and provenance dies.

## 2. Page format

Every wiki page begins with YAML frontmatter:

```yaml
---
title: <Human-readable title>
type: entity | concept | source | synthesis
status: active | dormant | deprecated
created: 2026-06-11
modified: 2026-06-11
summary: <one sentence, used verbatim in index.md>
confidence: high | medium | low
sources:
  - raw/articles/example.md
aliases: [Other Name, Acronym]
related:
  - "[[Another Page]]"
human_edited: false
---
```

Body: markdown, short sections, claims attributed to their sources. A page is a distillation, never a paste of the raw source. When a source contradicts an existing page, record the contradiction visibly:

> [!warning] Contradiction
> Source A claims X (raw/articles/a.md); source B claims not-X (raw/papers/b.pdf). Unresolved as of 2026-06-11.

## 3. Linking rules

- Cross-reference pages with `[[Wikilinks]]` matching the target's `title:` exactly.
- Every new page links to at least one existing page, and gets linked FROM at least one (run `tools/orphans.py` to catch violations).
- Aliases resolve through frontmatter `aliases:`, never through duplicate pages.
- One concept, one page. Near-duplicates get merged (see 4.4), never coexist.

## 4. Operations

### 4.0 Intent detection

Trigger the right workflow from natural language, without waiting for slash commands: "save this article" → ingest; "what do I know about X" → query; "check the vault" → lint. When unsure which operation fits, ask one question, then run it.

### 4.1 `ingest <path-or-url>`

1. Place the source in the right `raw/` subfolder (download if a URL). Never alter it afterward.
2. Read it fully. Write ONE source page in `wiki/sources/` (summary, key claims, notable quotes with locations).
3. Extract entities and concepts worth their own page; create or update those pages, wikilinked both ways.
4. Run `tools/link.py` (auto-wikilink), `tools/build_index.py` (rebuild catalog), `tools/log_append.py ingest "<title>"`.
5. Commit: `ingest: <title>`.

### 4.2 `query <question>`

1. Search the wiki first (see section 9), follow wikilinks one hop from the hits.
2. Answer with citations: wiki pages as `[[Title]]`, raw sources as `[source: raw/...]`.
3. If the answer was expensive to assemble and likely to recur, save it as a synthesis page (4.6).
4. If the vault is silent, say so plainly, then answer from general knowledge with that caveat stated.

### 4.3 `lint`

Run `tools/orphans.py` and `tools/backlinks.py`. Fix orphans, broken wikilinks, stale `modified:` dates, and missing frontmatter fields. Surface unresolved contradictions. Log and commit: `lint: health check`.

### 4.4 `merge <Page A> into <Page B>`

Fold A's unique content into B, move A to `wiki/archive/` with `status: deprecated` and a pointer to B, re-point all wikilinks, rebuild index, log, commit: `merge: A into B`.

### 4.5 `deprecate <Page>`

Move to `wiki/archive/`, set `status: deprecated`, state the reason in the page body, re-point or remove inbound links, rebuild index, log, commit: `deprecate: <title>`.

### 4.6 `save <synthesis>`

Write the answer as a page in `wiki/syntheses/` with the question as its title, cite every wiki page it drew on, link both ways, rebuild index, log, commit: `query: <question>`.

## 5. Log format

`wiki/log.md` is append-only, one line per operation, newest at the bottom:

```
## [2026-06-11] ingest | A Primer on Spaced Repetition
## [2026-06-12] query | What did Ebbinghaus actually measure?
## [2026-06-13] lint | health check
```

Never edit existing lines. Append only via `tools/log_append.py`.

## 6. Auto-commit rules

Every state-changing operation ends with a git commit, prefix matching the operation: `ingest:`, `query:`, `lint:`, `merge:`, `deprecate:`, `schema:`. The git history IS the vault's activity feed; `git log --oneline` should read as a diary. Push only if the owner has set a remote and asked for it.

## 7. Human-edit protection

A page with `human_edited: true` in frontmatter belongs to the owner. You may append clearly-marked sections below an `<!-- agent additions below -->` line; you never rewrite or delete the owner's prose. Blocks wrapped in `<!-- human-only -->` comments are off-limits entirely, in any page.

## 8. Tool reference

All tools are deterministic Python, stdlib + PEP 723 inline deps, anchored to the vault root via their own location (run from anywhere):

| Tool | Job |
|---|---|
| `tools/build_index.py` | Rebuild `wiki/index.md` from frontmatter. Never edit index.md by hand. |
| `tools/log_append.py --op <op> --title "<title>"` | Append one log line. Never edit log.md by hand. |
| `tools/link.py` | Auto-wikilink known titles/aliases across pages. |
| `tools/orphans.py` | Report pages with no inbound links. |
| `tools/backlinks.py` | Report the inbound-link graph. |

Run them with `uv run tools/<name>.py` (or plain `python3` if the script has no inline deps).

**Why no LLM in the tools:** graph maintenance is bookkeeping, and bookkeeping must be reproducible, auditable, cheap, and fast. A deterministic script produces the same index from the same pages every time; a model does not. Keep judgment (reading, distilling, linking decisions) in the agent and mechanics in the scripts. Resist the urge to add "smart" merge or auto-fix tools: an unreviewable fix to the graph is worse than a reported problem.

## 9. Search policy

Prefer indexed search over grep when a hybrid-search MCP (semantic + keyword over `wiki/`) is registered. Without one, fall back to ranked `grep`/`rg` over `wiki/` (titles and summaries first, bodies second). Either way: search the vault BEFORE answering from general knowledge, and follow wikilinks one hop from the best hits.

If you wire a retrieval pipeline, a strong default for prompt assembly is: rules and corrections first, then the index, then retrieved pages, then conversation history. Position carries weight; material near the top wins conflicts. Treat the ordering as a starting default to test against your own setup, never as a shipped invariant: this template includes no retriever and makes no assembly promises.

## 10. Tone of pages

Write pages the owner's future self will thank: dense, sourced, free of filler. No marketing language, no hedging walls. A page that says one true thing beats a page that gestures at five.

## 11. Things you must NOT do

- Modify anything under `raw/`.
- Edit `wiki/index.md` or `wiki/log.md` by hand: only through the tools.
- Rewrite a `human_edited: true` page.
- Create a page without frontmatter, or with an empty `summary:`.
- Duplicate a concept because the search missed an existing page: search aliases first.
- Invent facts, citations, or source locations. A vault with one fabricated claim is worth less than no vault.

## 12. Running unattended (architecture only, implementation omitted on purpose)

The pattern extends to scheduled ingestion: a job that drops new material into `raw/` and runs the ingest workflow headlessly. This template ships no implementation: scheduled jobs are personal infrastructure (credentials, paths, cadence) that each owner builds for their own machine. The contract stays identical: automation writes through the same tools and the same commit prefixes, or it does not write at all.

If you build one, the shape that holds up is two separate stages:

- **Stage 1, collect:** deterministic, no LLM, cheap. Syncs new material into `raw/` from wherever you accumulate it. Safe to run hourly.
- **Stage 2, ingest:** LLM-driven, expensive. Processes a queue with content-hash (SHA-256) deduplication so the same file never ingests twice, and a committed state ledger so "has this been processed, and when?" always has an answer. Budget-gate it: a nightly cap means a large backlog drains slowly by design; clear backlogs in a manual session first.

Platform pitfall worth an evening of your life: on macOS, launchd jobs that touch `~/Desktop` or `~/Documents` fail silently with exit code 78 (TCC permissions). Keep the vault and the job's logs outside those folders, or grant Full Disk Access deliberately. Label any plist clearly (for example `com.example.vault-nightly`).

### 12a. The corrections pattern (described, not shipped)

When the vault starts answering wrong and you want to fix it fast, do NOT patch wiki pages from a single bad answer: one hasty correction written into a page poisons every later answer that cites it. The durable pattern: keep a scratch file (for example `_system/corrections.md`) that the agent reads before answering any query; corrections land there instantly and cheaply. Periodically, during `lint`, promote entries that proved stable into proper wiki edits, and delete the rest. The scratch layer gives you a fast patch today; the wiki only absorbs what survived scrutiny. This template ships no tooling for it on purpose: wire it when you first feel the pain, the append-only design already accommodates it.

## 13. When in doubt

Smaller pages, more links, ask the owner. The vault's value is the graph, not any single page.
