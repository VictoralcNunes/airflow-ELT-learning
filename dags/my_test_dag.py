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
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator, SQLCheckOperator
from pendulum import datetime

@dag(
    dag_id="my_test_dag",
    start_date=datetime(2026, 1, 1),
    catchup=False,
)
def my_test_dag():
    @task
    def extract_data() -> str:
        # código para extrair dados da base de dados e salvar em csv/json localmente
        
        return "dados extraídos"
    
    @task
    def save_data_locally(data: str) -> str:
        # código para salvar os dados localmente
        return "local de salvamento"

    @task
    def load_data(local_arquivo: str):
        # código para carregar os dados para o target_db
        pass

    check_data   = SQLCheckOperator(
        task_id="check_data",
        conn_id="postgres_source", # id da conexão com o target_db
        sql="sql/check_ingestion.sql", # query para verificar se os dados foram carregados
    )

    # data = extract_data()
    # local = save_data_locally(data) 
    # load_data(local) >> check_data # type: ignore
    check_data
    
my_test_dag()