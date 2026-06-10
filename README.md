<img src="https://yurtayev.com/icon.svg" width="36" alt="">

# LLM Memory Vault

A template for a personal knowledge base that an LLM maintains and you own. Clone it, open it in Claude Code (or any capable agent), and say "save this article": the agent reads, distills, files, cross-links, and commits. Months later you ask "what do I know about X" and get an answer with citations instead of a folder of unread bookmarks.

This is a template, not a product. No roadmap, no support obligation. Fork it, adapt it, break it. PRs that improve the generic pattern are welcome; feature requests will be closed with thanks.

## The architecture

```
raw/  ──ingest──▶  wiki/  ──query──▶  answers with citations
(immutable          (the agent's        ([[Page]] + [source: raw/...])
 sources)            distillation)
```

Data flows one way. Sources are immutable; knowledge pages distill them; answers cite pages. The agent earns write access only through deterministic scripts that guard the catalog and the log, so the structure survives a thousand agent sessions without rotting.

The design rests on five ideas, distilled from a personal system that has run daily since spring 2026:

1. **`raw/` is immutable.** The agent reads sources, never edits them. Provenance stays checkable forever.
2. **Scripts guard the invariants.** `index.md` and `log.md` are built and appended only by deterministic tools, never by the model's hands. The LLM does judgment; the scripts do bookkeeping.
3. **`human_edited: true` protects your voice.** Pages you rewrite become yours; the agent may append below a marked line, never rewrite.
4. **Typed commits are the audit trail.** `ingest:`, `query:`, `lint:`: `git log --oneline` reads as the vault's diary.
5. **The manual is the contract.** [CLAUDE.md](CLAUDE.md) is the agent's operating contract, re-read every session. The vault is exactly as disciplined as the manual it can read.

## Quick start

```bash
gh repo clone Akitamex/llm-memory-vault my-vault && cd my-vault
rm -rf .git && git init    # your vault, your history
claude                      # open Claude Code here
```

Then try, in order:

```
ingest the example article in raw/articles/
what do I know about spaced repetition?
lint
```

The example pages in `wiki/` show the format working: four connected pages (an entity, a concept, a source, a synthesis), a provenance chain into `raw/`, and one recorded contradiction. Replace them with your own knowledge as it accumulates, or delete them after the tour.

## What's in the box

- **[CLAUDE.md](CLAUDE.md)**: the complete operating manual: page format, linking rules, the six operations (ingest / query / lint / merge / deprecate / save), commit discipline, human-edit protection.
- **`tools/`**: five deterministic helpers (index build, log append, auto-wikilink, orphan report, backlink graph). Python stdlib, run from anywhere.
- **`wiki/` examples**: a working four-page graph on learning and memory, every frontmatter field demonstrated.
- **`.claude/commands/`**: slash-command stubs for `/ingest`, `/query`, `/lint`.

## Honest notes

- Hybrid search (semantic + keyword) makes `query` meaningfully better; the manual's fallback is ranked grep, which works but misses synonyms. Wire any search MCP you like, the contract in section 9 stays the same.
- Scheduled nightly ingestion is possible and deliberately omitted: it is personal infrastructure (credentials, paths, cadence). Section 12 of the manual describes the contract your automation must keep.
- The graph beats the page. A vault of small, well-linked pages answers questions a folder of long documents cannot.

## License

[MIT](LICENSE). The example article in `raw/articles/` is original to this template and carries the same license.

---

Built by [Nikita Yurtayev](https://yurtayev.com) · [LinkedIn](https://linkedin.com/in/yurtayev) · siblings: [product-metric-breakdown](https://github.com/Akitamex/product-metric-breakdown), [ai-product-council](https://github.com/Akitamex/ai-product-council) · status at [yurtayev.com/now](https://yurtayev.com/now).
