from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "OK", 200

# Rota para lidar com as requisições do webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    # Processar a intent recebida
    intent_name = req.get('queryResult').get('intent').get('displayName')
    
    # Tratamento baseado no nome da intent
    if intent_name == 'floresta negra':
        response_text = "Certo, um bolo floresta negra"
    elif intent_name == 'cenoura':
        response_text = "Certo, um bolo de cenoura"
    elif intent_name == 'red velvet':
        response_text = "Certo, um bolo red velvet"
    else:
        response_text = "Desculpe, não entendi sua escolha."

    # Montar a resposta para o Dialogflow
    return make_webhook_response(response_text)

# Função para criar a resposta no formato aceito pelo Dialogflow
def make_webhook_response(text):
    return jsonify({
        "fulfillmentText": text,
        "source": "webhook"
    })

if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    # Iniciar o servidor Flask
    app.run(host='0.0.0.0', port=port)