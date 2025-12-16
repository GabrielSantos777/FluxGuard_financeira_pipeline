from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import dcc
from dash import html
import plotly.express as px

dotenv_path = find_dotenv()
print("Arquivo .env encontrado em:", dotenv_path)

load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 
engine = create_engine(DATABASE_URI)

def fetch_data_for_dashboard():
    try:
        df = pd.read_sql("SELECT timestamp_coleta, valor_compra FROM cotacoes ORDER BY timestamp_coleta ASC", engine)
        df['valor_compra'] = df['valor_compra'].round(4)
        print(f"Dados carregados com sucesso para o Dash: {df.shape[0]} registros.")
        return df
    except Exception as e:
        print(f"ERRO ao carregar dados do DB para o Dash: {e}")
        return pd.DataFrame()

app = dash.Dash(__name__)
df_cotacao = fetch_data_for_dashboard()

fig = px.line(
    df_cotacao,
    x='timestamp_coleta',
    y='valor_compra',
    title='Tendência Histórica da Cotação USD/BRL'
)

fig.update_layout(xaxis_title="Data e Hora da Coleta", yaxis_title="Valor de Compra (R$)")

app.layout = html.Div(children=[
    html.H1(children='Monitoramento Financeiro (USD/BRL)', style={'textAlign': 'center'}),
    
    html.Div(children=f'Última Coleta Registrada: {df_cotacao["timestamp_coleta"].max().strftime("%d-%m-%Y %H:%M")}', style={'textAlign': 'center', 'marginBottom': '20px'}),
  
    dcc.Graph(
        id='cotacao-graph',
        figure=fig
    ) 
    
])
if __name__ == '__main__':
    app.run(debug=True)