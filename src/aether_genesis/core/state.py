from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionType(str, Enum):
    PROPOSE = "propose"
    EXECUTE = "execute"
    VERIFY = "verify"
    APPROVE = "approve"
    ROLLBACK = "rollback"
    RECOVER = "recover"
    REPORT = "report"


class EvidenceType(str, Enum):
    FACT = "fact"
    MODEL_OUTPUT = "model_output"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"
    ASSUMPTION = "assumption"
    UNVERIFIED_CLAIM = "unverified_claim"


@dataclass(slots=True)
class Permission:
    name: str
    allowed: bool = True
    scope: str = "global"
    details: str | None = None


@dataclass(slots=True)
class ResourceBudget:
    time_seconds: float = 60.0
    cpu_percent: int = 50
    memory_mb: int = 512
    token_budget: int = 20000
    tool_calls: int = 10
    subprocesses: int = 2
    network_requests: int = 0
    monetary_cost: float = 0.0


@dataclass(slots=True)
class Action:
    action_id: str
    agent_id: str
    action_type: ActionType
    parameters: dict[str, Any] = field(default_factory=dict)
    requested_capabilities: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    confidence: float = 0.0
    risk_level: float = 0.0
    timestamp: str = ""
    parent_action_id: str | None = None
    task_id: str = ""
    tool_name: str | None = None


@dataclass(slots=True)
class TaskState:
    task_id: str
    title: str
    description: str
    status: str = "pending"
    created_at: str = ""
    updated_at: str = ""
    priority: str = "normal"


@dataclass(slots=True)
class AgentState:
    agent_id: str
    role: str
    capabilities: list[str] = field(default_factory=list)
    permissions: list[Permission] = field(default_factory=list)
    resource_budget: ResourceBudget = field(default_factory=ResourceBudget)
    task_context: dict[str, Any] = field(default_factory=dict)
    evidence_context: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    uncertainty: float = 0.5
    action_history: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    status: str = "idle"


@dataclass(slots=True)
class PermissionState:
    granted: list[str] = field(default_factory=list)
    denied: list[str] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ToolState:
    name: str
    allowed: bool = True
    category: str = "builtin"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ResourceState:
    time_used: float = 0.0
    cpu_used: float = 0.0
    memory_used_mb: int = 0
    tokens_used: int = 0
    tool_calls_used: int = 0
    subprocesses_used: int = 0
    network_requests_used: int = 0
    monetary_cost: float = 0.0


@dataclass(slots=True)
class RiskState:
    policy_violations: int = 0
    resource_pressure: float = 0.0
    uncertainty_score: float = 0.0
    contradiction_score: float = 0.0
    execution_risk: float = 0.0
    last_risk_summary: str = "stable"


@dataclass(slots=True)
class EvidenceState:
    entries: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class PolicyState:
    rules: list[str] = field(default_factory=list)
    mode: str = "strict"
    enforcement: str = "deny_by_default"


@dataclass(slots=True)
class ExecutionState:
    status: str = "idle"
    last_action_id: str | None = None
    verification_passed: bool = False
    sandbox_status: str = "inactive"
    recovery_mode: bool = False


@dataclass(slots=True)
class SystemState:
    task_state: TaskState
    agents: dict[str, AgentState] = field(default_factory=dict)
    permission_state: PermissionState = field(default_factory=PermissionState)
    tool_state: dict[str, ToolState] = field(default_factory=dict)
    resource_state: ResourceState = field(default_factory=ResourceState)
    risk_state: RiskState = field(default_factory=RiskState)
    evidence_state: EvidenceState = field(default_factory=EvidenceState)
    policy_state: PolicyState = field(default_factory=PolicyState)
    execution_state: ExecutionState = field(default_factory=ExecutionState)
