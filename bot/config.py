from dataclasses import dataclass
import os


@dataclass
class Config:
    github_token: str
    llm_provider: str
    openai_api_key: str | None
    openai_model: str | None
    openai_base_url: str
    gemini_api_key: str | None
    gemini_model: str | None
    gemini_base_url: str
    test_command: str
    test_timeout: int
    enable_labels: bool
    enable_draft_pr: bool
    patch_retry_attempts: int


def load_config() -> Config:
    github_token = os.getenv("GITHUB_TOKEN", "")
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL")
    openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/responses")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL")
    gemini_base_url = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/models")
    test_command = os.getenv("TEST_COMMAND", "").strip()
    test_timeout = int(os.getenv("TEST_TIMEOUT", "600"))
    enable_labels = os.getenv("ENABLE_LABELS", "0") == "1"
    enable_draft_pr = os.getenv("ENABLE_DRAFT_PR", "1") == "1"
    patch_retry_attempts = int(os.getenv("PATCH_RETRY_ATTEMPTS", "2"))

    return Config(
        github_token=github_token,
        llm_provider=llm_provider,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        openai_base_url=openai_base_url,
        gemini_api_key=gemini_api_key,
        gemini_model=gemini_model,
        gemini_base_url=gemini_base_url,
        test_command=test_command,
        test_timeout=test_timeout,
        enable_labels=enable_labels,
        enable_draft_pr=enable_draft_pr,
        patch_retry_attempts=patch_retry_attempts,
    )


def validate_config(config: Config) -> None:
    missing: list[str] = []
    if not config.github_token:
        missing.append("GITHUB_TOKEN")

    provider = config.llm_provider.lower()
    if provider == "openai":
        if not config.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if not config.openai_model:
            missing.append("OPENAI_MODEL")
    elif provider == "gemini":
        if not config.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        if not config.gemini_model:
            missing.append("GEMINI_MODEL")

    if missing:
        raise ValueError("Missing required env vars: " + ", ".join(missing))
