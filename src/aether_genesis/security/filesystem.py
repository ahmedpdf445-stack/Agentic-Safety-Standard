from __future__ import annotations

from pathlib import Path


class FilesystemGuard:
    """Filesystem boundarization with canonical path resolution."""

    def __init__(self, allowed_roots: list[str] | None = None) -> None:
        roots = allowed_roots or ["."]
        self.allowed_roots = [Path(root).resolve() for root in roots]

    def resolve(self, raw_path: str) -> Path:
        candidate = Path(raw_path)
        if candidate.is_absolute():
            return candidate.resolve()
        return (Path.cwd() / candidate).resolve()

    def is_authorized(self, raw_path: str) -> bool:
        resolved = self.resolve(raw_path)
        return any(resolved.is_relative_to(root) for root in self.allowed_roots)

    def ensure_authorized(self, raw_path: str) -> Path:
        resolved = self.resolve(raw_path)
        if not any(resolved.is_relative_to(root) for root in self.allowed_roots):
            raise ValueError(f"Path {raw_path} escapes authorized roots")
        return resolved
