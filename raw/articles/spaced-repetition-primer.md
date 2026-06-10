# A Primer on Spaced Repetition

_Byline: Template example article, original to this repo, MIT licensed._

---

## The forgetting curve

In 1885 Hermann Ebbinghaus published _Über das Gedächtnis_ (On Memory), reporting the first quantitative study of human memory and forgetting. He memorized lists of nonsense syllables (CVC trigrams such as "DAX" or "BUP"), then measured how quickly he forgot them. The resulting forgetting curve shows retention dropping steeply within the first hour, then flattening into a slow decline over days and weeks. The shape is approximately exponential: retention R at time t follows R = e^(-t/S), where S is the "stability" of the memory, a value that increases with each successful review.

## The 1885 self-experiments and the savings method

Ebbinghaus had no external subjects; he was both experimenter and participant. To avoid vocabulary effects, he invented nonsense syllables with no prior meaning. He would memorize a list until he could recite it perfectly, wait a fixed interval, then relearn it. The key metric was _savings_: the percentage reduction in trials needed to relearn versus the original learning. A 50% savings after one day meant half the effort was preserved. Savings remained measurable even weeks later, long after conscious recall had failed entirely. This showed that memory traces persist below the threshold of free recall.

## The spacing effect

Ebbinghaus also observed what he called the spacing effect: distributing study sessions across time produced better long-term retention than massing the same number of repetitions together. Two reviews spaced one day apart outperformed four reviews in a single sitting. The spacing effect is one of the most replicated findings in cognitive psychology, holding across ages, materials, and languages. The mechanism is not fully settled; leading accounts invoke _encoding variability_ (varied context strengthens the trace), _desirable difficulty_ (retrieving a fading memory recruits consolidation processes more deeply than refreshing a fresh one), and _study-phase retrieval_ (each review attempt involves partial reactivation of earlier study events, layering traces).

## Expanding-interval scheduling

Practical spaced-repetition systems (SRS) operationalize the spacing effect with expanding intervals: after a correct recall the next review is scheduled further out than the previous gap. A simple fixed-multiplier scheme: first review after 1 day, then 3, then 9, then 27 (multiplier 3). The SM-2 algorithm, published by Piotr Wozniak in 1987 and still the basis of Anki, refines this by modulating the multiplier (called the "ease factor") based on the graded difficulty of each recall. Cards recalled with difficulty get shorter intervals; easy recalls get longer ones. The key design principle is scheduling the review at the moment of near-forgetting, maximizing the consolidation benefit of retrieval.

**Rules of thumb for scheduling:**

- First exposure: review within 24 hours.
- After each correct recall, multiply the interval by 2 to 3.
- After a failed recall, reset to a short interval (1 day or less) and rebuild.
- Ease factor adjustments prevent runaway intervals on poorly learned material.

## The testing effect

The testing effect (also: retrieval practice effect) is related but distinct. It states that the act of retrieval itself, not merely re-exposure, strengthens memory. Roediger and Karpicke (2006) showed that students who tested themselves after reading retained far more after one week than students who re-read the same passage. Spaced repetition exploits both the spacing effect and the testing effect simultaneously: by scheduling reviews as retrieval practice rather than passive re-reading. However, the two phenomena are separable. Spacing alone (re-reading at intervals) beats massed re-reading; testing alone (one test after one study session) beats one study session alone; the combination is strongest.

The distinction matters for practice: a flashcard tool that simply shows you the answer (re-exposure) without requiring retrieval delivers spacing but loses the testing benefit. Cover the answer, force recall, then check.

---

_Sources: Ebbinghaus H. (1885/1913). Memory: A contribution to experimental psychology. Wozniak P. (1987). Optimization of learning. Roediger H.L. & Karpicke J.D. (2006). Test-enhanced learning. Science, 311, 772-775. This article is an original synthesis for the llm-memory-vault template; it is not a verbatim reproduction of any of these sources._
