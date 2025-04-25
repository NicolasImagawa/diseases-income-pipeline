{{
    config (
        materialized = "table",
        cluster_by = ["question_id", "data_value_unit", "stratification_cat_1", "stratification_id_1"],
    )
}}
WITH dim_disease AS (
    SELECT year_start,
           year_end,
           state_num,
           topic_num,
           question_num,
           datatypeunit_num,
           data_value_type_num,
           stratification_num,
           stratification_id_num,
           data_value,
           data_value_alt
        FROM {{ ref("dim_disease") }}
        WHERE topic_num IN (4, 5, 9, 15, 17)
), dims AS (
    SELECT dim_disease.year_start,
           dim_disease.year_end,
           states_num.state_abr,
           dim_topic.topic,
           dim_questionid.question_id,
           dim_question.question,
           dim_stratification.stratification_cat_1,
           dim_stratificationid.stratification_id_1,
           dim_datatypeunit.data_value_unit,
           dim_disease.data_value,
           dim_disease.data_value_alt
        FROM dim_disease
        INNER JOIN {{ source("seed_tables", "states_num") }} AS states_num
        ON dim_disease.state_num = states_num.state_num
        INNER JOIN {{ ref("dim_topic") }} AS dim_topic
        ON dim_disease.topic_num = dim_topic.topic_num
        INNER JOIN {{ ref("dim_questionid") }} AS dim_questionid
        ON dim_disease.question_num = dim_questionid.question_num
        INNER JOIN {{ ref("dim_question") }} AS dim_question
        ON dim_disease.question_num = dim_question.question_num
        INNER JOIN {{ ref("dim_stratification") }} AS dim_stratification
        ON dim_disease.stratification_num = dim_stratification.stratification_num
        INNER JOIN {{ ref("dim_stratificationid") }} AS dim_stratificationid
        ON dim_disease.stratification_id_num = dim_stratificationid.stratification_id_num
        INNER JOIN {{ ref("dim_datatypeunit") }} AS dim_datatypeunit
        ON dim_disease.datatypeunit_num = dim_datatypeunit.datatypeunit_num
) 

SELECT fact_diseases.year_start,
       fact_diseases.year_end,
       fact_diseases.state_abr,
       fact_diseases.topic,
       fact_diseases.question_id,
       fact_diseases.question,
       fact_diseases.stratification_cat_1,
       fact_diseases.stratification_id_1,
       fact_diseases.data_value_unit,
       fact_diseases.data_value,
       fact_diseases.data_value_alt
    FROM dims AS fact_diseases
{% if var('test_run', default=true) %}
    LIMIT 100
{% endif %}