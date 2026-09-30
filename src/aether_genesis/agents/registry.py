from __future__ import annotations

from dataclasses import dataclass, field

from aether_genesis.agents.base import Agent


@dataclass(slots=True)
class AgentRegistry:
    agents: dict[str, Agent] = field(default_factory=dict)

    def register(self, agent: Agent) -> None:
        self.agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent | None:
        return self.agents.get(agent_id)

    def roles(self) -> list[str]:
        return sorted({agent.role for agent in self.agents.values()})


__all__ = ["AgentRegistry"]
