{{
    config (
        materialized = "table"
    )
}}

SELECT stratification_num,
       stratification_cat_id_1
       FROM {{ source("ext_tables", "ext_dim_stratificationcatid") }}