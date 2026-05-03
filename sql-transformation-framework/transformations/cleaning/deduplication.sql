-- transformations/cleaning/deduplication.sql
-- ─────────────────────────────────────────────
-- Removes duplicate rows from the source table based on a unique key.
-- Keeps the most recently updated row when duplicates exist.
--
-- Parameters:
--   {{source}}      - Source table name (injected by engine)
--   {{unique_key}}  - Column(s) to determine uniqueness (comma-separated)
--   {{order_by}}    - Column used to pick the "best" row (default: updated_at)

WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY {{unique_key}}
            ORDER BY {{order_by}} DESC NULLS LAST
        ) AS _row_rank
    FROM {{source}}
)
SELECT * EXCLUDE (_row_rank)
FROM ranked
WHERE _row_rank = 1
