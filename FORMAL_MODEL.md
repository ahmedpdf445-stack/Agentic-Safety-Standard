# Formal Model

## Scope

This document describes the formal abstractions represented in the project, without claiming that the entire software stack is mathematically proved correct.

## Core definitions

- SystemState: explicit state object containing tasks, permissions, resources, policy, and execution status
- Action: typed action accepted by the governance pipeline
- Capability: explicit authorization object with scope and restrictions
- Policy: a rule set that constrains action legality
- Invariant: a property that must hold across valid transitions
- Transition: mapping from one state to another under policy and controller checks

## Temporal rule examples

The project encodes policies with a semantics inspired by LTL, but without claiming theorem-level equivalence:

- G(Execute -> RiskCheckPassed)
- This is a temporal statement about the relationship between execution and a preceding risk check in the action lifecycle.
- The implementation treats it as an explicit governance check recording prerequisite events in history, not as a universal theorem about all future behavior.

## SAT / UNSAT examples

The project includes simple formal examples in [research/formal/README.md](research/formal/README.md). The goal is to encode small, testable properties rather than to pretend a full solver proves the whole system.

## Limitations

Solver integration is intentionally small and testable. It does not replace system verification, runtime testing, or environment assumptions.
