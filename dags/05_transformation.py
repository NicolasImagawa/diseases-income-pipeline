from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonVirtualenvOperator

def run_dbt():
    import os
    from dbt.cli.main import dbtRunner

    PROFILE_PATH = "/opt/airflow/dbt"
    PROJECT_PATH = "/opt/airflow/dbt"

    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in {PROJECT_PATH}: {os.listdir(PROJECT_PATH)}")

    dbt = dbtRunner()

    dbt_commands = [
        [
            "seed",
            "--profiles-dir", PROFILE_PATH,
            "--project-dir", PROJECT_PATH
        ],
        [
            "run",
            "--profiles-dir", PROFILE_PATH,
            "--project-dir", PROJECT_PATH,
            "--vars", '{"test_run": false}'
        ]
    ]

    for command in dbt_commands:
        result = dbt.invoke(command)
    
        if result.success:
            print("dbt run succeeded!")
            print(result.result)
        else:
            print("dbt run failed!")
            print(result.exception)
            raise RuntimeError("dbt run failed")


with DAG(
    '05_transformation',
    description="DAG used to transform data.",
    start_date=None,
    schedule_interval=None
) as dag:
    
    print("Starting dbt DAG...")
    start_dag = EmptyOperator(
        task_id='start_trasformation_dag'
    )

    dbt =  PythonVirtualenvOperator(
        task_id='run_dbt',
        python_callable=run_dbt,
        python_version="3.9",
        requirements=["dbt-bigquery", "protobuf>=3.19,<5.0"],
        system_site_packages=False,
    )

    start_dag >> dbt
