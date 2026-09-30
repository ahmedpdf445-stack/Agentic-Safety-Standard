from aether_genesis.agents.base import Agent
from aether_genesis.core.state import (
    ActionType,
    ExecutionState,
    PermissionState,
    PolicyState,
    ResourceState,
    RiskState,
    SystemState,
    TaskState,
)
from aether_genesis.execution.engine import ExecutionEngine
from aether_genesis.governance.policy import PolicyEngine
from aether_genesis.governance.safety_controller import SafetyController
from aether_genesis.provenance.audit import AuditLog
from aether_genesis.sandbox.sandbox import Sandbox
from aether_genesis.security.capabilities import CapabilityGateway


def make_state() -> SystemState:
    task = TaskState(task_id="task-3", title="pipeline", description="integration")
    return SystemState(
        task_state=task,
        permission_state=PermissionState(granted=["read_file"], denied=["privileged"]),
        resource_state=ResourceState(tokens_used=1000, time_used=10.0),
        risk_state=RiskState(),
        policy_state=PolicyState(rules=["strict"], mode="strict"),
        execution_state=ExecutionState(status="idle"),
    )


def test_execution_engine_handles_safe_action() -> None:
    state = make_state()
    agent = Agent(
        agent_id="agent-x",
        role="Planner",
        capabilities=["read_file", "summarize"],
        permissions=["read_file"],
    )
    state.agents[agent.agent_id] = agent.as_state()
    engine = ExecutionEngine(
        PolicyEngine(allowed_tools={"read_file", "summarize"}),
        SafetyController(),
        CapabilityGateway(allowed_roots=["."], allow_network=False),
        Sandbox(allowed_tools={"read_file", "summarize"}),
        AuditLog(),
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "README.md"},
        requested_capabilities=["read_file"],
        evidence=["safe read"],
        confidence=0.8,
        risk_level=0.2,
        task_id=state.task_state.task_id,
        tool_name="read_file",
    )
    result = engine.submit(agent, action, state)
    assert result.decision == "allow"
    assert result.verification_passed is True


def test_execution_engine_blocks_unsafe_action() -> None:
    state = make_state()
    agent = Agent(
        agent_id="agent-y", role="RedTeam", capabilities=["privileged"], permissions=["privileged"]
    )
    state.agents[agent.agent_id] = agent.as_state()
    engine = ExecutionEngine(
        PolicyEngine(allowed_tools={"read_file", "summarize"}),
        SafetyController(),
        CapabilityGateway(allowed_roots=["."], allow_network=False),
        Sandbox(allowed_tools={"read_file", "summarize"}),
        AuditLog(),
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "/etc/passwd", "command": "rm -rf /"},
        requested_capabilities=["privileged"],
        evidence=["danger"],
        confidence=0.9,
        risk_level=0.95,
        task_id=state.task_state.task_id,
        tool_name="write_file",
    )
    result = engine.submit(agent, action, state)
    assert result.decision in {"deny", "pause", "safe_mode", "terminate"}
