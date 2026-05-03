# Adding a New Transformation

Follow these steps to add a new reusable SQL transformation to the framework.

## 1. Create the SQL template

Create a `.sql` file under `transformations/` in the appropriate subdirectory:

```
transformations/
└── cleaning/           ← e.g. for a new cleaning transform
    └── my_transform.sql
```

Use `{{double_curly}}` placeholders for parameters. The engine always injects `{{source}}` automatically:

```sql
-- transformations/cleaning/my_transform.sql
-- Parameters:
--   {{source}}     - Source table (auto-injected)
--   {{my_param}}   - Your custom parameter

SELECT *
FROM {{source}}
WHERE some_column = '{{my_param}}'
```

## 2. Use it in a pipeline

Reference the transform by its path key (relative to `transformations/`, without `.sql`):

```yaml
steps:
  - name: apply_my_transform
    transform: cleaning/my_transform
    params:
      my_param: some_value
```

## 3. Write a unit test

Add a test in `tests/unit/` to verify it renders correctly:

```python
def test_my_transform(temp_registry):
    sql = temp_registry.resolve(
        "cleaning/my_transform",
        source="raw.table",
        params={"my_param": "active"},
    )
    assert "raw.table" in sql
    assert "active" in sql
    assert "{{" not in sql
```

## Naming Conventions

| Category | Directory |
|----------|-----------|
| Data cleaning | `transformations/cleaning/` |
| Aggregation | `transformations/aggregation/` |
| Joins & enrichment | `transformations/joins/` |
| Data quality | `transformations/validation/` |

## Parameters

- Use descriptive parameter names
- Document all parameters at the top of the `.sql` file
- `{{source}}` is always available and injected by the engine
- List values are automatically joined with `, ` for use in SQL
