"""Finite demonstrations of the exact set-union congruence criterion.

This is a mathematical check, not part of the neural model or its inference.
"""
from itertools import combinations


def powerset(universe):
    values = tuple(universe)
    return [frozenset(c) for n in range(len(values) + 1)
            for c in combinations(values, n)]


def exact_merge_table(encoder, universe):
    """Construct an exact union merger or give a collision witness.

    Encoder outputs must be hashable. A collision witness establishes that no
    deterministic merger can reproduce this encoder's union states for all sets.
    """
    sets = powerset(universe)
    table, witnesses = {}, {}
    for a in sets:
        for b in sets:
            pair, result = (encoder(a), encoder(b)), encoder(a | b)
            if pair in table and table[pair] != result:
                raise ValueError({"input_states": pair,
                                  "first": witnesses[pair],
                                  "second": (a, b, result)})
            table[pair], witnesses[pair] = result, (a, b, result)
    return table
