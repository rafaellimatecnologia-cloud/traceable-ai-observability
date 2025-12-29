from __future__ import annotations

from traceable_ai_observability.replay import replay_pipeline


def demo_pipeline(input_value: int, route: list[str]) -> int:
    value = input_value
    for step in route:
        if step == "double":
            value *= 2
        elif step == "increment":
            value += 1
        else:
            raise ValueError(f"Unknown step: {step}")
    return value


def test_replay_success() -> None:
    route = ["double", "increment"]
    output = demo_pipeline(4, route)
    report = replay_pipeline(
        demo_pipeline,
        input_data=4,
        captured_route=route,
        expected_output=output,
    )
    assert report.match is True


def test_replay_failure() -> None:
    route = ["double", "increment"]
    report = replay_pipeline(
        demo_pipeline,
        input_data=4,
        captured_route=route,
        expected_output=999,
    )
    assert report.match is False


def test_determinism() -> None:
    route = ["double", "increment", "double"]
    output_one = demo_pipeline(3, route)
    output_two = demo_pipeline(3, route)
    assert output_one == output_two
