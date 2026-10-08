"""Independent descriptive audit of the frozen pilot's saved evidence.

Does not import or invoke the model implementation, train, tune, or generate new
evaluation worlds. Bootstrap is reconstructed independently from prediction CSV.
Checkpoint loading uses PyTorch's restricted weights-only loader on CPU.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FREEZE_UTC = "2026-10-08T16:32:32.407124+00:00"
PINNED_INPUTS = {
    "docs/PREREGISTRATION.md": "3415a1c8e60c2f5f3b83e5069feb445ed7fc6a4cb920def9d9e00d6416c616c4",
    "configs/pilot.json": "bf3ddbb08f19dbe0a08adf9811be9eb10a823528f3161eac4b08e18af1c7a38e",
    "src/merge_memory.py": "6a22f25e6b7ce617bc4a50b8f1903ebff4b50fda09975d7159aeae0dcfc8c7a4",
}
METHODS = ["learned", "deepsets", "sum", "max", "mean", "a_only", "b_only",
           "zero", "swapped_B", "full_reencode_sum", "full_reencode_max"]


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def inside(base: Path, name: str) -> Path:
    path = (base / name).resolve()
    path.relative_to(base.resolve())
    return path


def boolean(value: str) -> bool:
    if value in {"True", "true", "1"}:
        return True
    if value in {"False", "false", "0"}:
        return False
    raise ValueError(f"Invalid saved boolean: {value!r}")


class Audit:
    def __init__(self) -> None:
        self.report = {
            "schema_version": 1,
            "scope": "Independent reconstruction from saved artifacts; no model-code import, training, tuning, or new evaluation",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "auditor_sha256": digest(Path(__file__).resolve()),
            "checks": [], "details": {}, "warnings": [],
            "limitations": [
                "Bootstrap interval conditions on three fitted models, not a population of training seeds.",
                "Private ambiguity is checked against saved oracle counts; raw fact sets are not saved in CSV, so their counts cannot independently be recomputed here.",
                "Local freeze timestamps and hashes are provenance evidence, not an externally authenticated registration.",
                "Checkpoint weights are inspected; per-world latent states are not stored, so their runtime dtype relies additionally on the frozen source and pre-run tensor checks.",
            ],
        }

    def check(self, name: str, condition: bool, detail=None) -> None:
        entry = {"name": name, "passed": bool(condition)}
        if detail is not None:
            entry["detail"] = detail
        self.report["checks"].append(entry)
        if not condition:
            raise AssertionError(name)


def perform(audit: Audit, run: Path) -> None:
    freeze_path = ROOT / "results/freeze.json"
    freeze = json.loads(freeze_path.read_text())
    config = json.loads((ROOT / "configs/pilot.json").read_text())
    metrics = json.loads((run / "metrics.json").read_text())
    artifacts = json.loads((run / "artifact_hashes.json").read_text())
    details = audit.report["details"]
    details["freeze_sha256"] = digest(freeze_path)
    details["freeze_utc"] = freeze["created_utc"]
    audit.check("freeze_time_matches_observed_pre_run_record", freeze["created_utc"] == EXPECTED_FREEZE_UTC)
    audit.check("freeze_is_local_not_external_registration", freeze["status"] == "local_pre_run_freeze_not_external_registration")
    for name, expected in PINNED_INPUTS.items():
        audit.check(f"pinned_input:{name}", freeze["sha256"].get(name) == expected and digest(inside(ROOT, name)) == expected)
    verified_inputs = []
    for name, expected in freeze["sha256"].items():
        path = inside(ROOT, name)
        audit.check(f"frozen_hash:{name}", path.is_file() and digest(path) == expected)
        verified_inputs.append(name)
    details["verified_frozen_inputs"] = verified_inputs
    audit.check("configuration_matches_freeze_and_run", config == freeze["config"] == metrics["config"])
    for name, expected in artifacts.items():
        path = inside(run, name)
        audit.check(f"artifact_hash:{name}", path.is_file() and digest(path) == expected)
    required_artifacts = {"metrics.json", "predictions.csv.gz", "training-trace.json"} | set(metrics["checkpoints"])
    audit.check("all_required_artifacts_are_hashed", required_artifacts <= set(artifacts))
    details["artifact_manifest_sha256"] = digest(run / "artifact_hashes.json")

    seeds = config["training"]["seeds"]
    strata = config["evaluation"]["conditions"]
    methods = config["evaluation"]["methods"]
    audit.check("registered_seeds_strata_methods", seeds == [11, 23, 37] and strata == ["overlap_0.0", "overlap_0.25", "overlap_0.5"] and methods == METHODS)
    nworlds = int(config["evaluation"]["worlds_per_condition"])
    nqueries = int(config["evaluation"]["queries_per_world"])
    audit.check("registered_world_query_counts", nworlds == 1000 and nqueries == 4)
    nentities = int(config["dataset"]["n_entities"])
    nclasses = nentities + 1
    seed_index = {seed: i for i, seed in enumerate(seeds)}
    stratum_index = {name: i for i, name in enumerate(strata)}
    method_index = {name: i for i, name in enumerate(methods)}
    shape = (len(seeds), len(strata), nworlds, nqueries)
    seen = np.zeros(shape, dtype=np.uint16)
    targets = np.full(shape, -1, dtype=np.int8)
    hops = np.zeros(shape, dtype=np.int8)
    correct = np.zeros(shape + (len(methods),), dtype=np.bool_)
    predictions = np.full(shape + (len(methods),), -1, dtype=np.int8)
    max_probs = np.full(shape + (nclasses,), np.nan)
    reference_probs = np.full(shape + (nclasses,), np.nan)
    metadata = {}
    count = 0
    probability_tolerance = 1e-6
    worlds_per_batch = int(config["evaluation"]["batch_size"]) // nqueries
    with gzip.open(run / "predictions.csv.gz", "rt", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            count += 1
            seed, stratum, method = int(row["seed"]), row["stratum"], row["method"]
            world, query_id = int(row["world_id"]), int(row["query_id"])
            if seed not in seed_index or stratum not in stratum_index or method not in method_index:
                raise ValueError(f"Unregistered row identity at CSV row {count}")
            if not (0 <= world < nworlds and 0 <= query_id < nqueries):
                raise ValueError(f"Invalid world/query ID at CSV row {count}")
            key = (seed_index[seed], stratum_index[stratum], world, query_id)
            mi = method_index[method]
            if seen[key] & (1 << mi):
                raise ValueError(f"Duplicate method/query row at CSV row {count}")
            seen[key] |= 1 << mi
            subject, r1, r2 = int(row["subject"]), int(row["relation1"]), int(row["relation2"])
            target, prediction, hop_count = int(row["target"]), int(row["prediction"]), int(row["hops"])
            known, is_correct = boolean(row["known"]), boolean(row["correct"])
            local_a, local_b = int(row["local_possible_answers_a"]), int(row["local_possible_answers_b"])
            if not (0 <= subject < nentities and r1 in (0, 1) and 0 <= target < nclasses and 0 <= prediction < nclasses):
                raise ValueError(f"Out-of-range value at CSV row {count}")
            if hop_count != (1 if r2 == -1 else 2) or (r2 != -1 and r2 != 1 - r1):
                raise ValueError(f"Invalid query relation/hop structure at CSV row {count}")
            if hop_count != (1 if query_id < 2 else 2):
                raise ValueError(f"Incorrect one/two-hop grouping at CSV row {count}")
            if known != (target < nentities) or is_correct != (prediction == target):
                raise ValueError(f"Inconsistent label/correctness metadata at CSV row {count}")
            if not (1 <= local_a <= nentities and 1 <= local_b <= nentities):
                raise ValueError(f"Invalid ambiguity counts at CSV row {count}")
            if hop_count == 2 and known and (local_a < 2 or local_b < 2):
                raise ValueError(f"Private-party sufficiency in known two-hop row {count}")
            shared = (subject, r1, r2, hop_count, target, known, local_a, local_b)
            if key in metadata and metadata[key] != shared:
                raise ValueError(f"Labels/query/oracle metadata differ across methods at row {count}")
            metadata[key] = shared
            targets[key], hops[key] = target, hop_count
            correct[key + (mi,)], predictions[key + (mi,)] = is_correct, prediction
            probabilities = np.asarray(json.loads(row["probabilities"]), dtype=np.float64)
            confidence = float(row["confidence"])
            if probabilities.shape != (nclasses,) or not np.all(np.isfinite(probabilities)) or not math.isfinite(confidence):
                raise ValueError(f"Invalid probabilities at CSV row {count}")
            if np.min(probabilities) < 0 or np.max(probabilities) > 1 or abs(probabilities.sum() - 1) > probability_tolerance:
                raise ValueError(f"Invalid probability simplex at CSV row {count}")
            if int(np.argmax(probabilities)) != prediction or abs(float(probabilities.max()) - confidence) > probability_tolerance:
                raise ValueError(f"Prediction/confidence differs from probabilities at CSV row {count}")
            if method == "max":
                max_probs[key] = probabilities
            elif method == "full_reencode_max":
                reference_probs[key] = probabilities
            if method == "swapped_B":
                donor = int(row["donor_world_id"])
                batch_start = (world // worlds_per_batch) * worlds_per_batch
                batch_worlds = min(worlds_per_batch, nworlds - batch_start)
                expected_donor = batch_start + (world - batch_start - 1) % batch_worlds
                if donor == world or donor != expected_donor:
                    raise ValueError(f"Invalid grouped donor state at CSV row {count}")
            elif row["donor_world_id"] != "":
                raise ValueError(f"Unexpected donor metadata at CSV row {count}")

    expected_rows = len(seeds) * len(strata) * nworlds * nqueries * len(methods)
    audit.check("row_count_396000", count == expected_rows == 396000 == metrics["prediction_rows"], {"observed": count, "expected": expected_rows})
    audit.check("complete_unique_method_world_query_coverage", bool(np.all(seen == (1 << len(methods)) - 1)))
    audit.check("labels_query_and_oracle_counts_shared_across_methods", len(metadata) == int(np.prod(shape)))
    audit.check("known_two_hop_private_ambiguity", True, "Every saved known two-hop row has both private possible-answer counts >=2")
    audit.check("probabilities_predictions_confidence_and_correctness_consistent", True)
    audit.check("swapped_B_uses_distinct_grouped_donors", True)
    audit.check("maxset_and_full_max_predictions_identical", bool(np.array_equal(predictions[..., method_index["max"]], predictions[..., method_index["full_reencode_max"]])))
    max_probability_difference = float(np.max(np.abs(max_probs - reference_probs)))
    audit.check("maxset_and_full_max_probabilities_close", max_probability_difference <= probability_tolerance,
                {"max_absolute_difference": max_probability_difference, "absolute_tolerance": probability_tolerance})

    audit.check("three_unique_run_summaries", len(metrics["runs"]) == 3 and sorted(record["seed"] for record in metrics["runs"]) == seeds)
    run_by_seed = {record["seed"]: record for record in metrics["runs"]}
    data_summary = []
    for si, seed in enumerate(seeds):
        for ci, stratum in enumerate(strata):
            t, h = targets[si, ci], hops[si, ci]
            known = t < nentities
            eligible = known & (h == 2)
            eligible_counts = eligible.sum(axis=1)
            eligible_worlds = eligible_counts > 0
            data_summary.append({"seed": seed, "stratum": stratum, "worlds": nworlds,
                                 "queries": int(t.size), "known_queries": int(known.sum()),
                                 "unknown_queries": int((~known).sum()), "unknown_fraction": float((~known).mean()),
                                 "eligible_worlds": int(eligible_worlds.sum()), "eligible_queries": int(eligible.sum())})
            for method, mi in method_index.items():
                reported = run_by_seed[seed]["conditions"][stratum][method]
                observed_correct = correct[si, ci, ..., mi]
                macro = ((observed_correct & eligible).sum(axis=1)[eligible_worlds] / eligible_counts[eligible_worlds]).mean()
                audit.check(f"summary:{seed}:{stratum}:{method}",
                            reported["n"] == int(t.size) and abs(reported["accuracy"] - float(observed_correct.mean())) <= 1e-6
                            and reported["known_two_hop_world_count"] == int(eligible_worlds.sum())
                            and reported["known_two_hop_query_count"] == int(eligible.sum())
                            and abs(reported["known_two_hop_world_macro_accuracy"] - float(macro)) <= 1e-12)
    details["dataset_class_and_eligibility_counts"] = data_summary

    ci = stratum_index[config["evaluation"]["primary_condition"]]
    main, baseline = config["evaluation"]["primary_contrast"]
    differences_by_fit, reconstructed_fits = [], []
    for si, seed in enumerate(seeds):
        eligible = (targets[si, ci] < nentities) & (hops[si, ci] == 2)
        counts = eligible.sum(axis=1)
        mask = counts > 0
        main_world = (correct[si, ci, ..., method_index[main]] & eligible).sum(axis=1)[mask] / counts[mask]
        base_world = (correct[si, ci, ..., method_index[baseline]] & eligible).sum(axis=1)[mask] / counts[mask]
        differences = main_world - base_world
        differences_by_fit.append(differences)
        reconstructed_fits.append({"seed": seed, "worlds": int(mask.sum()), "queries": int(eligible.sum()),
                                   "difference": float(differences.mean()), "main_world_macro": float(main_world.mean()),
                                   "baseline_world_macro": float(base_world.mean())})
    rng = np.random.default_rng(int(config["evaluation"]["bootstrap_seed"]))
    resamples = int(config["evaluation"]["bootstrap_resamples"])
    audit.check("registered_bootstrap_settings", resamples == 5000 and config["evaluation"]["bootstrap_seed"] == 20261008)
    boot = np.zeros(resamples, dtype=np.float64)
    for differences in differences_by_fit:
        draw = rng.integers(len(differences), size=(resamples, len(differences)))
        boot += differences[draw].mean(axis=1) / len(seeds)
    interval = np.quantile(boot, [0.025, 0.975])
    effect = float(np.mean([values.mean() for values in differences_by_fit]))
    recorded = metrics["primary"]
    audit.check("primary_effect_independently_reconstructed", abs(effect - recorded["difference"]) <= 1e-12)
    audit.check("primary_interval_independently_reconstructed", bool(np.allclose(interval, recorded["conditional_95_percent_interval"], atol=1e-12, rtol=0)))
    recorded_fits = {record["seed"]: record for record in recorded["fits"]}
    audit.check("primary_fit_effects_and_eligible_world_counts_reconstructed", all(
        fit["worlds"] == recorded_fits[fit["seed"]]["worlds"] and
        abs(fit["difference"] - recorded_fits[fit["seed"]]["difference"]) <= 1e-12 for fit in reconstructed_fits))
    details["reconstructed_primary"] = {"main": main, "baseline": baseline, "condition": strata[ci],
        "difference_fraction": effect, "difference_percentage_points": 100 * effect,
        "conditional_95_percent_interval_fraction": interval.tolist(),
        "conditional_95_percent_interval_percentage_points": (100 * interval).tolist(),
        "bootstrap_resamples": resamples, "bootstrap_seed": config["evaluation"]["bootstrap_seed"],
        "fits": reconstructed_fits, "h1_supported": bool(interval[0] > 0)}

    checkpoints = metrics["checkpoints"]
    audit.check("three_final_checkpoints_present", len(checkpoints) == len(set(checkpoints)) == 3 and
                set(checkpoints) == {f"checkpoint-seed-{seed}.pt" for seed in seeds})
    checkpoint_details = []
    for seed in seeds:
        name = f"checkpoint-seed-{seed}.pt"
        path = inside(run, name)
        audit.check(f"checkpoint_nonempty:{seed}", path.is_file() and path.stat().st_size > 0)
        checkpoint = torch.load(path, map_location="cpu", weights_only=True)
        audit.check(f"checkpoint_metadata:{seed}", checkpoint["seed"] == seed and checkpoint["config"] == config
                    and checkpoint["selection_rule"] == "last configured step, no test selection")
        groups = {}
        for group, report_prefix, expected_count in [("model", "shared", 25623), ("merger", "merger", 6232), ("deepsets", "deepsets", 6320)]:
            tensors = list(checkpoint[group].values())
            audit.check(f"checkpoint_float32_tensors:{seed}:{group}", bool(tensors) and all(isinstance(value, torch.Tensor) and value.dtype == torch.float32 for value in tensors))
            tensor_count = sum(value.numel() for value in tensors)
            tensor_bytes = sum(value.numel() * value.element_size() for value in tensors)
            audit.check(f"checkpoint_parameter_payload:{seed}:{group}", tensor_count == expected_count == run_by_seed[seed][report_prefix + "_parameter_count"]
                        and tensor_bytes == run_by_seed[seed][report_prefix + "_parameter_bytes"])
            groups[group] = {"tensor_elements": tensor_count, "tensor_payload_bytes": tensor_bytes, "dtype": "float32"}
        audit.check(f"registered_state_size:{seed}", run_by_seed[seed]["state_float_count"] == 288 and run_by_seed[seed]["state_bytes"] == 1152)
        checkpoint_details.append({"seed": seed, "file": name, "file_bytes": path.stat().st_size, "sha256": digest(path), "groups": groups})
        del checkpoint
    details["checkpoints"] = checkpoint_details

    trace = json.loads((run / "training-trace.json").read_text())
    for seed in seeds:
        for phase, final_step in [("shared", 1500), ("learned", 1000), ("deepsets", 1000)]:
            entries = [entry for entry in trace if entry["seed"] == seed and entry["phase"] == phase]
            audit.check(f"scheduled_final_logged_step:{seed}:{phase}", [entry["step"] for entry in entries] == list(range(100, final_step + 1, 100))
                        and all(math.isfinite(entry["loss"]) and math.isfinite(entry["seconds"]) for entry in entries))
    audit.report["warnings"].append({"kind": "preregistered_reporting_omission",
        "detail": "Generator rejection/resampling attempt counts were not recorded by the frozen core. They cannot be reconstructed from saved predictions. This is disclosed without a new run or tuning."})
    details["versions"] = {"python": sys.version.split()[0], "numpy": np.__version__, "torch": torch.__version__}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=ROOT / "results/pilot")
    parser.add_argument("--out", type=Path, default=ROOT / "results/audit.json")
    args = parser.parse_args()
    run, out = args.run.resolve(), args.out.resolve()
    run.relative_to(ROOT)
    out.relative_to(ROOT)
    if out.exists():
        raise SystemExit("Refusing to overwrite an existing independent audit.")
    for name in ("metrics.json", "predictions.csv.gz", "artifact_hashes.json"):
        if not (run / name).is_file():
            raise SystemExit(f"Completed run evidence is not ready: {name}; no audit executed.")
    audit = Audit()
    try:
        perform(audit, run)
        audit.report["status"] = "passed_with_reporting_omission" if audit.report["warnings"] else "passed"
    except Exception as error:
        audit.report["status"] = "failed"
        audit.report["error"] = {"type": type(error).__name__, "message": str(error)}
    audit.report["all_recorded_assertions_passed"] = all(check["passed"] for check in audit.report["checks"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit.report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"audit": str(out.relative_to(ROOT)), "status": audit.report["status"],
                      "checks": len(audit.report["checks"]),
                      "primary": audit.report["details"].get("reconstructed_primary"),
                      "warnings": audit.report["warnings"]}, allow_nan=False))
    if audit.report["status"] == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
