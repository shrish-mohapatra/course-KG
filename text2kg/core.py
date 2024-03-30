import abc
from typing import List


class Task(abc.ABC):
    """Unit of work that processes data and produces an output"""

    @abc.abstractmethod
    def process(self, data):
        """
        Perform operation on data provided from previous task.
        Return value will be used as the input for the next task.
        """
        pass


class MultiTask(Task):
    """Split the task execution across an array of input data"""

    def process(self, data):
        return [
            self.process_single(single_data)
            for single_data in data
        ]

    @abc.abstractmethod
    def process_single(self, single_data):
        """Perform operation on single data element within main task input_data"""
        pass


class PipelineEngine(abc.ABC):
    """Pipeline engine is used to execute a sequence of tasks"""

    @abc.abstractmethod
    def execute(self, tasks: List[Task]):
        """Execute pipeline tasks"""
        pass


class Pipeline():
    """Specification for a sequence of tasks to execute"""

    def __init__(self, tasks: List[Task], pipeline_engine: PipelineEngine) -> None:
        self.tasks = tasks
        self.pipeline_engine = pipeline_engine

    def run(self):
        """Run pipeline of tasks"""
        self.pipeline_engine.execute(self.tasks)
