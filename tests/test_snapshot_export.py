from __future__ import annotations

from pathlib import Path

from traceable_ai_observability import (
    MetricsAggregator,
    SnapshotExporter,
    StructuredLogger,
    TraceContext,
)


def test_snapshot_export_creates_file(tmp_path: Path) -> None:
    context = TraceContext.from_seed(9)
    logger = StructuredLogger()
    metrics = MetricsAggregator()
    logger.log(
        context=context,
        level="info",
        message="export",
        fields={"ok": True},
    )
    metrics.record_latency("decision_ms", 10.0)
    exporter = SnapshotExporter()
    output_path = tmp_path / "trace.jsonl"
    result = exporter.write_jsonl(
        context=context,
        logs=logger.entries,
        metrics=metrics.snapshot(),
        output_path=output_path,
    )
    assert result.exists()
