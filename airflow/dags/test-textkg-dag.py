import sys
sys.path.append('/opt/libraries')

from text2kg.task import (
    ExtractTranscripts,
    LoadFolder,
    SplitTranscripts,
    SummarizeTranscripts,
)
from text2kg.airflow import AirflowEngine
from text2kg.core import Pipeline


pipeline = Pipeline(
    tasks=[
        LoadFolder(folder_path="/opt/course-materials/COMP4601-F23/Lecture Captions"),
        ExtractTranscripts(),
        SplitTranscripts(),
        SummarizeTranscripts(),
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
