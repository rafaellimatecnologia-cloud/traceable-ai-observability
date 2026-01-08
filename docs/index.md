# Traceable AI Observability

A minimal, production-minded observability toolkit for traceable AI/service pipelines.
It focuses on deterministic traces, structured logs, and portable snapshots that remain
offline-friendly.

## Guarantees

- Deterministic identifiers when seeded.
- Structured JSON logging for reliable parsing.
- Snapshot exports that can be archived and replayed offline.

## Quickstart

```bash
python -m pip install -e .
python examples/demo_cli.py
```

## Docs

- [README](../README.md)
- [Security](../SECURITY.md)
- [Contributing](../CONTRIBUTING.md)
