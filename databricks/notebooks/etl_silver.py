import requests
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, ArrayType, MapType
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar SparkSession
spark = SparkSession.builder.appName("CryptoDataSilverLayer").getOrCreate()

# Obtem a chave da API do ambiente
API_KEY = os.getenv('API_KEY')

def extract_data_from_api(limit=10, convert='USD'):
    """
    Extrai os dados mais recentes de preços de criptomoedas da API do CoinMarketCap.
    """
    if API_KEY is None:
        print("Chave da API não encontrada no arquivo .env")
        return None

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start': '1', 'limit': str(limit), 'convert': convert}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Erro na requisição à API: {e}")
        return None

data = extract_data_from_api()

if data:
    # Define o esquema para os dados extraídos
    quote_schema = StructType([
        StructField("price", DoubleType()),
        StructField("volume_24h", DoubleType()),
        StructField("percent_change_1h", DoubleType()),
        StructField("percent_change_24h", DoubleType()),
        StructField("market_cap", DoubleType()),
        StructField("last_updated", StringType())
    ])

    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("symbol", StringType(), True),
        StructField("num_market_pairs", IntegerType(), True),
        StructField("date_added", StringType(), True),
        StructField("tags", ArrayType(StringType(), True)),
        StructField("max_supply", DoubleType(), True),
        StructField("circulating_supply", DoubleType(), True),
        StructField("total_supply", DoubleType(), True),
        StructField("cmc_rank", IntegerType(), True),
        StructField("last_updated", StringType(), True),
        StructField("quote", StructType([StructField("USD", quote_schema)]))
    ])

    json_data = json.dumps(data['data'])
    df_raw = spark.read.schema(schema).json(spark.sparkContext.parallelize([json_data]))

    # Seleciona e transforma os dados necessários
    df_transformed = df_raw.select(
        "id", "name", "symbol", "num_market_pairs", "date_added",
        "max_supply", "circulating_supply", "total_supply", "cmc_rank",
        "last_updated", col("quote.USD.*")
    )

    df_transformed.show()
