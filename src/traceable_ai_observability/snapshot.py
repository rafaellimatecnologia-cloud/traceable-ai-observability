"""Snapshot export utilities."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .context import TraceContext


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


class SnapshotExporter:
    """Write trace snapshots to JSONL files."""

    def write_jsonl(
        self,
        *,
        context: TraceContext,
        logs: list[dict[str, Any]],
        metrics: Mapping[str, Any],
        output_path: str | Path,
    ) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            _canonical_json(
                {
                    "type": "trace_context",
                    "trace_id": context.trace_id,
                    "span_id": context.span_id,
                    "parent_id": context.parent_id,
                }
            )
        ]
        lines.extend(
            _canonical_json({"type": "log", "payload": entry}) for entry in logs
        )
        lines.append(_canonical_json({"type": "metrics", "payload": metrics}))
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        return path
