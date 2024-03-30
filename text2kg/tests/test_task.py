from text2kg.task import (
    LoadFolder,
    ExtractTranscripts
)


def test_load_folder():
    task = LoadFolder(folder_path="/home/student/course-materials")
    result = task.process(None)
    assert len(result) != 0


def test_extract_transcript():
    task = ExtractTranscripts()
    input_data = [
        '/home/student/course-materials/COMP1405-F19/LectureCaptions/1405-dec2_(SD_Large_-_WEB_MBL_(H264_1500)).mp4.csv',
        '/home/student/course-materials/COMP1405-F23/Lecture Captions/Linear Collections Lecture Recording.mp4.csv',
        '/home/student/course-materials/COMP1406-F23/Lecture Captions/Model View Controller Paradigm Lecture Recording.mp4.csv',
        '/home/student/course-materials/COMP1406-W23/Lecture Captions/MVC.mp4.csv',
        '/home/student/course-materials/COMP2406-W20/Lecture Captions/Template Engines Lecture Recording.mp4.csv',
        '/home/student/course-materials/COMP4601-F23/Lecture Captions/Search Lecture Recording.mp4.csv',
    ]
    result = task.process(input_data)
    assert len(result) != 0
