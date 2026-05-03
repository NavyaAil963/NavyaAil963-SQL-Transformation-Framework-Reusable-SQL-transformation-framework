-- transformations/validation/uniqueness_check.sql
-- ──────────────────────────────────────────────────
-- Data quality check: validates that a column (or combination of columns)
-- contains no duplicate values.
--
-- Parameters:
--   {{source}}     - Source table to validate
--   {{unique_key}} - Column or comma-separated columns that should be unique

WITH duplicates AS (
    SELECT
        {{unique_key}},
        COUNT(*) AS occurrences
    FROM {{source}}
    GROUP BY {{unique_key}}
    HAVING COUNT(*) > 1
),
summary AS (
    SELECT
        '{{unique_key}}'      AS checked_columns,
        COUNT(*)              AS duplicate_key_count,
        SUM(occurrences)      AS total_duplicate_rows,
        CURRENT_TIMESTAMP     AS checked_at
    FROM duplicates
)
SELECT
    checked_columns,
    duplicate_key_count,
    total_duplicate_rows,
    checked_at,
    CASE
        WHEN duplicate_key_count = 0 THEN 'PASS'
        ELSE 'FAIL — ' || duplicate_key_count || ' duplicate key(s) found in [{{unique_key}}]'
    END AS validation_result
FROM summary
WHERE duplicate_key_count > 0
