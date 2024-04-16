import sys
sys.path.append('/opt/libraries')

import text2kg.task as t2k
from text2kg.airflow import AirflowEngine
from text2kg.core import Pipeline


tasks = []
FOLDER_PATH = "/opt/course-materials/COMP4601-F23/Lecture Captions"
for model in ["gemma:2b", "gemma:7b"]:
    pre_process_configs = [
        [t2k.GroupByFile()],
        [
            t2k.SplitTranscripts(max_tokens=1000),
            t2k.SummarizeTranscripts(model=model),
            t2k.GroupByFile(),
            t2k.SplitSummaries(max_tokens=700),
        ],
    ]
    post_process_configs = [
        [],
        [t2k.FixKnowledgeGraphs(model=model)]
    ]

    for pre_process in pre_process_configs:
        for post_process in post_process_configs:
            exp_tasks = [
                t2k.LoadFolder(folder_path=FOLDER_PATH),
                t2k.ExtractTranscripts(),
            ]
            exp_tasks.extend(pre_process)
            exp_tasks.append(t2k.CreateKnowledgeGraphs(model=model))
            exp_tasks.extend(post_process)
            exp_tasks.extend([
                t2k.GroupByFolder(),
                t2k.CombineKnowledgeGraphs(),
            ])
            tasks.extend(exp_tasks)

pipeline = Pipeline(
    tasks=tasks,
    pipeline_engine=AirflowEngine(
        dag_name="experiment-textkg",
        description="experiment different pipeline configs for report discussion",
        tags=["auto-testing", "gemma2b", "gemma7b"],
        dag_args={
            'owner': 'shrish',
            'depends_on_past': False,
            'retries': 1,
        }
    )
)
pipeline.run()
