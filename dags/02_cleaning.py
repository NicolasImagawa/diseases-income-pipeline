import sys
from pathlib import Path
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.insert(0, str(Path((__file__)).parent.parent))
from libs.cleaning.fruits import clean_fruits
from libs.cleaning.vegetables import clean_vegetables
from libs.cleaning.diseases import clean_diseases
from libs.cleaning.behavior import clean_behaviors

with DAG(
    '02_cleaning_data',
    description="DAG used to clean the data.",
    start_date=None,
    schedule_interval=None
) as dag:

    print("Starting cleaning DAG...")
    start_dag = EmptyOperator(
        task_id='start_cleaning_dag'
    )

    clean_fruit = PythonOperator(
        task_id = 'clean_fruits',
        python_callable = clean_fruits
    )

    clean_vegetable = PythonOperator(
        task_id = 'clean_vegetables',
        python_callable = clean_vegetables
    )

    clean_disease = PythonOperator(
        task_id = 'clean_diseases',
        python_callable = clean_diseases
    )

    clean_behavior = PythonOperator(
        task_id = 'clean_behavior',
        python_callable = clean_behaviors
    )

    trigger_ingestion_dag = TriggerDagRunOperator(
        task_id='trigger_ingestion_dag',
        trigger_dag_id='03_GCS_ingestion'
    )
    print("Now trying to trigger GCS ingestion DAG...")

    start_dag >> [clean_fruit, clean_vegetable, clean_disease] >> clean_behavior >> trigger_ingestion_dag