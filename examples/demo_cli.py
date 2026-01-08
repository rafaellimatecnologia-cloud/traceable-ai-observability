"""Deterministic demo CLI for traceable observability."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from traceable_ai_observability import (
    MetricsAggregator,
    SnapshotExporter,
    StructuredLogger,
    TraceContext,
)


def main() -> None:
    context = TraceContext.from_seed(7)
    logger = StructuredLogger()
    metrics = MetricsAggregator()

    fixed_time = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    logger.log(
        context=context,
        level="info",
        message="request.received",
        fields={"route": "/demo", "user": "portfolio"},
        timestamp=fixed_time,
    )
    logger.log(
        context=context,
        level="info",
        message="decision.complete",
        fields={"decision": "allow", "score": 0.98},
        timestamp=fixed_time,
    )

    metrics.record_latency("decision_ms", 12.0)
    metrics.record_latency("decision_ms", 18.0)
    metrics.record_latency("decision_ms", 15.0)
    metrics.increment("decisions_total", 1)

    snapshot = SnapshotExporter()
    output_path = snapshot.write_jsonl(
        context=context,
        logs=logger.entries,
        metrics=metrics.snapshot(),
        output_path=Path("out/trace.jsonl"),
    )

    print(f"trace_id={context.trace_id} span_id={context.span_id}")
    print("structured_logs=")
    for line in logger.to_json_lines():
        print(line)
    print("metrics_snapshot=")
    print(metrics.snapshot())
    print(f"exported trace snapshot: {output_path}")


if __name__ == "__main__":
    main()
