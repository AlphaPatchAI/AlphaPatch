import json
import urllib.request
from typing import Any

from bot.github.models import Issue


class GitHubClient:
    def __init__(self, token: str):
        if not token:
            raise ValueError("GITHUB_TOKEN is required")
        self._token = token

    def _request_json(self, method: str, url: str, body: dict | None = None) -> Any:
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("Authorization", f"Bearer {self._token}")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        if body is not None:
            req.add_header("Content-Type", "application/json")

        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None

    def get_issue(self, repo: str, issue_number: int) -> Issue:
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
        data = self._request_json("GET", url)
        return Issue(
            number=data["number"],
            title=data.get("title", ""),
            body=data.get("body", ""),
            url=data.get("html_url", ""),
            author=(data.get("user") or {}).get("login"),
        )

    def create_comment(self, repo: str, issue_number: int, body: str) -> None:
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
        self._request_json("POST", url, {"body": body})
