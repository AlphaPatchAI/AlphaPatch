"""Compatibility wrapper for patch proposals."""

from bot.github.models import Issue
from bot.llm.providers import LLMProvider
from bot.patch.generator import generate_patch


def propose_patch(
    issue: Issue,
    context_files,
    provider: LLMProvider,
    feedback: str | None = None,
) -> str:
    """Generate a patch proposal (unified diff)."""
    return generate_patch(issue, context_files, provider, feedback=feedback)
