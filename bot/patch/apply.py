import os
import shutil
import subprocess
import tempfile


EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}


def _copy_repo(src: str, dst: str) -> None:
    def _ignore(path, names):
        return {name for name in names if name in EXCLUDE_DIRS}

    shutil.copytree(src, dst, ignore=_ignore, dirs_exist_ok=True)


def apply_patch_in_temp(repo_path: str, diff_text: str) -> tuple[bool, str]:
    if not diff_text.strip():
        return False, "Empty diff"

    with tempfile.TemporaryDirectory() as tmp:
        _copy_repo(repo_path, tmp)
        try:
            check = subprocess.run(
                ["git", "apply", "--check", "-"],
                input=diff_text,
                text=True,
                cwd=tmp,
                capture_output=True,
            )
            if check.returncode != 0:
                return False, check.stderr.strip() or "git apply --check failed"

            apply = subprocess.run(
                ["git", "apply", "-"],
                input=diff_text,
                text=True,
                cwd=tmp,
                capture_output=True,
            )
            if apply.returncode != 0:
                return False, apply.stderr.strip() or "git apply failed"
        except FileNotFoundError:
            return False, "git not available to apply patch"

    return True, "applied"
