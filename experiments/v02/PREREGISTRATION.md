# v0.2: writer-only mechanism diagnostic

This is a prospective **local** protocol, not externally registered research.
It follows the negative v0.1 result. All v0.1 hashed inputs and evidence remain
unchanged. v0.2 is a bounded diagnosis before capacity or language-model studies.

## Question and attribution

Does future-union supervision improve a query-blind event writer when the reader,
shared embeddings, state size and MAXSET composition are fixed? We do not claim
a new architecture, stronger compression, biological memory, or LLM capability.

For each retained v0.1 checkpoint (11,23,37), fork two identical writers. Train
only `event_key`, `event_value`, and `slot_keys`; freeze the reader and ALL shared
entity/relation/revision embeddings. Inference receives only local event tensors
at encoding, and state tensors plus queries at reading. Encoder has no query
input. No new merger is learned. Float32 state remains 12x24 = 1152 payload bytes.

`local`: mean CE on A and B with their respective local oracle labels, including
unknown when evidence is missing. `future`: 0.5 of the same local loss plus 0.5
CE on MAXSET(A,B) with the union label. Every CE includes 0.30 first-hop CE.
All arms compute the same three reader forwards; local discards the union loss.
Same initial weights, streamed worlds, optimizer, steps, batch size and final-step
selection. These objectives deliberately differ in supervision and its weights.
An improvement is not proof of a novel learning rule or equal information access
in training. Union labels/intermediates are privileged TRAINING supervision.

**Centralized equivalence control:** eventwise max pooling obeys
MAXSET(encode(A),encode(B)) = encode(A union B). Thus training the union term
centrally on the full raw union is mathematically equivalent here. Check states
and writer gradients on a deterministic test fixture before the run, and check
full-union predictions throughout evaluation. This experiment cannot establish a
special advantage for distributed training over centralized union rehearsal.

## Fixed budget and common tests

Exact numerical settings are in config.json: two writer arms x three inherited
fits x 1000 steps, 16 fresh training worlds/step, four queries/world, AdamW,
learning rate .001, decay .0001, clip 1, CPU one thread. Both arms use the same
per-step RNG seed (420000 + fit seed x 10000 + step), freshly generated worlds,
with overlap .30 and missing-path probability .20. Training stream hashes and
accept/reject counters must match between arms. No optimizer is run before freeze.
Each 16-world optimizer batch contains 64 query rows. Held-out strata use
independent seeds 20261010 + stratum index x 10000. The private-local gate is
the mean known-answer accuracy on A-only and B-only states. The union gate and
primary endpoint use the same known two-hop subset at overlap .50.

Generate and archive one common held-out corpus: 500 worlds at each of overlap
0,.25,.50, seed 20261010 + stratum index x 10000. Same v0.1 generative law and
private-answer ambiguity filter; instrument and save ALL attempted-world counts.
Save raw A/B evidence, queries, required paths, union/local targets and intermediate
targets; world-level identities cross all fits/arms. Four queries/world (two
one-hop, two two-hop). Test labels never guide optimization/checkpoint selection.
Archive final weights, all probability arrays, per-step corpus hashes and counts.
No adaptive extension, seed selection, early stopping or test-driven setting change.

## Outcomes and decisions

Primary endpoint: future minus local on known two-hop queries at overlap .50.
Within each world average eligible queries, then average the three inherited-fit
effects equally. Bootstrap SAME world indices across ALL fits, 5000 draws, seed
20261011. The interval is conditional on these three fits, not a population-of-
training-seeds interval. Declare the primary supervision effect supported only
if its lower bound exceeds zero; do not equate non-significance with equivalence.

Progress gate (all required): point gain >=2pp, primary lower bound >0, each of
three fits has positive gain, future union accuracy no more than 2pp below its
unadapted inherited baseline, and future private-local accuracy no more than
5pp below that inherited baseline. These two comparisons use known two-hop
queries at overlap .50. Require every future full-reencode known
two-hop accuracy >=.90. Private-local accuracy uses private labels; all private
states assessed against UNION labels are evidence-dependence controls instead.
Unknown accuracy and local known/unknown subsets must be reported separately so
majority unknown predictions cannot hide local forgetting. A failed gate stops
an immediate LLM scale-up from this study; it does not refute the whole research
direction. Gates are feasibility decisions, not additional confirmatory tests.

Evidence controls per writer: union, A only, B only, zero, swapped B (previous
whole world within stratum with cyclic wrap), full reencode, duplicate A
redelivery, and real three-party disjoint redistribution of the raw union.
Record both merge trees for the three-party test. MAXSET algebra is guaranteed
by construction; three-party and duplicate tests are sanity checks, not novel
convergence evidence. Save per-query class probabilities for all controls.
Update/conflict tests are out of scope; all revisions zero.

## Scope and limitations

N=6 and 1152 bytes are inherited to isolate the writer intervention, NOT a
capacity study: an explicit table is far smaller. Same finite alphabet, fixed
two-hop depth, no natural language, no pretrained LLM. Reader was trained on
union tasks in v0.1, so this is adaptation of an existing union-capable system,
not learning from scratch. Local-only training risks overwriting union capability;
report comparison against the unadapted baseline to expose that confound. If
future merely prevents such forgetting, say so instead of claiming new ability.
Current-query indistinguishability and future-extension witnesses are structural
illustrations only; no claim that learned states have become sufficient statistics.
