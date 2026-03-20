import json
import urllib.request
from typing import Any


class GitHubPRClient:
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

    def get_repo(self, repo: str) -> dict:
        url = f"https://api.github.com/repos/{repo}"
        return self._request_json("GET", url)

    def create_pull_request(
        self,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str,
        draft: bool = True,
    ) -> dict:
        url = f"https://api.github.com/repos/{repo}/pulls"
        payload = {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
            "draft": draft,
        }
        return self._request_json("POST", url, payload)
