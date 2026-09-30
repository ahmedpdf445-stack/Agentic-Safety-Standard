from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MetricSample:
    name: str
    value: float
    tags: dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Lightweight in-memory observability layer for policy and runtime events."""

    def __init__(self) -> None:
        self.samples: list[MetricSample] = []

    def record(self, name: str, value: float, **tags: str) -> MetricSample:
        sample = MetricSample(name=name, value=value, tags=dict(tags))
        self.samples.append(sample)
        return sample

    def get_value(self, name: str) -> float | None:
        for sample in reversed(self.samples):
            if sample.name == name:
                return sample.value
        return None


__all__ = ["MetricSample", "MetricsCollector"]
