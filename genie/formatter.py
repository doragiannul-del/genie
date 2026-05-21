from __future__ import annotations


def format_output(result: dict) -> str:
    """Format the AI response into a command + breakdown for display

    Example output:
        find . -name "*.pdf"

        # Breakdown:
        # find .        →  search from current directory
        # -name "*.pdf" →  match PDF files
    """
    command = result["command"]
    breakdown = result["breakdown"]

    # pad to the longest part so all → arrows align vertically
    pad = max(len(item["part"]) for item in breakdown)

    lines = [
        command,
        "",
        "# Breakdown:",
    ]

    for item in breakdown:
        lines.append(f"# {item['part']:<{pad}}  →  {item['explanation']}")

    return "\n".join(lines)
