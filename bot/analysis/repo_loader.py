from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".cs",
    ".rb",
    ".php",
    ".swift",
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
}

EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}


@dataclass
class RepoFile:
    path: str
    content: str


def load_repo_files(
    root: str,
    max_files: int = 50,
    max_chars_per_file: int = 4000,
    extensions: Iterable[str] | None = None,
) -> list[RepoFile]:
    root_path = Path(root).resolve()
    allowed_ext = set(extensions or DEFAULT_EXTENSIONS)

    files: list[RepoFile] = []
    for path in root_path.rglob("*"):
        if len(files) >= max_files:
            break
        if path.is_dir():
            if path.name in EXCLUDE_DIRS:
                continue
            continue
        if path.suffix and path.suffix not in allowed_ext:
            continue
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if not content.strip():
            continue
        if len(content) > max_chars_per_file:
            content = content[:max_chars_per_file] + "\n..."
        files.append(RepoFile(path=str(path.relative_to(root_path)), content=content))

    return files
