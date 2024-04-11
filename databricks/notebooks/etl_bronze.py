import requests
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obtem a chave da API do ambiente
API_KEY = os.getenv('API_KEY')

def extract_data_from_api(api_key):
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
        print(f"Error {response.status_code}: Failed to retrieve data from API")
        return None

# Verificar se a API_KEY foi definida no arquivo .env
if not API_KEY:
    print("API_KEY não encontrada no arquivo .env")
    exit(1)

data = extract_data_from_api(API_KEY)

if data:
    spark = SparkSession.builder.appName("CryptoPricesLoader").getOrCreate()
    json_data = json.dumps(data['data'])
    rdd = spark.sparkContext.parallelize([json_data])
    df = spark.read.json(rdd)

    # Transforma dados conforme necessário
    df_transformed = df.select(
        col("id"),
        col("name"),
        col("symbol"),
        col("quote.USD.price").alias("price_usd"),
        col("quote.USD.volume_24h").alias("volume_24h_usd"),
        col("quote.USD.percent_change_24h").alias("percent_change_24h")
    )
    
    # Mostrar DataFrame transformado
    df_transformed.show()

    # Salvar DataFrame como tabela no Databricks ou no DBFS
    df_transformed.write.mode('overwrite').saveAsTable('crypto_prices_today')
else:
    print("Não foi possível recuperar os dados da API")

