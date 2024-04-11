import requests
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obtem a chave da API do ambiente
api_key = os.getenv('API_KEY')

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
        return None

def save_data_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f)


if api_key:
    # função `extract_data_from_api` para extrair os dados
    data = extract_data_from_api(api_key)

    if data:
        print(json.dumps(data, indent=4))
        
        # Caminho onde o arquivo bronze.json será salvo e carregado
        bronze_json_path = '/home/your-user/seu-diretorio/projetos-datalake-coinmarketcap/datalake/bronze/bronze.json'
        
        # Salvando os dados localmente
        save_data_to_file(data, bronze_json_path)
        print(f"Dados salvos localmente em {bronze_json_path}")
        
        # Salvando os dados no Databricks
        databricks_token = os.getenv('DATABRICKS_TOKEN')
        dbfs_path = 'dbfs:/datalake/bronze/bronze.json'
        
        # Substitua <your-databricks-workspace-url> pela URL do seu workspace do Databricks
        upload_url = f'https://<your-databricks-workspace-url>/api/2.0/dbfs/put?path={dbfs_path}&overwrite=true'
        with open(bronze_json_path, 'rb') as f:
            upload_response = requests.put(upload_url, headers={'Authorization': f'Bearer {databricks_token}'}, data=f)
        
        if upload_response.status_code == 200:
            print(f"Dados salvos com sucesso no Databricks no caminho {dbfs_path}")
        else:
            print(f"Erro ao salvar os dados no Databricks: {upload_response.text}")
    else:
        print("Não foi possível recuperar os dados")
else:
    print("API_KEY não encontrada no arquivo .env")
