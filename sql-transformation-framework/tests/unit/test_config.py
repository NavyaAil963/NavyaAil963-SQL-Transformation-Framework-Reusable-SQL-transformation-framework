"""
tests/unit/test_config.py
--------------------------
Unit tests for FrameworkConfig.
"""

import os
import pytest
import yaml
from pathlib import Path

from core.config import FrameworkConfig


@pytest.fixture
def temp_config(tmp_path):
    config_data = {
        "database": {
            "adapter": "postgres",
            "host": "localhost",
            "port": 5432,
        },
        "execution": {
            "fail_fast": True,
        }
    }
    config_file = tmp_path / "settings.yaml"
    config_file.write_text(yaml.dump(config_data))
    return str(config_file)


class TestFrameworkConfig:

    def test_get_nested_key(self, temp_config):
        config = FrameworkConfig(temp_config)
        assert config.get("database.adapter") == "postgres"
        assert config.get("database.port") == 5432

    def test_get_default(self, temp_config):
        config = FrameworkConfig(temp_config)
        assert config.get("database.missing_key", "fallback") == "fallback"

    def test_env_override(self, temp_config, monkeypatch):
        monkeypatch.setenv("STF_DATABASE__HOST", "prod-db-host")
        config = FrameworkConfig(temp_config)
        assert config.get("database.host") == "prod-db-host"

    def test_missing_config_file(self):
        with pytest.raises(FileNotFoundError):
            FrameworkConfig("nonexistent/path.yaml")

    def test_top_level_key(self, temp_config):
        config = FrameworkConfig(temp_config)
        db = config.get("database")
        assert isinstance(db, dict)
        assert db["adapter"] == "postgres"
