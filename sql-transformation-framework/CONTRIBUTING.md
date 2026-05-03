# Contributing

Thanks for your interest in contributing! Here's how to get started.

## Setup

```bash
git clone https://github.com/your-username/sql-transformation-framework.git
cd sql-transformation-framework
pip install -r requirements.txt
```

## Making Changes

1. Fork the repo and create a feature branch: `git checkout -b feat/my-transform`
2. Add your transformation or fix under the appropriate directory
3. Write tests in `tests/unit/`
4. Run the test suite: `pytest tests/`
5. Open a PR with a clear description of what and why

## Code Style

- Python: follow PEP 8, use `ruff` for linting
- SQL: use uppercase keywords, lowercase identifiers, comment parameters at the top of each file

## Reporting Issues

Open a GitHub Issue with steps to reproduce, expected behavior, and actual behavior.
