# One Memory, Many Languages: Cross-Lingual Update Consistency

**Research sketch — 16 October 2026.** Proposal only; no experiment run, preregistration, or originality claim.

## Question and useful outcome

If a fact is learned in Chinese, corrected in English, and queried in a third language, does the assistant maintain one current belief or several language-specific versions? A useful system must carry corrections, scope, entity aliases, and uncertainty across languages. This matters for multilingual personal assistants and international teams.

The proposed distinction is update consistency in a persistent store, rather than multilingual question answering or cross-lingual retrieval alone. The model host stays fixed; this is not the earlier cross-model migration topic. Language-specific instructions must remain scoped when they intentionally differ: translating a fact does not imply applying one locale's policy everywhere.

## Nearest work and proposed contrast

[M3-Embedding](https://arxiv.org/abs/2402.03216v5) already supplies multilingual retrieval. [Hindsight](https://aclanthology.org/2026.acl-demo.27/) includes multilingual memory processing; its paper's section 4.4 describes language preservation. Multilingual memory is therefore not a new category. The proposed experiment isolates the write-language × correction-language × query-language interaction, with a translation and oracle-retrieval decomposition.

## Hypothesis and small first study

Hypothesis: a shared entity/update representation reduces stale-answer rates across languages compared with independently summarized language memories, at matched evidence and inference budgets. A translate-to-one-language baseline may already solve most of the problem and must be competitive.

Build controlled multi-session streams from one executable event ledger. Begin with Chinese and English, then add a third language with competent bilingual review. Vary aliases, explicit corrections, dates, negation, and context-scoped preferences. Keep names and facts randomized; have reviewers check meaning rather than rely on round-trip translation. Include equal-language controls and code-switching. Split by underlying world, so translated copies never cross train and test.

Compare multilingual vector retrieval, translation-pivot retrieval, a shared symbolic entity/version store, text summaries, and a candidate shared memory. All receive the same permitted aliases and timestamps. Give each method an oracle-evidence condition to distinguish memory failure from language comprehension. Count translated tokens, translation calls, storage bytes, and latency; equal token counts alone are not equal information across scripts.

Primary endpoint: current-fact accuracy averaged over the frozen language triples after a correction. Report stale-fact use, cross-language disagreement, unresolved-alias abstention, scoped-policy errors, and per-language gaps. Use world-paired intervals. Freeze triples, translation review rules, and thresholds before confirmation.

## Stop rule and deliverable

Stop the new-memory-method claim if translation quality explains the entire effect, a multilingual retrieval baseline matches it, or the symbolic store dominates. A benchmark contribution would still require a reliable language-aligned task generator and review evidence. The first deliverable is a language/update matrix and a failure taxonomy, not a multilingual leaderboard win. Broader novelty needs full-text and code review beyond this targeted scan.
