# traceable-ai-observability

A minimal, production-minded tracing and audit logging toolkit for decision pipelines.
It focuses on stable event schemas, deterministic replays, and portable export bundles.

## Features

- **Event schema**: `AuditEvent` dataclass with canonical JSON serialization.
- **Trace context**: `TraceContext` helper for consistent trace/decision identifiers.
- **Replay**: re-run deterministic pipelines and compare outputs.
- **Export bundle**: JSONL events plus a manifest with hashes.
- **Examples**: `examples/demo_pipeline.py` shows end-to-end usage.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Quickstart

```python
from traceable_ai_observability import TraceContext, replay_pipeline, write_bundle

context = TraceContext.new(subsystem="api", metadata={"owner": "team"})
route = ["double", "increment"]
input_value = 5


def pipeline(value: int, steps: list[str]) -> int:
    for step in steps:
        if step == "double":
            value *= 2
        elif step == "increment":
            value += 1
    return value

output_value = pipeline(input_value, route)

events = [
    context.event(event_type="start", payload={"input": input_value, "route": route}),
    context.event(event_type="output", payload={"output": output_value}),
]

write_bundle(events, "bundle")
report = replay_pipeline(
    pipeline,
    input_data=input_value,
    captured_route=route,
    expected_output=output_value,
)
print("Replay match:", report.match)
```

Run the demo:

```bash
python examples/demo_pipeline.py
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## License

MIT
