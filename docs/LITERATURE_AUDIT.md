# 文献与方法审计 / Literature and Method Audit

**项目：** Can Memories Be Merged Without Replaying Experience?  
**审计日期：** 2026-10-08（Asia/Shanghai）。已逐项核验下列原始论文页面；最近相关版本为 Cache Merging v2，2026-10-02。  
**文档角色：** 方法边界、必要对照与主张审查。正式实验的参数、随机种子、数据规模和停止标准以项目预注册及冻结配置为准。本文不包含实验结果，也不替代预注册。

**执行后说明：** 下文主张矩阵保留执行前的文献审查状态。首轮试验现已完成，当前证据与负结果以 [PILOT_REPORT.md](PILOT_REPORT.md) 和项目 `CLAIMS.md` 为准，不能把本文件的“未实验”误读成目前没有产物。

## 1. 判断 / Decision

这个方向可以继续，但贡献必须收窄为：**在固定持久状态预算内，合并独立写入的神经状态后，是否仍能进行联合关系推理，并在不同交付顺序与重复交付下保持可靠表现。**

潜在状态传递、关联记忆聚合、集合不变网络以及收敛合并都已有直接先例。不能把“神经记忆可以合并”“不用文本交流”“交换律”或“第一个神经 CRDT”当作已经成立的新颖性。

**English summary.** This project studies fixed-budget composition of independently written neural memory states. Existing work already covers latent-state exchange, associative-memory aggregation, permutation-invariant set processing, and convergent KV-fragment exchange. The open experimental question is whether a learned, fixed-capacity state can retain distributed relational bindings, support queries requiring information from multiple parties, and remain stable under merge order, redelivery, and subsequent writes. A small synthetic neural pilot establishes neither an LLM result nor a deployment guarantee. Novelty remains provisional pending broader literature review and actual comparisons.

## 2. 最接近的原始工作 / Closest primary work

| 原始工作 | 已核验内容 | 对本项目的限制 |
|---|---|---|
| **Cache Merging as a Convergent Replicated State for Multi-Agent Latent Reasoning**, Baquero & Brito，2026-07-01；v2 为 2026-10-02。[摘要](https://arxiv.org/abs/2607.01308v2)、[方法 §4.4](https://arxiv.org/html/2607.01308v2#S4.SS4) | 持久状态是内容寻址的 KV 片段集合；集合并集具有交换、结合、幂等性质，确定性 render 排列并拼接片段。已有分割证据与自然语言多跳实验。 | 已覆盖“潜在 CRDT 与分割推理”。新片段会增加存储，区别不是无限大状态中的次序不变性，而是固定字节压缩后保留何种能力。其重复吸收针对相同字节，不等于语义近重复。新版修正了初版 HotpotQA 的接近无损描述，不应沿用初版结果。 |
| **A Federated Many-to-One Hopfield Model for Associative Neural Networks**, Alessandrelli 等，2026-03-20。[摘要](https://arxiv.org/abs/2603.19902)、[方法 §3](https://arxiv.org/html/2603.19902v1#S3) | 客户端传递 Hebbian 算子，服务器聚合与分解，并将重建原型反馈给客户端；不集中重放原始样本。 | 已覆盖“固定形状关联算子聚合”。实验目标是原型恢复与关联检索，并非 LLM 中任意实体关系绑定、跨主体组合问答及冲突来源语义；本项目仍需与简单算子相加比较。 |
| **Deep Sets**, Zaheer 等，2017-03-10，NeurIPS 2017。[原文](https://arxiv.org/abs/1703.06114) | 学习排列不变集合函数，常用构造是对逐元素特征求和后读取。 | “对称网络”本身不新。必须加入可训练的 sum pooling 基线，不能只比较未经适配的算术操作。 |
| **PointNet**, Qi 等，2016-12-02，CVPR 2017。[原文](https://arxiv.org/abs/1612.00593) | 使用对称池化处理无序点集合。 | 可训练特征加 coordinatewise max 是强基线；其代数性质来自 max，不来自本项目的训练技巧。 |
| **A Comprehensive Study of Convergent and Commutative Replicated Data Types**, Shapiro 等，INRIA RR-7506，2011。[原始报告镜像](https://dsf.berkeley.edu/cs286/papers/crdt-tr2011.pdf) | 状态型 CRDT 的收敛依赖兼容的偏序、上确界合并及单调更新等条件。 | 一个 MLP 在测试集上近似交换、结合、幂等，不能据此获得分布式收敛定理；max 合并也不能自动修复非单调写入。 |
| **Mergeable Summaries**, Agarwal 等，PODS 2012；TODS 2013。[作者版](https://users.cs.duke.edu/~pankaj/publications/papers/merge-summ.pdf)、[出版页](https://doi.org/10.1145/2500128) | 紧凑摘要的合并应维持规定的容量与误差约束；线性 sketches 是基本先例。 | “固定大小摘要可合并”是经典问题。本项目的可能贡献须来自特定的关系推理任务、神经读写结构及量化的误差代价。 |

这里的“未展示”只描述已检查的论文内容，不证明全球文献不存在该结果。预印本结论按作者报告处理，不等同于我们已经独立复现。

## 3. 问题定义 / Problem definition

代理 A 与 B 使用相同、冻结版本的写入器，分别读取事件流 \(E_A,E_B\)，得到 \(M_A=W(E_A)\) 和 \(M_B=W(E_B)\)。合并器只接收状态：

\[
M_{AB}=F(M_A,M_B),\qquad \mathrm{bytes}(M_{AB})\leq B.
\]

读出器回答 \(R(M_{AB},q)\)。查询必须在本地写入完成之后才提供。若编码时看到查询，应另标为 query-aware 条件，不能与 query-blind 主条件混用。

合并过程不得访问旧事件、原始文本、原代理的可增长缓存或隐藏的检索库。固定形状不够：dtype、额外来源表、计数器、时间戳和保留的子状态都计入 \(B\)。训练时的临时张量与推理的临时工作内存另报，不能与持久状态容量混淆。

### 3.1 两种不同的重复 / Two notions of duplication

- **相同状态重投递 / State redelivery：** 再次交付同一个已写入状态；应测 \(F(M,M)\) 与 \(M\) 的差异。
- **事件重叠 / Overlapping experience：** A、B 独立编码部分相同事件，整体状态通常不同。幂等 \(F(M,M)=M\) 不足以证明它能消除重叠事件的影响。

第一阶段应同时报告互不重叠流与部分重叠流。不能只用重复交付破坏 sum，然后将 max 的代数优势解释为学到了语义去重。

### 3.2 时间与冲突 / Time and conflict

交换律适用于**交付顺序**。真实事件的发生时间仍可影响答案。若两个来源给出不同事实，必须预先定义时间、来源可信度与冲突答案语义；没有这些信息，模型无法从任意压缩状态中恢复未编码的真相。

时间戳、来源或命名空间若未进入首轮原型，不应声称实现了冲突消解、证据溯源或局部纠错。删除、撤回与遗忘也不等同于新增事实；它们需要独立协议和测试。

## 4. 方法审查与必要基线 / Method review and baselines

| 基线或候选 | 状态合并 | 实数算术下的代数性质 | 审查要点 |
|---|---|---|---|
| Sum / Hebbian-addition | \(M_A+M_B\) | 交换、结合；不幂等 | 有效的分布式累积基线。浮点求和次序会产生舍入差异。 |
| Mean | \((M_A+M_B)/2\) | 交换、幂等；一般不结合 | 若带事件计数做加权平均，计数必须计入状态；仍不能自动处理重叠来源。 |
| Coordinatewise max | \(\max(M_A,M_B)\) | 交换、结合、幂等 | 强代数基线。有限且无 NaN 的输入可逐元素验证；最大值并不保证关系语义正确。 |
| Trainable sum pooling | 累加逐事件的学习特征，再由共享读出器回答 | 累积层可交换、结合；不幂等 | 持久保存求和统计量，把非线性读出放在查询阶段。若每次合并后又应用非线性变换，结合性通常不保留。 |
| Trainable max pooling | 对学习特征做逐坐标 max，再读出 | 池化层可交换、结合、幂等 | 应允许编码器为 max 训练，避免给简单方法安排不适合它的状态。 |
| Symmetric learned pair merger | 例如基于 \([A+B,|A-B|]\) 的残差映射 | 可由结构保证交换；结合与幂等需另证或测试 | 对称的两输入 MLP 不自动具有多次合并的一致性。首轮可把它称为 learned merger，不能称为已证明的 neural CRDT。 |
| Sequential consolidation | 以 A 为旧状态写入 B，再反向重复 | 一般次序敏感 | 与循环记忆的自然基线比较，明确它输入的是状态还是重放事件。 |
| Full re-encode | 从去重后的联合原始事件重新写入同容量状态 | 由编码定义决定 | 这是访问旧经历的特权参考，不保证性能上界，违反 no-replay 主条件。必须单独标注。 |
| Explicit finite relation table | 保存任务宇宙内关系，按预定集合或冲突规则合并 | 可准确实现指定语义 | 是任务与容量参考。若小世界整个图轻易装入同预算，它会暴露原型未进入压缩难区间。 |

共享编码器加共享读出器适合隔离合并操作；但它回答的是“在这套表示上哪个合并器更好”。更强的架构比较应给 sum/max 自己适配的训练机会。两种比较均须说明参数量、训练样本、更新次数、验证选择及实际推理预算。

若使用代数正则化，应记录 \(\lambda_C,\lambda_A,\lambda_I\) 的选择，并分别报告有/无该损失的消融。训练三项损失同时降低，不足以证明任何一项在未见分布上得到保证。

## 5. 状态可合并性的必要条件 / Necessary conditions

以下是本项目的基础形式化备注，不主张发现了新的下界定理。

**碰撞无法被合并器逆转。** 设两段经历 \(A,B\) 被写入同一状态，即 \(W(A)=W(B)\)。若存在第三段经历 \(C\) 和查询 \(q\)，使正确答案满足

\[
\mathrm{Ans}(A\cup C,q)\ne\mathrm{Ans}(B\cup C,q),
\]

那么任何只接收 \(W(\cdot)\) 的确定性合并器，对这两个联合世界都接收完全相同的输入，无法同时回答正确。随机化也不能保证这两个世界总是正确。可合并编码需要保留未来查询与联合事件所需的区别，而不仅是本地当前的读出表现。

**有限精度容量限制。** 一个持久状态及全部辅助元数据若只有 \(b\) bits，最多有 \(2^b\) 种不同表示。若任务包含 \(n\) 个独立二元事实，并要求无误回答任意事实查询，则需区分 \(2^n\) 个世界，因此必须有 \(b\ge n\)。这是简单计数论证；不覆盖带误差、分布假设、概率保证或无限精度实数模型。它不证明小型神经实验应失败，也不为实际容量曲线提供紧界。

**代数与语义分开。** 一个全返回零的合并器也可以交换、结合、幂等。必须同时检查状态层性质与回答正确率。反过来，答案相同不代表内部状态相同；不同状态在后续新写入之后可能分歧。

**CRDT 额外条件。** 若想提出状态型 CRDT 结论，还须给出偏序、合并为上确界的证明、兼容且单调的本地写入，以及明确的交付与身份假设。带遗忘门的非单调循环状态不因为选用了 max 合并就自动满足这些条件。当前项目应优先报告可测误差，不使用未经证明的收敛保证。

## 6. 评测协议建议 / Evaluation protocol recommendations

### 6.1 首轮受控神经原型 / Controlled neural pilot

首轮可以使用随机小世界、离散实体与关系标识、可训练固定状态及读出器，在 CPU/MPS 上检验机制。它不是 LLM 实验；没有预训练语言骨干时，不得报告“LLM记忆性能”“自然语言迁移”或“人类式记忆已实现”。

正例的两条关键边应分别且仅存在于不同代理中。任一单方、丢掉任一关键边、错命名空间的状态均应不足以完成查询。无解样本要有明确 UNKNOWN 标签和独立评分，防止模型靠默认输出或答案分布获益。随机实体置换可以减弱标签捷径，但不能自动证明对新实体词汇或新世界规模泛化。

训练、验证、测试按完整世界及事件流分开；查询模板、图拓扑和随机种子的关系必须公开。先冻结测试生成规则，调参只看训练与验证。若训练中已经大量出现相同两跳形式，测试结果只能叫“未见世界上的同形式组合”，不能叫“未见推理规则”。

### 6.2 必须并列报告的指标 / Required reporting

1. **答案层：** 总体准确率、每种查询与 UNKNOWN 类的表现、每个世界的合并成功率；与最强可行基线做配对比较。
2. **局部信息控制：** A only、B only、drop-one-edge、wrong-namespace；联合成功须超过单方泄漏或先验猜测。
3. **状态层：** 交换误差 \(\|F(A,B)-F(B,A)\|\)、结合误差 \(\|F(F(A,B),C)-F(A,F(B,C))\|\)、幂等误差 \(\|F(A,A)-A\|\)，报告归一化误差、最大误差和精确相等比例；浮点行为明确说明。
4. **行为层代数：** 交换、不同合并树、重复交付后的答案一致率与正确率。状态近似相等不能取代此指标。
5. **容量与成本：** 持久字节、dtype、参数量、合并调用次数和时间；规模变化时保持主预算不变。
6. **重复类型：** 单个状态重投递与独立经历部分重叠分别报告。它们不是同一实验。
7. **随机性：** 独立训练种子与配对世界的不确定性；不能把同一世界下的多条相关查询当作独立复制。

首轮没有三代理测试就不支持结合性；没有继续写入就不支持 merge-then-write；没有真实事件时间、来源和冲突任务就不支持冲突消解。

### 6.3 后续增强 / Follow-on experiments

- 多代理与更深组合查询，互换合并树及交付顺序。
- 同容量下提高独立关系数与干扰，呈现压缩代价；同时用显式关系表校准任务难度。
- 合并后输入新事实、矛盾更正及无关新经历，检查旧事实、更新事实和相关组合答案。
- 语义近重复与别名需要单独的数据生成和评价，不能由 byte-level duplication 推导。
- 真正 LLM 骨干的接入是后续独立阶段；固定文本预算、模型版本及 prompt，训练/适配方法和全部开销明确记录。

## 7. 未解决主张矩阵 / Unresolved claim matrix

| 主张 / Claim | 当前状态 / Status | 足够的下一步证据 / Evidence needed | 当前允许的表述 / Allowed wording |
|---|---|---|---|
| 首个可合并神经记忆 | 不支持；已有直接先例 | 更全面原始文献审查仍不能单独证明优先权 | 不使用 first/首次 |
| 固定容量与不重放历史 | 设计约束，待代码审计 | 序列化全部状态及辅助元数据；检查合并输入与隐藏缓存 | proposed fixed-budget no-replay design |
| 学习合并器优于简单池化 | 未实验 | 同资源下训练 sum/max；多种子配对比较 | empirical question |
| 跨代理组合 | 未实验 | 关键边独占分割、单方与缺边控制、未见世界测试 | target capability |
| 严格交换性 | 取决于具体结构和数值路径 | 结构证明与实际字节检查 | exact only if established |
| 严格结合性及幂等 | 对普通对称 MLP 不成立 | 证明或限定为已测误差；三代理与重投递实验 | measured approximate consistency |
| 对重叠经历去重 | 未实验 | 独立流部分重叠及语义重复评价 | pending |
| 合并后持续更新 | 未实验 | merge-then-write 的新事实、干扰、修正任务 | pending |
| 冲突溯源与局部纠错 | 未编码就不可声称 | 时间、来源、冲突规则、相关与无关事实指标 | follow-on target |
| LLM 或自然语言有效性 | 首轮原型不支持 | 实际语言骨干和新数据上的独立实验 | synthetic neural pilot only |
| 人类式记忆、意识或 AGI | 本协议不检验 | 不能由这些行为测试推导 | 不作主张 |
| 有限容量存储无限经历且无损 | 不能作通用保证 | 需改成限定查询、误差及容量曲线 | bounded approximate memory |

## 8. 反证与继续条件 / Falsification and continuation

如果训练充分的 sum 或 max 在同容量下达到同等组合性能，最初的“新合并器”贡献应撤回，保留基准、容量曲线与机制分析。如果提升仅来自更多参数、更多训练或读取联合旧经历，应归因于这些差异。如果只在小型两跳同形式任务中有效，报告该范围，不外推长程推理。

继续投入更大模型的条件是：先展示预算审计、正确的单方控制，以及至少一种最强简单基线无法解释的可重复收益。具体数值门槛应在测试结果揭盲前由预注册固定。负结果也是可报告结果，不得在看到测试失败后悄悄替换主终点。

## 9. 术语 / Terminology

| 中文 | English | 本项目含义 |
|---|---|---|
| 固定持久状态预算 | fixed persistent-state budget | 包含全部辅助数据的固定存储上限 |
| 无经历重放 | no experience replay | 合并与查询不重新读取历史事件 |
| 合并次序 | delivery / merge order | 交付顺序，不是世界事件发生时间 |
| 组合查询 | compositional query | 正确答案依赖多个代理提供的信息 |
| 状态重投递 | state redelivery | 再次交付相同状态 |
| 重叠经历 | overlapping experience | 不同独立事件流共享部分观察 |
| 语义去重 | semantic deduplication | 识别字节不同但意义重复的信息 |
| 状态收敛 | state convergence | 明确条件下达到一致状态；不是准确率较高的同义词 |

## 10. 审计边界 / Audit limitations

本轮检索覆盖原始 arXiv 论文、作者论文页、原始研究报告与出版页，关键词包括 recurrent-state merge、latent memory merging、neural CRDT、federated associative memory 和 mergeable summaries。选择文献是针对本项目约束的定向审查，不是系统综述，也不是穷尽性优先权检索。HAL 的报告页遇到访问挑战，因此原始 CRDT 报告从高校保存的原文镜像读取；文献页面可读不代表已复现其代码与结果。

本文件仅建立可审查的研究范围。实验结果必须由真实产物另行记录，并注明设备、冻结配置、模型、数据与局限。
