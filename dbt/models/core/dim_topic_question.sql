{{
    config (
        materialized = "table"
    )
}}

SELECT topic_id,
       question_id
       FROM {{ source("ext_tables", "ext_dim_topic_question") }}