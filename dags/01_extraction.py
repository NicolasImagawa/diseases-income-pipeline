import sys
from pathlib import Path
from airflow import DAG
import json
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.insert(0, str(Path(__file__).parent.parent))  # 0: highest priority when including the folder common to dags and the extraction scripts.
from libs.extraction.extraction_pipeline import extract_data

year = {'extraction_year': 2022} 

json_path = "./config/paths.json"
with open(json_path, "r") as json_file:
    paths = json.load(json_file)


behavior_extraction = (paths["behavior"]["url"], paths["behavior"]["raw"])
cpi_extraction = (paths["cpi"]["url"], paths["cpi"]["raw"])
diseases_extraction = (paths["diseases"]["url"], paths["diseases"]["raw"])
fruits_extraction = (paths["fruits"]["url"].format(**year), paths["fruits"]["raw"])
vegetables_extraction = (paths["vegetables"]["url"].format(**year), paths["vegetables"]["raw"])


with DAG(
  '01_extracting_data',
  description="Data extraction DAG",
  start_date=None,
  schedule_interval=None
) as dag:
    
    print("Starting extraction DAG...")
    start_dag = EmptyOperator(
        task_id='start_extraction_dag'
    )

    extract_behavior = PythonOperator(
        task_id='behavior_extraction',
        python_callable = extract_data,
        op_kwargs = {'url': behavior_extraction[0], 'output': behavior_extraction[1]}
    )

    extract_cpi = PythonOperator(
        task_id='cpi_extraction',
        python_callable = extract_data,
        op_kwargs = {'url': cpi_extraction[0], 'output': cpi_extraction[1]}
    )

    extract_diseases = PythonOperator(
        task_id='diseases_extraction',
        python_callable = extract_data,
        op_kwargs = {'url': diseases_extraction[0], 'output': diseases_extraction[1]}
    )

    extract_fruits = PythonOperator(
        task_id='fruits_extraction',
        python_callable = extract_data,
        op_kwargs = {'url': fruits_extraction[0], 'output': fruits_extraction[1]}
    )

    extract_vegetables = PythonOperator(
        task_id='vegetables_extraction',
        python_callable = extract_data,
        op_kwargs = {'url': vegetables_extraction[0], 'output': vegetables_extraction[1]}
    )

    trigger_cleaning_dag = TriggerDagRunOperator(
        task_id='trigger_cleaning_dag',
        trigger_dag_id='02_cleaning_data'
    )
    print("Now trying to trigger cleaning DAG...")

    start_dag >> [extract_behavior, extract_cpi, extract_diseases, extract_fruits, extract_vegetables] >> trigger_cleaning_dag