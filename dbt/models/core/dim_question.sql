{{
    config (
        materialized = "table"
    )
}}

SELECT question_num,
       question
       FROM {{ source("ext_tables", "ext_dim_question") }}