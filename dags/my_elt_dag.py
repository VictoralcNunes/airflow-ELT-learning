# airflow imports

# criar dag

#tasks:
#  1 - conectar a base de dados e extrair os dados em csv (python operator ou decorator): 
#       - tabela costumers em source_db
#  2 - salvar em csv/json localmente
#  3 - carregar os dados para o target_db (postgres operator? sqlexecutequeryoperator?)
#  4 - (opcional) deletar o arquivo local
#  5 - fazer um check para garantir que os dados foram carregados corretamente (sql check operator)

#  chamar a dag
from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLCheckOperator, SQLExecuteQueryOperator
from pendulum import datetime
from include.utils import create_conn, read_sql, data_to_csv

@dag(
    dag_id="my_elt_dag",
    start_date=datetime(2026, 1, 1),
    catchup=False,
)
def my_elt_dag():
    @task
    def extract_data() -> str:
        # código para extrair dados da base de dados e salvar em csv/json localmente
        conn = create_conn("postgres_source")
        cursor = conn.cursor()

        sql= read_sql("extract_table.sql")

        cursor.execute(sql)
        
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] # pega os nomes das colunas

        output_path = "/usr/local/airflow/data/customers.csv"
        data_to_csv((headers, rows), output_path)
        
        return output_path
    
    # @task
    # def save_data_locally() -> str:
    #     # código para salvar os dados localmente
    #     return "local de salvamento"

    create_table_if_not_exists = SQLExecuteQueryOperator(
        task_id="create_table_if_not_exists",
        sql="sql/create_table.sql", # query para criar a tabela no target_db
        conn_id="postgres_target" # id da conexão com o target_db
    )

    @task
    def load_data(**context) -> None:
        # código para carregar os dados para o target_db
        conn = create_conn("postgres_target")
        cursor = conn.cursor()

        file_path = context['ti'].xcom_pull(task_ids='extract_data')
        with open(file_path, "r") as f:
            next(f)  # pula o cabeçalho
            cursor.copy_expert(
                "COPY customers FROM STDIN WITH CSV", f
            )

        conn.commit()
        cursor.close()
        conn.close()

    check_data   = SQLCheckOperator(
        task_id="check_data",
        sql="sql/check_ingestion.sql", # exemplo de query para verificar se os dados foram carregados
        conn_id="postgres_target" # id da conexão com o target_db
    )
    
    extract_data() >> create_table_if_not_exists >> load_data() >> check_data
    
my_elt_dag()