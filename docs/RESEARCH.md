# Research Notes

This document records research claims in a structured way to prevent presenting speculative ideas as proven results.

## Claim: capability boundaries reduce direct unsafe action

- Evidence: policy engine and capability gateway reject actions outside defined capabilities.
- Mechanism: explicit authorization and root-bound path checks restrict action surfaces.
- Metric: unauthorized action rate.
- Experiment: evaluate safe and unsafe actions under deterministic test fixtures.
- Result: unsafe privileged or absolute-path actions are blocked.
- Limitations: this does not replace full operating-system security assumptions.

## Claim: deterministic governance can structure agent execution

- Evidence: action pipeline uses typed states, policy evaluation, and explicit safety decisions.
- Mechanism: LLM proposals are translated into typed actions and checked against explicit state.
- Metric: policy compliance rate and action approval rate.
- Experiment: run safe and unsafe paths through the execution engine.
- Result: safe actions are allowed and unsafe actions are denied or paused.
- Limitations: this is a prototype governance layer, not universal autonomous safety.

## Claim: entropy-inspired metrics are engineering signals

- Evidence: the project defines a risk-weighted metric with explicit weights.
- Mechanism: risk, uncertainty, resource pressure, and contradiction contribute to a single score.
- Metric: system risk score.
- Experiment: compute the metric under varying conditions.
- Result: a numeric signal is produced for monitoring.
- Limitations: it is not thermodynamic entropy and does not infer physical meaning.
