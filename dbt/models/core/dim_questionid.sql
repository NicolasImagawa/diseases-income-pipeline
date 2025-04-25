{{
    config (
        materialized = "table"
    )
}}

SELECT question_num,
       question_id
       FROM {{ source("ext_tables", "ext_dim_questionid") }}