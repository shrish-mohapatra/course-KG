import logging

from typing import List
from text2kg.core import PipelineEngine, Task

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import task


def get_task_id(task: Task) -> str:
    """Return a Task ID that can be used in Airflow"""
    return type(task).__name__


def execute_task(task: Task, **kwargs):
    """Execute task with Airflow context"""
    input_data = kwargs['ti'].xcom_pull(key='return_value')
    output_data = task.process(input_data)
    return output_data


class AirflowEngine(PipelineEngine):
    def __init__(
        self,
        dag_name: str,
        description: str,
        tags: List[str],
        dag_args: dict
    ):
        """
        Using Airflow Operator API to execute tasks.
        Airflow uses DAG - Directed Acyclic Graph, to represent pipelines.

        Args:
        - dag_name: Name of DAG in interface
        - description: Description metadata for DAG
        - tags: Tags metadata for DAG
        - dag_args: Scheduling-related DAG arguments
        """
        self.dag_name = dag_name
        self.description = description
        self.tags = tags
        self.dag_args = dag_args

    def execute(self, tasks: List[Task]):
        logging.info('Executing airflow dag')
        with DAG(
            'test-textkg-dag',
            default_args={
                'owner': 'shrish',
                'depends_on_past': False,
                'retries': 1,
            },
            description='Example pipeline to convert transcripts to knowledge graph',
            tags=['testing'],
        ) as dag:
            # Register tasks with Airflow DAG
            for i in range(len(tasks)):
                task = tasks[i]
                task_id = get_task_id(task)
                task_operator = PythonOperator(
                    task_id=task_id,
                    python_callable=execute_task,
                    op_kwargs={'task': task},
                    provide_context=True,
                    dag=dag,
                )

                # Configure task dependencies
                if i > 0:
                    prev_task = tasks[i-1]
                    prev_task_id = get_task_id(prev_task)
                    dag.set_dependency(prev_task_id, task_id)
