from __future__ import annotations

"""Small formal test examples that represent explicit invariants.

These examples are not a claim of full system proof; they illustrate a minimal, testable formal layer.
"""


VALID_ACTION = {
    "tool_name": "read_file",
    "capabilities": {"read_file"},
    "risk_level": 0.2,
    "path": "README.md",
}

INVALID_ACTION = {
    "tool_name": "write_file",
    "capabilities": {"privileged"},
    "risk_level": 0.95,
    "path": "/etc/passwd",
}


def safe_action_satisfiable(action: dict[str, object]) -> bool:
    return (
        action["tool_name"] in {"read_file", "summarize"}
        and set(action["capabilities"]) <= {"read_file", "summarize"}
        and float(action["risk_level"]) <= 0.75
        and str(action["path"]).startswith(".")
    )


def unsafe_action_unsatisfiable(action: dict[str, object]) -> bool:
    return (
        "privileged" in set(action["capabilities"]) and not set(action["capabilities"]) <= {"read_file", "summarize"}
    )


if __name__ == "__main__":
    print({"valid": safe_action_satisfiable(VALID_ACTION), "invalid": unsafe_action_unsatisfiable(INVALID_ACTION)})
