{{
    config (
        materialized = "table"
    )
}}

SELECT stratification_id_num,
       stratification_id_1
       FROM {{ source("ext_tables", "ext_dim_stratificationid") }}