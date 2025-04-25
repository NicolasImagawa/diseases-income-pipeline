{{
    config (
        materialized = "table"
    )
}}

SELECT stratification_num,
       stratification_id_num
       FROM {{ source("ext_tables", "ext_dim_stratification_stratificationid") }}