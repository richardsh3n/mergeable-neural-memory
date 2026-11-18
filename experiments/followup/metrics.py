"""Common world-macro scoring, state validation, and finite algebra probes."""
from itertools import permutations

import numpy as np
import torch


def repeat_state(state, batch):
    return state.repeat_interleave(batch["queries_per_world"], dim=0)


def predict(model, state, batch):
    logits = model.read(repeat_state(state, batch), batch["queries"])
    if not bool(torch.isfinite(logits).all()):
        raise ValueError("Nonfinite readout logits")
    return logits.argmax(-1).reshape(len(state), -1)


def verify_payload(state, model):
    if (state.ndim != 3 or state.shape[1:] != (model.n_slots, model.state_dim)
            or state.dtype != torch.float32 or state.device.type != "cpu"
            or state[0].numel() * state.element_size() != model.state_bytes
            or not bool(torch.isfinite(state).all())):
        raise ValueError("Expected finite CPU float32 states with the configured payload")


def score(predictions, batch, unknown):
    n_queries = batch["queries_per_world"]
    targets = batch["targets"].reshape(-1, n_queries)
    hop2 = batch["queries"][:, 2].reshape(-1, n_queries) >= 0
    eligible = (targets != unknown) & hop2
    eligible_count = eligible.sum(1)
    correct = predictions == targets
    has_known = eligible_count > 0
    missing = targets == unknown
    return {
        "worlds": len(targets), "queries": targets.numel(),
        "known_two_hop_worlds": int(has_known.sum()),
        "known_two_hop_queries": int(eligible_count.sum()),
        "unknown_queries": int(missing.sum()),
        "known_two_hop_world_macro_accuracy": (
            float(((correct & eligible).sum(1)[has_known].double() / eligible_count[has_known]).mean())
            if bool(has_known.any()) else None
        ),
        "all_query_accuracy": float(correct.double().mean()),
        "unknown_recall": float(correct[missing].double().mean()) if bool(missing.any()) else None,
    }


def relative_l2(state, reference):
    delta = (state - reference).flatten(1).double().norm(dim=1)
    base = reference.flatten(1).double().norm(dim=1)
    return delta / base.clamp_min(1e-6)


def state_comparison(state, reference):
    same = (state == reference).flatten(1).all(dim=1)
    distances = relative_l2(state, reference)
    return {"exact_worlds": int(same.sum()), "mean_relative_l2": float(distances.mean()),
            "max_relative_l2": float(distances.max())}


def ordered_trees(merge, states):
    for i, j, k in permutations(range(3)):
        a, b, c = states[i], states[j], states[k]
        x, y, z = ("ABC"[index] for index in (i, j, k))
        yield f"({x}{y}){z}", merge(merge(a, b), c)
        yield f"{x}({y}{z})", merge(a, merge(b, c))


def ridge_predict(train, labels, test, classes, penalty):
    """Fit a ridge classifier with an unpenalized intercept."""
    x = np.asarray(train, dtype=np.float64)
    y = np.eye(classes, dtype=np.float64)[labels]
    center, average = x.mean(axis=0), y.mean(axis=0)
    x = x - center
    scale = max(float(np.sqrt(np.mean(x ** 2))), 1e-12)
    x = x / scale
    gram = x @ x.T
    gram.flat[::len(x) + 1] += penalty
    coefficients = x.T @ np.linalg.solve(gram, y - average)
    return (((test - center) / scale) @ coefficients + average).argmax(axis=1)
