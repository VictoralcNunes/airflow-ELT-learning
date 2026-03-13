# Airflow ELT Learning (Astro)

Este repositório contém um projeto de exemplo para aprender a desenvolver pipelines ELT com **Apache Airflow** + **Astro Runtime**.
O exercício foi proposto pela Indicium durante o Ciclo Preparatório para o Programa Lighthouse 26-1.
---

## 🚀 Objetivo

Este projeto demonstra como extrair dados de um banco Postgres (source), processar/carregar em outro Postgres (target) e como validar a ingestão usando DAGs do Airflow.

---

## 🧩 O que este projeto faz

O pipeline principal está implementado em `dags/my_elt_dag.py` e inclui:

- **Extração**: lê dados da tabela `customers` no Postgres de origem (`source_db`) via conexão `postgres_source`.
- **Persistência local**: salva os dados extraídos em CSV em `/usr/local/airflow/data/customers.csv`.
- **Carga**: cria a tabela de destino (se não existir) em `target_db` e importa o CSV usando `COPY`.
- **Validação**: executa um `SQLCheckOperator` para garantir que a ingestão ocorreu como esperado.

Além disso, há um DAG de exemplo (`dags/exampledag.py`) que demonstra o uso do TaskFlow API e *dynamic task mapping*.

---

## ✅ Pré-requisitos

1. **Git** (para clonar o repositório)
2. **Docker** (incluindo Docker Compose)
3. **Python 3.10+** (recomendado 3.11)
4. **Astro CLI** (recomendado para rodar localmente)
   - Instalação rápida: `curl -sSL https://install.astronomer.io | sh`
   - Documentação: https://www.astronomer.io/docs/astro/cli

> ⚠️ Se você não quiser usar Astro CLI, é possível rodar o Airflow nativo (via `airflow standalone`) após instalar as dependências Python.

---

## 🛠️ Setup (primeira vez)

```bash
# 1) Clone o repositório
git clone <URL_DO_REPO>
cd airflow-ELT-learning

# 2) Crie e ative um ambiente virtual Python
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

# 3) Instale dependências Python
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🐘 Rodar bancos de dados (Postgres)

O projeto inclui um `docker-compose.yml` em `include/docker-compose.yml` que sobe dois bancos Postgres (source/target).

```bash
# 1) Crie a rede Docker usada pelo compose (se ainda não existir)
docker network create lighthouse-exercise_4bdc08_airflow || true

# 2) Inicie os containers
docker compose -f include/docker-compose.yml up -d
```

> 🔎 Os bancos ficam disponíveis em:
> - Source: `localhost:5433` (db `source_db` / user `postgres` / senha `postgres`)
> - Target: `localhost:5434` (db `target_db` / user `postgres` / senha `postgres`)

---

## ▶️ Executar o Airflow (recomendado: Astro CLI)

```bash
# Inicia o Airflow (webserver + scheduler + triggerer, etc.)
astro dev start
```

Após subir, acesse o Airflow UI em: http://localhost:8080

> 🔧 O arquivo `airflow_settings.yaml` já configura as conexões `postgres_source` e `postgres_target` usadas pelos DAGs.

---

## 🧪 Executar testes

```bash
pytest
```

---

## 📂 Onde colocar novos DAGs / código

- **DAGs**: `dags/`
- **SQL**: `dags/sql/`
- **Helpers**: `include/utils.py`
- **Configuração local do Airflow**: `airflow_settings.yaml`

---

## 📝 Observações

- Este projeto usa a imagem do Astro Runtime via `Dockerfile`.
- Se precisar alterar versões de dependências, edite `requirements.txt` e reconstrua o runtime (Astro rebuild).
