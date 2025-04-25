{{
    config (
        materialized = "table"
    )
}}
SELECT datatypeunit_num,
       data_value_type_num
       FROM {{ source("ext_tables", "ext_dim_datatype_datatypeunit") }}
