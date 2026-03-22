from __future__ import annotations

from typing import Any


class Plugin:
    name = "base"

    def after_analysis(self, analysis: dict) -> dict:
        return analysis

    def after_patch(self, diff_text: str) -> str:
        return diff_text

    def after_response(self, response_text: str) -> str:
        return response_text
