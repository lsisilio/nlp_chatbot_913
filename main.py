import os
import logging
from typing import List
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200

def format_response(texts: List[str]) -> jsonify:
    return jsonify({"fulfillmentMessages": [{"text": {"text": texts}}]})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Verificar a estrutura recebida
    logger.info(f"Recebido JSON: {data}")

    action = data['queryResult'].get('action', 'Unknown Action')
    parameters = data['queryResult'].get('parameters', {})
    
    # Extrair callback_data corretamente da requisição do Telegram
    callback_data = data['originalDetectIntentRequest']['payload']['data']['callback_query'].get('data')

    # Usando logs ao invés de print
    logger.info(f"action: {action}")
    logger.info(f"callback_data: {callback_data}")

    if action == 'cep':
        # Verificando se o CEP informado tem oito caracteres
        if re.fullmatch(r'\d{8}', callback_data):
            data = get_address(callback_data)
            response = format_response([data])
        else:
            logger.warning(f'callback_data não reconhecido: {callback_data}')
            response = format_response(['Nenhuma opção válida foi selecionada.'])

    elif action == 'inputUnknown':
        response = format_response(['Sorry, I did not understand that clearly.'])

    else:
        response = format_response([f'No handler for the action name {action}.'])
    return response


import requests
import random
# API ViaCEP
# https://viacep.com.br/
def get_address(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    
    response = requests.get(url)
    response_data = response.json()
    # print(response_data)
    if response.status_code == 200:
        previsão_entrega = random.randint(1, 14)    
        data = f"O documento será entregue na {response_data['logradouro']}, {response_data['localidade']} - {response_data['uf']} em até {previsão_entrega} dias."
        return data
    else:
        return f"Erro na requisição: {response.status_code}"


if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)
