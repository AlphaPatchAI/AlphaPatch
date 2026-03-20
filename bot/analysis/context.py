import re
from dataclasses import dataclass

from bot.analysis.repo_loader import RepoFile


@dataclass
class ContextFile:
    path: str
    snippet: str
    score: int


def _tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z_]{2,}", text.lower())
    return set(tokens)


def select_relevant_files(issue_text: str, files: list[RepoFile], max_files: int = 5) -> list[ContextFile]:
    issue_tokens = _tokenize(issue_text)
    ranked: list[ContextFile] = []

    for repo_file in files:
        haystack = f"{repo_file.path}\n{repo_file.content[:2000]}".lower()
        score = sum(1 for token in issue_tokens if token in haystack)
        if score == 0:
            continue
        snippet = repo_file.content[:600].rstrip()
        ranked.append(ContextFile(path=repo_file.path, snippet=snippet, score=score))

    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked[:max_files]
