from __future__ import annotations

import pendulum

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator

def _extract(**context):
    from extract.extract_weather import run_weather_report
    run_weather_report(context["ds"])

def _load(**context):
    from load.load_weather import load_weather_data
    load_weather_data(context["ds"])

DBT_PROJECT_DIR = "/opt/airflow/dbt/weather_dbt"

with DAG(
    dag_id="weather_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(2026,8,1, tz="UTC"),
    catchup=False,
) as dag:

    extract_weather = PythonOperator(
        task_id="extract_weather",
        python_callable=_extract
    )

    load_weather = PythonOperator(
        task_id="load_weather",
        python_callable=_load
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test"
    )

    extract_weather >> load_weather >> dbt_run >> dbt_test