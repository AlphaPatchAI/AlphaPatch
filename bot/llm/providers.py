import json
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass
class OpenAIProvider:
    api_key: str
    model: str
    base_url: str = "https://api.openai.com/v1/responses"

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
        if not self.model:
            raise ValueError("OPENAI_MODEL is required for OpenAI provider")

        payload = {
            "model": self.model,
            "input": prompt,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")

        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            response = json.loads(raw)

        return _extract_text_from_response(response)


@dataclass
class GeminiProvider:
    api_key: str
    model: str
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini provider")
        if not self.model:
            raise ValueError("GEMINI_MODEL is required for Gemini provider")

        url = f"{self.base_url}/{self.model}:generateContent"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("x-goog-api-key", self.api_key)

        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            response = json.loads(raw)

        return _extract_text_from_gemini_response(response)


@dataclass
class EchoProvider:
    def generate(self, prompt: str) -> str:
        return (
            "Thanks for the issue report. "
            "I reviewed the details and will follow up with suggested next steps soon."
        )


def _extract_text_from_response(response: dict) -> str:
    output = response.get("output", [])
    for item in output:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content.get("text", "").strip()
    return "(No response text returned by model.)"


def _extract_text_from_gemini_response(response: dict) -> str:
    candidates = response.get("candidates", [])
    if not candidates:
        return "(No response candidates returned by Gemini.)"
    content = candidates[0].get("content", {})
    parts = content.get("parts", [])
    if not parts:
        return "(No response parts returned by Gemini.)"
    return (parts[0].get("text") or "").strip() or "(Empty response text from Gemini.)"
