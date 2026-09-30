from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class VerificationResult:
    passed_: bool
    evidence: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


class Verifier:
    """Validation layer for evidence and result quality."""

    def validate(
        self, output: Any, *, required_evidence: list[str] | None = None
    ) -> VerificationResult:
        required_evidence = required_evidence or []
        evidence = []
        issues = []

        if output is None:
            issues.append("Output is missing")

        if not isinstance(output, str):
            evidence.append("structured result observed")
        else:
            evidence.append("output text produced")

        for item in required_evidence:
            if item not in str(output):
                issues.append(f"Missing required evidence: {item}")

        return VerificationResult(passed_=not issues, evidence=evidence, issues=issues)


__all__ = ["VerificationResult", "Verifier"]
