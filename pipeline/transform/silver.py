# Databricks notebook source
import json
import requests

# token de acesso pessoal do Databricks
databricks_token = 'your-databricks-token'

def transform_to_silver(bronze_data):
    silver_data = []
    
    for item in bronze_data.get('data', []):
        # remove espaços extras no nome
        name = item.get('name', '').strip()

        # converte o preço para um formato fixo
        price = float(item.get('quote', {}).get('USD', {}).get('price', 0))
        price = round(price, 2)  

        # calcula o valor de mercado em BRL assumindo uma taxa de câmbio fixa
        exchange_rate_usd_to_brl = 5.0  
        market_cap_brl = price * exchange_rate_usd_to_brl

        # Cria um novo dicionário com os dados transformados
        transformed_data = {
            'name': name,
            'symbol': item.get('symbol', ''),
            'price_usd': price,
            'market_cap_brl': market_cap_brl,
        }

        silver_data.append(transformed_data)
    
    return silver_data


def load_to_silver(silver_data):
    dbfs_path = 'dbfs:/datalake/silver/silver.json'
    
    with open("/home/your-user/seu-diretorio/datalake/silver/silver.json", "w") as f:
        json.dump(silver_data, f)
    
    upload_url = f'https://<your-databricks-workspace-url>/api/2.0/dbfs/put?path={dbfs_path}&overwrite=true'
    
    with open("/home/your-user/seu-diretorio/datalake/silver/silver.json", 'rb') as f:
        upload_response = requests.put(upload_url, headers={'Authorization': f'Bearer {databricks_token}'}, data=f)
    
    if upload_response.status_code == 200:
        print(f"Silver data saved successfully to {dbfs_path}")
    else:
        print(f"Error saving silver data: {upload_response.text}")

# Carregar dados da camada bronze 
bronze_data = json.loads(requests.get('https://api.example.com/bronze-data').text)

# Transformar dados para a camada silver
silver_data = transform_to_silver(bronze_data)

# Carregar dados na camada silver
load_to_silver(silver_data)
