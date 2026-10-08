# Exact mergeability: a constraint, not an originality claim

## Definition

Let an episode history be a finite **set** of events, with duplicates representing
the same event, rather than independent repeated observations. Let E map each set
to a memory state. Exact state mergeability asks for a function M satisfying

`M(E(A), E(B)) = E(A union B)` for every A and B.

The equivalence relation induced by E must be a congruence for union:

`E(A) = E(A') implies E(A union B) = E(A' union B)` for every B.

This condition is necessary and sufficient. Necessity follows by applying the
same merger to the same input states. For sufficiency, define the merger on
encoded states using any representative histories. Congruence makes the result
independent of the choice of representatives. The resulting operator is
commutative, associative and idempotent on reachable states.

This is a standard quotient-algebra argument. We claim no new theorem here.
Exact equality of encoded states is stronger than query-level behavioral
equivalence; neither should be inferred from the other without assumptions.

## Why adding memories can fail under overlap

Suppose events a, b and c contribute the scalar values 1, 2 and 3. Additive
encoding gives E({c}) = E({a,b}) = 3. Merging either state with E({a}) = 1
would require different outputs: E({c,a}) = 4 but E({a,b}) = 3. No deterministic
merger seeing only (3,1) can satisfy both requirements. Extra training cannot
recover information that this encoder has discarded.

The example concerns deduplicated event-set semantics. Addition is appropriate
when two reports are independent evidence whose counts should accumulate. The
pilot uses identical event tuples as duplicates; it does not solve evidence
identity, provenance or trust in natural language.

## Exact algebra alone is insufficient

Elementwise max is exactly mergeable for max-pooled event codes. A constant-zero
state is also exactly mergeable. Neither fact proves useful relational memory.
The pilot therefore jointly measures task accuracy and algebraic defects.
Max pooling is a strong established baseline, not our novel method.

## Finite capacity

A B-bit state has at most 2^B distinguishable values. If an arbitrary event set
over N independent events must answer every membership query without error,
there are 2^N distinguishable histories and B must be at least N. More expressive
questions can impose additional requirements. Fixed-capacity memory cannot
preserve arbitrary unlimited histories without loss. We study bounded tasks and
report failures, rather than claim lossless lifelong storage.

## Scope of this project

The candidate merger is symmetric by construction. Associativity and
idempotence are empirical objectives, not mathematical guarantees. The pilot is
a small learned symbolic-world model, not a pretrained LLM experiment. An exact
lookup used to generate labels is never available to the model at inference.

## 中文解读

压缩状态能否合并，首先取决于编码时有没有保留合并所需的信息。两个不同
经历如果已经压成相同状态，却在与第三段经历合并时需要不同结果，后面的
合并网络就无法保证全部正确。这是表示约束，不是增加网络规模就一定能解决。

所以本项目同时检查“合并规律”和“是否记住了有用关系”。简单最大值合并
天然满足交换、结合和去重，仍可能损失回答问题所需的信息。本研究不把这些
已有代数性质当作原创贡献。
