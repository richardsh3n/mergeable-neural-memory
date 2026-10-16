# 二十四项长期记忆与 agent 课题：审阅导航

**更新：2026-10-16。**以下是五轮研究提案，不是二十四篇已完成论文。各方向的文献核查范围和实验状态见原稿。

| 轮次 | 课题 | 主要问题 | 完整提案 |
|---|---|---|---|
| 第一轮 | 反事实充分记忆状态 | 压缩状态保留哪些因果信息才能回答干预问题？ | [英文稿](01_counterfactual_state.md) |
| 第一轮 | 按决策价值遗忘 | 容量有限时，哪些已有记忆应该被淘汰？ | [英文稿](02_decision_value_forgetting.md) |
| 第一轮 | 可撤销共享潜在记忆 | 信息压缩、派生、合并后，能否按来源撤回？ | [英文稿](03_revocable_shared_memory.md) |
| 第二轮 | 工具任务前瞻记忆 | 被打断后，能否在正确未来条件满足时执行承诺？ | [英文稿](round-2/01_prospective_tool_memory.md) |
| 第二轮 | 自我确认记忆闭环 | 行动选择怎样改变证据采样并强化错误记忆？ | [英文稿](round-2/02_self_confirming_loop.md) |
| 第二轮 | 主动证据采集 | 当前应观察和记录什么，才有利于未知未来任务？ | [英文稿](round-2/03_active_evidence_capture.md) |
| 第三轮 | 可写记忆跨模型迁移 | 模型升级后，旧记忆和新写入还能共同工作吗？ | [英文稿](round-3/01_writable_state_portability.md) |
| 第三轮 | 保留证据依赖的记忆压缩 | 如何避免把同一消息的多次转述当作独立佐证？ | [英文稿](round-3/02_dependency_preserving_memory.md) |
| 第三轮 | 记忆损坏后的选择性可靠召回 | 状态坏了一部分，能否回答完好的部分并适当拒答？ | [英文稿](round-3/03_graceful_memory_degradation.md) |
| 第四轮 | 跨语言更新一致性 | 换语言纠正和查询时，能否保留同一个当前事实？ | [英文稿](round-4/01_crosslingual_updates.md) |
| 第四轮 | 潜在记忆局部纠正 | 修改一条事实时，能否保留无关信息并更新真正的依赖后果？ | [英文稿](round-4/02_local_latent_correction.md) |
| 第四轮 | 多模态关联绑定 | 线索变化时，能否仍把人、物与事件绑定到正确对象？ | [英文稿](round-4/03_crossmodal_binding.md) |
| 第四轮 | 带契约的技能组合 | 工具版本改变后，记忆中的流程能否继续正确组合？ | [英文稿](round-4/04_skill_contract_composition.md) |
| 第四轮 | 搜索覆盖范围与负向记忆 | 能否记住搜索失败，同时不把未命中误当成不存在？ | [英文稿](round-4/05_coverage_aware_negative_memory.md) |
| 第五轮 | 并发整理的记忆一致性 | 慢总结会不会覆盖其他 writer 刚写入的新事实？ | [英文稿](round-5/01_concurrent_consolidation.md) |
| 第五轮 | 整理路径依赖 | 同一证据在不同合法处理顺序下，能否保留一致且正确的记忆？ | [英文稿](round-5/02_consolidation_path_dependence.md) |
| 第五轮 | 保留探索能力的经验使用 | 调整成功先例的暴露时机，能否改善固定预算内的解法质量？ | [英文稿](round-5/03_exploration_preserving_memory.md) |
| 第五轮 | 项目与角色适用范围 | 如何避免把真实记忆应用到错误项目？ | [英文稿](round-5/04_context_scope_switching.md) |
| 第五轮 | 私人例外与模型先验 | 模型会不会用通用常识替代可信的私人特殊事实？ | [英文稿](round-5/05_private_exceptions.md) |
| 第五轮 | 潜在推理中断续接 | 能否压缩保存未完成计算，并在同一模型上继续？ | [英文稿](round-5/06_resumable_latent_reasoning.md) |
| 第五轮 | 额外思考价值与停止 | 能否按多算一步的预期收益决定是否继续？ | [英文稿](round-5/07_value_calibrated_halting.md) |
| 第五轮 | 概念定义变更与记忆重解释 | 概念被细分后，能否区分可重判记录和缺信息记录？ | [英文稿](round-5/08_ontology_refinement.md) |
| 第五轮 | 延迟反馈的版本归因 | 晚到的结果是否归到实际执行的流程版本？ | [英文稿](round-5/09_delayed_feedback_credit.md) |
| 第五轮 | 投毒残留与长期恢复 | 错误经验在正常任务与总结中如何残留、复发或消退？ | [英文稿](round-5/10_poisoning_persistence.md) |

五轮中文总览：[第一轮](OVERVIEW.zh-CN.md)、[第二轮](round-2/OVERVIEW.zh-CN.md)、[第三轮](round-3/OVERVIEW.zh-CN.md)、[第四轮](round-4/OVERVIEW.zh-CN.md)、[第五轮](round-5/OVERVIEW.zh-CN.md)。

主项目已有合成试验：[v0.1 结果](../docs/PILOT_REPORT.md)、[v0.2 诊断](../experiments/v02/RESULTS.md)。这些历史结果不能作为二十四项提案已获验证的证据。新实验应在独立协议、冻结输入和新的结果目录中进行。
