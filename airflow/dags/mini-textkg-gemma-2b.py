import sys
sys.path.append('/opt/libraries')

import text2kg.task as t2k
from text2kg.airflow import AirflowEngine
from text2kg.core import Pipeline


pipeline = Pipeline(
    tasks=[
        t2k.LoadFolder(folder_path="/opt/course-materials/COMP4601-F23/Lecture Captions"),
        # t2k.LoadFolder(folder_path="/opt/course-materials/COMP1405-F19/LectureCaptions"),
        # LoadFolder(),
        t2k.ExtractTranscripts(),
        t2k.SplitTranscripts(max_tokens=1000),
        t2k.SummarizeTranscripts(model="gemma:2b"),
        # t2k.GroupByFile(),
        # t2k.SplitSummaries(max_tokens=700),
        # t2k.ExtractConcepts(model="gemma:2b"),
        t2k.GroupByFile(),
        t2k.SplitSummaries(max_tokens=700),
        t2k.CreateKnowledgeGraphs(model="gemma:2b"),
        t2k.FixKnowledgeGraphs(model="gemma:2b"),
        t2k.GroupByFolder(),
        t2k.CombineKnowledgeGraphs(),
        t2k.SaveToDatabase(collection_name="mini-kg2"),
    ],
    pipeline_engine=AirflowEngine(
        dag_name="mini-textkg-gemma-2b",
        description="using gemma2b with all transformations on COMP 4601 folder",
        tags=["testing"],
        dag_args={
            'owner': 'shrish',
            'depends_on_past': False,
            'retries': 1,
        }
    )
)
pipeline.run()
