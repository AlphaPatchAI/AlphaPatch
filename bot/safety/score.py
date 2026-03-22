from __future__ import annotations

from dataclasses import dataclass

from bot.patch.diff import is_valid_unified_diff


@dataclass
class DiffStats:
    files: int
    additions: int
    deletions: int
    new_files: int
    removed_files: int
    touches_tests: bool
    touches_lockfiles: bool
    has_binary: bool


def _analyze_diff(diff_text: str) -> DiffStats:
    files = 0
    additions = 0
    deletions = 0
    new_files = 0
    removed_files = 0
    touches_tests = False
    touches_lockfiles = False
    has_binary = "GIT binary patch" in diff_text

    current_path = ""
    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            files += 1
            parts = line.split(" ")
            if len(parts) >= 4:
                current_path = parts[3].replace("b/", "", 1)
            else:
                current_path = ""

            lower = current_path.lower()
            if "test" in lower or "spec" in lower:
                touches_tests = True
            if lower.endswith(("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock")):
                touches_lockfiles = True
            continue

        if line.startswith("--- ") and line.strip().endswith("/dev/null"):
            new_files += 1
        elif line.startswith("+++ ") and line.strip().endswith("/dev/null"):
            removed_files += 1

        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            additions += 1
        elif line.startswith("-"):
            deletions += 1

    return DiffStats(
        files=files,
        additions=additions,
        deletions=deletions,
        new_files=new_files,
        removed_files=removed_files,
        touches_tests=touches_tests,
        touches_lockfiles=touches_lockfiles,
        has_binary=has_binary,
    )


def compute_confidence(diff_text: str, patch_applied: bool, tests_passed: bool | None) -> tuple[int, str]:
    if not diff_text.strip():
        return 0, "low"

    stats = _analyze_diff(diff_text)
    lines_changed = stats.additions + stats.deletions

    score = 20
    if is_valid_unified_diff(diff_text):
        score += 10
    if patch_applied:
        score += 25

    if lines_changed <= 50:
        score += 12
    elif lines_changed <= 150:
        score += 6
    elif lines_changed <= 400:
        score -= 4
    else:
        score -= 15

    if stats.files <= 3:
        score += 5
    elif stats.files > 8:
        score -= 10

    if stats.new_files <= 1:
        score += 3
    elif stats.new_files > 3:
        score -= 6

    if stats.removed_files > 0 and stats.additions == 0:
        score -= 6

    if stats.touches_tests:
        score += 5
    if stats.touches_lockfiles:
        score -= 5
    if stats.has_binary:
        score -= 30

    if tests_passed is True:
        score += 20
    elif tests_passed is False:
        score -= 25

    score = max(0, min(100, score))
    if score >= 80:
        level = "high"
    elif score >= 50:
        level = "medium"
    else:
        level = "low"

    return score, level
