{{
    config (
        materialized = "table"
    )
}}

SELECT topic_num,
       question_num
       FROM {{ source("ext_tables","ext_dim_topicid_questionid") }}