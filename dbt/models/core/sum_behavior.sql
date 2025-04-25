{{
    config (
        materialized = "table",
        cluster_by = ["state_abr", "stratification_id_1"]
    )
}}

SELECT year_start,
      state_abr,
      topic,
      question,
      stratification_id_1,
      data_value
FROM {{ ref("fact_behavior") }}
WHERE year_start = 2021
AND question_id IN("FVB01", "FVB02")