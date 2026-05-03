-- transformations/aggregation/daily_rollup.sql
-- ──────────────────────────────────────────────
-- Aggregates source data into daily summary metrics.
-- Supports SUM, COUNT, AVG, MIN, MAX per group.
--
-- Parameters:
--   {{source}}       - Source table name
--   {{date_column}}  - Column to truncate to day (e.g. created_at)
--   {{group_by}}     - Additional grouping columns (e.g. region, product_id)
--   {{sum_column}}   - Column to SUM (e.g. revenue)
--   {{count_column}} - Column to COUNT (e.g. order_id)

SELECT
    DATE_TRUNC('day', {{date_column}})  AS report_date,
    {{group_by}},

    -- Volume metrics
    COUNT(*)                             AS total_records,
    COUNT(DISTINCT {{count_column}})     AS unique_count,

    -- Value metrics
    SUM({{sum_column}})                  AS total_value,
    AVG({{sum_column}})                  AS avg_value,
    MIN({{sum_column}})                  AS min_value,
    MAX({{sum_column}})                  AS max_value,

    -- Audit
    CURRENT_TIMESTAMP                    AS transformed_at

FROM {{source}}
WHERE {{date_column}} IS NOT NULL
GROUP BY 1, 2
ORDER BY 1 DESC, 2
