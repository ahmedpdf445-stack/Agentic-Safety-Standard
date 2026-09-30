from aether_genesis.demo import run_demo


def test_demo_executes_and_blocks_unsafe_action() -> None:
    result = run_demo()
    assert result["safe"].decision == "allow"
    assert result["unsafe"].decision in {"deny", "pause", "safe_mode", "terminate"}
    assert len(result["audit_log"]) >= 2
