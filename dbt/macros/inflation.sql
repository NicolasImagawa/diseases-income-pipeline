
{% macro inflation(end_att, begin_att) %}
    with cpi_end AS (
    SELECT value/100 AS value
    FROM {{ ref("cpi_2022_2025") }}
    WHERE Attribute = '{{ end_att }}'
    AND `Aggregate` NOT IN ("Food away from home", "Food at home")
    ), cpi_begin AS (
    SELECT value/100 AS value
    FROM {{ ref("cpi_2022_2025") }}
    WHERE Attribute = '{{ begin_att }}'
    AND `Aggregate` NOT IN ("Food away from home", "Food at home")
    )
{% endmacro %}