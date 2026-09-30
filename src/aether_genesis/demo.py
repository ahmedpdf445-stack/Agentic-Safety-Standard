from __future__ import annotations

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


def build_demo_state() -> SystemState:
    task = TaskState(
        task_id="task-001", title="Governed read", description="Safe demonstration task"
    )
    initial_state = SystemState(
        task_state=task,
        agents={},
        permission_state=PermissionState(
            granted=["read_file", "write_file"], denied=["privileged"]
        ),
        tool_state={},
        resource_state=ResourceState(tokens_used=1500, time_used=12.0),
        risk_state=RiskState(),
        policy_state=PolicyState(
            rules=["deny_by_default", "explicit_capability_required"], mode="strict"
        ),
        execution_state=ExecutionState(status="idle"),
    )
    return initial_state


def create_demo_agent() -> Agent:
    return Agent(
        agent_id="agent-1",
        role="Researcher",
        capabilities=["read_file", "summarize"],
        permissions=["read_file"],
        confidence=0.8,
        uncertainty=0.2,
        provenance={"owner": "demo"},
    )


def run_demo() -> dict[str, object]:
    state = build_demo_state()
    agent = create_demo_agent()
    state.agents[agent.agent_id] = agent.as_state()
    policy_engine = PolicyEngine(allowed_tools={"read_file", "summarize"}, allow_network=False)
    safety_controller = SafetyController()
    capability_gateway = CapabilityGateway(allowed_roots=["."], allow_network=False)
    sandbox = Sandbox(allowed_tools={"read_file", "summarize"})
    audit_log = AuditLog()
    engine = ExecutionEngine(
        policy_engine, safety_controller, capability_gateway, sandbox, audit_log
    )

    safe_action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "README.md", "text": "demo test"},
        requested_capabilities=["read_file"],
        evidence=["read action requested"],
        confidence=0.9,
        risk_level=0.2,
        task_id=state.task_state.task_id,
        tool_name="read_file",
    )
    safe_result = engine.submit(agent, safe_action, state)

    unsafe_action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "/etc/passwd", "command": "rm -rf /"},
        requested_capabilities=["privileged"],
        evidence=["unsafe attempt"],
        confidence=0.9,
        risk_level=0.95,
        task_id=state.task_state.task_id,
        tool_name="write_file",
    )
    unsafe_result = engine.submit(agent, unsafe_action, state)

    result = {
        "safe": safe_result,
        "unsafe": unsafe_result,
        "audit_log": audit_log.get_entries(),
    }
    print(f"SAFE_ACTION: {safe_result.decision} :: {safe_result.message}")
    print(f"UNSAFE_ACTION: {unsafe_result.decision} :: {unsafe_result.message}")
    return result


if __name__ == "__main__":
    run_demo()
