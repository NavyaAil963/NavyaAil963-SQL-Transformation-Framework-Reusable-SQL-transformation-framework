"""
tests/unit/test_registry.py
---------------------------
Unit tests for the TransformationRegistry.
Tests template loading, rendering, and error handling.
"""

import pytest
import tempfile
import os
from pathlib import Path

from core.registry import TransformationRegistry


@pytest.fixture
def temp_registry(tmp_path):
    """Create a temporary transformations directory with test SQL files."""
    # cleaning/dedup.sql
    cleaning_dir = tmp_path / "cleaning"
    cleaning_dir.mkdir()
    (cleaning_dir / "deduplication.sql").write_text(
        "SELECT * FROM {{source}} WHERE id IN (SELECT MIN(id) FROM {{source}} GROUP BY {{unique_key}})"
    )

    # validation/not_null.sql
    validation_dir = tmp_path / "validation"
    validation_dir.mkdir()
    (validation_dir / "not_null_check.sql").write_text(
        "SELECT * FROM {{source}} WHERE {{columns}} IS NOT NULL"
    )

    return TransformationRegistry(transformations_dir=str(tmp_path))


class TestTransformationRegistry:

    def test_resolve_basic(self, temp_registry):
        """Should render SQL with source and params correctly."""
        sql = temp_registry.resolve(
            "cleaning/deduplication",
            source="raw.orders",
            params={"unique_key": "order_id"},
        )
        assert "raw.orders" in sql
        assert "order_id" in sql
        assert "{{" not in sql   # No unresolved placeholders

    def test_resolve_missing_transform(self, temp_registry):
        """Should raise FileNotFoundError for unknown transforms."""
        with pytest.raises(FileNotFoundError, match="not found"):
            temp_registry.resolve("nonexistent/transform", source="raw.table")

    def test_resolve_missing_param(self, temp_registry):
        """Should raise KeyError when a required param is missing."""
        with pytest.raises(KeyError, match="unique_key"):
            temp_registry.resolve(
                "cleaning/deduplication",
                source="raw.orders",
                params={},  # missing unique_key
            )

    def test_list_transforms(self, temp_registry):
        """Should list all available transforms."""
        transforms = temp_registry.list_transforms()
        assert "cleaning/deduplication" in transforms
        assert "validation/not_null_check" in transforms

    def test_caching(self, temp_registry):
        """Same template should be loaded once and cached."""
        sql1 = temp_registry.resolve("validation/not_null_check", source="t", params={"columns": "id"})
        sql2 = temp_registry.resolve("validation/not_null_check", source="t", params={"columns": "id"})
        assert sql1 == sql2
        assert "validation/not_null_check" in temp_registry._cache

    def test_list_param_rendered(self, temp_registry):
        """List params should be joined as comma-separated strings."""
        sql = temp_registry.resolve(
            "validation/not_null_check",
            source="raw.orders",
            params={"columns": ["col_a", "col_b", "col_c"]},
        )
        assert "col_a, col_b, col_c" in sql
