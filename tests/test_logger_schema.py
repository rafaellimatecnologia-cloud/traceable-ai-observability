from __future__ import annotations

from datetime import datetime, timezone

from traceable_ai_observability.context import TraceContext
from traceable_ai_observability.logger import StructuredLogger


def test_log_schema_fields_present() -> None:
    context = TraceContext.from_seed(1)
    logger = StructuredLogger()
    entry = logger.log(
        context=context,
        level="info",
        message="schema.check",
        fields={"key": "value"},
        timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    for field in [
        "timestamp",
        "level",
        "message",
        "trace_id",
        "span_id",
        "parent_id",
        "fields",
    ]:
        assert field in entry
