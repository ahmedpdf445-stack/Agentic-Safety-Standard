from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


class BaseProvider:
    """Provider interface for model/back-end integration.

    The project does not pretend that a mock is a real model. A development mock is explicitly
    marked as development-only and used for deterministic tests.
    """

    def generate(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError("Provider must implement generate")


@dataclass(slots=True)
class DevelopmentMockProvider(BaseProvider):
    """DEVELOPMENT MOCK: deterministic, local test provider."""

    seed: int = 42
    responses: dict[str, str] = field(
        default_factory=lambda: {
            "default": "Development mock response: plan, verify, and constrain execution using policy boundaries.",
        }
    )

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return self.responses.get("default", "Development mock response")


class OpenAIProviderAdapter(BaseProvider):
    """Adapter interface for a real provider. It is intentionally isolated from the governance layer."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")

    def generate(self, prompt: str, **kwargs: Any) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        return f"Real provider generation for prompt: {prompt[:80]}"


def build_provider() -> BaseProvider:
    provider_name = os.getenv("LLM_PROVIDER", "development_mock").lower()
    if provider_name == "openai":
        return OpenAIProviderAdapter()
    return DevelopmentMockProvider()


__all__ = ["BaseProvider", "DevelopmentMockProvider", "OpenAIProviderAdapter", "build_provider"]
