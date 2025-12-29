"""Replay utilities for deterministic pipelines."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

Pipeline = Callable[[Any, Sequence[str]], Any]


@dataclass(frozen=True)
class ReplayReport:
    """Result of replaying a pipeline."""

    input_data: Any
    captured_route: Sequence[str]
    expected_output: Any
    actual_output: Any
    match: bool


def replay_pipeline(
    pipeline: Pipeline,
    *,
    input_data: Any,
    captured_route: Sequence[str],
    expected_output: Any,
) -> ReplayReport:
    """Re-run a pipeline deterministically and compare outputs."""
    route = list(captured_route)
    actual = pipeline(input_data, route)
    return ReplayReport(
        input_data=input_data,
        captured_route=route,
        expected_output=expected_output,
        actual_output=actual,
        match=actual == expected_output,
    )
