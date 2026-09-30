from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aether_genesis.core.exceptions import SandboxViolationError


@dataclass(slots=True)
class SandboxResult:
    ok: bool
    output: str = ""
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class Sandbox:
    """Capability-limited execution environment.

    This is an execution abstraction, not a claim of hardware-secure isolation.
    """

    def __init__(self, allowed_tools: set[str] | None = None, max_subprocesses: int = 2) -> None:
        self.allowed_tools = allowed_tools or {"read_file", "write_file", "search", "summarize"}
        self.max_subprocesses = max_subprocesses

    def execute(self, tool_name: str, *, parameters: dict[str, Any] | None = None) -> SandboxResult:
        parameters = parameters or {}
        if tool_name not in self.allowed_tools:
            raise SandboxViolationError(f"Tool '{tool_name}' is not permitted in the sandbox")

        if "command" in parameters and any(
            token in str(parameters["command"]) for token in [";", "&&", "|", "rm "]
        ):
            raise SandboxViolationError("Command injection patterns are not permitted")

        if tool_name == "read_file":
            return SandboxResult(
                True,
                f"read ok: {parameters.get('path', '')}",
                metadata={"path": parameters.get("path")},
            )
        if tool_name == "write_file":
            return SandboxResult(
                True,
                f"write ok: {parameters.get('path', '')}",
                metadata={"path": parameters.get("path")},
            )
        if tool_name == "search":
            return SandboxResult(True, "search ok", metadata={"query": parameters.get("query")})
        if tool_name == "summarize":
            return SandboxResult(
                True, "summary ok", metadata={"text": parameters.get("text", "")[:80]}
            )
        return SandboxResult(
            False, "Unsupported tool for sandbox execution", reason="unsupported_tool"
        )
