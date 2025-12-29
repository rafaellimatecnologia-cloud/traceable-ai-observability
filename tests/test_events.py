from __future__ import annotations

from datetime import UTC, datetime

from traceable_ai_observability.events import AuditEvent


def test_canonical_json_stability() -> None:
    timestamp = datetime(2024, 1, 1, tzinfo=UTC)
    event = AuditEvent.create(
        trace_id="trace",
        decision_id="decision",
        subsystem="unit",
        event_type="created",
        payload={"b": 2, "a": 1},
        timestamp=timestamp,
    )
    json_one = event.to_json()
    json_two = event.to_json()
    assert json_one == json_two
    assert json_one.index("\"a\"") < json_one.index("\"b\"")
