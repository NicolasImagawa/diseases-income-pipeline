import sys
from pathlib import Path
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.insert(0, str(Path((__file__)).parent.parent))
from libs.cloud_ingestion.send_to_gcs import upload_files
from libs.terraform.create_iac import run_terraform

TF_FILEPATH = "/opt/airflow/terraform/dataset_and_bucket"

with DAG(
    '03_GCS_ingestion',
    description="DAG used to create the dataset and ingest data to GCS.",
    start_date=None,
    schedule_interval=None
) as dag:
    
    print("Starting ingestion DAG...")
    start_dag = EmptyOperator(
        task_id='start_ingestion_dag'
    )

    create_dataset_bucket  = PythonOperator(
        task_id = 'create_dataset_bucket',
        python_callable = run_terraform,
        op_kwargs={'filepath': TF_FILEPATH}
    )

    upload_data = PythonOperator(
        task_id = 'upload_data',
        python_callable = upload_files
    )

    trigger_iac_dag = TriggerDagRunOperator(
        task_id='trigger_ingestion_dag',
        trigger_dag_id='04_creating_IAC'
    )
    print("Now trying to trigger IAC DAG...")


    start_dag >> create_dataset_bucket >> upload_data >> trigger_iac_dag