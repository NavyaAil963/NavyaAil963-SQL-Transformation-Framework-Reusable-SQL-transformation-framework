-- transformations/aggregation/cohort_analysis.sql
-- ──────────────────────────────────────────────────
-- Cohort retention analysis: groups users/customers by their
-- first-seen period and tracks activity in subsequent periods.
--
-- Parameters:
--   {{source}}         - Source events table
--   {{entity_id}}      - User or customer identifier column
--   {{event_date}}     - Date column for each event
--   {{cohort_period}}  - Truncation period: 'month' | 'week' | 'day'

WITH cohort_base AS (
    -- Determine the first activity period per entity (cohort assignment)
    SELECT
        {{entity_id}},
        MIN(DATE_TRUNC('{{cohort_period}}', {{event_date}})) AS cohort_period
    FROM {{source}}
    GROUP BY {{entity_id}}
),
activity AS (
    -- All activity with cohort tag
    SELECT
        e.{{entity_id}},
        c.cohort_period,
        DATE_TRUNC('{{cohort_period}}', e.{{event_date}}) AS activity_period
    FROM {{source}} e
    INNER JOIN cohort_base c USING ({{entity_id}})
),
cohort_size AS (
    -- Size of each cohort at period 0
    SELECT
        cohort_period,
        COUNT(DISTINCT {{entity_id}}) AS cohort_users
    FROM cohort_base
    GROUP BY cohort_period
),
retention AS (
    -- Activity per cohort per period offset
    SELECT
        a.cohort_period,
        DATEDIFF('{{cohort_period}}', a.cohort_period, a.activity_period) AS period_offset,
        COUNT(DISTINCT a.{{entity_id}})                                    AS active_users
    FROM activity a
    GROUP BY 1, 2
)
SELECT
    r.cohort_period,
    r.period_offset,
    s.cohort_users,
    r.active_users,
    ROUND(100.0 * r.active_users / NULLIF(s.cohort_users, 0), 2) AS retention_pct
FROM retention r
INNER JOIN cohort_size s USING (cohort_period)
ORDER BY r.cohort_period, r.period_offset
