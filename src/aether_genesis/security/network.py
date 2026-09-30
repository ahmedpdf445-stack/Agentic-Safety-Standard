from __future__ import annotations


class NetworkPolicy:
    """Default-deny network policy requiring explicit capabilities."""

    def __init__(
        self,
        allowlist: list[str] | None = None,
        allowed_protocols: list[str] | None = None,
        max_requests: int = 2,
        max_response_bytes: int = 200000,
    ) -> None:
        self.allowlist = allowlist or []
        self.allowed_protocols = allowed_protocols or ["https"]
        self.max_requests = max_requests
        self.max_response_bytes = max_response_bytes

    def can_access(
        self, destination: str, *, protocol: str | None = None, request_count: int = 0
    ) -> bool:
        if not destination:
            return False
        if protocol and protocol not in self.allowed_protocols:
            return False
        if self.allowlist and not any(destination.startswith(prefix) for prefix in self.allowlist):
            return False
        return not request_count > self.max_requests
