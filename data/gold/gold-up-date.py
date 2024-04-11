import json
from pymongo import MongoClient

# Dados a serem inseridos
data_to_insert = [
    {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "num_market_pairs": 10485,
        "date_added": "2010-07-13T00:00:00.000Z",
        "tags": "['mineable', 'pow', 'sha-256', 'store-of-value', 'state-channel', 'coinbase-ventures-portfolio', 'three-arrows-capital-portfolio', 'polychain-capital-portfolio', 'binance-labs-portfolio', 'blockchain-capital-portfolio', 'boostvc-portfolio', 'cms-holdings-portfolio', 'dcg-portfolio', 'dragonfly-capital-portfolio', 'electric-capital-portfolio', 'fabric-ventures-portfolio', 'framework-ventures-portfolio', 'galaxy-digital-portfolio', 'huobi-capital-portfolio', 'alameda-research-portfolio', 'a16z-portfolio', '1confirmation-portfolio', 'winklevoss-capital-portfolio', 'usv-portfolio', 'placeholder-ventures-portfolio', 'pantera-capital-portfolio', 'multicoin-capital-portfolio', 'paradigm-portfolio', 'bitcoin-ecosystem', 'ftx-bankruptcy-estate']",
        "max_supply": 21000000.0,
        "circulating_supply": 19504200.0,
        "total_supply": 19504200.0,
        "infinite_supply": False,
        "platform": None,
        "cmc_rank": 1,
        "self_reported_circulating_supply": None,
        "self_reported_market_cap": None,
        "tvl_ratio": None,
        "last_updated": "2023-10-05T01:29:00.000Z",
        "quote": "{'USD': {'price': 27737.411843883205, 'volume_24h': 10506637937.101198, 'volume_change_24h': -9.3355, 'percent_change_1h': -0.00175727, 'percent_change_24h': 1.49183613, 'percent_change_7d': 4.92686048, 'percent_change_30d': 7.73726917, 'percent_change_60d': -4.43975531, 'percent_change_90d': -7.58082087, 'market_cap': 540996028085.4668, 'market_cap_dominance': 49.6655, 'fully_diluted_market_cap': 582485648721.55, 'tvl': None, 'last_updated': '2023-10-05T01:29:00.000Z'}}"
    },
    {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "num_market_pairs": 7481,
        "date_added": "2015-08-07T00:00:00.000Z",
        "tags": "['pos', 'smart-contracts', 'ethereum-ecosystem', 'coinbase-ventures-portfolio', 'three-arrows-capital-portfolio', 'polychain-capital-portfolio', 'binance-labs-portfolio', 'blockchain-capital-portfolio', 'boostvc-portfolio', 'cms-holdings-portfolio', 'dcg-portfolio', 'dragonfly-capital-portfolio', 'electric-capital-portfolio', 'fabric-ventures-portfolio', 'framework-ventures-portfolio', 'hashkey-capital-portfolio', 'kenetic-capital-portfolio', 'huobi-capital-portfolio', 'alameda-research-portfolio', 'a16z-portfolio', '1confirmation-portfolio', 'winklevoss-capital-portfolio', 'usv-portfolio', 'placeholder-ventures-portfolio', 'pantera-capital-portfolio', 'multicoin-capital-portfolio', 'paradigm-portfolio', 'injective-ecosystem', 'layer-1', 'ftx-bankruptcy-estate']",
        "max_supply": None,
        "circulating_supply": 120241846.7043367773,
        "total_supply": 120241846.7043367773,
        "infinite_supply": True,
        "platform": None,
        "cmc_rank": 2,
        "self_reported_circulating_supply": None,
        "self_reported_market_cap": None,
        "tvl_ratio": None,
        "last_updated": "2023-10-05T01:29:00.000Z",
        "quote": "{'USD': {'price': 1647.2474157984113, 'volume_24h': 4597029645.57362, 'volume_change_24h': -12.4218, 'percent_change_1h': 0.11307395, 'percent_change_24h': 0.50414316, 'percent_change_7d': 2.62806468, 'percent_change_30d': 1.4586345, 'percent_change_60d': -10.19165419, 'percent_change_90d': -10.80335934, 'market_cap': 198068071254.5475, 'market_cap_dominance': 18.1823, 'fully_diluted_market_cap': 198068071254.55, 'tvl': None, 'last_updated': '2023-10-05T01:29:00.000Z'}}"
    },
    
]

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['your_db']
collection = db['your_collection']

# Inserir os dados no MongoDB
collection.insert_many(data_to_insert)

# Verificar se os dados foram inseridos corretamente
print(collection.count_documents({}))  
