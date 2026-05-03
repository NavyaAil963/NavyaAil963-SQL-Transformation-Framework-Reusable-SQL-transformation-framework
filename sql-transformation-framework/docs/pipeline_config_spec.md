# Pipeline Config Specification

A pipeline is defined in a YAML file. Here is the full reference:

```yaml
pipeline:
  # ─── Required fields ───────────────────────────────
  name: my_pipeline_name             # Unique identifier
  source: schema.table_name          # Input table
  target: analytics.output_table    # Output table

  # ─── Optional metadata ─────────────────────────────
  description: "Human-readable description"
  version: "1.0"
  owner: team@company.com
  schedule: "0 3 * * *"             # Cron schedule (informational)
  tags:
    - finance
    - daily

  # ─── Execution settings ────────────────────────────
  fail_fast: true                   # Stop on first step failure (default: true)

  # ─── Steps (executed in order) ────────────────────
  steps:
    - name: step_name               # Human-readable step name
      transform: category/key       # Path to .sql template (no .sql extension)
      params:
        param_name: param_value     # Parameters injected into the template
```

## Step Params

Params are injected into SQL templates as `{{param_name}}`. List values are joined with `, `.

```yaml
params:
  columns: [col_a, col_b]    # Becomes: col_a, col_b in SQL
  threshold: 100             # Becomes: 100 in SQL
```

## Available Transforms

| Key | Description |
|-----|-------------|
| `cleaning/deduplication` | Remove duplicates by key |
| `cleaning/null_handler` | Drop or fill NULLs |
| `cleaning/type_casting` | Cast column types |
| `aggregation/daily_rollup` | Daily metric aggregation |
| `aggregation/window_functions` | Running totals and period comparisons |
| `aggregation/cohort_analysis` | Cohort retention analysis |
| `joins/safe_left_join` | Left join with match flag |
| `joins/enrichment_join` | Dimension enrichment join |
| `validation/not_null_check` | Assert non-null columns |
| `validation/range_check` | Assert numeric range |
| `validation/uniqueness_check` | Assert column uniqueness |
