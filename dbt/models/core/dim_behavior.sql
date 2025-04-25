{{
    config (
        materialized = "table",
        cluster_by = ["state_num", "stratification_num"],
    )
}}

SELECT year_start,
       year_end,
       state_num,
       topic_num,
       question_num,
       stratification_id_num,
       stratification_num,
       data_value_unit,
       data_value,
       data_value_alt
       FROM {{ source("ext_tables", "ext_dim_behavior") }}