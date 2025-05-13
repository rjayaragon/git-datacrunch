from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

# DAG config
default_args = {
    "owner": "rjaya",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="datacrunch_etl_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 5, 10),
    schedule_interval="@daily",  # or None for manual
    catchup=False,
)


# --- Script wrapper functions ---
def run_generate():
    os.system("python /opt/airflow/scripts/generate_faker_data.py")


def run_clean():
    os.system("python /opt/airflow/scripts/clean_factsales.py")


def run_load():
    os.system("python /opt/airflow/scripts/load_to_postgres.py")


def run_validate():
    os.system("python /opt/airflow/scripts/validate_data.py")


# --- Define tasks ---
generate = PythonOperator(
    task_id="generate_data", python_callable=run_generate, dag=dag
)

clean = PythonOperator(task_id="clean_data", python_callable=run_clean, dag=dag)

load = PythonOperator(task_id="load_data", python_callable=run_load, dag=dag)

validate = PythonOperator(
    task_id="validate_data", python_callable=run_validate, dag=dag
)

# --- Set task dependencies ---
generate >> clean >> load >> validate
