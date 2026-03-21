from pathlib import Path

from bot.analysis.classify import classify_issue
from bot.analysis.context import select_relevant_files
from bot.analysis.language import detect_primary_language
from bot.analysis.repo_loader import load_repo_files
from bot.analysis.summarize import summarize_issue
from bot.github.models import Issue
from bot.llm.providers import LLMProvider


_PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "issue_analysis.txt"


def _load_prompt_template() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _format_context(context_files) -> str:
    if not context_files:
        return "(No relevant files found.)"
    blocks = []
    for item in context_files:
        blocks.append(f"- {item.path}\n{item.snippet}")
    return "\n\n".join(blocks)


def analyze_issue(issue: Issue, provider: LLMProvider, repo_path: str) -> dict:
    classification = classify_issue(issue)
    summary = summarize_issue(issue)

    repo_files = load_repo_files(repo_path)
    language = detect_primary_language(issue, repo_files)
    context_files = select_relevant_files(f"{issue.title}\n{issue.body}", repo_files)

    prompt_template = _load_prompt_template()
    prompt = prompt_template.format(
        classification=classification,
        language=language,
        title=issue.title,
        author=issue.author or "unknown",
        body=summary,
        context=_format_context(context_files),
    )

    response_text = provider.generate(prompt)

    return {
        "classification": classification,
        "language": language,
        "summary": summary,
        "response": response_text,
        "context_files": context_files,
    }
