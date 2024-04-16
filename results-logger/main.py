import os
import json
import re
import copy
from datetime import datetime


class ResultsPlotter:
    """
    Create graphs based on pipeline results
    """

    def __init__(self, results_path: str) -> None:
        self.results_path = results_path

    def load_metrics(self):
        """

        1. iterate through each task folder in results_path
        if task.name == LoadFolder
            set start time
        if task.name == CreateKnowledgeGraphs or CombineKnowledgeGraph
            count num warnings -> hallucinations
            count num ERRORS -> failures
        if task.name CombineKnowledgeGraph
            count num_nodes, num_edges, avg_node_degree
            set end time
            add cur_result to results
            create new one

        """
        DIR_PREFIX = "task_id="
        CHECK_TASKS = [
            "LoadFolder",
            "CreateKnowledgeGraphs",
            "CombineKnowledgeGraph"
        ]
        tasks_logs = []

        # Get relevant task logs
        for root, _, files in os.walk(results_path):
            if DIR_PREFIX not in root:
                continue

            # check task name
            matches = [
                check_task
                for check_task in CHECK_TASKS
                if check_task in root
            ]
            if not matches:
                continue

            task_files = []

            for file in files:
                task_files.append(os.path.join(root, file))

            task_id = int(re.search(r'/task_id=(\d+)',
                          task_files[-1]).group(1))
            tasks_logs.append([task_id, task_files[-1]])

        tasks_logs.sort(key=lambda x: x[0])
        # print("\ntask_logs=")
        # print(json.dumps(tasks_logs, indent=2))

        # get metrics
        results = []
        reset_results = {
            "start_time": 0,
            "end_time": 0,
            "time_taken": 0,
            "hallucinations": 0,
            "failures": 0,
            "num_nodes": 0,
            "num_edges": 0,
            "avg_node_degree": 0,
        }
        cur_results = copy.deepcopy(reset_results)

        for task_index, task_log in tasks_logs:
            with open(task_log, "r") as log_file:
                for line in log_file:
                    if "LoadFolder" in task_log:
                        # getting start time
                        if "Executing <Task(PythonOperator)" in line:
                            start = line.find('[') + 1
                            end = line.find(']')
                            timestamp = line[start:end]
                            cur_results["start_time"] = timestamp

                    if "CreateKnowledgeGraphs" in task_log or "CombineKnowledgeGraph" in task_log:
                        # getting hallucinations
                        if "WARNING" in line:
                            cur_results["hallucinations"] += 1

                        # getting failures
                        if "ERROR" in line:
                            cur_results["failures"] += 1

                    if "CombineKnowledgeGraph" in task_log:
                        # getting num_nodes, num_edges, avg_node_degree
                        metrics = ["num_nodes", "num_edges", "avg_node_degree"]
                        for metric in metrics:
                            keyword = f"METRICS: {metric}="
                            if keyword in line:
                                start = line.find(keyword) + len(keyword)
                                cur_results[metric] = float(line[start:])

                        # getting end time from
                        if "Returned value was" in line:
                            start = line.find('[') + 1
                            end = line.find(']')
                            timestamp = line[start:end]
                            cur_results["end_time"] = timestamp

                            date_format = "%Y-%m-%dT%H:%M:%S.%f%z"
                            date1 = datetime.strptime(cur_results["start_time"], date_format)
                            date2 = datetime.strptime(cur_results["end_time"], date_format)
                            cur_results["time_taken"] = (date2 - date1).total_seconds()

                            results.append(cur_results)
                            cur_results = copy.deepcopy(reset_results)

        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    results_path = "airflow/logs/dag_id=tests-textkg/run_id=manual__2024-04-15T23:26:16.764764+00:00"
    rp = ResultsPlotter(results_path)
    rp.load_metrics()
