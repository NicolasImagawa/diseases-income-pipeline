{{
    config (
        materialized = "table"
    )
}}

SELECT datatypeunit_num,
       data_value_unit
       FROM {{ source("ext_tables", "ext_dim_datatypeunit") }}