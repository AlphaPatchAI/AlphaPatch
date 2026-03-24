"""Utilities for posting GitHub issue comments."""

from bot.github.client import GitHubClient


def post_issue_comment(repo: str, issue_number: int, body: str, token: str) -> None:
    """Post a comment to a GitHub issue."""
    client = GitHubClient(token)
    client.create_comment(repo, issue_number, body)
