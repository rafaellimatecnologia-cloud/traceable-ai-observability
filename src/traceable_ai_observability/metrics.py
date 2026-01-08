"""Metrics aggregation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(round((percentile / 100) * (len(ordered) - 1)))
    return ordered[index]


@dataclass
class MetricsAggregator:
    """Aggregate latency metrics and counters."""

    latencies: dict[str, list[float]] = field(default_factory=dict)
    counters: dict[str, int] = field(default_factory=dict)

    def record_latency(self, name: str, value_ms: float) -> None:
        self.latencies.setdefault(name, []).append(value_ms)

    def increment(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount

    def snapshot(self) -> dict[str, Any]:
        latency_snapshot: dict[str, dict[str, float]] = {}
        for name, values in self.latencies.items():
            latency_snapshot[name] = {
                "count": float(len(values)),
                "p50_ms": _percentile(values, 50),
                "p95_ms": _percentile(values, 95),
                "min_ms": min(values),
                "max_ms": max(values),
            }
        return {
            "latencies": latency_snapshot,
            "counters": dict(self.counters),
        }
