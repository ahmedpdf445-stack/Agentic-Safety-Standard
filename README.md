# AETHER-GENESIS

AETHER-GENESIS is a formally governed autonomous computational research system in which probabilistic AI/agent intelligence operates inside explicit deterministic governance boundaries.

## Executive Summary

The project distinguishes between:

- probabilistic intelligence from a model or agent
- deterministic governance from policy, state transition rules, and safety checks
- evidence-based verification from unverified output
- system-level risk metrics from physical thermodynamic entropy

The system is designed around a simple thesis: probabilistic intelligence is valuable only when embedded inside explicit state, permissions, invariants, resource budgets, and verifiable execution boundaries.

## Problem

Current agent systems often exhibit several failure modes:

- hallucinated outputs presented as facts
- unrestricted tool usage and escape from bounded execution
- privilege escalation through implicit capability growth
- runaway execution without budget or timeout enforcement
- weak provenance and weak reproducibility
- policy signals embedded in natural language without machine-readable checks

AETHER-GENESIS addresses these by enforcing a deterministic governance layer between model proposals and any action that can affect the outside world.

## Why Current Agent Systems Are Insufficient

- Probabilistic behavior: LLMs are not deterministic functions over arbitrary tasks.
- Hallucination: model output can be fluent, confident, and wrong.
- Tool risk: an agent can invoke tools that mutate state, access files, or reach the network.
- Privilege escalation: a model may incorrectly infer that it should have system power or broader filesystem access.
- Runaway execution: unbounded recursion, tool loops, and rebinding can exhaust resources.
- Weak provenance: outputs without traceable lineage are difficult to audit.
- Weak reproducibility: natural-language-only state makes reproduction difficult.
- Unclear governance: without explicit policy and state transitions, decisions become informal.

## Core Thesis

Probabilistic intelligence operating inside deterministic governance boundaries.

This means:

- LLMs propose actions
- the policy engine checks structural legality
- the safety controller applies decision logic
- the capability gateway authorizes only explicit capabilities
- the sandbox executes under restrictions
- the verifier assesses results
- provenance and evidence are recorded
- state updates remain explicit and machine-readable

## Architecture

The implementation is organized into layered subsystems:

- Layer 0: Hardware / trust assumptions (interface-level abstraction)
- Layer 1: Execution isolation and sandboxing
- Layer 2: Explicit typed state machine
- Agent layer: role-based agent abstractions
- Governance layer: policy and safety controller
- Capability layer: filesystem/network authorization
- Verification layer: evidence and validation
- Observability and provenance: logs, metrics, and event chains

Architecture flow:

LLM / agent proposal
  -> Policy Engine
  -> Safety Controller
  -> Capability Gateway
  -> Sandbox Execution
  -> Verification
  -> Evidence and Provenance
  -> State Update

## Execution Flow

1. Agent proposes an action.
2. Policy engine checks tool policy, risk, budgets, and path/network constraints.
3. Safety controller decides allow, pause, deny, or safe mode.
4. Capability gateway authorizes permissions and bounded filesystem/network access.
5. Sandbox executes only on allowed tools and command patterns.
6. Verifier validates outputs against evidence requirements.
7. Provenance log records the action, decision, timing, and outputs.
8. State is updated only through explicit transitions.

## Formal Model

The project uses explicit state objects and typed actions instead of natural-language-only governance. The formal model includes definitions for:

- system state
- action
- capability
- policy
- invariant
- transition
- safe state
- unsafe state
- recovery state

These are documented in [research/formal/README.md](research/formal/README.md). The implementation uses modest, testable abstractions rather than claiming that a full software system is formally proved by a solver.

## Security Model

The security model follows default-deny design:

- prompt injection is treated as an input-validation problem
- command injection is blocked by sandbox command pattern checks
- path traversal is blocked by canonical path resolution and root restrictions
- network access is denied unless explicitly enabled
- filesystem access is restricted to explicit roots
- secrets and credentials are never committed
- tools are allowlisted and restricted to expected operations
- resource budgets are enforced before and during execution
- provenance prevents silent conversion of model output to fact

## Verification

The project distinguishes verification categories explicitly:

- formally verified: only selected small properties are represented in a formal specification; not the whole software system
- statically checked: linting, import sorting, and type analysis
- dynamically tested: unit, integration, security, and end-to-end tests
- empirically validated: observed behavior under the project’s smoke tests and deterministic fixtures
- currently unverified: full hardware enclave security, arbitrary agent swarms, and general adversarial autonomy at scale

## Benchmarks

Notable metrics include:

- policy violation rate
- unauthorized action rate
- recovery success rate
- execution reliability
- latency
- resource consumption
- tool failure rate
- provenance completeness
- reproducibility quality
- security test pass rate

## Research Questions

- How should policy and execution boundaries scale with multi-agent coordination?
- What agent-level evidence thresholds are appropriate for transitioning from hypothesis to fact?
- How do dynamic capability budgets impact adjudication under malicious or contradictory outputs?
- How can safety controllers be combined with formal invariants without overclaiming guarantees?

## Limitations

This project does not guarantee:

- complete system security under all adversarial conditions
- mathematical proof of all software correctness
- full deterministic AI behavior
- hardware enclave guarantees without actual attestation infrastructure
- secure execution of arbitrary third-party code in a real hosting environment

This project implements a governance layer that is testable and explicit, but it is not a claim of universal safety.

## Roadmap

- Implemented: state model, policy engine, capability gateway, execution engine, provenance, tests, demo
- Prototype: more realistic sandbox adapters and richer tool orchestration
- Research: stronger formal models, dynamic risk metrics, and distributed multi-agent communication
- Future: hardware-backed attestation, stronger solver-backed policy validation, and larger real-world deployment studies

## Reproducibility

To reproduce the project:

1. Create a Python 3.11 virtual environment.
2. Install project dependencies: `python -m pip install -r ...` (editable install via `pip install -e .` is used in this workspace).
3. Run `pytest -q`.
4. Run the smoke demo: `python -m aether_genesis demo`.
5. Review logs and provenance outputs in the execution path.

## Documentation Index

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [SECURITY.md](SECURITY.md)
- [THREAT_MODEL.md](THREAT_MODEL.md)
- [FORMAL_MODEL.md](FORMAL_MODEL.md)
- [DEVELOPMENT.md](DEVELOPMENT.md)
- [TESTING.md](TESTING.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CHANGELOG.md](CHANGELOG.md)
- [docs/BUSINESS.md](docs/BUSINESS.md)
- [docs/CTO_GUIDE.md](docs/CTO_GUIDE.md)
- [docs/RESEARCH.md](docs/RESEARCH.md)
