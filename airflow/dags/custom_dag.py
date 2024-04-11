# Databricks notebook source
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from datetime import datetime, timedelta
import json
import os

# Argumentos padrão que serão passados para cada operador
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir a DAG
dag = DAG(
    'custom_dag',
    default_args=default_args,
    description='A simple tutorial DAG with business logic',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Definir a função callable para o PythonOperator
def process_json_file():
    # Substitua 'input_file_path' pelo caminho real do seu arquivo JSON de entrada
    input_file_path = '/home/your-user/projetos-datalake-coinmarketcap/datalake/gold/file.json'
    # Substitua 'output_file_path' pelo caminho real do seu arquivo de saída
    output_file_path = '/home/your-user/projetos-datalake-coinmarketcap/datalake/gold/results.txt'
    
    # Ler o arquivo JSON
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    
    #conta o número de itens
    item_count = len(data)
    
    # Escreve o resultado em outro arquivo
    with open(output_file_path, 'w') as file:
        file.write(f'Number of items: {item_count}\n')

# Tarefa para verificar a presença do arquivo
check_file_task = BaseSensorOperator(
    task_id='check_file_existence',
    poke_interval=300,  
    timeout=600,        
    mode='poke',
    python_callable=lambda: os.path.isfile('/home/your-user/projetos-datalake-coinmarketcap/datalake/gold/file.json'),
    dag=dag
)

# Tarefa que executa a lógica de negócios
process_file_task = PythonOperator(
    task_id='process_json_file',
    python_callable=process_json_file,
    dag=dag
)

check_file_task >> process_file_task