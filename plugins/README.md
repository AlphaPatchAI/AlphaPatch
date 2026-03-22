# AlphaPatch Plugins

Drop a `*.py` file in this directory to customize behavior.

Required shape:
- Export a `Plugin` class that extends `bot.plugins.base.Plugin`.

Hooks:
- `after_analysis(analysis: dict) -> dict`
- `after_patch(diff_text: str) -> str`
- `after_response(response_text: str) -> str`
