"""Structured logging utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .context import TraceContext


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


@dataclass
class StructuredLogger:
    """Collect structured log entries as JSON lines."""

    entries: list[dict[str, Any]] = field(default_factory=list)

    def log(
        self,
        *,
        context: TraceContext,
        level: str,
        message: str,
        fields: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> dict[str, Any]:
        event_time = timestamp or datetime.now(timezone.utc)
        payload = {
            "timestamp": event_time.isoformat(),
            "level": level,
            "message": message,
            "trace_id": context.trace_id,
            "span_id": context.span_id,
            "parent_id": context.parent_id,
            "fields": fields or {},
        }
        self.entries.append(payload)
        return payload

    def to_json_lines(self) -> list[str]:
        return [_canonical_json(entry) for entry in self.entries]
