from dataclasses import dataclass
import os


@dataclass
class Config:
    github_token: str
    llm_provider: str
    openai_api_key: str | None
    openai_model: str | None
    openai_base_url: str


def load_config() -> Config:
    github_token = os.getenv("GITHUB_TOKEN", "")
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL")
    openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/responses")

    return Config(
        github_token=github_token,
        llm_provider=llm_provider,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        openai_base_url=openai_base_url,
    )
