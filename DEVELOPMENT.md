# Development Guide

## Environment

- Python 3.11+
- Editable installation via `pip install -e .`
- Virtual environment recommended

## Local workflow

1. Create environment
2. Install project tools
3. Run `pytest -q`
4. Run lints and type checks
5. Run demo and smoke test

## Code boundaries

- `src/aether_genesis/core`: state and common exceptions
- `src/aether_genesis/governance`: policy and safety controller
- `src/aether_genesis/security`: capabilities and filesystem/network restrictions
- `src/aether_genesis/sandbox`: execution boundary
- `src/aether_genesis/execution`: orchestration engine
- `src/aether_genesis/provenance`: audit trail
- `src/aether_genesis/verification`: evidence validation
- `src/aether_genesis/research`: research metrics and control abstractions

## Conventions

- explicit state, not hidden global state
- deterministic fixtures in tests
- no hard-coded secrets
- no fake claims of formal proof beyond documented scope
