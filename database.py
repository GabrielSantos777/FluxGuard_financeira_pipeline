import requests
import pandas as pd
import json
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TABLE_NAME = "cotacoes"

def get_db_engine():
    try:
        engine = create_engine(DATABASE_URI)
        engine.connect()
        print("Conexão feita com sucesso!")
        return engine
    except Exception as e:
        print("Erro ao criar conexão: ", e)
        return None
    


def save_to_db(df: pd.DataFrame):

    engine = get_db_engine()

    if engine is None:
        print("Salvar no DB falhou: Motor de conexão indisponível.")
        return

    if df.empty:
        print("Salvar no DB ignorado: DataFrame está vazio.")
        return

    try:
        df.to_sql(
            TABLE_NAME,
            engine,
            if_exists='append',
            index=False,
            schema='public'
        )
        print(f"Dados inseridos com sucesso na tabela '{TABLE_NAME}'.")
    except Exception as e:
        print(f"ERRO ao inserir dados no banco: {e}")
    finally:
        engine.dispose()
        print("Conexão com o banco de dados fechada.")