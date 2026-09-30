from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aether_genesis.core.exceptions import PolicyViolationError
from aether_genesis.core.state import Action, SystemState


@dataclass(slots=True)
class PolicyDecision:
    allowed: bool
    reason: str = ""
    requires_approval: bool = False
    decision: str = "allow"
    metadata: dict[str, Any] = field(default_factory=dict)


class PolicyEngine:
    """Independent governance decision engine.

    The LLM may propose actions, but the policy engine decides whether the action is structurally
    legal under the defined governance model.
    """

    def __init__(
        self,
        allowed_tools: set[str] | None = None,
        allowed_capabilities: set[str] | None = None,
        max_time_seconds: float = 300.0,
        max_token_budget: int = 50000,
        max_risk_level: float = 0.75,
        allow_network: bool = False,
    ) -> None:
        self.allowed_tools = allowed_tools or {"read_file", "write_file", "search", "summarize"}
        self.allowed_capabilities = allowed_capabilities or {
            "read_file",
            "write_file",
            "search",
            "summarize",
            "network:deny",
            "filesystem:read",
            "filesystem:write",
        }
        self.max_time_seconds = max_time_seconds
        self.max_token_budget = max_token_budget
        self.max_risk_level = max_risk_level
        self.allow_network = allow_network

    def evaluate(self, action: Action, state: SystemState) -> PolicyDecision:
        if action.action_type.value not in {
            "propose",
            "execute",
            "verify",
            "approve",
            "rollback",
            "recover",
        }:
            return PolicyDecision(False, "Unsupported action type", decision="deny")

        if action.tool_name and action.tool_name not in self.allowed_tools:
            return PolicyDecision(
                False, f"Tool '{action.tool_name}' is not allowed", decision="deny"
            )

        if action.requested_capabilities:
            unauthorized = [
                cap for cap in action.requested_capabilities if cap not in self.allowed_capabilities
            ]
            if unauthorized:
                return PolicyDecision(
                    False,
                    f"Requested capabilities are not authorized: {unauthorized}",
                    decision="deny",
                )

        if action.risk_level > self.max_risk_level:
            return PolicyDecision(
                False,
                f"Risk score {action.risk_level} exceeds policy maximum {self.max_risk_level}",
                decision="deny",
            )

        if action.confidence < 0.5 and action.action_type == action.action_type.EXECUTE:
            return PolicyDecision(
                True,
                "Execution confidence is below threshold; human approval required.",
                requires_approval=True,
                decision="pause",
            )

        if state.resource_state.time_used > self.max_time_seconds:
            raise PolicyViolationError("Time budget exceeded")

        if state.resource_state.tokens_used > self.max_token_budget:
            raise PolicyViolationError("Token budget exceeded")

        if action.parameters.get("path"):
            path_value = str(action.parameters["path"])
            if ".." in path_value or path_value.startswith("/"):
                return PolicyDecision(
                    False,
                    "Absolute or traversal paths are not permitted in the governance layer.",
                    decision="deny",
                )

        if action.parameters.get("url") and not self.allow_network:
            return PolicyDecision(
                False, "Network access requires an explicit capability.", decision="deny"
            )

        return PolicyDecision(True, "Action satisfies policy constraints", decision="allow")

    def validate_temporal_rule(self, prerequisite: str, event: str) -> str:
        """Return a temporal rule description, not a claim of theorem-proving.

        This is an explicit governance encoding inspired by LTL semantics: the state machine
        records prerequisites in history and checks them before acting.
        """
        return f"G({event} -> {prerequisite})"


__all__ = ["PolicyDecision", "PolicyEngine"]
