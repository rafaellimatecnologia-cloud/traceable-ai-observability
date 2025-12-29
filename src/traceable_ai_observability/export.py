"""Export bundles for audit events."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from .events import AuditEvent


@dataclass(frozen=True)
class BundleManifest:
    """Metadata for an export bundle."""

    created_at: str
    event_count: int
    files: dict[str, str]

    def to_json(self) -> str:
        return json.dumps(
            {
                "created_at": self.created_at,
                "event_count": self.event_count,
                "files": self.files,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_bundle(
    events: Iterable[AuditEvent],
    output_dir: str | Path,
) -> BundleManifest:
    """Write JSONL events and a manifest with hashes."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    events_path = output_path / "events.jsonl"
    with events_path.open("w", encoding="utf-8") as handle:
        event_count = 0
        for event in events:
            handle.write(event.to_json())
            handle.write("\n")
            event_count += 1

    files = {
        "events.jsonl": _file_sha256(events_path),
    }
    manifest = BundleManifest(
        created_at=datetime.now(UTC).isoformat(),
        event_count=event_count,
        files=files,
    )
    manifest_path = output_path / "manifest.json"
    manifest_path.write_text(manifest.to_json(), encoding="utf-8")
    return manifest
