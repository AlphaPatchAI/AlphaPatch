#!/usr/bin/env python3
import argparse
import os
import re

from bot.analysis.analyzer import analyze_issue
from bot.config import load_config
from bot.github.client import GitHubClient
from bot.llm import EchoProvider, OpenAIProvider


def parse_args():
    parser = argparse.ArgumentParser(description="AlphaPatch bot entry point")
    parser.add_argument("--repo", required=True, help="GitHub repository in owner/name form")
    parser.add_argument("--issue", required=True, help="Issue number or URL")
    return parser.parse_args()


def _parse_issue_number(value: str) -> int:
    if value.isdigit():
        return int(value)
    match = re.search(r"/issues/(\d+)", value)
    if match:
        return int(match.group(1))
    raise ValueError("--issue must be a number or issue URL")


def _select_provider(config):
    provider = config.llm_provider.lower()
    if provider == "openai":
        return OpenAIProvider(
            api_key=config.openai_api_key or "",
            model=config.openai_model or "",
            base_url=config.openai_base_url,
        )
    if provider == "echo":
        return EchoProvider()
    raise ValueError(f"Unsupported LLM_PROVIDER: {config.llm_provider}")


def main():
    args = parse_args()
    issue_number = _parse_issue_number(args.issue)

    config = load_config()
    gh = GitHubClient(config.github_token)

    issue = gh.get_issue(args.repo, issue_number)

    provider = _select_provider(config)
    repo_path = os.getenv("GITHUB_WORKSPACE", os.getcwd())
    result = analyze_issue(issue, provider, repo_path)

    body = (
        "AlphaPatch response:\n\n"
        f"**Classification:** {result['classification']}\n"
        f"**Summary:** {result['summary']}\n\n"
        f"{result['response']}\n\n"
        "_To change the LLM provider, set `LLM_PROVIDER`._"
    )
    gh.create_comment(args.repo, issue_number, body)


if __name__ == "__main__":
    main()
