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
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    examples:
    $ genie compress output.txt and move it to root
    → gzip output.txt && mv output.txt.gz /

    breakdown:
        gzip output.txt       → compress the file
        mv output.txt.gz /    → move archive to root

    $ genie --linux find all files modified in the last 7 days
    → find . -mtime -7 -type f

    breakdown:
        find .      → search from current directory
        -mtime -7   → modified in the last 7 days
        -type f     → files only
        """,
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
