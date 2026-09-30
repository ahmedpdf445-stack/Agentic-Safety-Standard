class AetherGenesisError(Exception):
    """Base exception for the governance system."""


class PolicyViolationError(AetherGenesisError):
    """Raised when a policy check rejects an action."""


class CapabilityDeniedError(AetherGenesisError):
    """Raised when a capability is not allowed."""


class BudgetExceededError(AetherGenesisError):
    """Raised when the execution exceeds its budget."""


class SandboxViolationError(AetherGenesisError):
    """Raised when sandbox restrictions are violated."""


class VerificationFailureError(AetherGenesisError):
    """Raised when verification fails."""
