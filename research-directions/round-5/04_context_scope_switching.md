# Right Memory, Wrong Project: Applicability under Context Switching

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

Can an assistant avoid applying a true preference or constraint to the wrong project when names and task vocabulary overlap? The same person can want different behavior in different roles. Accurate retrieval alone does not establish applicability.

[PersistBench](https://arxiv.org/abs/2602.01146) already tests cross-domain leakage, and [TANGLE](https://arxiv.org/abs/2608.13921) already studies unresolved memory conflicts. The proposed contrast is controlled project/role switching with graded context ambiguity and an explicit cost for needless clarification. Explicit namespace filtering is a required baseline, not an innovation.

## Hypothesis and minimal experiment

Hypothesis: a scope-aware routing policy reduces wrong-context applications while preserving useful same-project recall better than unconditional retrieval or always asking. It must not outperform by being given scope labels unavailable to controls.

Create synthetic multi-project histories with overlapping entity names and mutually compatible, scope-specific rules. Query streams explicitly name the project, imply it through valid cues, or remain genuinely ambiguous. Randomize switch frequency and distractor density. Keep all underlying facts true; do not introduce corrections or source deletion.

Compare flat retrieval, hard namespace filtering with explicit labels, inferred routing, clarification-first policy, and a scope-aware candidate. Include an oracle-scope diagnostic to separate route inference from within-scope memory quality. Use deterministic mock actions and predetermined user replies. Shared facts may be applicable across projects only under a declared rule, not a free-form model guess.

Primary endpoint: correct scoped task behavior. Report wrong-project disclosure/application, missed useful memory, clarification burden, completion rate, latency and bytes. For genuinely ambiguous cases, score asking or deferring as appropriate rather than selecting a hidden project arbitrarily. Analyze explicit, implicit and ambiguous subsets separately and group uncertainty by persona/project set.

## Stop rule and value

Stop the new-policy claim if explicit namespaces plus a simple ambiguity rule suffice, if it hides failures through excessive refusal, or if gains rely on hidden labels. This would benefit assistants juggling multiple clients or roles. It does not infer authorization from semantic similarity and is distinct from revocation: the information stays stored and valid, with different application scopes.
