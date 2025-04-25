{{
    config (
        materialized = "table",
        cluster_by = ["state_abr", "topic"]
    )
}}

SELECT year_start,
       state_abr,
       topic,
       question,
       stratification_id_1,
       data_value_unit,
       data_value
FROM {{ ref("fact_disease") }}
WHERE year_start = 2021
AND question_id IN ("CVD01", "CVD07", "CVD08", "CVD09", "DIA01", "DIA04", "NPW02", "NPW04")
AND data_value_unit IN ("%", "cases per 100,000")
AND stratification_cat_1 = "Age"
AND stratification_id_1 IN ("AGE1844", "AGE0_44")