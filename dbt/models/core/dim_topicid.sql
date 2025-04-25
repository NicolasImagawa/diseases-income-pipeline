{{
    config (
        materialized = "table"
    )
}}

SELECT topic_num,
       topic_id
       FROM {{ source("ext_tables","ext_dim_topicid") }}