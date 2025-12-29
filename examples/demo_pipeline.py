"""Demo pipeline with tracing, replay, and export."""

from __future__ import annotations

from pathlib import Path

from traceable_ai_observability import TraceContext, replay_pipeline, write_bundle


def demo_pipeline(input_value: int, route: list[str]) -> int:
    """Deterministic pipeline that applies steps in order."""
    value = input_value
    for step in route:
        if step == "double":
            value *= 2
        elif step == "increment":
            value += 1
        else:
            raise ValueError(f"Unknown step: {step}")
    return value


def main() -> None:
    context = TraceContext.new(subsystem="demo", metadata={"owner": "example"})
    route = ["double", "increment"]
    input_value = 10

    events = [
        context.event(
            event_type="start",
            payload={"input": input_value, "route": route},
        ),
    ]

    output_value = demo_pipeline(input_value, route)
    events.append(context.event(event_type="output", payload={"output": output_value}))

    bundle_dir = Path("bundle")
    write_bundle(events, bundle_dir)

    report = replay_pipeline(
        demo_pipeline,
        input_data=input_value,
        captured_route=route,
        expected_output=output_value,
    )
    print("Replay match:", report.match)


if __name__ == "__main__":
    main()
