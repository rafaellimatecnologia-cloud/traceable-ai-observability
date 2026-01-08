"""Trace context primitives."""

from __future__ import annotations

import random
from dataclasses import dataclass


def _generate_id(rng: random.Random, length: int = 16) -> str:
    alphabet = "0123456789abcdef"
    return "".join(rng.choice(alphabet) for _ in range(length))


@dataclass(frozen=True)
class TraceContext:
    """Context for correlating logs, metrics, and snapshots."""

    trace_id: str
    span_id: str
    parent_id: str | None = None

    @classmethod
    def new(cls) -> TraceContext:
        rng = random.Random()
        return cls(
            trace_id=_generate_id(rng),
            span_id=_generate_id(rng),
            parent_id=None,
        )

    @classmethod
    def from_seed(cls, seed: int, parent_id: str | None = None) -> TraceContext:
        rng = random.Random(seed)
        return cls(
            trace_id=_generate_id(rng),
            span_id=_generate_id(rng),
            parent_id=parent_id,
        )
