# Architecture Overview

## How the Framework Works

```
Pipeline YAML
    │
    ▼
PipelineEngine.run()
    │
    ├── Loads YAML config
    ├── Connects to database via adapter
    │
    └── For each step:
            │
            ├── TransformationRegistry.resolve(key, source, params)
            │       │
            │       ├── Loads .sql template from disk (cached)
            │       └── Renders {{placeholders}} with params
            │
            └── Database.execute(rendered_sql)
                    │
                    └── Returns rows_affected
```

## Component Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| `PipelineEngine` | `core/engine.py` | Orchestrates step execution |
| `TransformationRegistry` | `core/registry.py` | Loads & renders SQL templates |
| `FrameworkConfig` | `core/config.py` | Reads YAML + env var config |
| SQL Templates | `transformations/**/*.sql` | Reusable parameterized SQL |
| Pipeline Configs | `pipelines/**/*.yaml` | Declare which transforms to run |
| CLI Runner | `scripts/run_pipeline.py` | Shell entrypoint |

## Design Principles

1. **Separation of concerns** — SQL logic lives in `.sql` files, not Python
2. **Composability** — Any transformation can be reused in any pipeline
3. **Fail loudly** — Validation steps surface issues rather than hiding them
4. **Config-driven** — New pipelines need zero Python code
5. **Testable** — Every transformation is independently testable with fixture data
