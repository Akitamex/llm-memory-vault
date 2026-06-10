# /query

Run the query workflow from CLAUDE.md section 4.2 on: $ARGUMENTS

**Key invariants:**
- Search the wiki first; follow wikilinks one hop from the best hits before answering.
- Cite wiki pages as `[[Title]]` and raw sources as `[source: raw/...]`. If the vault is silent, say so, then answer from general knowledge with that caveat.
- If the answer is expensive to assemble and likely to recur, save it as a synthesis page (section 4.6) and run `tools/build_index.py` + `tools/log_append.py --op query --title "<question>"`. Commit: `query: <question>`.
