import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from database import get_db_engine

def fetch_historical_data(days: int = 7):
    engine = get_db_engine()

    if engine is None:
        return pd.DataFrame()
    
    date_limit = datetime.now() - timedelta(days=days)

    SQL_QUERY = text("""
        SELECT
                timestamp_coleta,
                valor_compra
        FROM cotacoes
        WHERE timestamp_coleta >= :limit
        ORDER BY timestamp_coleta DESC
    """)

    try:
        df_history = pd.read_sql(
            SQL_QUERY,
            engine,
            params={'limit' : date_limit}
        )
        print(f"Histórico de {df_history.shape[0]} registros carregado com sucesso.")
        return df_history
    except Exception as e:
        print(f"ERRO ao buscar dados históricos: {e}")
        return pd.DataFrame()
    finally:
        engine.dispose()

def check_anomaly(df_current_data: pd.DataFrame, df_history: pd.DataFrame, threshold: float = 0.03):

    if df_history.empty:
        print("Alerta: Histórico insuficiente para análise.")
        return False
    
    # Valor de compra mais recente
    current_value = df_current_data['valor_compra'].iloc[0]

    # Média Móvel Histórica
    historic_mean = df_history['valor_compra'].mean()

    # Variação Percentual
    percentage_change = abs(current_value - historic_mean) / historic_mean

    print(f"\n--- Análise de Anomalia ---")
    print(f"Valor Atual (Compra): {current_value:.4f}")
    print(f"Média Histórica (Últimos 7 dias): {historic_mean:.4f}")
    print(f"Variação em Relação à Média: {percentage_change:.2%}")

    if percentage_change > threshold:
        print(f"Variação de {percentage_change:.2%} excede o limite de {threshold:.2%}!")
        return True
    else:
        print("Status: Variação dentro do limite normal. Sem alerta.")
        return False
