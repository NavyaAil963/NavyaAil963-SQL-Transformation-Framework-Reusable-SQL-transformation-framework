"""
core/engine.py
--------------
Pipeline orchestration engine for the SQL Transformation Framework.
Loads pipeline configs, resolves transformation steps, and executes them
in sequence against the configured database connection.
"""

import time
import yaml
import logging
from pathlib import Path
from typing import Any

from core.registry import TransformationRegistry
from core.logger import get_logger
from core.config import FrameworkConfig


class PipelineEngine:
    """
    Orchestrates the execution of a full ETL pipeline defined in YAML.

    Usage:
        engine = PipelineEngine(config_path="config/settings.yaml")
        engine.run("pipelines/ecommerce/orders_pipeline.yaml")
    """

    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = FrameworkConfig(config_path)
        self.registry = TransformationRegistry(
            transformations_dir=self.config.get("transformations_dir", "transformations")
        )
        self.logger = get_logger("PipelineEngine")
        self.db = self._connect()

    def _connect(self):
        """Establish a database connection based on config."""
        adapter = self.config.get("database.adapter", "postgres")
        self.logger.info(f"Connecting to database via adapter: {adapter}")

        if adapter == "postgres":
            from adapters.postgres import PostgresAdapter
            return PostgresAdapter(self.config.get("database"))

        elif adapter == "snowflake":
            from adapters.snowflake import SnowflakeAdapter
            return SnowflakeAdapter(self.config.get("database"))

        elif adapter == "bigquery":
            from adapters.bigquery import BigQueryAdapter
            return BigQueryAdapter(self.config.get("database"))

        else:
            raise ValueError(f"Unsupported database adapter: '{adapter}'")

    def run(self, pipeline_path: str) -> dict:
        """
        Load and execute a pipeline from a YAML config file.

        Args:
            pipeline_path: Path to the pipeline YAML file.

        Returns:
            A summary dict with step results and metadata.
        """
        pipeline_path = Path(pipeline_path)
        if not pipeline_path.exists():
            raise FileNotFoundError(f"Pipeline config not found: {pipeline_path}")

        with open(pipeline_path) as f:
            config = yaml.safe_load(f)

        pipeline = config.get("pipeline", {})
        name = pipeline.get("name", pipeline_path.stem)
        source = pipeline.get("source")
        target = pipeline.get("target")
        steps = pipeline.get("steps", [])

        self.logger.info(f"━━━ Starting pipeline: {name} ━━━")
        self.logger.info(f"Source: {source}  →  Target: {target}")
        self.logger.info(f"Steps: {len(steps)}")

        results = []
        current_table = source
        start_time = time.time()

        for i, step in enumerate(steps, 1):
            step_name = step.get("name", f"step_{i}")
            transform_key = step.get("transform")
            params = step.get("params", {})

            self.logger.info(f"  [{i}/{len(steps)}] Running: {step_name} ({transform_key})")

            try:
                sql = self.registry.resolve(transform_key, source=current_table, params=params)
                result = self._execute_step(sql, step_name)
                results.append({"step": step_name, "status": "success", **result})
                self.logger.info(f"  ✓ {step_name} completed ({result.get('rows_affected', '?')} rows)")
            except Exception as e:
                self.logger.error(f"  ✗ {step_name} FAILED: {e}")
                results.append({"step": step_name, "status": "failed", "error": str(e)})
                if pipeline.get("fail_fast", True):
                    break

        elapsed = round(time.time() - start_time, 2)
        status = "success" if all(r["status"] == "success" for r in results) else "partial_failure"

        summary = {
            "pipeline": name,
            "status": status,
            "elapsed_seconds": elapsed,
            "steps": results,
        }

        self.logger.info(f"━━━ Pipeline '{name}' finished in {elapsed}s — {status.upper()} ━━━")
        return summary

    def _execute_step(self, sql: str, step_name: str) -> dict:
        """Execute a single SQL step and return metadata."""
        t0 = time.time()
        rows_affected = self.db.execute(sql)
        elapsed = round(time.time() - t0, 3)
        return {"rows_affected": rows_affected, "elapsed_seconds": elapsed}
