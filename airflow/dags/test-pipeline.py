from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'shrish',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'test-airflow-dag',
    default_args=default_args,
    description='Example pipeline to convert transcripts to knowledge graph',
    tags=['testing'],
) as dag:

    @task
    def extract_transcripts():
        print("extracting transcripts")
        return ["text1", "text2", "text3"]

    @task
    def transform_to_graph(transcripts):
        print("creating graph from", transcripts)
        return {"nodes": [1,2,3], "edges": []}

    @task
    def load_to_database(graph):
        print("saving to graph DB:", graph)

    # Setting up dependencies
    transcripts = extract_transcripts()
    graph = transform_to_graph(transcripts)
    load = load_to_database(graph)
