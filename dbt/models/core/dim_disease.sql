{{
    config (
        materialized = "table",
        cluster_by = ["state_num", "topic_num"],
    )
}}

SELECT year_start,
       year_end,
       state_num,
       data_source,
       topic_num,
       question_num,
       datatypeunit_num,
       data_value_type_num,
       stratification_num,
       stratification_id_num,
       data_value,
       data_value_alt,
       low_confidence_limit,
       high_confidence_limit
       FROM {{ source("ext_tables", "ext_dim_disease") }}