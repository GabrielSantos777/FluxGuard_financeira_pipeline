import requests
import pandas as pd
import json
from datetime import datetime

# URL da API para a cotação Dólar x Real
API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

#Requisição GET 
#código HTTP (200 = Sucesso, 404 = Não Encontrado, 500 = Erro Interno).
try:
    response = requests.get(API_URL)
    response.raise_for_status()

    data = response.json()
    print('Dados recebidos')
except requests.exceptions.RequestException as e:
    print("Erro ao Conectar à API: {e}")
    data = None

def transform_data(data):
    if not data or "USDBRL" not in data:
        print("Estrutura de Dados Invalida")
        return pd.DataFrame()
    
    quote = data['USDBRL']

    transformed = {
        'moeda_origem' : quote.get('code'),
        'moeda_destino' : quote.get('codein'),
        'valor_compra' : float(quote.get('bid')),
        'valor_venda' : float(quote.get('ask')),
        'timestamp_coleta' : datetime.now(),
        'data_coleta_api': datetime.fromtimestamp(int(quote.get('timestamp')))
    }

    df = pd.DataFrame([transformed])

    df = df[[
        'timestamp_coleta', 'data_coleta_api', 'moeda_origem', 'moeda_destino', 'valor_compra', 'valor_venda'
    ]]

    print("Dados Transformados em DataFrame do Pandas.")
    print(df.head())
    return df

if data:
    df_cotacao = transform_data(data)
    