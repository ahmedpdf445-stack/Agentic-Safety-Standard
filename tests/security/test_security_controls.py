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
    task = TaskState(task_id="task-security", title="security", description="red team")
    return SystemState(
        task_state=task,
        permission_state=PermissionState(granted=["read_file"], denied=["privileged"]),
        resource_state=ResourceState(tokens_used=500, time_used=1.0),
        risk_state=RiskState(),
        policy_state=PolicyState(rules=["strict"], mode="strict"),
        execution_state=ExecutionState(status="idle"),
    )


def test_path_traversal_is_blocked() -> None:
    state = make_state()
    agent = Agent(
        agent_id="sec-1",
        role="SecurityAgent",
        capabilities=["read_file"],
        permissions=["read_file"],
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "../secrets/.env"},
        requested_capabilities=["read_file"],
        evidence=["read secret"],
        confidence=0.7,
        risk_level=0.3,
        task_id=state.task_state.task_id,
        tool_name="read_file",
    )
    decision = PolicyEngine().evaluate(action, state)
    assert decision.allowed is False


def test_untrusted_network_is_blocked() -> None:
    state = make_state()
    agent = Agent(
        agent_id="sec-2", role="Researcher", capabilities=["search"], permissions=["search"]
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"url": "https://example.com"},
        requested_capabilities=["search"],
        evidence=["network request"],
        confidence=0.8,
        risk_level=0.4,
        task_id=state.task_state.task_id,
        tool_name="search",
    )
    decision = PolicyEngine(allow_network=False).evaluate(action, state)
    assert decision.allowed is False
