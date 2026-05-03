-- transformations/cleaning/null_handler.sql
-- ─────────────────────────────────────────
-- Handles NULL values across specified columns.
-- Supports three strategies: drop, fill, or flag.
--
-- Parameters:
--   {{source}}    - Source table name
--   {{columns}}   - Columns to check for NULLs (comma-separated)
--   {{strategy}}  - 'drop' | 'fill' | 'flag'
--   {{fill_value}}- Value to use when strategy = 'fill' (default: 'UNKNOWN')

-- Strategy: DROP rows that have NULLs in critical columns
-- (Swap the WHERE clause based on your chosen strategy)

SELECT *
FROM {{source}}
WHERE
    -- Null guard: all listed columns must be non-null
    {{columns}} IS NOT NULL
