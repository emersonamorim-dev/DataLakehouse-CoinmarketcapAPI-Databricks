import requests
import json
from databricks_api import DatabricksAPI
from datetime import datetime
from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obtem as chaves da API do ambiente
COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')
DATABRICKS_URL = os.getenv('DATABRICKS_URL')

# Verificar se todas as variáveis de ambiente foram definidas
if not all([COINMARKETCAP_API_KEY, DATABRICKS_TOKEN, DATABRICKS_URL]):
    print("Por favor, verifique se COINMARKETCAP_API_KEY, DATABRICKS_TOKEN e DATABRICKS_URL estão definidos no arquivo .env")
    exit(1)

# Inicialize a API do Databricks
db = DatabricksAPI(
    host=DATABRICKS_URL,
    token=DATABRICKS_TOKEN
)

def extract_latest_data(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data")
        return None

def transform_data(data):
    """
    Transforma os dados extraídos, realizando limpeza, formatação e enriquecimento.
    """
    # Adicionando uma transformação para limpar valores nulos
    cleaned_data = [item for item in data['data'] if item['quote']['USD']['price'] is not None]

    return cleaned_data

def load_to_databricks(transformed_data, dbfs_path):
    """
    Carrega os dados transformados para o Databricks File System (DBFS).
    """
    # Inicializando uma sessão Spark
    spark = SparkSession.builder \
        .appName("Load Data to Databricks") \
        .getOrCreate()

    # Convertendo os dados transformados para um DataFrame Spark
    df = spark.createDataFrame(transformed_data)

    # Escrevendo o DataFrame para o DBFS como um arquivo parquet 
    df.write.mode('overwrite').parquet(dbfs_path)

    print(f"Data loaded to Databricks at {dbfs_path}")

def daily_update():
    print(f"Starting daily update at {datetime.now()}")

    # Extract
    data = extract_latest_data(COINMARKETCAP_API_KEY)
    if data is None:
        print("Update failed during extraction")
        return

    # Transform
    transformed_data = transform_data(data)

    # Load
    dbfs_path = '/datalake/bronze/bronze.parquet'
    load_to_databricks(transformed_data, dbfs_path)

    print(f"Daily update completed at {datetime.now()}")

# Execute o processo de atualização diária
daily_update()
