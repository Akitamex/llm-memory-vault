<img src="https://yurtayev.com/icon.svg" width="36" alt="">

# LLM Memory Vault

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![Wiki lint](https://github.com/Akitamex/llm-memory-vault/actions/workflows/lint.yml/badge.svg)](https://github.com/Akitamex/llm-memory-vault/actions/workflows/lint.yml) [![Release](https://img.shields.io/github/v/tag/Akitamex/llm-memory-vault?label=release)](https://github.com/Akitamex/llm-memory-vault/releases)

A template for a personal knowledge base that an LLM maintains and you own. You feed it articles; months later it answers questions with citations instead of leaving you a folder of unread bookmarks.

## What it looks like

```text
vault$ claude
> what do I know about spaced repetition?

Spaced repetition works through two mechanisms that compound: the spacing
effect and the testing effect.

The spacing effect, documented by [[Hermann Ebbinghaus]] in 1885, means a
memory consolidated across distributed sessions outlasts massed practice.
Each successful retrieval pushes the next forgetting event further out.
The testing effect adds a separate contribution: retrieval itself
strengthens the trace [source: raw/articles/spaced-repetition-primer.md].

Open question on file: whether interval timing or retrieval success rate
dominates. Recorded as an unresolved contradiction on [[Spaced Repetition]].

Sources: [[What Makes Spaced Repetition Work]] · [[Spaced Repetition]] ·
[[Hermann Ebbinghaus]]
```

That answer is real: it comes from the four example pages shipped in `wiki/`, distilled by an agent from one article in `raw/`, with the provenance chain intact and one honest contradiction on record. Browse [the synthesis page](wiki/syntheses/what-makes-spaced-repetition-work.md) to see the format behind it.

## Quick start: 5 minutes to your first cited answer

Click **Use this template** above (recommended: your vault starts with clean history and stays private by default, with no fork link back here). Or clone:

```bash
gh repo clone Akitamex/llm-memory-vault my-vault && cd my-vault
rm -rf .git && git init
claude
```

Then, inside Claude Code:

```
ingest the example article in raw/articles/
what do I know about spaced repetition?
lint
```

Delete the example pages once you've seen the loop work, and start feeding it your own reading.

## How it works

```
raw/  ──ingest──▶  wiki/  ──query──▶  answers with citations
(immutable          (the agent's        ([[Page]] + [source: raw/...])
 sources)            distillation)
```

Data flows one way. Sources are immutable; knowledge pages distill them; answers cite pages. The agent earns write access only through deterministic scripts that guard the catalog and the log, so the structure survives a thousand agent sessions without rotting.

Five load-bearing ideas, distilled from a personal system that has run daily since spring 2026:

1. **`raw/` is immutable.** The agent reads sources, never edits them. Provenance stays checkable forever.
2. **Scripts guard the invariants.** `index.md` and `log.md` are built and appended only by deterministic tools, never by the model's hands. The LLM does judgment; the scripts do bookkeeping.
3. **`human_edited: true` protects your voice** (see [Ownership model](#ownership-model)).
4. **Typed commits are the audit trail.** `ingest:`, `query:`, `lint:`: `git log --oneline` reads as the vault's diary.
5. **The manual is the contract.** [CLAUDE.md](CLAUDE.md) is the agent's operating contract, re-read every session. The vault is exactly as disciplined as the manual it can read.

## What's in the box

- **[CLAUDE.md](CLAUDE.md)**: the complete operating manual: page format, linking rules, the six operations (ingest / query / lint / merge / deprecate / save), commit discipline, ownership protection, pitfalls.
- **`tools/`**: five deterministic helpers (index build, log append, auto-wikilink, orphan report, backlink graph). Python stdlib, run from anywhere, no LLM calls. CI lints the example wiki with these same tools on every push.
- **`wiki/` examples**: a working four-page graph on learning and memory, every frontmatter field demonstrated, one recorded contradiction.
- **`.claude/commands/`**: slash-command stubs for `/ingest`, `/query`, `/lint`.

## Design rationale

<details>
<summary><b>Why a wiki, not a vector store</b></summary>

Retrieval over raw documents asks the model to synthesize across noisy, redundant sources at query time, every time. A curated wiki moves that synthesis to ingest time: each page is already distilled, deduplicated, and cross-linked, so at query time the model rephrases trusted material instead of reconciling contradictions under pressure. Andrej Karpathy made this observation about LLM-oriented wikis; this template stands on that idea, on Vannevar Bush's Memex (1945), and on the Zettelkasten tradition of small, densely linked notes.

The same logic explains the template's two stubborn choices. Plain markdown files, because you own them: no app coupling, no plugin, no server, readable in thirty years. Deterministic scripts, because graph maintenance (index freshness, link integrity, orphan detection) is bookkeeping, and bookkeeping done by an LLM is expensive, slow, and occasionally creative in the wrong ways.

One advisory note: if you wire a retrieval pipeline (any search MCP), assembly order matters: rules and corrections first, then the index, then retrieved pages, then conversation history. Treat that ordering as a strong default to start from, not a law; the template itself ships with grep-based fallback and makes no assembly promises.

</details>

## Ownership model

The standing fear with agent-maintained notes: "will it rewrite something I wrote carefully?" Two mechanisms answer it.

- A page with `human_edited: true` in frontmatter is yours. The agent reads and cites it, appends below a marked line if invited, and never rewrites your prose.
- A `<!-- human-only -->` block inside any page is off-limits entirely.

Both are plain-text conventions enforced by the operating contract, visible in every diff. No accounts, no permissions system, just a flag the agent is bound to respect.

This repo itself follows the same spirit: it is a template, not a product. Fork it, adapt it, break it. PRs that improve the generic pattern are welcome; feature requests will be closed with thanks.

## Pitfalls (read before week two)

- **Orphans accumulate silently.** A page nothing links to is invisible to graph traversal. Run `lint` monthly; the first pass on a 20-page vault typically surfaces a few.
- **Quality drift has no error message.** Over-compressed source pages lose the nuance you'll want back later. If answers start feeling thin, reread the recent source pages, not the query pipeline.
- **Don't patch the wiki from one bad answer.** A single correction written straight into a page can poison every later answer. Collect corrections in a scratch file the agent reads first, and promote them into pages only once they prove stable. The manual describes this pattern (CLAUDE.md, section 12a).

## Honest notes

- Hybrid search (semantic + keyword) makes `query` meaningfully better; the fallback is ranked grep, which works but misses synonyms. Wire any search MCP you like, the contract stays the same.
- Scheduled nightly ingestion is possible and deliberately omitted: it is personal infrastructure. The manual's section 12 describes the two-stage architecture your automation should follow, including the macOS pitfall that costs people an evening.
- The graph beats the page. A vault of small, well-linked pages answers questions a folder of long documents cannot.

## License

[MIT](LICENSE). The example article in `raw/articles/` is original to this template and carries the same license.

---

Built by [Nikita Yurtayev](https://yurtayev.com) · [LinkedIn](https://linkedin.com/in/yurtayev) · siblings: [product-metric-breakdown](https://github.com/Akitamex/product-metric-breakdown), [ai-product-council](https://github.com/Akitamex/ai-product-council) · status at [yurtayev.com/now](https://yurtayev.com/now).
