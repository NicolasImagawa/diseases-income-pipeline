{{
    config (
        materialized = "table"
    )
}}

SELECT topic_num,
       topic
       FROM {{ source("ext_tables", "ext_dim_topic") }}