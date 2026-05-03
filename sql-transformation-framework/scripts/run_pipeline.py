#!/usr/bin/env python3
"""
scripts/run_pipeline.py
-----------------------
CLI entrypoint for executing a single ETL pipeline.

Usage:
    python scripts/run_pipeline.py --pipeline pipelines/ecommerce/orders_pipeline.yaml
    python scripts/run_pipeline.py --pipeline pipelines/marketing/campaign_pipeline.yaml --dry-run
    python scripts/run_pipeline.py --list
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.engine import PipelineEngine
from core.logger import get_logger

logger = get_logger("CLI")


def parse_args():
    parser = argparse.ArgumentParser(
        description="SQL Transformation Framework — Pipeline Runner",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--pipeline", "-p",
        type=str,
        help="Path to the pipeline YAML config file",
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config/settings.yaml",
        help="Path to the framework config (default: config/settings.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the pipeline config without executing SQL",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available pipelines and transformations",
    )
    parser.add_argument(
        "--output", "-o",
        choices=["text", "json"],
        default="text",
        help="Output format for the run summary (default: text)",
    )
    return parser.parse_args()


def list_resources():
    """Print all available pipelines and transformations."""
    pipelines = list(Path("pipelines").rglob("*.yaml"))
    transforms = list(Path("transformations").rglob("*.sql"))

    print("\n📂 Available Pipelines:")
    for p in sorted(pipelines):
        print(f"  • {p}")

    print("\n🔧 Available Transformations:")
    for t in sorted(transforms):
        key = str(t.relative_to("transformations")).replace(".sql", "")
        print(f"  • {key}")

    print()


def main():
    args = parse_args()

    if args.list:
        list_resources()
        return

    if not args.pipeline:
        print("Error: --pipeline is required unless using --list.\n")
        print("Usage: python scripts/run_pipeline.py --pipeline <path/to/pipeline.yaml>")
        sys.exit(1)

    if args.dry_run:
        logger.info(f"[DRY RUN] Validating pipeline config: {args.pipeline}")
        import yaml
        with open(args.pipeline) as f:
            config = yaml.safe_load(f)
        print(json.dumps(config, indent=2, default=str))
        logger.info("[DRY RUN] Config is valid — no SQL executed.")
        return

    engine = PipelineEngine(config_path=args.config)
    summary = engine.run(args.pipeline)

    if args.output == "json":
        print(json.dumps(summary, indent=2, default=str))
    else:
        status_icon = "✅" if summary["status"] == "success" else "⚠️"
        print(f"\n{status_icon}  Pipeline: {summary['pipeline']}")
        print(f"   Status:  {summary['status'].upper()}")
        print(f"   Elapsed: {summary['elapsed_seconds']}s")
        print(f"   Steps:   {len(summary['steps'])}")
        for step in summary["steps"]:
            icon = "✓" if step["status"] == "success" else "✗"
            print(f"     {icon} {step['step']}")

    sys.exit(0 if summary["status"] == "success" else 1)


if __name__ == "__main__":
    main()
