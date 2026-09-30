from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aether_genesis.core.state import Action, ActionType, AgentState, ResourceBudget


@dataclass(slots=True)
class Agent:
    agent_id: str
    role: str
    capabilities: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    resource_budget: ResourceBudget = field(default_factory=ResourceBudget)
    task_context: dict[str, Any] = field(default_factory=dict)
    evidence_context: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    uncertainty: float = 0.5
    action_history: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    status: str = "idle"

    def as_state(self) -> AgentState:
        return AgentState(
            agent_id=self.agent_id,
            role=self.role,
            capabilities=self.capabilities,
            permissions=[
                type("P", (), {"name": p, "allowed": True, "scope": "agent", "details": None})()
                for p in self.permissions
            ],
            resource_budget=self.resource_budget,
            task_context=self.task_context,
            evidence_context=self.evidence_context,
            confidence=self.confidence,
            uncertainty=self.uncertainty,
            action_history=self.action_history,
            provenance=self.provenance,
            status=self.status,
        )

    def propose_action(
        self,
        action_type: ActionType,
        *,
        parameters: dict[str, Any] | None = None,
        requested_capabilities: list[str] | None = None,
        evidence: list[str] | None = None,
        confidence: float = 0.5,
        risk_level: float = 0.1,
        task_id: str = "",
        parent_action_id: str | None = None,
        tool_name: str | None = None,
    ) -> Action:
        action = Action(
            action_id=f"{self.agent_id}:{len(self.action_history) + 1}",
            agent_id=self.agent_id,
            action_type=action_type,
            parameters=parameters or {},
            requested_capabilities=requested_capabilities or [],
            evidence=evidence or [],
            confidence=confidence,
            risk_level=risk_level,
            timestamp="",
            parent_action_id=parent_action_id,
            task_id=task_id,
            tool_name=tool_name,
        )
        self.action_history.append(action.action_id)
        return action
