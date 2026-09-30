from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class InvariantSetController:
    """A small control-theoretic abstraction for invariant enforcement.

    This module does not claim to prove safety for arbitrary cyber-physical systems. It only
    enforces a scalar invariant in a simplified, executable setting.
    """

    invariant_value: float = 0.0
    tolerance: float = 0.05
    max_control_input: float = 1.0

    def check_invariant(self, observed_value: float) -> bool:
        return abs(observed_value - self.invariant_value) <= self.tolerance

    def compute_safe_control(self, observed_value: float) -> float:
        error = self.invariant_value - observed_value
        bounded_error = max(-self.max_control_input, min(self.max_control_input, error))
        return bounded_error


__all__ = ["InvariantSetController"]
