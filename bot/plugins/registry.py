from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Iterable

from bot.plugins.base import Plugin


def _load_plugin_from_file(path: Path) -> Plugin | None:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    plugin_cls = getattr(module, "Plugin", None)
    if plugin_cls is None:
        return None
    instance = plugin_cls()
    if not isinstance(instance, Plugin):
        return None
    return instance


def load_plugins(plugin_dir: str) -> list[Plugin]:
    path = Path(plugin_dir)
    if not path.exists() or not path.is_dir():
        return []

    plugins: list[Plugin] = []
    for file in path.glob("*.py"):
        if file.name.startswith("_"):
            continue
        plugin = _load_plugin_from_file(file)
        if plugin:
            plugins.append(plugin)
    return plugins


def apply_after_analysis(plugins: Iterable[Plugin], analysis: dict) -> dict:
    result = analysis
    for plugin in plugins:
        result = plugin.after_analysis(result)
    return result


def apply_after_patch(plugins: Iterable[Plugin], diff_text: str) -> str:
    result = diff_text
    for plugin in plugins:
        result = plugin.after_patch(result)
    return result


def apply_after_response(plugins: Iterable[Plugin], response_text: str) -> str:
    result = response_text
    for plugin in plugins:
        result = plugin.after_response(result)
    return result
