"""Reconstruct follow-up accuracy from saved corpora and predictions, without PyTorch."""
import argparse
from collections import Counter
import gzip
import json
from math import isclose
from pathlib import Path
from statistics import mean
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.run_io import digest


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def answers(parties, queries, unknown):
    table = {(s, r): o for party in parties for s, r, o, _ in party}
    output = []
    for s, r1, r2 in queries:
        intermediate = table.get((s, r1), unknown)
        target = intermediate if r2 == -1 else table.get((intermediate, r2), unknown)
        output.append((target, intermediate))
    return output


def reconstruct(corpus, predictions, unknown, result):
    require(len(corpus) == len(predictions), "Prediction world count differs from corpus")
    world_macro, overall, abstentions = [], [], []
    eligible_queries = 0
    for world, values in zip(corpus, predictions):
        eligible = []
        require(len(world["queries"]) == len(values), "Prediction query count differs from corpus")
        require(all(isinstance(value, int) and 0 <= value <= unknown for value in values),
                "Prediction out of range")
        for query, target, value in zip(world["queries"], world["targets"], values):
            overall.append(target == value)
            if target == unknown:
                abstentions.append(target == value)
            elif query[2] >= 0:
                eligible.append(target == value)
        if eligible:
            world_macro.append(mean(eligible))
            eligible_queries += len(eligible)
    for key, got in {
        "worlds": len(corpus), "queries": len(overall),
        "known_two_hop_worlds": len(world_macro), "known_two_hop_queries": eligible_queries,
        "unknown_queries": len(abstentions),
        "known_two_hop_world_macro_accuracy": mean(world_macro) if world_macro else None,
        "all_query_accuracy": mean(overall),
        "unknown_recall": mean(abstentions) if abstentions else None,
    }.items():
        want = result[key]
        match = want is None if got is None else want is not None and isclose(got, want, abs_tol=1e-12)
        require(match, f"Mismatched {key}: expected {want}, reconstructed {got}")


def audit(directory, require_checkpoints=False):
    config = read_json(directory / "config.json")
    summary = read_json(directory / "results.json")
    inputs = read_json(directory / "inputs.json")
    require(digest(directory / "config.json") == inputs["config_sha256"], "Config hash differs")
    for name, expected in inputs["input_hashes"].items():
        require(digest(ROOT / name) == expected, f"Input hash differs: {name}")
    manifest = read_json(directory / "artifact_hashes.json")
    require({"config.json", "inputs.json", "results.json", "evidence.jsonl.gz"} <= manifest.keys(),
            "Required evidence is uncovered by hashes")
    missing_weights = []
    for name, expected in manifest.items():
        path = directory / name
        if path.suffix == ".pt" and not path.exists() and not require_checkpoints:
            missing_weights.append(name)
        else:
            require(digest(path) == expected, f"Artifact hash differs: {name}")

    corpora, prediction_rows, counts = {}, [], Counter()
    with gzip.open(directory / "evidence.jsonl.gz", "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            section = row["section"]
            counts[section] += 1
            if section.endswith("_world"):
                key = (section, row.get("relations"), row.get("overlap"))
                corpus = corpora.setdefault(key, [])
                require(row["id"] == len(corpus), "Out-of-order or duplicate world ID")
                corpus.append(row)
            else:
                prediction_rows.append(row)

    for (section, _, _), corpus in corpora.items():
        for world in corpus:
            if section == "continuation_world":
                for variant, target in zip(world["variants"], world["targets"]):
                    private = answers([variant], [world["query"]], 6)[0][0]
                    combined = answers([variant, [world["bridge"]]], [world["query"]], 6)[0][0]
                    require(private == 6 and combined == target, "Invalid continuation labels")
                require(len(set(world["targets"])) == 2, "Counterfactual labels must differ")
            else:
                n = 6 if section == "three_party_world" else config["capacity"]["n_entities"]
                targets, intermediates = zip(*answers(world["parties"], world["queries"], n))
                require(list(targets) == world["targets"] and list(intermediates) == world["intermediates"],
                        "Saved label differs from independent union lookup")

    capacity = {(r["relations"], r["state_bytes"], r["seed"]): r for r in summary["capacity"]}
    continuation = corpora["continuation_world", None, None]
    paths, pairs = set(), Counter()
    correct = Counter()
    collisions = Counter()
    reconstructed = 0
    for row in prediction_rows:
        section = row["section"]
        if section == "capacity_predictions":
            key = row["relations"], row["bytes"], row["seed"]
            corpus = corpora["capacity_world", row["relations"], row["overlap"]]
            result = capacity[key]["scores"][str(row["overlap"])]
            predictions = row["predictions_in_world_id_order"]
            require(result.keys() == predictions.keys(), "Capacity method coverage differs")
            for method, values in predictions.items():
                reconstruct(corpus, values, config["capacity"]["n_entities"], result[method])
            reconstructed += len(predictions)
            identity = section, key, row["overlap"]
        elif section == "three_party_predictions":
            corpus = corpora["three_party_world", None, row["overlap"]]
            key = f'{row["seed"]}/{row["method"]}'
            result = summary["three_party"][str(row["overlap"])]["methods"][key][row["variant"]]
            reconstruct(corpus, row["predictions_in_world_id_order"], 6, result)
            reconstructed += 1
            identity = section, key, row["overlap"], row["variant"]
        else:
            require(section == "continuation_predictions", f"Unexpected section: {section}")
            key = f'{row["seed"]}/{row["pool"]}'
            world = continuation[row["id"]]
            for name, values in row["predictions"].items():
                targets = [6, 6] if name == "native_local" else world["targets"]
                require(len(values) == 2, "Expected two continuation predictions")
                correct[key, name] += sum(a == b for a, b in zip(values, targets))
            pairs[key] += 1
            collisions[key] += row["exact_collision"]
            require(row["exact_collision"] == (row["relative_l2"] == 0.0),
                    "Exact collision flag disagrees with recorded distance")
            identity = section, key, row["id"]
        require(identity not in paths, f"Duplicate prediction {identity}")
        paths.add(identity)

    for key, result in summary["continuation"].items():
        require(pairs[key] == result["pairs"] == len(continuation), "Missing continuation pairs")
        require(collisions[key] == result["exact_collision_pairs"], "Collision count differs")
        for metric, value in result["accuracy"].items():
            require(isclose(correct[key, metric] / (2 * pairs[key]), value, abs_tol=1e-12),
                    f"Continuation accuracy differs: {key}/{metric}")
            reconstructed += 1
    expected = (sum(len(r["accuracy"]) for r in summary["continuation"].values())
                + sum(len(variants) for row in summary["three_party"].values()
                      for variants in row["methods"].values())
                + sum(len(methods) for row in summary["capacity"] for methods in row["scores"].values()))
    require(reconstructed == expected, "Missing reported method/condition cells")
    return {"status": "passed", "rows_by_section": dict(counts), "score_cells_reconstructed": reconstructed,
            "missing_checkpoint_artifacts": missing_weights,
            "scope": "Saved labels, accuracy, collision counts and hashes; no model re-execution."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--require-checkpoints", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.directory, args.require_checkpoints), indent=2))


if __name__ == "__main__":
    main()
