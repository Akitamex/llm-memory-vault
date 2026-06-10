---
title: Spaced Repetition
type: concept
status: active
created: 2026-06-11
modified: 2026-06-11
summary: A study technique that schedules reviews at expanding intervals to maximize long-term retention by exploiting the spacing effect.
confidence: high
sources:
  - raw/articles/spaced-repetition-primer.md
aliases: [SRS, Spaced Practice]
related:
  - "[[Hermann Ebbinghaus]]"
human_edited: false
---

Spaced repetition is a learning method that exploits the _spacing effect_: distributing practice across time produces stronger long-term retention than the same total study time massed together. The technique traces to [[Hermann Ebbinghaus]], whose 1885 experiments showed that distributing reviews of nonsense syllables outperformed massed repetition even when total study time was held constant.

## Mechanism

The core scheduling rule is expanding intervals: after a successful recall, the next review is set further out than the previous gap. A minimal scheme uses a fixed multiplier, e.g. 1 day, then 3, then 9, then 27 days. Production systems such as Anki (based on the SM-2 algorithm) modulate the multiplier per item using a graded difficulty score. A card recalled with effort earns a smaller multiplier; one recalled with ease earns a larger one.

The design target is to schedule each review near the point of near-forgetting. This maximizes the consolidation benefit of the retrieval attempt, per the _desirable difficulty_ hypothesis: retrieving a fading memory engages deeper processing than refreshing a fresh one.

## Spacing vs. the testing effect

The testing effect is related but distinct. Spacing alone (re-reading at intervals) outperforms massed re-reading. Retrieval practice alone (one self-test after one study session) outperforms passive re-reading. Spaced repetition combines both: reviews are retrieval practice, not passive re-exposure. A tool that reveals the answer without requiring active recall delivers the spacing benefit while forfeiting the testing benefit.

## Open contradiction

> [!warning] Contradiction
> The primer ([source: raw/articles/spaced-repetition-primer.md]) describes expanding-interval scheduling driven by a fixed multiplier or ease factor as the central design mechanism. Later large-scale studies (raw source pending ingestion) suggest that interval timing matters less than retrieval success rate: schedules optimized for difficulty (not timing) produce comparable or better retention. Which variable dominates in practice remains unresolved as of 2026-06-11.

See [[A Primer on Spaced Repetition]] for source detail on the Ebbinghaus curve, the SM-2 algorithm, and the Roediger-Karpicke testing-effect experiments.
