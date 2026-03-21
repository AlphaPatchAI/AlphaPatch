from __future__ import annotations

from collections import Counter

from bot.analysis.repo_loader import RepoFile
from bot.github.models import Issue


EXTENSION_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
}

LANGUAGE_HINTS = {
    "python": ["python", "pip", "pytest"],
    "javascript": ["javascript", "node", "npm", "yarn", "pnpm"],
    "typescript": ["typescript", "tsc"],
    "go": ["golang", "go mod"],
    "rust": ["cargo", "rust"],
    "java": ["gradle", "maven", "java"],
    "kotlin": ["kotlin"],
    "csharp": ["c#", "dotnet"],
    "ruby": ["ruby", "bundler"],
    "php": ["composer", "php"],
    "swift": ["swift"],
}


def detect_primary_language(issue: Issue, files: list[RepoFile]) -> str:
    counter: Counter[str] = Counter()

    for file in files:
        for ext, lang in EXTENSION_LANGUAGE.items():
            if file.path.endswith(ext):
                counter[lang] += 1
                break

    text = f"{issue.title}\n{issue.body}".lower()
    for lang, hints in LANGUAGE_HINTS.items():
        if any(hint in text for hint in hints):
            counter[lang] += 2

    if not counter:
        return "unknown"

    return counter.most_common(1)[0][0]
