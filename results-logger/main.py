import os
import json
import re
import copy
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class ResultsPlotter:
    """
    Create graphs based on pipeline results
    """

    def __init__(self, results_path: str, experiment_configs: dict) -> None:
        self.results_path = results_path
        self.experiment_configs = experiment_configs

    def load_metrics(self):
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
                            date1 = datetime.strptime(
                                cur_results["start_time"], date_format)
                            date2 = datetime.strptime(
                                cur_results["end_time"], date_format)
                            cur_results["time_taken"] = (
                                date2 - date1).total_seconds()

                            results.append(cur_results)
                            cur_results = copy.deepcopy(reset_results)

        for i, result in enumerate(results):
            result["config"] = self.experiment_configs[i]
        print(json.dumps(results, indent=2))
        self.results = results

    def create_graphs(self):
        metrics = ["time_taken", "hallucinations", "failures", "num_nodes", "num_edges", "avg_node_degree"]
        group1 = list(filter(lambda x : x["config"]["model"] == "gemma:2b", self.results))
        group2 = list(filter(lambda x : x["config"]["model"] == "gemma:7b", self.results))

        for metric in metrics:
            fig, ax = plt.subplots()
            g1 = list(map(lambda x: x[metric], group1))
            g2 = list(map(lambda x: x[metric], group2))

            configs = list(map(lambda x: x["config"], group1))
            bar_labels = []
            for config in configs:
                if config["pre_process"] == "none" and config["post_process"] == "none":
                    bar_labels.append("no pre/post process")
                elif config["pre_process"] == "none":
                    bar_labels.append("post process")
                elif config["post_process"] == "none":
                    bar_labels.append("pre process")
                else:
                    bar_labels.append("both pre/post process")
            
            x = np.arange(4)
            width = 0.35

            bars1 = ax.bar(x - width/2, g1, width, label='gemma:2b')
            bars2 = ax.bar(x + width/2, g2, width, label='gemma:7b')

            title = f"Configuration vs {metric}"

            ax.set_xlabel('Pipeline Configuration')
            ax.set_ylabel(metric)
            ax.set_title(title)
            ax.set_xticks(x)
            ax.set_xticklabels(bar_labels)
            ax.legend()

            graph_file_path = f"results-logger/graphs/{title}.png"
            plt.savefig(graph_file_path)
            print("Saved graph to", graph_file_path)
            plt.clf()
        # print(configs)
        # print(bar_labels)
            

        # group1 = [10, 15, 20, 25]
        # group2 = [12, 18, 22, 28]
        # x = np.arange(4)

        




if __name__ == "__main__":
    results_path = "airflow/logs/dag_id=experiment-textkg/run_id=manual__2024-04-16T02:32:41.582902+00:00"
    experiment_configs = [
        {'model': 'gemma:2b', 'pre_process': 'none', 'post_process': 'none'},
        {'model': 'gemma:2b', 'pre_process': 'none', 'post_process': 'fix'},
        {'model': 'gemma:2b', 'pre_process': 'summarize', 'post_process': 'none'},
        {'model': 'gemma:2b', 'pre_process': 'summarize', 'post_process': 'fix'},
        {'model': 'gemma:7b', 'pre_process': 'none', 'post_process': 'none'},
        {'model': 'gemma:7b', 'pre_process': 'none', 'post_process': 'fix'},
        {'model': 'gemma:7b', 'pre_process': 'summarize', 'post_process': 'none'},
        {'model': 'gemma:7b', 'pre_process': 'summarize', 'post_process': 'fix'}
    ]
    rp = ResultsPlotter(results_path, experiment_configs)
    rp.load_metrics()
    rp.create_graphs()
