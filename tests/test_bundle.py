from __future__ import annotations

import json
from pathlib import Path

from traceable_ai_observability.context import TraceContext
from traceable_ai_observability.export import _file_sha256, write_bundle


def test_hash_changes_on_tamper(tmp_path: Path) -> None:
    context = TraceContext.new(subsystem="unit")
    events = [context.event(event_type="start", payload={"value": 1})]

    manifest = write_bundle(events, tmp_path)
    events_path = tmp_path / "events.jsonl"

    original_hash = manifest.files["events.jsonl"]
    assert original_hash == _file_sha256(events_path)

    events_path.write_text("tampered\n", encoding="utf-8")
    tampered_hash = _file_sha256(events_path)
    assert tampered_hash != original_hash

    manifest_path = tmp_path / "manifest.json"
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert loaded["files"]["events.jsonl"] == original_hash
