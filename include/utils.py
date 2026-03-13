from airflow.providers.postgres.hooks.postgres import PostgresHook
import csv
import os

def create_conn(conn_id: str):
    hook = PostgresHook(postgres_conn_id=conn_id)
    conn = hook.get_conn()

    return conn

def read_sql(filename: str) -> str:
    with open(f"/usr/local/airflow/dags/sql/{filename}", "r") as f:
        return f.read()
    
def data_to_csv(data: tuple, output_path: str) -> None:
    headers, rows = data[0], data[1]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='') as file:
        writer =csv.writer(file)
        writer.writerow(headers) # escreve os nomes das colunas
        writer.writerows(rows)