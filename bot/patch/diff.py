import re


_DIFF_HEADER_RE = re.compile(r"^(diff --git|---\s|\+\+\+\s)")


def is_valid_unified_diff(text: str) -> bool:
    if not text:
        return False
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return False
    return any(_DIFF_HEADER_RE.match(line) for line in lines[:5])


def trim_diff(text: str, max_lines: int = 120) -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    return "\n".join(lines[:max_lines]) + "\n..."
