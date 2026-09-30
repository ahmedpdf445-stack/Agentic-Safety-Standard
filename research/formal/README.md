# Formal Methods Notes

## System state

A state is represented as a typed structure containing task, agent, permission, tool, resource, risk, evidence, policy, and execution components.

## Action

An action includes:

- action_id
- agent_id
- action_type
- parameters
- requested_capabilities
- evidence
- confidence
- risk_level
- timestamp
- parent_action_id

## Capability

A capability is a named authorization value that must appear in an allowlist before execution.

## Policy

Policy is encoded as a rule set with explicit allow/deny conditions and risk thresholds.

## Invariant

Invariant examples:

- no action may request a capability outside an authorized set
- no execution may exceed a configured time or token budget
- no path may escape the root boundary

## Transition

A transition is a state change that occurs only if governance checks pass.

## Safe state

Safe state means all required checks pass and no active budget or policy thresholds are violated.

## Unsafe state

Unsafe state includes policy violations, privilege escalation requests, or path escape attempts.

## Recovery state

Recovery state is the system condition after a denial or pause, where safe mode or rollback logic is triggered.

## SAT example

A safe action can satisfy:

- action.tool_name in allowed_tools
- action.risk_level <= threshold
- path in authorized root

This is satisfiable under the policy model.

## UNSAT example

The following is unsatisfiable under the current policy:

- action.requested_capabilities = {privileged}
- allow_privilege = False

Therefore the action cannot be accepted under the defined policy.

## Solver note

The project includes formal examples and is prepared for solver-backed validation of selected properties, but it does not claim that the entire software system is proven correct by an SMT solver.
