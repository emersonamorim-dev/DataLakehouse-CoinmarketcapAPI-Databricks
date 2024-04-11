# Databricks notebook source
import json
import requests
from airflow.models import Variable
import logging

# Config logging
logger = logging.getLogger(__name__)

# Obtem o token de acesso e a URL do workspace do Databricks das variáveis do Airflow
databricks_token = Variable.get("databricks_token")
databricks_workspace_url = Variable.get("databricks_workspace_url")

def transform_to_silver(bronze_data):
    silver_data = []
    
    for item in bronze_data.get('data', []):
        name = item.get('name', '').strip()
        price = float(item.get('quote', {}).get('USD', {}).get('price', 0))
        price = round(price, 2)

        # Assume uma taxa de câmbio, que deveria ser obtida de uma fonte confiável ou configurável
        exchange_rate_usd_to_brl = 5.0
        market_cap_brl = price * exchange_rate_usd_to_brl

        transformed_data = {
            'name': name,
            'symbol': item.get('symbol', ''),
            'price_usd': price,
            'market_cap_brl': market_cap_brl,
        }

        silver_data.append(transformed_data)
    
    return silver_data

def load_to_silver(silver_data):
    try:
        dbfs_path = 'dbfs:/datalake/silver/silver.json'
        local_path = "/tmp/silver.json"
        with open(local_path, "w") as f:
            json.dump(silver_data, f)

        upload_url = f'https://{databricks_workspace_url}/api/2.0/dbfs/put?path={dbfs_path}&overwrite=true'
        with open(local_path, 'rb') as f:
            upload_response = requests.put(
                upload_url, 
                headers={'Authorization': f'Bearer {databricks_token}'}, 
                data=f
            )

        if upload_response.status_code == 200:
            logger.info(f"Silver data saved successfully to {dbfs_path}")
        else:
            logger.error(f"Error saving silver data: {upload_response.text}")

    except Exception as e:
        logger.error(f"Error loading data to silver layer: {str(e)}")

def transform_to_gold(silver_data):
    total_market_cap_brl = sum(item.get('market_cap_brl', 0) for item in silver_data)
    total_cryptocurrencies = len(silver_data)
    average_price_usd = sum(item.get('price_usd', 0) for item in silver_data) / total_cryptocurrencies if total_cryptocurrencies > 0 else 0

    gold_data = {
        'total_market_cap_brl': round(total_market_cap_brl, 2),
        'total_cryptocurrencies': total_cryptocurrencies,
        'average_price_usd': round(average_price_usd, 2),
    }
    
    return gold_data

def load_to_gold(gold_data):
    try:
        dbfs_path = 'dbfs:/datalake/gold/gold.json'
        local_path = "/tmp/gold.json"
        with open(local_path, "w") as f:
            json.dump(gold_data, f)

        upload_url = f'https://{databricks_workspace_url}/api/2.0/dbfs/put?path={dbfs_path}&overwrite=true'
        with open(local_path, 'rb') as f:
            upload_response = requests.put(
                upload_url, 
                headers={'Authorization': f'Bearer {databricks_token}'}, 
                data=f
            )

        if upload_response.status_code == 200:
            logger.info(f"Gold data saved successfully to {dbfs_path}")
        else:
            logger.error(f"Error saving gold data: {upload_response.text}")

    except Exception as e:
        logger.error(f"Error loading data to gold layer: {str(e)}")

def etl_bronze_to_gold():
    # função para carregar os dados bronze
    bronze_data = get_bronze_data()  
    silver_data = transform_to_silver(bronze_data)
    load_to_silver(silver_data)
    gold_data = transform_to_gold(silver_data)
    load_to_gold(gold_data)