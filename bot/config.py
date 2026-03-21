from dataclasses import dataclass
import os


@dataclass
class Config:
    github_token: str
    llm_provider: str
    openai_api_key: str | None
    openai_model: str | None
    openai_base_url: str
    test_command: str
    test_timeout: int
    enable_labels: bool
    enable_draft_pr: bool


def load_config() -> Config:
    github_token = os.getenv("GITHUB_TOKEN", "")
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL")
    openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/responses")
    test_command = os.getenv("TEST_COMMAND", "").strip()
    test_timeout = int(os.getenv("TEST_TIMEOUT", "600"))
    enable_labels = os.getenv("ENABLE_LABELS", "0") == "1"
    enable_draft_pr = os.getenv("ENABLE_DRAFT_PR", "0") == "1"

    return Config(
        github_token=github_token,
        llm_provider=llm_provider,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        openai_base_url=openai_base_url,
        test_command=test_command,
        test_timeout=test_timeout,
        enable_labels=enable_labels,
        enable_draft_pr=enable_draft_pr,
    )
