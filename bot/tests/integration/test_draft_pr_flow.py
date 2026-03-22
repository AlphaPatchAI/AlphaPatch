import os
import subprocess
import tempfile
import unittest

import bot.pr.draft as draft


class _DummyGitHubClient:
    def __init__(self, token: str):
        self.token = token

    def get_repo(self, repo: str) -> dict:
        return {"default_branch": "main"}

    def create_pull_request(self, repo: str, title: str, body: str, head: str, base: str, draft: bool = True) -> dict:
        return {"html_url": f"https://example.com/{repo}/pull/1"}


def _run_git(args, cwd, input_text=None):
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        input=input_text,
        capture_output=True,
        check=True,
    )


def _init_repo(path: str) -> None:
    _run_git(["init"], path)
    _run_git(["config", "user.name", "Test Bot"], path)
    _run_git(["config", "user.email", "test@example.com"], path)
    with open(os.path.join(path, "base.txt"), "w", encoding="utf-8") as fh:
        fh.write("base\n")
    _run_git(["add", "base.txt"], path)
    _run_git(["commit", "-m", "init"], path)


def _create_diff(path: str) -> str:
    with open(os.path.join(path, "test.txt"), "w", encoding="utf-8") as fh:
        fh.write("hello\n")
    result = _run_git(["diff"], path)
    return result.stdout


class DraftPRFlowTest(unittest.TestCase):
    def test_create_draft_pr_from_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            _init_repo(tmp)
            diff_text = _create_diff(tmp)

            # Patch network-dependent pieces
            original_client = draft.GitHubPRClient
            original_push = draft._push_branch
            try:
                draft.GitHubPRClient = _DummyGitHubClient
                draft._push_branch = lambda *args, **kwargs: None

                result = draft.create_draft_pr_from_diff(
                    repo_path=tmp,
                    repo="owner/repo",
                    diff_text=diff_text,
                    title="Test PR",
                    body="Body",
                    token="test-token",
                )
                self.assertTrue(result.pr_url.startswith("https://example.com/"))
            finally:
                draft.GitHubPRClient = original_client
                draft._push_branch = original_push


if __name__ == "__main__":
    unittest.main()
