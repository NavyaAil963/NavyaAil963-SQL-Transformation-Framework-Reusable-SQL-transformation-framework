"""
core/registry.py
----------------
Manages discovery and resolution of SQL transformation templates.
Transforms are stored as .sql files under the transformations/ directory
and resolved by their relative path key (e.g., "cleaning/deduplication").
"""

import re
from pathlib import Path
from typing import Any


class TransformationRegistry:
    """
    Loads, caches, and renders SQL transformation templates.

    Templates support simple {{param}} placeholder substitution,
    making them configurable without hardcoded values.
    """

    def __init__(self, transformations_dir: str = "transformations"):
        self.base_dir = Path(transformations_dir)
        self._cache: dict[str, str] = {}

        if not self.base_dir.exists():
            raise FileNotFoundError(f"Transformations directory not found: {self.base_dir}")

    def resolve(self, key: str, source: str, params: dict[str, Any] = None) -> str:
        """
        Resolve a transformation key to rendered SQL.

        Args:
            key:    Relative path to the .sql file, e.g. "cleaning/deduplication"
            source: The current source table name to inject into the template
            params: Optional dict of additional template parameters

        Returns:
            Rendered SQL string ready for execution.
        """
        template = self._load(key)
        context = {"source": source, **(params or {})}
        return self._render(template, context)

    def list_transforms(self) -> list[str]:
        """Return all available transformation keys."""
        return [
            str(p.relative_to(self.base_dir)).replace(".sql", "").replace("\\", "/")
            for p in self.base_dir.rglob("*.sql")
        ]

    def _load(self, key: str) -> str:
        """Load and cache a SQL template file."""
        if key in self._cache:
            return self._cache[key]

        path = self.base_dir / f"{key}.sql"
        if not path.exists():
            available = self.list_transforms()
            raise FileNotFoundError(
                f"Transformation '{key}' not found.\n"
                f"Available transformations:\n" + "\n".join(f"  - {t}" for t in available)
            )

        template = path.read_text(encoding="utf-8")
        self._cache[key] = template
        return template

    def _render(self, template: str, context: dict[str, Any]) -> str:
        """
        Simple {{placeholder}} substitution in SQL templates.
        Lists are converted to comma-separated SQL strings.
        """
        def replacer(match):
            key = match.group(1).strip()
            if key not in context:
                raise KeyError(f"Missing template parameter: '{key}'")
            value = context[key]
            if isinstance(value, list):
                return ", ".join(str(v) for v in value)
            return str(value)

        return re.sub(r"\{\{\s*(\w+)\s*\}\}", replacer, template)
