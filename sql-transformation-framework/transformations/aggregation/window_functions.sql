-- transformations/aggregation/window_functions.sql
-- ──────────────────────────────────────────────────
-- Adds common window function columns to a dataset:
--   - Running totals
--   - Row rank
--   - Previous/next period comparison
--   - Period-over-period % change
--
-- Parameters:
--   {{source}}        - Source table name
--   {{partition_by}}  - Column to partition over (e.g. customer_id)
--   {{order_by}}      - Column to order within partition (e.g. order_date)
--   {{value_column}}  - Numeric column to apply window functions to

SELECT
    *,

    -- Running total within partition
    SUM({{value_column}}) OVER (
        PARTITION BY {{partition_by}}
        ORDER BY {{order_by}}
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,

    -- Rank within partition (latest = 1)
    ROW_NUMBER() OVER (
        PARTITION BY {{partition_by}}
        ORDER BY {{order_by}} DESC
    ) AS recency_rank,

    -- Previous row value (for period comparison)
    LAG({{value_column}}, 1) OVER (
        PARTITION BY {{partition_by}}
        ORDER BY {{order_by}}
    ) AS prev_value,

    -- Period-over-period change
    {{value_column}} - LAG({{value_column}}, 1) OVER (
        PARTITION BY {{partition_by}}
        ORDER BY {{order_by}}
    ) AS period_delta,

    -- % change vs prior period
    ROUND(
        100.0 * (
            {{value_column}} - LAG({{value_column}}, 1) OVER (
                PARTITION BY {{partition_by}}
                ORDER BY {{order_by}}
            )
        ) / NULLIF(
            LAG({{value_column}}, 1) OVER (
                PARTITION BY {{partition_by}}
                ORDER BY {{order_by}}
            ), 0
        ), 2
    ) AS period_pct_change

FROM {{source}}
