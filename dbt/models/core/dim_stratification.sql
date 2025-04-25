{{
    config (
        materialized = "table"
    )
}}

SELECT stratification_num,
       stratification_cat_1
       FROM {{ source("ext_tables", "ext_dim_stratification") }}