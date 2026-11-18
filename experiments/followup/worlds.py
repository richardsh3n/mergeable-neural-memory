"""Synthetic worlds for the two follow-up tasks. Oracles stay outside inference."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import numpy as np
import torch

from src.merge_memory import pad_facts, possible_answers, reference_answer

Fact = tuple[int, int, int, int]
Key = tuple[int, int]
Query = tuple[int, int, int]


@dataclass
class World:
    parties: list[list[Fact]]
    queries: list[Query]
    targets: list[int]
    intermediates: list[int]
    paths: list[tuple[Key, ...]]

    @property
    def union(self) -> list[Fact]:
        return sorted({fact for party in self.parties for fact in party})


def key_for(index: int, relations: int) -> Key:
    return divmod(int(index), relations)


def draw_world(rng, n: int, relations: int, overlap: float, attempts: Counter,
               party_count: int = 2) -> World:
    """Draw a shared-evidence query block with audited private ambiguity."""
    for _ in range(1000):
        objects = rng.integers(n, size=(n, relations))
        keys = [key_for(i, relations) for i in range(n * relations)]
        if party_count == 2:
            groups = np.empty(relations, dtype=int)
            groups[rng.permutation(relations)] = np.arange(relations) % 2
            one_keys = [keys[i] for i in rng.choice(len(keys), 2, replace=False)]
            two_keys = [keys[i] for i in rng.choice(len(keys), 2, replace=False)]
            pairs = None
        else:
            groups = np.arange(relations)
            one_keys = []
            two_keys = [keys[i] for i in rng.choice(len(keys), 3, replace=False)]
            pairs = [(0, 1), (1, 2), (2, 0)]
        queries = [(s, r, -1) for s, r in one_keys]
        queries += [(s, r, int(rng.choice(np.flatnonzero(groups != groups[r]))))
                    for s, r in two_keys]
        paths = [((s, r),) if r2 < 0 else ((s, r), (int(objects[s, r]), r2))
                 for s, r, r2 in queries]
        critical_paths = paths[len(one_keys):]
        critical = {key for path in critical_paths for key in path}
        if pairs is not None and len(critical) != 6:
            attempts["shared_critical_key"] += 1
            continue

        if pairs is None:
            missing = {path[int(rng.integers(len(path)))] for path in paths if rng.random() < 0.20}
            owners = {key: (int(groups[key[1]]),) for key in critical}
        else:
            missing = set()
            owners = {key: (owner,) for path, pair in zip(critical_paths, pairs)
                      for key, owner in zip(path, pair)}
        required = {key for path in paths for key in path}
        parties: list[list[Fact]] = [[] for _ in range(party_count)]
        for key in keys:
            if key in missing or (key not in required and rng.random() > 0.85):
                continue
            s, r = key
            fact = (s, r, int(objects[s, r]), 0)
            if key in owners:
                destinations = owners[key]
            else:
                count = 2 if rng.random() < overlap else 1
                destinations = rng.choice(party_count, count, replace=False)
            for owner in destinations:
                parties[owner].append(fact)

        without_party = [sorted({fact for i, party in enumerate(parties) if i != excluded
                                 for fact in party}) for excluded in range(party_count)]
        union = sorted(set().union(*map(set, parties)))
        answers = [reference_answer(union, query, n) for query in queries]
        audited_pairs = [(0, 1)] * len(critical_paths) if pairs is None else pairs
        offset = len(one_keys)
        for query, (target, _), pair in zip(queries[offset:], answers[offset:], audited_pairs):
            if target != n and any(len(possible_answers(without_party[p], query, n)) < 2 for p in pair):
                attempts["private_answer_determined"] += 1
                break
        else:
            attempts["accepted"] += 1
            for party in parties:
                rng.shuffle(party)
            targets, intermediates = zip(*answers)
            return World(parties, queries, list(targets), list(intermediates), paths)
    raise RuntimeError(f"Unable to sample a valid world in 1000 attempts: {dict(attempts)}")


def collate_facts(rows: list[list[Fact]]):
    # A positive padded axis also supports a batch of wholly empty histories.
    return pad_facts(rows, max(1, max(map(len, rows))))


def batch_worlds(worlds: list[World]) -> dict:
    """Encode each party once per world. Broadcast states across its queries."""
    parties = [collate_facts(list(rows)) for rows in zip(*(w.parties for w in worlds))]
    return {
        "parties": parties,
        "union": collate_facts([w.union for w in worlds]),
        "queries_per_world": len(worlds[0].queries),
        "queries": torch.tensor([q for w in worlds for q in w.queries]),
        "targets": torch.tensor([t for w in worlds for t in w.targets]),
        "intermediate_targets": torch.tensor([t for w in worlds for t in w.intermediates]),
    }
