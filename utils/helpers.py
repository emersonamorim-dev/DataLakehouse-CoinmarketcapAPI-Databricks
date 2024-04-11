import logging
import json
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_info(message):
    """
    Log uma mensagem informativa.

    :param message: Mensagem para logar
    """
    logging.info(message)

def log_error(message):
    """
    Log uma mensagem de erro.

    :param message: Mensagem para logar
    """
    logging.error(message)

def load_json_file(filepath):
    """
    Carregar um arquivo JSON.

    :param filepath: Caminho do arquivo JSON
    :return: Dados carregados do arquivo JSON
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        log_error(f"Erro ao carregar o arquivo JSON: {e}")
        return None

def save_json_file(data, filepath):
    """
    Salvar dados em um arquivo JSON.

    :param data: Dados para salvar
    :param filepath: Caminho do arquivo para salvar os dados
    """
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        log_info(f"Dados salvos com sucesso em {filepath}")
    except Exception as e:
        log_error(f"Erro ao salvar o arquivo JSON: {e}")
