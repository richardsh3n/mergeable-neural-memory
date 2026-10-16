# When Concepts Split: Memory under Ontology Refinement

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

When a project changes a category's meaning, can old memory distinguish records that can be reclassified from those that lack the necessary detail? Splitting “vehicle” into new subclasses is more than renaming a storage field. An old compressed record may not contain the attribute required by the new definition.

[MindMemOS](https://arxiv.org/abs/2608.12428) already evolves memory schemas. [AgentCore's official metadata documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-memory-metadata.html) already covers schema changes and warns that existing records are not automatically backfilled. Schema evolution is therefore established. The proposed test focuses on semantic recoverability and calibrated unknowns after concept refinement.

## Hypothesis and minimal experiment

Hypothesis: a schema-versioned representation with explicit missingness reduces invented reclassifications while retaining more answerable queries than blind schema rewriting. A standard symbolic migration may be sufficient and must be compared.

Generate worlds with exact attributes and several evolving taxonomies. Store only a controlled subset of attributes, then issue definition changes: split, merge, scope refinement and purely cosmetic rename. The host model and tools remain fixed. Query both historical definitions and current definitions. Where the necessary attribute was never retained, correct behavior is unresolved rather than a guessed label.

Compare blind summary conversion, version tags plus prompting, explicit symbolic mappings, a learned schema adapter, and full-evidence reconstruction. Match available definitions, evidence and retained bytes. Reconstructing from raw episodes is a recovery upper bound when compressed-state methods lack that access. Split by ontology operation and unseen attribute combinations; do not test only renamed training labels.

Primary endpoint: correct answer-or-unknown decisions under the new definitions. Report recoverable-subset accuracy, unsupported reclassification, historical-query consistency, migration cost, missingness calibration and storage. Use world-paired intervals and show each schema-change type separately.

## Stop rule and value

Stop a neural-method claim if ordinary versioned symbolic migration wins, if the method invents missing attributes, or if schema semantics are ambiguous to reviewers. The output is a recoverability benchmark for evolving scientific/team vocabularies. Unlike tool-version skill contracts, the changed object is the meaning of remembered categories; unlike model migration, the host is unchanged.
