-- transformations/joins/safe_left_join.sql
-- ──────────────────────────────────────────
-- Performs a LEFT JOIN and includes a flag column indicating
-- whether each row had a successful match. Unmatched rows are
-- surfaced rather than silently dropped.
--
-- Parameters:
--   {{source}}         - Left (base) table
--   {{join_table}}     - Right (lookup) table
--   {{join_key}}       - Column name used to join both tables
--   {{select_columns}} - Columns to bring in from the right table

SELECT
    base.*,
    lookup.{{select_columns}},

    -- Match quality flag
    CASE
        WHEN lookup.{{join_key}} IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS _join_matched

FROM {{source}} AS base
LEFT JOIN {{join_table}} AS lookup
    ON base.{{join_key}} = lookup.{{join_key}}
