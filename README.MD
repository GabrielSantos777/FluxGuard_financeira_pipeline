# Pipeline de Ingestão e Monitoramento de Dados Financeiros

Este projeto representa uma solução completa de **Engenharia de Dados (ETL)** e **Monitoramento em Tempo Real**, focada na série temporal da cotação USD/BRL. O objetivo principal foi sair do ambiente de Notebooks e construir uma pipeline automatizada (*full-stack*), integrando diversas tecnologias de produção, incluindo Python, PostgreSQL, Go (Golang) e Plotly Dash.

---

## Resultados e Funcionalidades

| Funcionalidade | Descrição | Status |
| :--- | :--- | :--- |
| **ETL Automatizado** | Coleta diária/horária de dados da cotação via API, persistindo o histórico no PostgreSQL. | ✅ Completo |
| **Módulo de Sistema (Go)** | Serviço em Go para consultas rápidas ao DB, simulando um *backend* de alta performance. | ✅ Completo |
| **Análise de Anomalia** | Lógica de negócio (Média Móvel) para disparar alertas se o preço variar > 3% do padrão. | ✅ Completo |
| **Dashboard Web Interativo** | Visualização completa do histórico da cotação via Plotly Dash (Python). | ✅ Completo |

---

## Stack Tecnológica

* **Linguagem de Análise e ETL:** Python
* **Bibliotecas Python:** `requests`, `pandas`, `SQLAlchemy`, `Plotly Dash`
* **Linguagem de Backend/Sistema:** Go (Golang)
* **Banco de Dados:** PostgreSQL
* **Driver Go:** `github.com/jackc/pgx/v4`
* **Orquestração:** Simulação de `cron` / Task Scheduler
* **Visualização:** Plotly Dash

---

## Ganhos de Conhecimento e Habilidades

Este projeto foi desenhado para expandir a *stack* do Python para as linguagens de Engenharia de Dados:

1.  **Engenharia de Dados (ETL em Produção):** Modularização do código (`ingest.py`, `database.py`, `main_pipeline.py`) e foco em *scripts* executáveis, prontos para agendamento.
2.  **SQL e Modelagem:** Configuração de um ambiente PostgreSQL real e prática na escrita de *queries* para séries temporais (usando `ORDER BY` e `LIMIT`).
3.  **Go (Golang) e Backend:** Introdução a uma linguagem estaticamente tipada, construindo um microserviço simples de consulta de banco, crucial para performance em *backend*.
4.  **Full-Stack de Dados:** Conexão bem-sucedida entre quatro tecnologias distintas, do Agendador (`cron`) ao Frontend (`Dash`), entregando um produto final ao usuário.

---

## Estrutura da Pipeline (Roadmap)

A solução foi construída em 6 fases interconectadas:

### Fase 1 & 2: Ingestão e Persistência (ETL)
* **`ingest.py`**: Conexão com a Awesome API (`requests`) e transformação dos dados (Pandas).
* **`database.py`**: Gerenciamento da conexão com o PostgreSQL (`SQLAlchemy`) e função `save_to_db` para inserção de novos registros.

### Fase 3 & 4: Análise e Automação
* **`analysis.py`**: Busca o histórico no DB, calcula a **Média Móvel** e verifica anomalias (variação > 3%).
* **`main_pipeline.py`**: O ponto de entrada unificado, que executa o ciclo completo e está pronto para ser agendado via `cron` ou Task Scheduler.

### Fase 5 & 6: Módulos de Deploy e Visualização
* **`go_monitor/monitor.go`**: Módulo em Go que se conecta ao DB para buscar o último valor, demonstrando uma alternativa de *backend* de alta performance para monitoramento.
* **`dashboard.py`**: Aplicação Plotly Dash que serve um dashboard web, lendo os dados históricos do PostgreSQL.

---

## Como Executar o Projeto

Para replicar esta pipeline, siga os passos abaixo:

### 1. Pré-requisitos
* Python 3.x e `pip`
* PostgreSQL instalado e rodando (com um banco de dados chamado `pipeline_db`)
* Go 1.18+ (opcional, para rodar a Fase 5)

### 2. Configuração do Ambiente Python
```bash
# Crie e ative o ambiente virtual
python -m venv pipeline_env
source pipeline_env/bin/activate 

# Instale as dependências
pip install pandas requests sqlalchemy psycopg2-binary dash plotly
```
### 3. Configuração do Banco de Dados
Importante: Atualize a variável DB_PASSWORD dentro do arquivo database.py com sua senha real do PostgreSQL.

### 4. Configuração do Ambiente Python
```bash
# Para rodar uma única coleta, salvando e analisando
python main_pipeline.py 
```
### 5. Execução do Dashboard Web
```bash
# Para iniciar o Dashboard (acessível em [http://127.0.0.1:8050/](http://127.0.0.1:8050/))
python dashboard.py
```
### 6. Execução do Módulo Go
```bash
# Navegue até a pasta do módulo
cd go_monitor
# Execute o programa Go
go run monitor.go
```
## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para criar problemas (issues) ou enviar solicitações de pull (pull requests) para melhorias ou correções.

## :memo: Licença

Esse projeto está sob a licença MIT.

---

*Este projeto foi desenvolvido por [Gabriel Santos/GabrielSantos777].*