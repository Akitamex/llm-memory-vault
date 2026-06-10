---
title: What Makes Spaced Repetition Work
type: synthesis
status: active
created: 2026-06-11
modified: 2026-06-11
summary: Synthesis drawing on the Ebbinghaus entity, the Spaced Repetition concept, and the primer source to answer what the mechanism of spaced repetition actually is.
confidence: medium
sources:
  - raw/articles/spaced-repetition-primer.md
aliases: []
related:
  - "[[Hermann Ebbinghaus]]"
  - "[[Spaced Repetition]]"
  - "[[A Primer on Spaced Repetition]]"
human_edited: false
---

Spaced repetition works through two mechanisms that compound: the spacing effect and the testing effect.

The spacing effect, documented by [[Hermann Ebbinghaus]] in 1885, means that a memory consolidated during a distributed study session is more durable than one formed through massed practice. The leading explanation is desirable difficulty: retrieving a fading memory recruits deeper encoding processes than refreshing a fresh one. The forgetting curve's shape, exponential with a stability parameter that grows with each review, predicts that each successful retrieval pushes the next forgetting event further out.

The testing effect adds a separate contribution. The act of retrieval itself strengthens the trace, independent of timing. Showing an answer passively delivers spacing but loses this benefit. Requiring active recall before the reveal captures both [source: raw/articles/spaced-repetition-primer.md].

In practice, these two effects mean that the right design for a review session is: schedule it near the point of near-forgetting (spacing), and require genuine recall before revealing the answer (testing). The [[Spaced Repetition]] concept page covers the SM-2 algorithm and the expanding-interval scheduling rules that operationalize this.

**Open question.** The [[Spaced Repetition]] concept page records an unresolved contradiction: whether interval timing or retrieval success rate is the dominant variable. If retrieval success rate dominates, the precise interval schedule matters less than ensuring each review is genuinely difficult. This synthesis treats the current state as uncertain on that point.
