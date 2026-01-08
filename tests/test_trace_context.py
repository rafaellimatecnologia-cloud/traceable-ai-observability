from __future__ import annotations

from traceable_ai_observability.context import TraceContext


def test_trace_id_deterministic_with_seed() -> None:
    first = TraceContext.from_seed(42)
    second = TraceContext.from_seed(42)
    assert first.trace_id == second.trace_id
    assert first.span_id == second.span_id
    assert first.parent_id == second.parent_id
