-- transformations/validation/not_null_check.sql
-- ────────────────────────────────────────────────
-- Data quality check: raises a failure-compatible result
-- if any critical columns contain NULL values.
--
-- Returns a zero-row result on success, or a descriptive
-- error row for each NULL found (so failures are observable).
--
-- Parameters:
--   {{source}}   - Source table to validate
--   {{columns}}  - Comma-separated list of columns to check

WITH null_violations AS (
    SELECT
        '{{columns}}'           AS checked_columns,
        COUNT(*)                AS total_rows,
        COUNT(*) FILTER (
            WHERE {{columns}} IS NULL
        )                       AS null_count,
        CURRENT_TIMESTAMP       AS checked_at
    FROM {{source}}
)
SELECT
    checked_columns,
    total_rows,
    null_count,
    checked_at,
    CASE
        WHEN null_count = 0 THEN 'PASS'
        ELSE 'FAIL — ' || null_count || ' NULL(s) found in [{{columns}}]'
    END AS validation_result
FROM null_violations
WHERE null_count > 0  -- Only surface failures; suppress on clean data
