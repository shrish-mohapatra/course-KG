from text2kg.core import Task, MultiTask
from typing import List

import logging
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
    - output: List of {file_path, transcript}
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


class CreateKnowledgeGraph(Task):
    """Create knowledge graph from transcripts"""

    def process(self, data):
        logging.info(f"Creating KG from transcripts: {data}")
        return {"nodes": [1, 2, 3], "edges": []}


class SaveToDatabase(Task):
    """Save knowledge graph to database"""

    def process(self, data):
        logging.info(f"Saving graph to DB: {data}")
