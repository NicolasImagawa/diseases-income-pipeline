import sys
from pathlib import Path
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.insert(0, str(Path((__file__)).parent.parent))
from libs.terraform.create_iac import run_terraform

TF_FILEPATH = "/opt/airflow/terraform/tables"

with DAG(
    '04_creating_IAC',
    description="DAG used to create IaC.",
    start_date=None,
    schedule_interval=None
) as dag:
    
    print("Starting IaC DAG...")
    start_dag = EmptyOperator(
        task_id='start_iac_dag'
    )

    terraform = PythonOperator(
        task_id = 'run_terraform',
        python_callable = run_terraform,
        op_kwargs={'filepath': TF_FILEPATH}
    )

    trigger_dbt_dag = TriggerDagRunOperator(
        task_id='trigger_dbt_dag',
        trigger_dag_id='05_transformation'
    )
    print("Now trying to trigger dbt DAG...")


    start_dag >> terraform >> trigger_dbt_dag
