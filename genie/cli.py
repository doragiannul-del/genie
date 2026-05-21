from __future__ import annotations

import argparse
import sys

from genie.ai import get_command
from genie.config import load_config
from genie.formatter import format_output


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="genie",
        description="Turn plain English into shell commands.",
    )
    parser.add_argument(
        "prompt", nargs="+", help="What you want to do, in plain English."
    )
    parser.add_argument(
        "--linux",
        action="store_true",
        help="Generate a Linux command instead of macOS (default).",
    )
    args = parser.parse_args()

    try:
        config = load_config()
        result = get_command(" ".join(args.prompt), config, linux=args.linux)
        print(format_output(result))
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
