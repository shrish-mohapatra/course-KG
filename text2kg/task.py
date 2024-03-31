from text2kg.core import Task, MultiTask, LLMTask
from typing import List

import logging
import ollama
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


class GroupByFile(Task):
    """
    Group array-like data by file
    - input: [{file_path, summary}]
    - output: [[{file_path1, summary}], [{file_path2, summary}]]
    """

    def process(self, data):
        logging.info(f"Creating buckets for data={data}")
        buckets = {}

        for single_data in data:
            file_path = single_data["file_path"]
            if file_path not in buckets:
                buckets[file_path] = []

            buckets[file_path].append(single_data)

        result = list(buckets.values())
        logging.info(f"Created {len(result)} buckets")
        logging.info(f"Buckets={result}")
        return result


class CreateKnowledgeGraphs(MultiTask, LLMTask):
    """
    Invoke an LLM to create knowledge graphs based on summaries
    - single_input: [{file_path, summary}]
    - single_output: [{file_path, kg, contributors: [str]}]
    """

    DEFAULT_SYSTEM_PROMPT = """
    Given the following key concepts extracted from a university lecture transcript, list the nodes and edges in JSON format that can form a knowledge graph based on the key topics.
    Only create nodes based on large concepts. Only create an edge if the source concept is a prequisite to understand the target concept.
    """

    DEFAULT_FORMAT_PROMPT = """
    # Output Format Instructions
    Produce only JSON output and nothing else like so: ```json\n{nodes: [{id: <name of concept>}...], edges: [{source: <id of source concept node>, target: <id of target concept node>}]}\n```
    # Key Concepts
    """

    DEFAULT_PROMPT = DEFAULT_SYSTEM_PROMPT + DEFAULT_FORMAT_PROMPT

    def __init__(self, prompt=DEFAULT_PROMPT, *args, **kwargs):
        super().__init__(prompt, *args, **kwargs)

    def process_single(self, single_data):
        file_path = single_data[0]["file_path"]

        logging.info(f"Creating KG on {len(single_data)} summaries")
        joint_summaries = list(map(lambda x: x["summary"], single_data))
        joint_summaries_text = "\n".join(joint_summaries)

        prompt = self.prompt.strip() + joint_summaries_text
        logging.info(f"Creating prompt of length={len(prompt)}")
        logging.info(f"Creating prompt={prompt}")

        response = self._llm.generate(self.model, prompt)
        llm_response = response["response"]
        logging.info(f"Received LLM response={llm_response}")

        result = {
            "file_path": file_path,
            "kg": llm_response
        }
        return result


class SaveToDatabase(Task):
    """Save knowledge graph to database"""

    def process(self, data):
        logging.info(f"Saving graph to DB: {data}")
