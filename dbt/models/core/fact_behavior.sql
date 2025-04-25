{{
    config (
        materialized = "table",
        cluster_by = ["year_start", "question_id"]
    )
}}
WITH dim_behavior AS (
    SELECT year_start,
           year_end,
           state_num,
           topic_num,
           question_num,
           stratification_num,
           stratification_id_num,
           data_value,
           data_value_alt
        FROM {{ ref("dim_behavior") }}
        WHERE stratification_num = 7
), dims AS (
    SELECT dim_behavior.year_start,
           dim_behavior.year_end,
           states_num.state_abr,
           dim_topic.topic,
           dim_questionid.question_id,
           dim_question.question,
           dim_stratification.stratification_cat_1,
           dim_stratificationid.stratification_id_1,
           dim_behavior.data_value,
           dim_behavior.data_value_alt
        FROM dim_behavior
        INNER JOIN {{ source("seed_tables", "states_num") }} AS states_num
        ON dim_behavior.state_num = states_num.state_num
        INNER JOIN {{ ref("dim_topic") }} AS dim_topic
        ON dim_behavior.topic_num = dim_topic.topic_num
        INNER JOIN {{ ref("dim_questionid") }} AS dim_questionid
        ON dim_behavior.question_num = dim_questionid.question_num
        INNER JOIN {{ ref("dim_question") }} AS dim_question
        ON dim_behavior.question_num = dim_question.question_num
        INNER JOIN {{ ref("dim_stratification") }} AS dim_stratification
        ON dim_behavior.stratification_num = dim_stratification.stratification_num
        INNER JOIN {{ ref("dim_stratificationid") }} AS dim_stratificationid
        ON dim_behavior.stratification_id_num = dim_stratificationid.stratification_id_num
) 

SELECT fact_behavior.year_start,
       fact_behavior.year_end,
       fact_behavior.state_abr,
       fact_behavior.topic,
       fact_behavior.question_id,
       fact_behavior.question,
       fact_behavior.stratification_cat_1,
       fact_behavior.stratification_id_1,
       fact_behavior.data_value,
       fact_behavior.data_value_alt
    FROM dims AS fact_behavior
{% if var('test_run', default=true) %}
    LIMIT 100
{% endif %}