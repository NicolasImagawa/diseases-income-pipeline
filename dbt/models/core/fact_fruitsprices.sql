{{
    config (
        materialized = "table"
    )
}}

{{ inflation("Annual 2024", "Annual 2023") }}
  SELECT fruit,
         form,
         retail_price_unit,
         yield,
         ROUND(retail_price * (1.0 + cpi_begin.value) * (1.0 + cpi_end.value),2) AS retail_price_inflation
      FROM cpi_end, cpi_begin, {{ ref("dim_fruitsprices") }}