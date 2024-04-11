import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, date_trunc

# Config de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializa SparkSession
spark = SparkSession.builder.appName("CryptoDataGoldLayer").getOrCreate()

try:
    # Carrega dados da camada Silver
    silver_table_name = "silver_crypto_prices" 
    df_silver = spark.table(silver_table_name)
    
    # Agrega dados para calcular o preço médio diário por criptomoeda
    df_daily_avg = df_silver.groupBy("symbol", date_trunc("day", "timestamp").alias("day")) \
                            .agg(avg("price").alias("daily_avg_price"))
    
    
    # Salva o DataFrame resultante na camada Gold, otimizado para consultas BI
    gold_table_name = "gold_daily_avg_prices"  
    df_daily_avg.write.mode("overwrite").saveAsTable(gold_table_name)
    
    # Para salva para uso com ferramentas de BI externas
    logging.info("Processamento da camada Gold concluído com sucesso.")
except Exception as e:
    logging.error(f"Erro ao processar a camada Gold: {e}")
    raise e