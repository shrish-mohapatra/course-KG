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
        cur_transcript = ""

        for sentence in total_sentences:
            if len(cur_transcript) + len(sentence) > self.max_tokens:
                result.append({
                    "file_path": file_path,
                    "transcript": cur_transcript,
                })
                cur_transcript = ""

            cur_transcript += sentence

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

        response = self._llm.generate(self.model, prompt)
        llm_response = response["response"]
        logging.info(f"Received LLM response={llm_response}")

        result = {
            "file_path": file_path,
            "summary": llm_response
        }
        return result


class CreateKnowledgeGraph(Task):
    """Create knowledge graph from transcripts"""

    def process(self, data):
        logging.info(f"Creating KG from transcripts: {data}")
        return {"nodes": [1, 2, 3], "edges": []}


class SaveToDatabase(Task):
    """Save knowledge graph to database"""

    def process(self, data):
        logging.info(f"Saving graph to DB: {data}")
