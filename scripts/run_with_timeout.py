#!/usr/bin/env python3
"""Run one command with a cross-platform wall-clock timeout."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("seconds", type=float)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error("seconds must be positive")
    if not args.command:
        parser.error("pass a command after --")
    command = args.command[1:] if args.command[0] == "--" else args.command
    try:
        return subprocess.run(command, timeout=args.seconds, check=False).returncode
    except subprocess.TimeoutExpired:
        print(f"command timed out after {args.seconds:g} seconds", file=sys.stderr)
        return 124


if __name__ == "__main__":
    raise SystemExit(main())
