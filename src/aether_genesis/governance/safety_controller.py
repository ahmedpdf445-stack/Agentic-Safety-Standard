from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aether_genesis.core.state import Action, SystemState


@dataclass(slots=True)
class SafetyDecision:
    status: str
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)


class SafetyController:
    """Deterministic controller that decides allow/deny/pause/rollback etc."""

    def __init__(
        self,
        max_recursion_depth: int = 3,
        rate_limit_per_minute: int = 20,
        circuit_breaker_threshold: int = 5,
    ) -> None:
        self.max_recursion_depth = max_recursion_depth
        self.rate_limit_per_minute = rate_limit_per_minute
        self.circuit_breaker_threshold = circuit_breaker_threshold

    def decide(
        self,
        action: Action,
        policy_result: Any,
        state: SystemState,
    ) -> SafetyDecision:
        if not policy_result.allowed:
            return SafetyDecision("deny", policy_result.reason)

        if action.risk_level >= 0.8:
            return SafetyDecision("pause", "Risk exceeds safe operating threshold")

        if state.risk_state.policy_violations >= self.circuit_breaker_threshold:
            return SafetyDecision("safe_mode", "Circuit breaker triggered by policy violations")

        if action.parameters.get("depth", 0) > self.max_recursion_depth:
            return SafetyDecision("terminate", "Maximum delegation depth exceeded")

        if action.action_type.value == "execute" and state.resource_state.time_used > 300:
            return SafetyDecision("terminate", "Execution time exceeded budget")

        if policy_result.requires_approval:
            return SafetyDecision("require_human_approval", policy_result.reason)

        return SafetyDecision("allow", "Governance and safety checks passed")

    def apply(self, decision: SafetyDecision, action: Action) -> SafetyDecision:
        if decision.status == "allow":
            return SafetyDecision("allow", f"Action {action.action_id} approved")
        if decision.status == "pause":
            return SafetyDecision("pause", f"Action {action.action_id} paused pending review")
        if decision.status == "deny":
            return SafetyDecision("deny", f"Action {action.action_id} denied")
        return decision


__all__ = ["SafetyController", "SafetyDecision"]
