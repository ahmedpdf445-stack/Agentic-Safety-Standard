from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AETHER-GENESIS governance demo runner")
    parser.add_argument("command", nargs="?", default="demo", choices=["demo", "version"])
    args = parser.parse_args(argv)

    if args.command == "version":
        print("AETHER-GENESIS 0.1.0")
        return 0

    from .demo import run_demo

    run_demo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
