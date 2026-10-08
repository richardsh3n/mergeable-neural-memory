"""Descriptive rendering of frozen-run evidence; no model fitting or selection."""
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    "learned": "Symmetric residual", "deepsets": "DeepSets", "sum": "SUM",
    "max": "MAXSET", "mean": "MEAN", "a_only": "A only", "b_only": "B only",
    "zero": "Zero", "swapped_B": "Swapped B", "full_reencode_sum": "Union SUM (replay)",
    "full_reencode_max": "Union MAX (replay)",
}
COLORS = {"learned": "#2753b9", "deepsets": "#9471b5", "sum": "#da7a33",
          "max": "#2b9277", "mean": "#878b91", "full_reencode_sum": "#252b35"}


def main():
    metrics = json.loads((ROOT / "results/pilot/metrics.json").read_text())
    freeze = json.loads((ROOT / "results/freeze.json").read_text())
    cfg, runs = metrics["config"], metrics["runs"]
    methods = cfg["evaluation"]["methods"]
    conditions = cfg["evaluation"]["conditions"]
    primary = metrics["primary"]
    primary_condition = cfg["evaluation"]["primary_condition"]
    counts = defaultdict(lambda: {"known": 0, "unknown": 0, "twohop_known": 0, "queries": 0})
    with gzip.open(ROOT / "results/pilot/predictions.csv.gz", "rt") as handle:
        for row in csv.DictReader(handle):
            if row["method"] != "learned":
                continue
            c = counts[(int(row["seed"]), row["stratum"])]
            known = row["known"] == "True"
            c["queries"] += 1
            c["known" if known else "unknown"] += 1
            c["twohop_known"] += int(known and row["hops"] == "2")

    def values(method, key, condition=primary_condition):
        return np.array([r["conditions"][condition][method][key] for r in runs], dtype=float)

    def avg(method, key, condition=primary_condition):
        return float(values(method, key, condition).mean())

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "savefig.dpi": 180, "figure.dpi": 120})
    figures = ROOT / "figures"
    figures.mkdir(exist_ok=True)

    def save(fig, name):
        for extension in ("png", "svg", "pdf"):
            fig.savefig(figures / f"{name}.{extension}", bbox_inches="tight")
        plt.close(fig)

    fig, (ax, fits_ax) = plt.subplots(1, 2, figsize=(9, 4.2), gridspec_kw={"width_ratios": [2.8, 1]}, sharey=True)
    xs = np.array(cfg["evaluation"]["overlap_levels"])
    for method in COLORS:
        ys = np.array([values(method, "known_two_hop_world_macro_accuracy", c) for c in conditions]) * 100
        ax.plot(xs, ys.mean(1), marker="o", label=LABELS[method], color=COLORS[method], linewidth=2)
    ax.set(xlabel="Distractor-overlap probability", ylabel="Known two-hop world-macro accuracy (%)",
           title="Equal-fit means across overlap", xticks=xs, ylim=(-2, 102))
    ax.legend(fontsize=8, ncol=2, loc="lower left")
    for method in ("learned", "max"):
        fits_ax.plot(np.arange(len(runs)), values(method, "known_two_hop_world_macro_accuracy")*100,
                     marker="o", label=LABELS[method], color=COLORS[method], linewidth=1.5)
    fits_ax.set(title="Primary scores by fit", xlabel="Training seed", xticks=np.arange(len(runs)),
                xticklabels=[str(r["seed"]) for r in runs])
    ax.text(0.01, -0.23, "Right: all 3 fitted-model scores at overlap 0.50.\nPrimary conditional interval does not represent variability over training seeds.",
            transform=ax.transAxes, fontsize=8, color="#515765")
    save(fig, "accuracy_overlap")

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    algebra_methods = ["learned", "deepsets", "sum", "max", "mean"]
    for ax, name in zip(axes, ("commutativity", "idempotence", "associativity")):
        ys = [avg(m, name + "_relative_rmse") for m in algebra_methods]
        ax.bar(np.arange(len(ys)), np.maximum(ys, 1e-9), color=[COLORS[m] for m in algebra_methods])
        ax.set(yscale="log", title=name.capitalize(), xticks=np.arange(len(ys)),
               xticklabels=["Residual", "DeepSets", "SUM", "MAX", "MEAN"], ylim=(1e-10, max(10, max(ys) * 3)))
        ax.tick_params(axis="x", labelrotation=45)
        for i, y in enumerate(ys):
            ax.text(i, max(y, 1e-9) * 1.8, "0" if y == 0 else f"{y:.2g}", ha="center", fontsize=7)
    axes[0].set_ylabel("Relative state RMSE (zeros shown at 1e-9)")
    fig.suptitle("Numerical defects at overlap 0.50; associativity is not a three-party semantic test", fontsize=10)
    fig.tight_layout()
    save(fig, "algebra_defects")

    trace = json.loads((ROOT / "results/pilot/training-trace.json").read_text())
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.3))
    for ax, phase in zip(axes, ("shared", "learned", "deepsets")):
        for seed in cfg["training"]["seeds"]:
            rows = [r for r in trace if r["seed"] == seed and r["phase"] == phase]
            ax.plot([r["step"] for r in rows], [r["loss"] for r in rows], label=f"Seed {seed}")
        ax.set(xlabel="Optimization step", ylabel="Observed minibatch loss", title=phase.capitalize(), yscale="log")
    axes[0].legend(fontsize=8)
    fig.suptitle("All registered fits; unsmoothed 100-step log samples (different phase objectives)", fontsize=10)
    fig.tight_layout()
    save(fig, "training_losses")

    delta = primary["difference"] * 100
    lower, upper = np.array(primary["conditional_95_percent_interval"]) * 100
    supported = lower > 0
    best_simple = max(("sum", "max", "mean"), key=lambda m: avg(m, "known_two_hop_world_macro_accuracy"))
    best_all = max(("learned", "deepsets", "sum", "max", "mean"), key=lambda m: avg(m, "known_two_hop_world_macro_accuracy"))
    lines = ["# Locked pilot results / 冻结试验结果", "",
             f"**H1 {'supported' if supported else 'unsupported'} in this synthetic pilot:** residual − MAXSET = **{delta:+.2f} percentage points**, paired world-bootstrap conditional 95% interval **[{lower:+.2f}, {upper:+.2f}]**.", "",
             "该区间以这三份已训练模型为条件，不覆盖任意训练随机种子的总体不确定性。主终点保持冻结定义，没有以其他基线或分层替换。", "",
             f"最强简单基线为 **{LABELS[best_simple]}**；五种有效合并方法中最高均值为 **{LABELS[best_all]}**。与 MAXSET 的主比较不能解释成战胜所有方法。", "",
             f"执行范围：3 个训练种子 × 3 个条件 × 1,000 世界 × 4 查询；11 方法，共 **{metrics['prediction_rows']:,}** 行预测。实际运行 **{metrics['elapsed_seconds']:.1f} 秒**，不作为端到端性能基准。", "",
             f"运行前冻结 UTC：`{freeze['created_utc']}`。客户日期 `{freeze['client_date']}`（Asia/Shanghai）。本地 SHA 冻结，不是外部注册。", "",
             "## Primary outcomes by fit", "",
             "| Seed | Eligible worlds | Eligible queries | Residual (%) | MAXSET (%) | Difference (pp) |", "|---|---:|---:|---:|---:|---:|"]
    for run, fit in zip(runs, primary["fits"]):
        a = run["conditions"][primary_condition]["learned"]
        b = run["conditions"][primary_condition]["max"]
        lines.append(f"| {run['seed']} | {fit['worlds']} | {a['known_two_hop_query_count']} | {a['known_two_hop_world_macro_accuracy']*100:.2f} | {b['known_two_hop_world_macro_accuracy']*100:.2f} | {fit['difference']*100:+.2f} |")
    lines += ["", "## All methods at overlap 0.50", "",
              "All entries equally average the three fits. These are descriptive means, not additional confirmatory tests. ECE uses 10 fixed-width bins.", "",
              "| Method | Known 2-hop world macro (%) | All queries (%) | Known (%) | One-hop (%) | Two-hop incl unknown (%) | Unknown recall (%) | ECE |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for method in methods:
        columns = [avg(method, key) * 100 for key in ("known_two_hop_world_macro_accuracy", "accuracy", "known_accuracy", "one_hop_accuracy", "two_hop_accuracy", "unknown_recall")]
        lines.append("| " + LABELS[method] + " | " + " | ".join(f"{v:.2f}" for v in columns) + f" | {avg(method,'ece'):.4f} |")
    lines += ["", "Union references reread deduplicated raw facts; they are privileged references, not guaranteed accuracy upper bounds. Swapped B is a destructive evidence-matching control. Single-party and zero states are controls, not alternative joint-memory models.", "",
              "## Overlap sweep", "",
              "| Method | 0.00 (%) | 0.25 (%) | 0.50 (%) |", "|---|---:|---:|---:|"]
    for method in methods:
        lines.append("| " + LABELS[method] + " | " + " | ".join(f"{avg(method,'known_two_hop_world_macro_accuracy',c)*100:.2f}" for c in conditions) + " |")
    lines += ["", "![Accuracy and individual primary fit scores](../figures/accuracy_overlap.png)", "",
              "## Realized labels", "",
              "Only one method is counted, because the methods share labels. Deletion opportunities were 0.20 per path; the actual unknown class fraction differs.", "",
              "| Seed | Condition | Worlds | Queries | Known | Unknown | Unknown fraction (%) | Known two-hop queries |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for (seed, condition), c in sorted(counts.items()):
        lines.append(f"| {seed} | {condition} | {cfg['evaluation']['worlds_per_condition']} | {c['queries']} | {c['known']} | {c['unknown']} | {c['unknown']/c['queries']*100:.2f} | {c['twohop_known']} |")
    lines += ["", "## State algebra diagnostics", "",
              "Relative state RMSE, mean across fits. This is numerical state behavior; it is not semantic convergence. The frozen associativity probe rolls one query row, so 75% of the third states coincide with A. No same-world three-party answer experiment was run.", "",
              "| Method | Commutativity | Idempotence | Associativity (weak numeric probe) |", "|---|---:|---:|---:|"]
    for method in algebra_methods:
        lines.append("| " + LABELS[method] + " | " + " | ".join(f"{avg(method,k+'_relative_rmse'):.6g}" for k in ("commutativity", "idempotence", "associativity")) + " |")
    lines += ["", "![Numerical algebra defects](../figures/algebra_defects.png)", "", "## Resources and provenance", "",
              "| Seed | Shared parameters | Residual parameters | DeepSets parameters | Retained floats | Retained bytes | Checkpoint bytes |", "|---|---:|---:|---:|---:|---:|---:|"]
    for run, checkpoint in zip(runs, metrics["checkpoints"]):
        lines.append(f"| {run['seed']} | {run['shared_parameter_count']} | {run['merger_parameter_count']} | {run['deepsets_parameter_count']} | {run['state_float_count']} | {run['state_bytes']} | {(ROOT/'results/pilot'/checkpoint).stat().st_size} |")
    lines += ["", "The two input states occupy 2,304 payload bytes; the retained output occupies 1,152 bytes. Peak allocations, model weights and training cost are separate. CPU, one thread, final scheduled checkpoints only. The neural state is larger than a direct table for this tiny world, so this is not strong compression evidence.", "",
              "![Training traces](../figures/training_losses.png)", "",
              "## Interpretation and limits", "",
              "- No pretrained LLM or natural-language data was used. The reader receives six-entity/two-relation IDs and two explicit read passes.",
              "- The main merger has extra supervision and optimization relative to arithmetic baselines. DeepSets has a matched additional training budget, but different inductive bias.",
              "- Overlap concerns identical distractor event tuples, not paraphrases, source trust or semantic deduplication.",
              "- Updates, deletions, conflicts, incompatible encoders, within-party duplication and semantic three-party tests remain unperformed.",
              "- High accuracy on this small known-form task can be saturation. It cannot establish a new general memory paradigm.", "",
              "Generator rejection-attempt counts were not retained. The audit recomputes saved-prediction statistics and checks recorded private-ambiguity counts; raw facts and per-world states were not archived for independent row-level regeneration. These evidence limitations are detailed in `DEVIATIONS.md` and `results/audit.json`.", "",
              "See `CLAIMS.md`, `DEVIATIONS.md`, and `docs/NEXT_STAGE.md` for the scientific decision. Machine-readable evidence: `results/pilot/metrics.json`, `predictions.csv.gz`, checkpoints, `artifact_hashes.json`; independent reconstruction: `results/audit.json`."]
    (ROOT / "docs/PILOT_REPORT.md").write_text("\n".join(lines) + "\n")
    compact = {"primary_supported": bool(supported), "delta_pp": delta, "conditional_ci_pp": [lower, upper],
               "best_simple": best_simple, "best_nonreplay": best_all,
               "primary_scores_percent": {m: avg(m,"known_two_hop_world_macro_accuracy")*100 for m in methods}}
    (ROOT / "results/descriptive_summary.json").write_text(json.dumps(compact, indent=2) + "\n")
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
