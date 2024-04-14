import sys
sys.path.append('/opt/libraries')

from text2kg.task import (
    CombineKnowledgeGraphs,
    CreateKnowledgeGraphs,
    ExtractTranscripts,
    GroupByFile,
    GroupByFolder,
    LoadFolder,
    SaveToDatabase,
    SplitTranscripts,
    SplitSummaries,
    SummarizeTranscripts,
)
from text2kg.airflow import AirflowEngine
from text2kg.core import Pipeline


pipeline = Pipeline(
    tasks=[
        LoadFolder(),
        ExtractTranscripts(),
        SplitTranscripts(max_tokens=1000),
        SummarizeTranscripts(model="gemma:7b"),
        GroupByFile(),
        SplitSummaries(max_tokens=700),
        CreateKnowledgeGraphs(model="gemma:7b"),
        GroupByFolder(),
        CombineKnowledgeGraphs(),
        SaveToDatabase(collection_name="kg-7b"),
    ],
    pipeline_engine=AirflowEngine(
        dag_name="textkg-gemma-7b",
        description="using gemma7b with all transformations",
        tags=["testing"],
        dag_args={
            'owner': 'shrish',
            'depends_on_past': False,
            'retries': 1,
        }
    )
)
pipeline.run()
