# Databricks notebook source
import json
import requests

# Substitua com o seu token de acesso pessoal do Databricks
databricks_token = 'your-databricks-token'

def transform_to_gold(silver_data):
    total_market_cap_brl = 0
    total_cryptocurrencies = 0
    average_price_usd = 0
    
    # Calcula o total de capitalização de mercado em BRL e o total de criptomoedas
    for item in silver_data:
        total_market_cap_brl += item.get('market_cap_brl', 0)
        total_cryptocurrencies += 1
    
    # Calcula o preço médio em USD
    if total_cryptocurrencies > 0:
        average_price_usd = sum(item.get('price_usd', 0) for item in silver_data) / total_cryptocurrencies
    
    # Cria um dicionário com os dados agregados
    gold_data = {
        'total_market_cap_brl': round(total_market_cap_brl, 2),
        'total_cryptocurrencies': total_cryptocurrencies,
        'average_price_usd': round(average_price_usd, 2),
    }
    
    return gold_data

def load_to_gold(gold_data):
    dbfs_path = 'dbfs:/datalake/gold/gold.json'
    
    with open("/home/your-user/seu-diretorio/datalake/gold/gold.json", "w") as f:
        json.dump(gold_data, f)
    
    upload_url = f'https://<your-databricks-workspace-url>/api/2.0/dbfs/put?path={dbfs_path}&overwrite=true'
    
    with open("/home/your-user/seu-diretorio/datalake/gold/gold.json", 'rb') as f:
        upload_response = requests.put(upload_url, headers={'Authorization': f'Bearer {databricks_token}'}, data=f)
    
    if upload_response.status_code == 200:
        print(f"Gold data saved successfully to {dbfs_path}")
    else:
        print(f"Error saving gold data: {upload_response.text}")

# Carrega dados da camada silver 
silver_data = json.loads(requests.get('https://api.example.com/silver-data').text)

# Transforma dados para a camada gold
gold_data = transform_to_gold(silver_data)

# Carrega dados na camada gold
load_to_gold(gold_data)
