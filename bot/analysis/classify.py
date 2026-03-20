from bot.github.models import Issue


BUG_KEYWORDS = [
    "bug",
    "error",
    "exception",
    "traceback",
    "stack trace",
    "crash",
    "fails",
    "failure",
    "broken",
    "regression",
]

FEATURE_KEYWORDS = [
    "feature",
    "enhancement",
    "request",
    "proposal",
    "improvement",
    "support",
]

QUESTION_KEYWORDS = [
    "question",
    "how do i",
    "how to",
    "help",
    "clarify",
    "what is",
    "why",
]


def classify_issue(issue: Issue) -> str:
    text = f"{issue.title}\n{issue.body}".lower()

    if any(k in text for k in BUG_KEYWORDS):
        return "bug"
    if any(k in text for k in FEATURE_KEYWORDS):
        return "feature"
    if any(k in text for k in QUESTION_KEYWORDS):
        return "question"

    return "question"
