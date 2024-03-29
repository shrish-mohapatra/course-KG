from text2kg.core import Pipeline, Task

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import DirectoryLoader


class LoadTranscripts(Task):
    def __init__(self, src_folder: str) -> None:
        """
        Load text transcripts from specified folder

        Args:
        - src_folder: Location containing transcripts
        """
        self.src_folder = src_folder

    def process(self, data):
        Task.logger.info("loading file")
        # loader = DirectoryLoader(
        #     self.src_folder,
        #     glob="**/*.csv",
        #     loader_cls=CSVLoader,
        #     loader_kwargs={},
        # )
        # docs = loader.load()
        # return docs

src_folder = "/home/student/course-materials/COMP2406-W20/Lecture Captions"

pipeline = Pipeline([
    LoadTranscripts(src_folder=src_folder)
])
pipeline.run()
