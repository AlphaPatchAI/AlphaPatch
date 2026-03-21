import shutil
import subprocess
import tempfile


EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}


def _copy_repo(src: str, dst: str) -> None:
    def _ignore(path, names):
        return {name for name in names if name in EXCLUDE_DIRS}

    shutil.copytree(src, dst, ignore=_ignore, dirs_exist_ok=True)


def run_tests_in_temp(repo_path: str, diff_text: str, command: str, timeout: int) -> tuple[bool, str]:
    if not command:
        return True, "No test command configured"

    with tempfile.TemporaryDirectory() as tmp:
        _copy_repo(repo_path, tmp)
        try:
            apply = subprocess.run(
                ["git", "apply", "-"],
                input=diff_text,
                text=True,
                cwd=tmp,
                capture_output=True,
            )
            if apply.returncode != 0:
                return False, apply.stderr.strip() or "git apply failed"

            result = subprocess.run(
                command,
                shell=True,
                text=True,
                cwd=tmp,
                capture_output=True,
                timeout=timeout,
            )
        except FileNotFoundError:
            return False, "git not available to apply patch"
        except subprocess.TimeoutExpired:
            return False, f"Tests timed out after {timeout}s"

    output = (result.stdout or "") + "\n" + (result.stderr or "")
    output = output.strip()
    if result.returncode == 0:
        return True, output[-2000:]
    return False, output[-2000:]
