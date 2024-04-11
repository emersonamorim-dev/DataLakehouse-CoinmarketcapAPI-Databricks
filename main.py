# Databricks notebook source
from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

API_KEY = os.getenv('COINMARKETCAP_API_KEY')

# Caminho relativo ajustado
relative_path = '/home/your-user/seu-diretorio/data-lakehouse-coinmarketcap/datalake/bronze/bronze.json'
BRONZE_FILE_PATH = os.path.join(os.getenv('HOME'), relative_path)

# Cria o diretório se não existir
os.makedirs(os.path.dirname(BRONZE_FILE_PATH), exist_ok=True)

# Importando após a verificação do diretório
from pipeline.extract.channels import extract_data_from_api, save_data_to_file
from pipeline.transform.silver import transform_to_silver, load_to_silver
from pipeline.aggregate.gold import transform_to_gold, load_to_gold

def fetch_data():
    try:
        print("Starting extraction...")
        bronze_data = extract_data_from_api(API_KEY)
        
        if bronze_data is None:
            print("Extraction failed. Exiting pipeline.")
            return None
        
        print("Extraction completed.")
        save_data_to_file(bronze_data, BRONZE_FILE_PATH)

        print("Transforming data to Silver...")
        silver_data = transform_to_silver(bronze_data)
        
        print("Transformation to Silver completed.")

        print("Transforming data to Gold...")
        gold_data = transform_to_gold(silver_data)
        
        print("Transformation to Gold completed.")

        print("Pipeline execution completed.")
        
        return bronze_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/')
def run_pipeline():
    data = fetch_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to execute data pipeline."})

if __name__ == "__main__":
    app.run(debug=True)