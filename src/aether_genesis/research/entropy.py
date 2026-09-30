from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EntropyInspiredMetric:
    """Engineering/system metric, intentionally not thermodynamic entropy."""

    policy_violation_risk: float = 0.0
    uncertainty: float = 0.0
    contradiction_score: float = 0.0
    resource_pressure: float = 0.0
    execution_risk: float = 0.0
    weights: dict[str, float] = field(
        default_factory=lambda: {
            "policy_violation_risk": 0.35,
            "uncertainty": 0.2,
            "contradiction_score": 0.15,
            "resource_pressure": 0.15,
            "execution_risk": 0.15,
        }
    )

    def score(self) -> float:
        total = 0.0
        for key, weight in self.weights.items():
            value = getattr(self, key)
            total += weight * value
        return total

    def __str__(self) -> str:
        return "entropy-inspired system metric"


__all__ = ["EntropyInspiredMetric"]
