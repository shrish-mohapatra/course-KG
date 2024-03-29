import abc
import logging

from typing import List


class Task(abc.ABC):
    """Abstract base class for tasks to execute within a Pipeline"""
    logger: logging.Logger = logging.getLogger("taskLogger")

    @abc.abstractmethod
    def process(self, data):
        """
        Receive data from previous tasks and perform some operation with it.
        Return values will be passed to next task.
        """
        pass


class Pipeline:
    """Pipeline for transforming text transcripts into knowledge graphs"""

    def __init__(self, tasks: List[Task]):
        """
        Args
        - tasks: list of Task instances to run in order
        """
        self.tasks = tasks

    def run(self, data=None):
        """Execute pipeline's sequence of tasks"""
        for task in self.tasks:
            data = task.process(data)
        return data
