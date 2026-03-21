from __future__ import annotations

from bot.patch.diff import is_valid_unified_diff


def _count_changed_lines(diff_text: str) -> int:
    count = 0
    for line in diff_text.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+") or line.startswith("-"):
            count += 1
    return count


def compute_confidence(diff_text: str, patch_applied: bool, tests_passed: bool | None) -> tuple[int, str]:
    if not diff_text.strip():
        return 0, "low"

    score = 30
    if is_valid_unified_diff(diff_text):
        score += 10
    if patch_applied:
        score += 20

    changed_lines = _count_changed_lines(diff_text)
    if changed_lines <= 50:
        score += 10
    elif changed_lines > 200:
        score -= 20

    if tests_passed is True:
        score += 20
    elif tests_passed is False:
        score -= 20

    score = max(0, min(100, score))
    if score >= 80:
        level = "high"
    elif score >= 50:
        level = "medium"
    else:
        level = "low"

    return score, level
