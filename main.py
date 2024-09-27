import os
import logging
from typing import List
from flask import Flask, request, jsonify

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

    # Tratar diferentes ações baseadas na intent detectada
    if action == 'defaultWelcomeIntent':
        response = format_response(['Hi, how can I help you today?'])

    elif action == 'input.welcome':
        response = format_response(['testando resposta', 'apareceu aii?'])

    elif action == 'city.action':
        # Tratar o callback_data com mais cuidado, para lidar com None
        if callback_data == 'São Paulo':
            data = get_current_climate('São Paulo')
            response = format_response([data['temperature_mean']])
        elif callback_data == 'Berlin':
            data = get_current_climate('Berlin')
            response = format_response([data['temperature_mean']])
        elif callback_data == 'Tokyo':
            data = get_current_climate('Tokyo')
            response = format_response([data['temperature_mean']])
        else:
            logger.warning(f'callback_data não reconhecido: {callback_data}')
            response = format_response(['Nenhuma opção válida foi selecionada.'])

    elif action == 'inputUnknown':
        response = format_response(['Sorry, I did not understand that clearly.'])

    else:
        response = format_response([f'No handler for the action name {action}.'])

    return response


import json
import requests

# OpenWeatherMap API
WEATHER_API_BASE_URL    = 'http://api.openweathermap.org/data/2.5/forecast?'
WEATHER_API_KEY         = os.getenv('weather_api_key')
UNITS = 'metric'

def get_current_climate(city):
    url = WEATHER_API_BASE_URL + 'appid=' + WEATHER_API_KEY + '&q=' + city + '&units=' + UNITS
    
    response = requests.get(url).json()

    if response.status_code == 200:
        
        data = {
        'description': response['list'][0]['weather'][0]['description'],
        'temperature': response['list'][0]['main']['temp']
        }
        #chat_response = f'In {city}, we have {description} and the temperature is {temperature} degrees.'
        return data
    else:
        return f"Erro na requisição: {response.status_code}"
    

if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)





# def webhook():
#     req = request.get_json(silent=True, force=True)
    
#     # Processar a intent recebida
#     intent_name = req.get('queryResult').get('intent').get('displayName')
    
#     # Tratamento baseado no nome da intent
#     if intent_name == 'floresta negra':
#         response_text = "Certo, um bolo floresta negra"
#     elif intent_name == 'cenoura':
#         response_text = "Certo, um bolo de cenoura"
#     elif intent_name == 'red velvet':
#         response_text = "Certo, um bolo red velvet"
#     else:
#         response_text = "Desculpe, não entendi sua escolha."

#     # Montar a resposta para o Dialogflow
#     return make_webhook_response(response_text)
