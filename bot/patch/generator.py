from pathlib import Path

from bot.github.models import Issue
from bot.llm.providers import LLMProvider


_PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "patch_generation.txt"


def _load_prompt_template() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _format_context(context_files) -> str:
    if not context_files:
        return "(No relevant files found.)"
    blocks = []
    for item in context_files:
        blocks.append(f"- {item.path}\n{item.snippet}")
    return "\n\n".join(blocks)


def generate_patch(issue: Issue, context_files, provider: LLMProvider) -> str:
    prompt_template = _load_prompt_template()
    prompt = prompt_template.format(
        title=issue.title,
        body=issue.body or "",
        context=_format_context(context_files),
    )
    return provider.generate(prompt)
