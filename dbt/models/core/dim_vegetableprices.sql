{{
    config (
        materialized = "table"
    )
}}

SELECT vegetable,
       form,
       retail_price,
       retail_price_unit,
       yield,
       cup_equivalent_size,
       cup_equivalent_unit,
       cup_equivalent_price
       FROM {{ source("ext_tables", "ext_dim_vegetableprices") }}