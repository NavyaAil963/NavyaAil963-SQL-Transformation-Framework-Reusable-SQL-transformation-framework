-- transformations/validation/range_check.sql
-- ─────────────────────────────────────────────
-- Data quality check: validates that a numeric column's values
-- fall within an expected [min, max] range.
--
-- Parameters:
--   {{source}}     - Source table to validate
--   {{column}}     - Column to check
--   {{min_value}}  - Lower bound (inclusive)
--   {{max_value}}  - Upper bound (inclusive)

WITH range_violations AS (
    SELECT
        '{{column}}'              AS checked_column,
        '{{min_value}}'           AS expected_min,
        '{{max_value}}'           AS expected_max,
        COUNT(*)                  AS total_rows,
        COUNT(*) FILTER (
            WHERE {{column}} < {{min_value}}
               OR {{column}} > {{max_value}}
        )                         AS out_of_range_count,
        MIN({{column}})           AS actual_min,
        MAX({{column}})           AS actual_max,
        CURRENT_TIMESTAMP         AS checked_at
    FROM {{source}}
)
SELECT
    checked_column,
    expected_min,
    expected_max,
    total_rows,
    out_of_range_count,
    actual_min,
    actual_max,
    checked_at,
    CASE
        WHEN out_of_range_count = 0 THEN 'PASS'
        ELSE 'FAIL — ' || out_of_range_count || ' value(s) outside [{{min_value}}, {{max_value}}]'
    END AS validation_result
FROM range_violations
WHERE out_of_range_count > 0
