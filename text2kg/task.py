from datetime import datetime
from pymongo import MongoClient
from text2kg.core import Task, MultiTask, LLMTask, GroupByTask
from typing import List

import logging
import json
import os
import pandas as pd


class LoadFolder(Task):
    """
    Load files from folder path
    - input: None
    - output: list of files to process
    """

    def __init__(
        self,
        folder_path="/opt/course-materials",
        file_ext=".mp4.csv",
    ):
        """
        Args:
        - folder_path: Directory to load transcripts from
        - file_ext: File extension for transcripts to parse
        """
        self.folder_path = folder_path
        self.file_ext = file_ext

    def process(self, data: None) -> List:
        logging.info(f"Searching for transcripts in: {self.folder_path}")

        transcript_files = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith(self.file_ext):
                    file_path = os.path.join(root, file)
                    transcript_files.append(file_path)

        logging.info(f"Found transcript files={transcript_files}")
        return transcript_files


class ExtractTranscripts(MultiTask):
    """
    Extract transcript text from Zoom-generated CSV files
    - single_input: file_path
    - single_output: {file_path, transcript}
    """

    def process_single(self, single_data):
        file_path = single_data
        logging.info(f"Extract transcripts from file={file_path}")

        df = pd.read_csv(file_path)
        text_data = df['Text'].values
        transcript = " ".join(text_data)

        result = {
            "file_path": file_path,
            "transcript": transcript,
        }

        logging.info(f"Generated transcript={result}")
        return result


class SplitTranscripts(MultiTask):
    """
    Split transcripts into multiple smaller forms adhering to a context window
    - single_input: {file_path, transcript}
    - single_output: [{file_path, transcript1}, {file_path, transcript2}, ...]
    """

    def __init__(self, max_tokens=2000):
        """
        Args:
        - max_tokens: Maximum characters per transcript
        """
        self.max_tokens = max_tokens

    def process_single(self, single_data):
        file_path = single_data['file_path']
        transcript = single_data['transcript']

        logging.info(f"Splitting transcripts for file={file_path}")

        total_tokens = transcript.split(" ")
        logging.info(f"Original transcript tokens={len(total_tokens)}")

        if len(total_tokens) <= self.max_tokens:
            logging.info(f"No splitting neccesary")
            return single_data

        total_sentences = transcript.split(".")
        logging.info(f"Original transcript sentences={len(total_sentences)}")

        result = []
        cur_transcript = []

        for sentence in total_sentences:
            sentence_words = sentence.split(" ")
            if len(cur_transcript) + len(sentence_words) > self.max_tokens:
                result.append({
                    "file_path": file_path,
                    "transcript": " ".join(cur_transcript),
                })
                logging.info(f"Split into {len(cur_transcript)} tokens")
                cur_transcript = []

            cur_transcript.extend(sentence_words)

        logging.info(f'Split into {len(result)} transcripts')
        logging.info(f'Sub transcripts={result}')
        return result


class SummarizeTranscripts(MultiTask, LLMTask):
    """
    Invoke an LLM to summarize lecture transcript
    - single_input: {file_path, transcript}
    - single_output: {file_path, summary, contributors: [str]}
    """

    DEFAULT_PROMPT = """
    Summarize the following lecture transcript to identify key concepts relevant to the class.
    # Lecture Transcript
    {transcript}
    """

    def __init__(self, prompt=DEFAULT_PROMPT, *args, **kwargs):
        super().__init__(prompt, *args, **kwargs)

    def process_single(self, single_data):
        file_path = single_data['file_path']
        transcript = single_data['transcript']
        logging.info(f"Summarizing transcript for file_path={file_path}")

        prompt = self.prompt.format(transcript=transcript).strip()
        logging.info(f"Created LLM prompt={prompt}")
        logging.info(f"LLM prompt length={len(prompt)}")

        response = self._llm.generate(self.model, prompt)
        llm_response = response["response"]
        logging.info(f"Received LLM response={llm_response}")
        logging.info(f"LLM response length={len(llm_response)}")

        result = {
            "file_path": file_path,
            "summary": llm_response
        }
        return result


class SelectFew(Task):
    """Select few outputs for multi-output task. Useful for testing :D"""

    def __init__(self, start_index=0, count=1):
        """
        Args:
        - start_index: index to start selection from multi-output
        - count: number of outputs to select
        """
        self.start_index = start_index
        self.count = count

    def process(self, data):
        logging.info(f"Selecting one data from={data}")
        result = data[self.start_index:self.start_index + self.count]
        logging.info(f"Selected result={result}")
        return result


class GroupByFile(GroupByTask):
    """
    Group array-like data by file
    - input: [{file_path, summary}]
    - output: [[{file_path1, summary}], [{file_path2, summary}]]
    """

    def get_bucket_key(self, single_data):
        return single_data["file_path"]


class GroupByFolder(GroupByTask):
    """
    Group array-like data by folder
    - input: [{file_path=folder1/file1, summary}, {file_path=folder1/file2, summary}]
    - output: [[{file_path=folder1/file1, summary}, {file_path=folder1/file2, summary}], [...]]
    """

    def __init__(self, folder_mask='/opt/course-materials') -> None:
        """
        Args:
        - folder_mask: Path to exclude when grouping by folders
        """
        super().__init__()
        self.folder_mask = folder_mask

    def get_bucket_key(self, single_data):
        file_path = single_data["file_path"]
        logging.info(f"Creating bucket key for file_path={file_path}")

        masked_file_path = file_path[len(self.folder_mask)+1:]
        fp_elements = masked_file_path.split('/')
        bucket_key = fp_elements[0]

        logging.info(f"Using bucket key={bucket_key}")
        return bucket_key


class SplitSummaries(Task):
    """
    Enforce maximum token limit on buckets
    - input: [[{file_path1, summary1},{file_path1, summary2}], [{file_path2, summary}]]
    """

    def __init__(self, max_tokens=1000) -> None:
        """
        Args:
        - max_tokens: Maximum tokens per bucket
        """
        super().__init__()
        self.max_tokens = max_tokens

    def process(self, data):
        new_buckets = []

        for bucket in data:
            cur_bucket = []
            cur_tokens = 0

            for element in bucket:
                summary = element["summary"]
                summary_tokens = len(summary.split(" "))

                if cur_tokens + summary_tokens > self.max_tokens:
                    new_buckets.append(cur_bucket)
                    cur_bucket = []
                    cur_tokens = 0

                cur_tokens += summary_tokens
                cur_bucket.append(element)

            if cur_bucket:
                new_buckets.append(cur_bucket)

        logging.info(f"Created {len(new_buckets)} buckets")
        logging.info(f"Created buckets={new_buckets}")
        return new_buckets


class CreateKnowledgeGraphs(MultiTask, LLMTask):
    """
    Invoke an LLM to create knowledge graphs based on summaries
    - single_input: [{file_path, summary}]
    - single_output: [{file_path, nodes, edges, contributors: [str]}]
    """

    DEFAULT_SYSTEM_PROMPT = """
    Given the following key concepts extracted from a university lecture transcript, list the nodes and edges in JSON format that can form a knowledge graph based on the key topics.
    Only create nodes based on large concepts. Only create an edge if the source concept is a prequisite to understand the target concept.
    """

    DEFAULT_FORMAT_PROMPT = """
    # Output Format Instructions
    Produce only JSON output exactly like this: ```json\n{nodes: [{id: <name of concept>}...], edges: [{source: <id of source concept node>, target: <id of target concept node>}]}\n```
    # Key Concepts
    """

    DEFAULT_PROMPT = DEFAULT_SYSTEM_PROMPT + DEFAULT_FORMAT_PROMPT

    def __init__(self, prompt=DEFAULT_PROMPT, retries=3, *args, **kwargs):
        """
        Args:
        - prompt: Prompt used to generate knowledge graph
        - retries: Number of times to re-prompt LLM in case of invalid JSON
        """
        super().__init__(prompt, *args, **kwargs)
        self.retries = retries

    def process_single(self, single_data):
        file_path = single_data[0]["file_path"]

        logging.info(f"Creating KG on {len(single_data)} summaries")
        joint_summaries = list(map(lambda x: x["summary"], single_data))
        joint_summaries_text = "\n".join(joint_summaries)

        prompt = self.prompt.strip() + joint_summaries_text
        num_tokens = len(prompt.split(" "))
        logging.info(f"Creating prompt of length characters={len(prompt)}")
        logging.info(f"Creating prompt of length tokens={num_tokens}")
        logging.info(f"Creating prompt={prompt}")

        for _ in range(self.retries + 1):
            response = self._llm.generate(self.model, prompt)
            llm_response = response["response"]
            logging.info(f"Received LLM response={llm_response}")

            json_kg = self._santize_kg(llm_response)
            if json_kg:
                break

        if not json_kg:
            logging.error(
                f"Failed to create JSON KG after {self.retries} retries")
            return None

        result = {
            "file_path": file_path,
            "nodes": json_kg["nodes"],
            "edges": json_kg["edges"],
        }
        return result

    def _santize_kg(self, raw_kg: str):
        """
        Convert LLM response into JSON object
        Args:
        - raw_kg: LLM response containing knowledge graph
        """
        start_delim = "{"
        start_index = raw_kg.find(start_delim)
        end_delim = "}"
        end_index = raw_kg.rfind(end_delim)
        json_like_kg = raw_kg[start_index:end_index + len(end_delim)]

        try:
            json_kg = json.loads(json_like_kg)
            logging.info(f"Succesfully parsed as JSON={json_kg}")
            return json_kg
        except Exception as e:
            logging.warning(f"Unable to parse as JSON error={e}")
            return None


class CombineKnowledgeGraphs(MultiTask):
    """
    Combine a list of knowledge graphs into one
    - single_input: [{file_path, nodes, edges}] to combine
    - single_output: {nodes, edges} combined
    """

    def process_single(self, single_data):
        kg = {
            "file_path": "",
            "nodes": {},
            "edges": {},
        }
        renamed_ids = {}

        for single_kg in single_data:
            file_path: str = single_kg["file_path"]
            kg["file_path"] = file_path

            # Add nodes
            for node in single_kg["nodes"]:
                node_id: str = node["id"]

                new_node_id = node_id.lower()
                new_node = {
                    "id": new_node_id,
                    "sources": [file_path]
                }

                if new_node_id in kg["nodes"]:
                    # Update node sources
                    kg["nodes"][new_node_id]["sources"].append(file_path)
                else:
                    # Create node for first time
                    kg["nodes"][new_node_id] = new_node

                renamed_ids[node_id] = new_node_id

            # Add edges
            for edge in single_kg["edges"]:
                source = edge["source"]
                target = edge["target"]

                if source not in renamed_ids:
                    new_node_id = source.lower()
                    kg["nodes"][new_node_id] = {
                        "id": new_node_id,
                        "sources": [file_path]
                    }
                    logging.warning(
                        f"Adding new node from edges={new_node_id}")
                    renamed_ids[source] = new_node_id

                if target not in renamed_ids:
                    new_node_id = target.lower()
                    kg["nodes"][new_node_id] = {
                        "id": new_node_id,
                        "sources": [file_path]
                    }
                    logging.warning(
                        f"Adding new node from edges={new_node_id}")
                    renamed_ids[target] = new_node_id

                new_source = renamed_ids[source]
                new_target = renamed_ids[target]
                new_edge = {
                    "source": new_source,
                    "target": new_target,
                }

                kg["edges"][source + target] = new_edge

        kg["nodes"] = list(kg["nodes"].values())
        kg["edges"] = list(kg["edges"].values())

        num_nodes = len(kg["nodes"])
        num_edges = len(kg["edges"])

        logging.info(f"Created {num_nodes} nodes")
        logging.info(f"Created {num_edges} edges")

        return kg


class SaveToDatabase(MultiTask):
    """
    Save knowledge graph to database
    - single_input: [{file_path, nodes, edges}] to save
    - single_output: MongoDB result
    """

    def __init__(
        self,
        mongo_host='mongodb',
        mongo_port=27017,
        mongo_username="root",
        mongo_password="pw",

        folder_mask='/opt/course-materials',
        db_name='course-kg',
        collection_name='kg',
    ):
        """
        Args:
        - mongo_host: MongoDB host address
        - mongo_port: MongoDB port
        - mongo_username: MongoDB username
        - mongo_password: MongoDB password
        - folder_mask: Path to exclude when creating MongoDB collection
        - db_name: Name of database to use
        - collection_name: Name of collection to store KG in 
        """
        super().__init__()
        self.folder_mask = folder_mask

        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_username = mongo_username
        self.mongo_password = mongo_password

        self.db_name = db_name
        self.collection_name = collection_name

        self._connect_db()

    def _connect_db(self):
        self._client = MongoClient(
            self.mongo_host,
            self.mongo_port,
            username="root",
            password="pw",
        )
        self._db = self._client[self.db_name]
        self.collection = self._db[self.collection_name]
        logging.info(f"Using collection={self.collection}")

    def process_single(self, single_data):
        file_path = single_data["file_path"]
        masked_file_path = file_path[len(self.folder_mask)+1:]
        fp_elements = masked_file_path.split('/')
        project_name = f"{fp_elements[0]} {str(datetime.now())}"

        logging.info(f"Saving graph to DB: {project_name}")

        project = {
            "project_name": project_name,
            "nodes": single_data["nodes"],
            "edges": single_data["edges"],
        }

        project_id = self.collection.insert_one(project).inserted_id
        project_id_str = str(project_id)
        logging.info(f"Created project id={project_id_str}")
        return project_id_str
