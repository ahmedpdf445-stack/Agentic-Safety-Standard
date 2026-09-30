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
from aether_genesis.governance.policy import PolicyDecision
from aether_genesis.governance.safety_controller import SafetyController


def make_state() -> SystemState:
    task = TaskState(task_id="task-2", title="safety", description="budget")
    return SystemState(
        task_state=task,
        permission_state=PermissionState(granted=["read_file"], denied=["privileged"]),
        resource_state=ResourceState(tokens_used=10_000, time_used=100.0),
        risk_state=RiskState(policy_violations=2),
        policy_state=PolicyState(rules=["strict"], mode="strict"),
        execution_state=ExecutionState(status="idle"),
    )


def test_safety_controller_pauses_high_risk_action() -> None:
    state = make_state()
    controller = SafetyController()
    agent = Agent(
        agent_id="a3", role="Analyst", capabilities=["read_file"], permissions=["read_file"]
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "notes.txt"},
        requested_capabilities=["read_file"],
        evidence=["review"],
        confidence=0.6,
        risk_level=0.85,
        task_id=state.task_state.task_id,
        tool_name="summarize",
    )
    decision = controller.decide(action, PolicyDecision(True, "OK"), state)
    assert decision.status == "pause"


def test_system_trips_circuit_breaker() -> None:
    state = make_state()
    state.risk_state.policy_violations = 10
    controller = SafetyController(circuit_breaker_threshold=5)
    agent = Agent(
        agent_id="a4", role="Reviewer", capabilities=["read_file"], permissions=["read_file"]
    )
    action = agent.propose_action(
        ActionType.EXECUTE,
        parameters={"path": "report.txt"},
        requested_capabilities=["read_file"],
        evidence=["nominal"],
        confidence=0.5,
        risk_level=0.2,
        task_id=state.task_state.task_id,
        tool_name="read_file",
    )
    decision = controller.decide(action, PolicyDecision(True, "OK"), state)
    assert decision.status == "safe_mode"
