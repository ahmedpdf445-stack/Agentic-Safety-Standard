#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e .[dev]
python -m ruff check src tests
python -m mypy src
python -m pytest -q
python -m bandit -r src -q
python -m aether_genesis demo
