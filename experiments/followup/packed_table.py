"""Fixed-byte functional-table baseline for conflict-free, revision-zero worlds."""
from dataclasses import dataclass

from src.merge_memory import reference_answer


@dataclass(frozen=True)
class PackedTable:
    entities: int
    relations: int
    budget: int

    @property
    def width(self):
        return self.entities.bit_length()  # codes 0 (unknown) through entities

    @property
    def key_count(self):
        return min(self.entities * self.relations, 8 * self.budget // self.width)

    def _pack(self, values):
        integer = sum(value << (i * self.width) for i, value in enumerate(values))
        return integer.to_bytes(self.budget, "little")

    def _unpack(self, payload):
        if len(payload) != self.budget:
            raise ValueError("Invalid packed payload length")
        integer = int.from_bytes(payload, "little")
        mask = (1 << self.width) - 1
        return [(integer >> (i * self.width)) & mask for i in range(self.key_count)]

    def encode(self, facts):
        values = [0] * self.key_count
        for s, r, o, rev in facts:
            if rev != 0:
                raise ValueError("Packed baseline only supports revision zero")
            key = s * self.relations + r
            if key < self.key_count:
                if values[key] not in (0, o + 1):
                    raise ValueError("Contradictory functional evidence")
                values[key] = o + 1
        return self._pack(values)

    def merge(self, a, b):
        pairs = list(zip(self._unpack(a), self._unpack(b)))
        if any(x and y and x != y for x, y in pairs):
            raise ValueError("Contradictory functional evidence")
        return self._pack(max(x, y) for x, y in pairs)

    def read(self, payload, queries):
        facts = [(*divmod(i, self.relations), value - 1, 0)
                 for i, value in enumerate(self._unpack(payload)) if value > 0]
        return [reference_answer(facts, query, self.entities)[0] for query in queries]
