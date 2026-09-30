# Testing Guide

## Test suite

The project includes:

- unit tests for policy and state transitions
- integration tests for the governance pipeline
- security tests for traversal, policy bypass, and network restrictions
- end-to-end demo tests

## Commands

- `pytest -q`
- `ruff check src tests`
- `mypy src`
- `bandit -r src -q`

## Determinism

All tests use deterministic fixtures and seedable development mocks. External provider integrations are isolated behind an explicit interface and not required for local validation.
