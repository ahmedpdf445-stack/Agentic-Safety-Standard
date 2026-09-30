from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aether_genesis.agents.base import Agent
from aether_genesis.core.exceptions import BudgetExceededError, CapabilityDeniedError
from aether_genesis.core.state import Action, SystemState
from aether_genesis.governance.policy import PolicyEngine
from aether_genesis.governance.safety_controller import SafetyController
from aether_genesis.provenance.audit import AuditLog
from aether_genesis.sandbox.sandbox import Sandbox
from aether_genesis.security.capabilities import CapabilityGateway


@dataclass(slots=True)
class ExecutionResult:
    decision: str
    message: str
    action_id: str | None = None
    verification_passed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class ExecutionEngine:
    def __init__(
        self,
        policy_engine: PolicyEngine,
        safety_controller: SafetyController,
        capability_gateway: CapabilityGateway,
        sandbox: Sandbox,
        audit_log: AuditLog,
    ) -> None:
        self.policy_engine = policy_engine
        self.safety_controller = safety_controller
        self.capability_gateway = capability_gateway
        self.sandbox = sandbox
        self.audit_log = audit_log

    def submit(self, agent: Agent, action: Action, state: SystemState) -> ExecutionResult:
        state.execution_state.last_action_id = action.action_id
        state.execution_state.status = "review"

        self.audit_log.record(
            agent_id=agent.agent_id,
            action_id=action.action_id,
            event="action_received",
            metadata={"action_type": action.action_type.value, "risk": action.risk_level},
        )

        if state.resource_state.time_used > self.policy_engine.max_time_seconds:
            raise BudgetExceededError("Time budget exceeded")

        policy_result = self.policy_engine.evaluate(action, state)
        if not policy_result.allowed:
            self.audit_log.record(
                agent_id=agent.agent_id,
                action_id=action.action_id,
                event="policy_denied",
                metadata={"reason": policy_result.reason},
            )
            return ExecutionResult(
                policy_result.decision, policy_result.reason, action.action_id, False
            )

        try:
            self.capability_gateway.authorize(action, state)
        except CapabilityDeniedError as exc:
            self.audit_log.record(
                agent_id=agent.agent_id,
                action_id=action.action_id,
                event="capability_denied",
                metadata={"reason": str(exc)},
            )
            return ExecutionResult("deny", str(exc), action.action_id, False)

        safety_decision = self.safety_controller.decide(action, policy_result, state)
        if safety_decision.status not in {"allow", "require_human_approval"}:
            self.audit_log.record(
                agent_id=agent.agent_id,
                action_id=action.action_id,
                event="safety_blocked",
                metadata={"status": safety_decision.status},
            )
            return ExecutionResult(
                safety_decision.status, safety_decision.reason, action.action_id, False
            )

        state.execution_state.status = "executing"
        result = self.sandbox.execute(action.tool_name or "summarize", parameters=action.parameters)
        state.execution_state.verification_passed = result.ok
        self.audit_log.record(
            agent_id=agent.agent_id,
            action_id=action.action_id,
            event="execution_complete",
            metadata={"ok": result.ok, "output": result.output},
        )

        if result.ok:
            return ExecutionResult(
                "allow",
                result.output,
                action.action_id,
                True,
                metadata={"sandbox": result.metadata},
            )
        return ExecutionResult("deny", result.reason, action.action_id, False)


__all__ = ["ExecutionEngine", "ExecutionResult"]
