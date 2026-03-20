from bot.github.models import Issue


def summarize_issue(issue: Issue, max_chars: int = 280) -> str:
    body = (issue.body or "").strip().replace("\r\n", "\n")
    if not body:
        return "No issue body provided."
    summary = body.split("\n\n")[0].strip()
    if len(summary) > max_chars:
        return summary[: max_chars - 3].rstrip() + "..."
    return summary
