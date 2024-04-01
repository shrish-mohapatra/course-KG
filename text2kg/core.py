import abc
import logging
import ollama
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
        result = []
        num_sub_tasks = len(data)
        num_failures = 0

        for i in range(num_sub_tasks):
            logging.info(f"Processing subtask {i+1}/{num_sub_tasks}")
            single_data = data[i]
            single_result = self.process_single(single_data)

            if not single_result:
                num_failures += 1
                continue

            if isinstance(single_result, list):
                result.extend(single_result)
            else:
                result.append(single_result)

        logging.info(f"Number of failed subtasks={num_failures}")
        return result

    @abc.abstractmethod
    def process_single(self, single_data):
        """Perform operation on single data element within main task input_data"""
        pass


class GroupByTask(Task, abc.ABC):
    """
    Group array-like data by bucket-key
    - input: [data1, data2,...]
    - output: [ [data1, data2], [data3, data4], ...]
    """

    def process(self, data):
        logging.info(f"Creating buckets for data={data}")
        buckets = {}

        for single_data in data:
            bucket_key = self.get_bucket_key(single_data)
            if bucket_key not in buckets:
                buckets[bucket_key] = []

            buckets[bucket_key].append(single_data)

        result = list(buckets.values())
        logging.info(f"Created {len(result)} buckets")
        logging.info(f"Buckets={result}")
        return result
    
    @abc.abstractmethod
    def get_bucket_key(self, single_data):
        """
        Operation applied on single_data to be used as the key for creating buckets
        Args:
        - single_data: Single element from array-like data passed to task
        """
        pass


class LLMTask(Task):
    """Task which invokes an LLM to handle the processing of data"""

    DEFAULT_LLM_MODEL = "gemma:7b"
    DEFAULT_OLLAMA_HOST = "ollama"

    def __init__(
        self,
        prompt: str,
        model=DEFAULT_LLM_MODEL,
        host=DEFAULT_OLLAMA_HOST,
    ):
        self.prompt = prompt
        self.model = model
        self.host = host

        self._connect()

    def _connect(self):
        """Connect to LLM client"""
        self._llm = ollama.Client(host=self.host)
        logging.info(f"Connected to ollama client host={self.host}")


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
        return self.pipeline_engine.execute(self.tasks)
