import requests
import pandas as pd
import json
import os
from datetime import datetime
from database import save_to_db
from analysis import fetch_historical_data, check_anomaly

API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

def fetch_transform():
    try:
        response = requests.get(API_URL)
        response.raise_for_status() 
        data = response.json()
        quote = data.get('USDBRL', {})
        
        if not quote:
            print("Erro: Dados de cotação inválidos ou incompletos.")
            return pd.DataFrame()

        transformed = {
            'moeda_origem': quote.get('code'),
            'moeda_destino': 'BRL',
            'valor_compra': float(quote.get('bid')),
            'valor_venda': float(quote.get('ask')),
            'timestamp_coleta': datetime.now(),
            'data_coleta_api': datetime.fromtimestamp(int(quote.get('timestamp')))
        }
        
        df = pd.DataFrame([transformed])
        df = df[[
            'timestamp_coleta', 'data_coleta_api', 'moeda_origem', 
            'moeda_destino', 'valor_compra', 'valor_venda'
        ]]
        print(f"Ingestão e Transformação SUCESSO. Valor: {df['valor_compra'].iloc[0]:.4f}")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE REQUISIÇÃO: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"ERRO INESPERADO na transformação: {e}")
        return pd.DataFrame()
    
def run_pipeline():
    df_current_data = fetch_transform()
    
    if df_current_data.empty:
        print("Pipeline interrompida devido a falha na ingestão.")
        return
    
    save_to_db(df_current_data)
    
    df_history = fetch_historical_data(days=7)
    check_anomaly(df_current_data, df_history, threshold=0.03)
    
    print("Pipeline executada com sucesso.")
    
# Ponto de Entrada para Execução Automática

if __name__ == "__main__":
    run_pipeline()
