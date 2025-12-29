"""Event schema and canonical serialization utilities."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    """Represents a single audit event in a trace."""

    trace_id: str
    decision_id: str
    timestamp: str
    subsystem: str
    event_type: str
    payload: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        trace_id: str,
        decision_id: str,
        subsystem: str,
        event_type: str,
        payload: Mapping[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> AuditEvent:
        """Create an event with a UTC timestamp."""
        event_time = timestamp or datetime.now(UTC)
        return cls(
            trace_id=trace_id,
            decision_id=decision_id,
            timestamp=event_time.isoformat(),
            subsystem=subsystem,
            event_type=event_type,
            payload=payload or {},
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        return {
            "trace_id": self.trace_id,
            "decision_id": self.decision_id,
            "timestamp": self.timestamp,
            "subsystem": self.subsystem,
            "event_type": self.event_type,
            "payload": self.payload,
        }

    def to_json(self) -> str:
        """Return a canonical JSON string with sorted keys."""
        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
