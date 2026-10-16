# Who Goes with What? Cue-Swap Tests for Cross-Modal Episodic Binding

**Research sketch — 16 October 2026.** Proposal only; no experiment run, preregistration, or originality claim.

## Question and useful outcome

Can an assistant associate a person, object, and event across modalities when names or familiar background cues disappear? For example, remembering which fictional person used a particular car should survive a clothing or background change, while a misleading familiar car should not make the system identify the wrong person. This connects associative recall to multimodal assistants and personal-media search.

This is a binding and cue-reliability question: test whether the remembered relation follows the right entity rather than an incidental correlated feature. It is distinct from recovering damaged memory bytes; the stored episode is intact but the query cues change.

## Nearest work and proposed contrast

[ICM-Bench](https://arxiv.org/abs/2609.04438v3), revised 13 October 2026, directly tests long-term person identity reasoning. [M3Exam](https://arxiv.org/abs/2606.07402v1) already tests multimodal conversational memory. These are close predecessors, so generic multimodal memory or identity reasoning is not a new claim. The proposed contrast is a paired cue-swap/missing-cue intervention that separates identity binding, perception, and caption shortcuts under a fixed memory budget.

## Hypothesis and small first study

Hypothesis: an entity-bound multimodal memory will make fewer wrong-entity transfers under incidental cue swaps than caption-only or pooled-embedding memories, while appropriately abstaining when the remaining evidence cannot identify the person. A stronger visual encoder alone may explain any apparent gain and needs its own control.

Construct a small controlled album of synthetic adult characters and objects with exact event annotations. Independently vary appearance, clothing, object ownership, location and time. Present some episodes visually and some as text; query with images, text, or both. Use designed ambiguity cases and paired variants where only a distractor cue changes. Annotators must validate that identity remains recognizable in intended solvable cases. Do not call an actually identity-changing intervention a harmless perturbation.

Compare captions plus retrieval, raw-image retrieval, multimodal embeddings, an entity/event graph, a bound-state candidate, and full evidence. Give all methods identical permitted media and metadata. Include oracle entity labels and oracle retrieved evidence as diagnostic arms, plus name-only and background-only shortcut baselines. Raw images, thumbnails and indexes count toward storage; no free media side channel is allowed for one method.

Primary endpoint: correct entity–object/event binding on paired cue interventions. Report wrong-identity transfer, abstention on genuinely ambiguous queries, intact-cue accuracy, perception-only accuracy, query modality, storage and latency. Split by character and event arrangement; do not leak synthetic character templates across training and confirmation.

## Stop rule and deliverable

Stop the memory-specific claim if oracle entity recognition eliminates the difference, caption shortcuts explain performance, or the entity graph dominates at lower cost. First release a small diagnostic with validated interventions and exact relation labels. This would not establish recognition reliability for real people or across unconstrained real-world videos.
