# 🔄 SQL Transformation Framework

> A reusable, modular SQL transformation framework built for scalable ETL pipelines — reducing development time and enforcing data quality standards across teams.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL%20%7C%20Snowflake%20%7C%20BigQuery-orange.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 📌 Overview

The **SQL Transformation Framework** is a production-grade ETL toolkit originally developed at **BAM Creatives** to standardize and accelerate data pipeline development across 10+ ETL workflows. It reduces boilerplate, enforces consistency, and makes complex SQL transformations composable and testable.

### Key Benefits

| Before | After |
|--------|-------|
| Copy-paste SQL across pipelines | Centralized, reusable transformation blocks |
| No validation standards | Built-in data quality checks |
| Weeks to build a new pipeline | Hours using pre-built modules |
| Hard to debug failures | Logged, step-by-step transformation tracing |
| Inconsistent naming conventions | Enforced schema standards |

---

## 🗂️ Project Structure

```
sql-transformation-framework/
├── core/                          # Framework engine
│   ├── engine.py                  # Pipeline orchestration engine
│   ├── registry.py                # Transformation registry
│   ├── logger.py                  # Structured logging
│   └── config.py                  # Config loader
│
├── transformations/               # Reusable SQL transformation modules
│   ├── cleaning/                  # Data cleaning transforms
│   │   ├── null_handler.sql
│   │   ├── deduplication.sql
│   │   └── type_casting.sql
│   ├── aggregation/               # Aggregation patterns
│   │   ├── daily_rollup.sql
│   │   ├── window_functions.sql
│   │   └── cohort_analysis.sql
│   ├── joins/                     # Join templates
│   │   ├── safe_left_join.sql
│   │   └── enrichment_join.sql
│   └── validation/                # Data quality checks
│       ├── not_null_check.sql
│       ├── range_check.sql
│       └── uniqueness_check.sql
│
├── pipelines/                     # Pipeline definitions (per domain)
│   ├── ecommerce/
│   │   ├── orders_pipeline.yaml
│   │   └── revenue_pipeline.yaml
│   ├── marketing/
│   │   └── campaign_pipeline.yaml
│   ├── finance/
│   │   └── gl_pipeline.yaml
│   └── inventory/
│       └── stock_pipeline.yaml
│
├── tests/
│   ├── unit/                      # Unit tests per transformation
│   └── integration/               # End-to-end pipeline tests
│
├── scripts/
│   ├── run_pipeline.py            # CLI runner
│   └── validate_schema.py         # Schema validation utility
│
├── examples/                      # Example pipelines to get started
│   └── quickstart_pipeline.yaml
│
├── docs/
│   ├── architecture.md
│   ├── adding_transformations.md
│   └── pipeline_config_spec.md
│
├── config/
│   └── settings.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/your-username/sql-transformation-framework.git
cd sql-transformation-framework
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Run a sample pipeline

```bash
python scripts/run_pipeline.py --pipeline examples/quickstart_pipeline.yaml
```

---

## ⚙️ How It Works

### Pipeline Definition (YAML)

Each pipeline is defined in a YAML config file:

```yaml
pipeline:
  name: orders_daily_rollup
  description: Aggregates raw order data into daily summaries
  source: raw.orders
  target: analytics.orders_daily

  steps:
    - name: remove_duplicates
      transform: cleaning/deduplication
      params:
        unique_key: order_id

    - name: cast_types
      transform: cleaning/type_casting
      params:
        columns:
          order_date: DATE
          amount: NUMERIC

    - name: daily_aggregation
      transform: aggregation/daily_rollup
      params:
        date_column: order_date
        metrics:
          - sum: amount
          - count: order_id

    - name: validate_output
      transform: validation/not_null_check
      params:
        columns: [order_date, total_revenue]
```

### Running a Pipeline

```python
from core.engine import PipelineEngine

engine = PipelineEngine(config_path="config/settings.yaml")
engine.run("pipelines/ecommerce/orders_pipeline.yaml")
```

---

## 🧩 Core Transformations

### Cleaning

| Transform | Description |
|-----------|-------------|
| `cleaning/null_handler` | Replace or drop NULLs with configurable strategy |
| `cleaning/deduplication` | Remove duplicate rows by key columns |
| `cleaning/type_casting` | Safe column type casting with error logging |

### Aggregation

| Transform | Description |
|-----------|-------------|
| `aggregation/daily_rollup` | Aggregate metrics by day |
| `aggregation/window_functions` | Running totals, ranks, lag/lead |
| `aggregation/cohort_analysis` | Cohort retention and revenue analysis |

### Joins

| Transform | Description |
|-----------|-------------|
| `joins/safe_left_join` | Left join with unmatched row alerting |
| `joins/enrichment_join` | Enrich base table with dimension data |

### Validation

| Transform | Description |
|-----------|-------------|
| `validation/not_null_check` | Assert no NULLs in critical columns |
| `validation/range_check` | Assert values fall within expected range |
| `validation/uniqueness_check` | Assert column uniqueness constraints |

---

## 🗃️ Supported Databases

- ✅ PostgreSQL
- ✅ Snowflake
- ✅ Google BigQuery
- ✅ Amazon Redshift
- 🔜 DuckDB (coming soon)

---

## 🧪 Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests (requires DB connection)
pytest tests/integration/ --env=test
```

---

## 📖 Documentation

- [Architecture Overview](docs/architecture.md)
- [Adding a New Transformation](docs/adding_transformations.md)
- [Pipeline Config Spec](docs/pipeline_config_spec.md)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
