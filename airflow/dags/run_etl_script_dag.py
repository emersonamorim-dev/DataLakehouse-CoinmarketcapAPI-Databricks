# Databricks notebook source
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# argumentos padrão
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['emerson_tecno@hotmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'run_etl_script',
    default_args=default_args,
    description='DAG with a script task',
    schedule=timedelta(days=1),  # Modificado aqui
    start_date=datetime(2024, 1, 1),
    catchup=False
)

run_etl_script = BashOperator(
    task_id='run_etl_script',
    bash_command='python /home/your-user/seu-diretorio/airflow/scripts/etl_script.py.py /home/emerdev/projetos-datalake-coinmarketcap/datalake/goldinput.json /path/to/output.json',
    dag=dag,
)

run_etl_script