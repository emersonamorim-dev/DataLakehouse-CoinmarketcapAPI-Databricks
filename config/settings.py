import os

# Configurações da API do CoinMarketCap
CMC_API_KEY = os.environ.get('CMC_API_KEY', 'YOUR_DEFAULT_API_KEY')

# Configurações do Databricks
DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN', 'YOUR_DEFAULT_DATABRICKS_TOKEN')
DATABRICKS_WORKSPACE_URL = os.environ.get('DATABRICKS_WORKSPACE_URL', 'YOUR_DEFAULT_WORKSPACE_URL')

# Outras configurações globais
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')

# Verificar e criar diretórios necessários
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
