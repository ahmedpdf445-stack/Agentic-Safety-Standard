# Threat Model

## Trust boundaries

- model output is untrusted
- tool outputs are untrusted
- filesystem is partially trusted only within the registered roots
- network is untrusted and denied by default
- governance state is trusted only when stored in explicit typed structures

## Attack surfaces

- prompt injection into agent requests
- malicious tool payloads
- path traversal attempts
- command injection sequences
- policy bypass via capability specification
- state manipulation through unverified natural language
- excessive resource consumption
- unauthorized delegation depth

## Controls

- typed actions
- capability checks
- allowlisted tools
- canonical path validation
- default block network access
- risk thresholding
- resource budgeting
- audit logging

## Limitations

This is not a hardware-certified secure enclave design. It is a governance-layer implementation with explicit assumptions and documented limits.
