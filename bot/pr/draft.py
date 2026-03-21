import subprocess
import time
from dataclasses import dataclass
import os

from bot.github.github_client import GitHubPRClient


@dataclass
class DraftPRResult:
    branch: str
    pr_url: str


def _run_git(args: list[str], cwd: str, input_text: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        input=input_text,
        capture_output=True,
    )


def _ensure_git_repo(repo_path: str) -> None:
    check = _run_git(["git", "rev-parse", "--is-inside-work-tree"], repo_path)
    if check.returncode != 0 or check.stdout.strip() != "true":
        raise RuntimeError("Not a git repository")


def _current_branch(repo_path: str) -> str:
    result = _run_git(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_path)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Failed to get current branch")
    return result.stdout.strip()


def _ensure_git_identity(repo_path: str) -> None:
    name = (
        os.getenv("GIT_AUTHOR_NAME")
        or os.getenv("GIT_COMMITTER_NAME")
        or os.getenv("GITHUB_ACTOR")
        or "AlphaPatch Bot"
    )
    email = (
        os.getenv("GIT_AUTHOR_EMAIL")
        or os.getenv("GIT_COMMITTER_EMAIL")
        or (
            f"{os.getenv('GITHUB_ACTOR')}@users.noreply.github.com"
            if os.getenv("GITHUB_ACTOR")
            else None
        )
        or "alphapatch-bot@users.noreply.github.com"
    )
    _run_git(["git", "config", "user.name", name], repo_path)
    _run_git(["git", "config", "user.email", email], repo_path)


def _push_branch(repo_path: str, repo: str, branch: str, token: str) -> None:
    remote_url = f"https://x-access-token:{token}@github.com/{repo}.git"
    push = _run_git(["git", "push", remote_url, branch], repo_path)
    if push.returncode != 0:
        raise RuntimeError(push.stderr.strip() or "git push failed")


def create_draft_pr_from_diff(
    repo_path: str,
    repo: str,
    diff_text: str,
    title: str,
    body: str,
    token: str,
) -> DraftPRResult:
    if not diff_text.strip():
        raise ValueError("Diff is empty")

    _ensure_git_repo(repo_path)
    original_branch = _current_branch(repo_path)
    branch = f"alphapatch/{int(time.time())}"

    try:
        checkout = _run_git(["git", "checkout", "-b", branch], repo_path)
        if checkout.returncode != 0:
            raise RuntimeError(checkout.stderr.strip() or "git checkout -b failed")

        _ensure_git_identity(repo_path)

        apply = _run_git(["git", "apply", "-"], repo_path, input_text=diff_text)
        if apply.returncode != 0:
            raise RuntimeError(apply.stderr.strip() or "git apply failed")

        add = _run_git(["git", "add", "-A"], repo_path)
        if add.returncode != 0:
            raise RuntimeError(add.stderr.strip() or "git add failed")

        commit = _run_git(["git", "commit", "-m", title], repo_path)
        if commit.returncode != 0:
            raise RuntimeError(commit.stderr.strip() or "git commit failed")

        _push_branch(repo_path, repo, branch, token)

        client = GitHubPRClient(token)
        repo_info = client.get_repo(repo)
        base = repo_info.get("default_branch", original_branch)
        pr = client.create_pull_request(repo, title, body, head=branch, base=base, draft=True)

        return DraftPRResult(branch=branch, pr_url=pr.get("html_url", ""))
    finally:
        _run_git(["git", "checkout", original_branch], repo_path)
