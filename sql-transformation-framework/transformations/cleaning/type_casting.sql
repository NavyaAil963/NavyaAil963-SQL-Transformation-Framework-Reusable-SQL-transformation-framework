-- transformations/cleaning/type_casting.sql
-- ──────────────────────────────────────────
-- Safely casts columns to target types using TRY_CAST where supported,
-- logging failures as NULLs rather than raising errors.
--
-- Parameters:
--   {{source}}      - Source table name
--   {{date_columns}}- Columns to cast to DATE
--   {{num_columns}} - Columns to cast to NUMERIC
--   {{int_columns}} - Columns to cast to INTEGER

SELECT
    -- Pass through all columns
    * EXCLUDE ({{date_columns}}, {{num_columns}}, {{int_columns}}),

    -- Date casts
    TRY_CAST({{date_columns}} AS DATE)    AS {{date_columns}},

    -- Numeric casts
    TRY_CAST({{num_columns}} AS NUMERIC)  AS {{num_columns}},

    -- Integer casts
    TRY_CAST({{int_columns}} AS INTEGER)  AS {{int_columns}}

FROM {{source}}
