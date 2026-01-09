# traceable-ai-observability

[![CI](https://github.com/rafaellimatecnologia-cloud/traceable-ai-observability/actions/workflows/ci.yml/badge.svg)](https://github.com/rafaellimatecnologia-cloud/traceable-ai-observability/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Ruff](https://img.shields.io/badge/ruff-enabled-000000)
![Tests](https://img.shields.io/badge/tests-pytest-blue)
 codex/create-traceable-ai-observability-repository
![Typecheck](https://img.shields.io/badge/typecheck-pyright-blueviolet)
![Coverage](https://img.shields.io/badge/coverage-xml%2Bhtml-informational)

**Portfolio Note (Safe-to-Publish):** This repository is a clean-room sample intended for public review.

Minimal, deterministic observability primitives for AI/service pipelines: structured logs, metrics
snapshots, and trace correlation with offline-friendly exports.

## Demo (3 seconds)

![Demo CLI](docs/assets/demo.gif)

> `demo.gif` will be uploaded manually outside this PR. This placeholder keeps the README stable.

## Why this matters

- Deterministic traces make post-incident reviews reproducible.
- Structured logs simplify downstream search and parsing.
- Metrics snapshots create compact, portable audit evidence.
 main

## Architecture

```mermaid
flowchart LR
  Producer --> TraceContext
  TraceContext --> StructuredLog
  TraceContext --> Metrics
  StructuredLog --> Export
  Metrics --> Export
  Export --> Viewer
  Export --> CLI
```


## Guarantees (Invariants)

- Deterministic identifiers when seeded.
- Stable JSON log schema for parsing and audits.
- Replayable snapshots with JSONL exports.
- No network calls in demos or tests.
- UTF-8 (no BOM) and LF line ending hygiene.
## What this demonstrates

- Determinism with seed-based correlation identifiers.
- Trace/span propagation across structured logs.
- Metrics aggregation with latency percentiles.
- Snapshot exports for offline review.
- Minimal primitives that are easy to test.

## Use cases

- Auditing model decisions in regulated environments.
- Reproducing pipeline behavior during incidents.
- Sharing trace snapshots with offline stakeholders.
 main

## Quickstart

### macOS/Linux

```bash
python -m pip install -e .
python -m pip install pytest ruff pyright
python examples/demo_cli.py
pytest -q
```

### Windows (PowerShell)

```powershell
python -m pip install -e .
python -m pip install pytest ruff pyright
python examples/demo_cli.py
pytest -q
```

## Development

```bash
python -m pip install -e ".[dev]"
python tools/report_hidden_unicode.py
python tools/sanitize_unicode.py
ruff check .
ruff format --check .
pyright
pytest -q
```

## License

MIT License. See [LICENSE](https://github.com/rafaellimatecnologia-cloud/local-first-ai-service/blob/main/LICENSE).
