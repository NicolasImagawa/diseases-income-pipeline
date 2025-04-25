{{
    config (
        materialized = "table"
    )
}}

SELECT data_value_type_num,
       data_value_type_id
       FROM {{ source("ext_tables", "ext_dim_datatypeid") }}