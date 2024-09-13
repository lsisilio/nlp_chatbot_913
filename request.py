import requests
import json

# URL do seu webhook
webhook_url = "http://localhost:5000/webhook"

# Corpo da requisição (similar ao que o Dialogflow envia)
request_body = {
    "responseId": "12345678-1234-5678-1234-567812345678",
    "queryResult": {
        "queryText": "Escolhi a opção 1",
        "action": "input.welcome",
        "parameters": {
            "opcao": "1"
        },
        "allRequiredParamsPresent": True,
        "intent": {
            "displayName": "Opção 1 Intent"
        },
        "intentDetectionConfidence": 0.9,
        "languageCode": "pt-BR"
    },
    "session": "projects/project-id/agent/sessions/session-id"
}

# Enviando a requisição para o webhook
response = requests.post(webhook_url, json=request_body)

# Imprimindo a resposta
print("Resposta do webhook:", response.text)
