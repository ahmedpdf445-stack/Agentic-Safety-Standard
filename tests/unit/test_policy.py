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
from aether_genesis.governance.policy import PolicyEngine


def make_state() -> SystemState:
    task = TaskState(task_id="task-1", title="demo", description="demo")
    return SystemState(
        task_state=task,
        permission_state=PermissionState(granted=["read_file"], denied=["privileged"]),
        resource_state=ResourceState(tokens_used=1000, time_used=5.0),
        risk_state=RiskState(),
        policy_state=PolicyState(rules=["strict"], mode="strict"),
        execution_state=ExecutionState(status="idle"),
    )


def test_safe_action_is_allowed() -> None:
    state = make_state()
    agent = Agent(
        agent_id="a1", role="Researcher", capabilities=["read_file"], permissions=["read_file"]
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "README.md"},
        requested_capabilities=["read_file"],
        evidence=["safe read"],
        confidence=0.9,
        risk_level=0.2,
        task_id=state.task_state.task_id,
        tool_name="read_file",
    )

    decision = PolicyEngine().evaluate(action, state)
    assert decision.allowed is True


def test_unsafe_path_is_denied() -> None:
    state = make_state()
    agent = Agent(
        agent_id="a2", role="RedTeam", capabilities=["privileged"], permissions=["privileged"]
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "/etc/passwd"},
        requested_capabilities=["privileged"],
        evidence=["path traversal"],
        confidence=0.9,
        risk_level=0.9,
        task_id=state.task_state.task_id,
        tool_name="write_file",
    )

    decision = PolicyEngine().evaluate(action, state)
    assert decision.allowed is False
