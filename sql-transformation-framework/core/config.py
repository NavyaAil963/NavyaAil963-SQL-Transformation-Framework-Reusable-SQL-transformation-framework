"""
core/config.py
--------------
Loads and provides access to the framework configuration from a YAML file,
with support for environment variable overrides via a .env file.
"""

import os
import yaml
from pathlib import Path
from typing import Any


class FrameworkConfig:
    """
    Loads settings from a YAML config file.
    Supports dot-notation access: config.get("database.host")
    Environment variables prefixed with STF_ override YAML values.

    Example:
        STF_DATABASE__HOST=localhost overrides database.host
    """

    def __init__(self, config_path: str = "config/settings.yaml"):
        self._config = self._load(config_path)
        self._apply_env_overrides()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Access config with dot notation.

        Args:
            key: Dot-separated key path, e.g. "database.host"
            default: Fallback value if key is missing

        Returns:
            The config value or default.
        """
        keys = key.split(".")
        value = self._config
        for k in keys:
            if not isinstance(value, dict) or k not in value:
                return default
            value = value[k]
        return value

    def _load(self, path: str) -> dict:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(p) as f:
            return yaml.safe_load(f) or {}

    def _apply_env_overrides(self):
        """
        Override config values with environment variables.
        Format: STF_SECTION__KEY=value → config["section"]["key"] = value
        """
        prefix = "STF_"
        for env_key, env_val in os.environ.items():
            if env_key.startswith(prefix):
                path = env_key[len(prefix):].lower().split("__")
                self._set_nested(self._config, path, env_val)

    def _set_nested(self, d: dict, keys: list, value: str):
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value
