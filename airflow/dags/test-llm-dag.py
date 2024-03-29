import ollama

from airflow import DAG
from airflow.decorators import task

from datetime import timedelta

LLM_MODEL = "gemma:7b"

default_args = {
    'owner': 'shrish',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create connection to ollama container
llm = ollama.Client(host='ollama')

with DAG(
    'test-llm-dag',
    default_args=default_args,
    description='Example DAG to invoke LLM',
    tags=['testing'],
) as dag:

    @task
    def extract_transcripts():
        print("extracting transcripts")
        return ["NLP", "Computer Vision", "Graph Neural Networks"]

    @task
    def summarize_transcripts(transcripts):
        print("summarizing transcripts for", transcripts)
        
        summaries = {}
        for transcript in transcripts:
            response = llm.chat(model=LLM_MODEL, messages=[
                {
                    'role': 'user',
                    'content': f'Briefly explain the following concept: {transcript}'
                }
            ])
            summaries[transcript] = response["message"]["content"]
            print(f'Generated summary for {transcript}: {summaries[transcript]}')
        
        return summaries

    @task
    def load_to_database(graph):
        print("saving to graph DB:", graph)

    # Setting up dependencies
    transcripts = extract_transcripts()
    graph = summarize_transcripts(transcripts)
    load = load_to_database(graph)
