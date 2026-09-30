from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class AuditEntry:
    timestamp: str
    agent_id: str
    action_id: str
    event: str
    metadata: dict[str, Any] = field(default_factory=dict)


class AuditLog:
    """Append-only, traceable event log."""

    def __init__(self) -> None:
        self.entries: list[AuditEntry] = []

    def record(
        self, *, agent_id: str, action_id: str, event: str, metadata: dict[str, Any] | None = None
    ) -> AuditEntry:
        entry = AuditEntry(
            timestamp=datetime.now(UTC).isoformat(),
            agent_id=agent_id,
            action_id=action_id,
            event=event,
            metadata=metadata or {},
        )
        self.entries.append(entry)
        return entry

    def get_entries(self, *, action_id: str | None = None) -> list[AuditEntry]:
        if action_id is None:
            return list(self.entries)
        return [entry for entry in self.entries if entry.action_id == action_id]


__all__ = ["AuditEntry", "AuditLog"]
