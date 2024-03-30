from text2kg.core import Task
import logging


class LoadCSVTranscripts(Task):
    """Load CSV transcripts from folder path"""

    def process(self, data):
        logging.info("Loading transcripts")
        return ["text1", "text2", "text3"]


class CreateKnowledgeGraph(Task):
    """Create knowledge graph from transcripts"""

    def process(self, data):
        logging.info(f"Creating KG from transcripts: {data}")
        return {"nodes": [1, 2, 3], "edges": []}


class SaveToDatabase(Task):
    """Save knowledge graph to database"""

    def process(self, data):
        logging.info(f"Saving graph to DB: {data}")
