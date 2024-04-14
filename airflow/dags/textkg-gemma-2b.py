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
        # LoadFolder(folder_path="/opt/course-materials/COMP4601-F23/Lecture Captions"),
        # LoadFolder(folder_path="/opt/course-materials/COMP1405-F19/LectureCaptions"),
        LoadFolder(),
        ExtractTranscripts(),
        SplitTranscripts(max_tokens=1000),
        SummarizeTranscripts(model="gemma:2b"),
        GroupByFile(),
        SplitSummaries(max_tokens=700),
        CreateKnowledgeGraphs(model="gemma:2b"),
        GroupByFolder(),
        CombineKnowledgeGraphs(),
        SaveToDatabase(),
    ],
    pipeline_engine=AirflowEngine(
        dag_name="textkg-gemma-2b",
        description="using gemma2b with all transformations",
        tags=["testing"],
        dag_args={
            'owner': 'shrish',
            'depends_on_past': False,
            'retries': 1,
        }
    )
)
pipeline.run()
