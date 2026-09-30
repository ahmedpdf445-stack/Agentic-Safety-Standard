from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aether_genesis.core.exceptions import CapabilityDeniedError
from aether_genesis.core.state import Action, SystemState


@dataclass(slots=True)
class Capability:
    name: str
    allowed: bool = True
    details: dict[str, Any] = field(default_factory=dict)


class CapabilityGateway:
    """Capability gateway that authorizes allowed actions."""

    def __init__(
        self,
        allowed_roots: list[str] | None = None,
        allow_network: bool = False,
        allow_privilege: bool = False,
    ) -> None:
        self.allowed_roots = [Path(root).resolve() for root in (allowed_roots or ["."])]
        self.allow_network = allow_network
        self.allow_privilege = allow_privilege

    def authorize(self, action: Action, state: SystemState) -> bool:
        for capability in action.requested_capabilities:
            if capability in {"read_file", "write_file", "search", "summarize"}:
                continue
            if capability == "network" and not self.allow_network:
                raise CapabilityDeniedError("Network capability is disabled by policy")
            if capability == "privileged" and not self.allow_privilege:
                raise CapabilityDeniedError("Privileged operations are not allowed")

        if action.parameters.get("path"):
            requested_path = Path(action.parameters["path"]).resolve()
            if not any(requested_path.is_relative_to(root) for root in self.allowed_roots):
                raise CapabilityDeniedError(
                    f"Path {requested_path} is outside the authorized roots"
                )

        return True

    def authorize_network(self, destination: str) -> bool:
        if not self.allow_network:
            raise CapabilityDeniedError("Network requests are denied by default")
        return destination.startswith(("http://", "https://"))


__all__ = ["Capability", "CapabilityGateway"]
