import sys
sys.path.append('/opt/libraries')

from text2kg.core import Pipeline
from text2kg.airflow import AirflowEngine
from text2kg.task import (
    CreateKnowledgeGraph,
    ExtractTranscripts,
    LoadFolder,
    SaveToDatabase,
)


pipeline = Pipeline(
    tasks=[
        LoadFolder(),
        ExtractTranscripts(),
        # CreateKnowledgeGraph(),
        # SaveToDatabase(),
    ],
    pipeline_engine=AirflowEngine(
        dag_name="test-textkg",
        description="testing custom pipeline library",
        tags=["testing"],
        dag_args={
            'owner': 'shrish',
            'depends_on_past': False,
            'retries': 1,
        }
    )
)
pipeline.run()
