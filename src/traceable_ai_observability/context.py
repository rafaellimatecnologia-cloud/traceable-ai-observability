"""Trace context helpers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from .events import AuditEvent


@dataclass(frozen=True)
class TraceContext:
    """Generate trace identifiers and consistent metadata."""

    trace_id: str
    decision_id: str
    subsystem: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def new(
        cls,
        *,
        subsystem: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> TraceContext:
        """Create a new trace context with fresh identifiers."""
        return cls(
            trace_id=uuid4().hex,
            decision_id=uuid4().hex,
            subsystem=subsystem,
            metadata=metadata or {},
        )

    def event(
        self,
        *,
        event_type: str,
        payload: Mapping[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> AuditEvent:
        """Create an audit event within the trace context."""
        combined_payload: dict[str, Any] = {**self.metadata}
        if payload:
            combined_payload.update(payload)
        event_time = timestamp or datetime.now(UTC)
        return AuditEvent(
            trace_id=self.trace_id,
            decision_id=self.decision_id,
            timestamp=event_time.isoformat(),
            subsystem=self.subsystem,
            event_type=event_type,
            payload=combined_payload,
        )
