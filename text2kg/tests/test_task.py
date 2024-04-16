import pytest
from pymongo import MongoClient

from text2kg.task import (
    CombineKnowledgeGraphs,
    LoadFolder,
    ExtractTranscripts,
    SummarizeTranscripts,
    SplitTranscripts,
    GroupByFile,
    GroupByFolder,
    SplitSummaries,
    SaveToDatabase,
)

import text2kg.task as t2k


@pytest.fixture
def real_transcript():
    real_transcript_text = ""
    with open("./text2kg/tests/real_transcript.txt", "r") as f:
        real_transcript_text = f.read()

    return real_transcript_text


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


def test_summarize():
    task = SummarizeTranscripts(host="localhost:11434")
    input_data = [
        {
            'file_path': 'comp2406-express.mp4.csv',
            'transcript': 'Good morning everyone. Today, we will be discussing Express.js, a popular web application framework for Node.js. Express.js is known for its simplicity and flexibility, making it a favorite among developers for building web applications and APIs. Express.js is built on top of Node.js, which means it leverages the power of JavaScript and allows developers to easily create server-side applications. It provides a robust set of features that help in creating web servers, handling HTTP requests, and managing routes. One of the key features of Express.js is its middleware system. Middleware functions are functions that have access to the request object, the response object, and the next middleware function in the application’s request-response cycle. This allows developers to perform various tasks such as authentication, logging, and error handling before sending a response to the client. Another important aspect of Express.js is routing. With Express.js, developers can define routes for different HTTP methods such as GET, POST, PUT, and DELETE. This makes it easy to handle different types of requests and perform different actions based on the request method. Express.js also comes with a variety of built-in middleware and additional modules that can be easily integrated into an application. Some of these modules include body-parser for parsing incoming request bodies, cookie-parser for parsing cookie headers, and multer for handling file uploads. In addition to these features, Express.js also provides a templating engine called Pug (formerly known as Jade) that allows developers to generate HTML dynamically. This makes it easy to create dynamic web pages and render data from the server to the client. Overall, Express.js is a powerful and flexible framework for building web applications and APIs. Its simplicity and ease of use make it a popular choice among developers. Whether you are a beginner or an experienced developer, Express.js can help you build robust and scalable web applications. That concludes our lecture on Express.js. Thank you for joining us today. If you have any questions, feel free to ask.',
        },
        {
            'file_path': 'comp4601-recommender-systems.mp4.csv',
            'transcript': 'Good morning, everyone. Today, we will be discussing recommender systems. Recommender systems have become an essential part of our everyday lives, helping us discover new products, services, and content that we may not have otherwise come across. But what exactly are recommender systems? Recommender systems are algorithms that analyze user data and make personalized recommendations based on that information. These systems are used in a variety of industries, including e-commerce, streaming services, social media platforms, and more. They aim to provide users with relevant and personalized suggestions to improve their overall experience. There are several types of recommender systems, including collaborative filtering, content-based filtering, and hybrid systems. Collaborative filtering analyzes user behavior and preferences to recommend items that similar users have enjoyed. Content-based filtering, on the other hand, recommends items based on their attributes and features. Hybrid systems combine both collaborative and content-based filtering to provide more accurate and diverse recommendations. Recommender systems use various algorithms to make predictions and recommendations. Some common algorithms include matrix factorization, nearest neighbor, and deep learning models. These algorithms analyze user data, such as browsing history, ratings, and interactions, to generate personalized recommendations. There are several challenges associated with recommender systems, including data sparsity, cold start problems, and scalability issues. Data sparsity occurs when there is a lack of user data, making it difficult to generate accurate recommendations. Cold start problems occur when new items or users have limited data available, making it challenging to provide relevant suggestions. Scalability issues arise when recommender systems struggle to handle large amounts of data efficiently. Despite these challenges, recommender systems have proven to be highly effective in improving user engagement, increasing sales, and enhancing the overall user experience. Companies such as Amazon, Netflix, and Spotify rely on recommender systems to drive their businesses and provide personalized recommendations to their users. In conclusion, recommender systems play a crucial role in helping users discover new content and products, ultimately enhancing their overall experience. By analyzing user data and utilizing various algorithms, recommender systems can provide personalized and relevant recommendations to users, leading to increased user satisfaction and engagement. Thank you for listening.',
        }
    ]
    result = task.process(input_data)
    print(result)
    assert len(result) != 0


def test_split_transcript(real_transcript):
    task = SplitTranscripts()
    input_data = [
        {
            'file_path': 'comp2406-express.mp4.csv',
            'transcript': 'Good morning everyone. Today, we will be discussing Express.js, a popular web application framework for Node.js. Express.js is known for its simplicity and flexibility, making it a favorite among developers for building web applications and APIs. Express.js is built on top of Node.js, which means it leverages the power of JavaScript and allows developers to easily create server-side applications. It provides a robust set of features that help in creating web servers, handling HTTP requests, and managing routes. One of the key features of Express.js is its middleware system. Middleware functions are functions that have access to the request object, the response object, and the next middleware function in the application’s request-response cycle. This allows developers to perform various tasks such as authentication, logging, and error handling before sending a response to the client. Another important aspect of Express.js is routing. With Express.js, developers can define routes for different HTTP methods such as GET, POST, PUT, and DELETE. This makes it easy to handle different types of requests and perform different actions based on the request method. Express.js also comes with a variety of built-in middleware and additional modules that can be easily integrated into an application. Some of these modules include body-parser for parsing incoming request bodies, cookie-parser for parsing cookie headers, and multer for handling file uploads. In addition to these features, Express.js also provides a templating engine called Pug (formerly known as Jade) that allows developers to generate HTML dynamically. This makes it easy to create dynamic web pages and render data from the server to the client. Overall, Express.js is a powerful and flexible framework for building web applications and APIs. Its simplicity and ease of use make it a popular choice among developers. Whether you are a beginner or an experienced developer, Express.js can help you build robust and scalable web applications. That concludes our lecture on Express.js. Thank you for joining us today. If you have any questions, feel free to ask.',
        },
        {
            'file_path': 'comp4601-Rec systems.mp4.csv',
            'transcript': real_transcript,
        },
    ]
    result = task.process(input_data)
    print(result)
    assert len(result) != 0


def test_summarize2(real_transcript):
    t1 = SplitTranscripts(max_tokens=2000)
    t2 = SummarizeTranscripts(host="localhost:11434")
    input_data = [
        {
            'file_path': 'comp2406-express.mp4.csv',
            'transcript': real_transcript,
        }
    ]
    split_transcripts = t1.process(input_data)
    summaries = t2.process(split_transcripts)
    print(summaries)
    assert len(summaries) != 0


def test_group_by_file():
    input_data = [
        {'file_path': '/opt/course/COMP2406/Lecture/lec1.csv', 'summary': 'test'},
        {'file_path': '/opt/course/COMP2406/Lecture/lec2.csv', 'summary': 'test'},
        {'file_path': '/opt/course/COMP2406/Lecture/lec2.csv', 'summary': 'test'},
        {'file_path': '/opt/course/COMP4601/Lecture/lec1.csv', 'summary': 'test'},
        {'file_path': '/opt/course/COMP4601/Lecture/lec2-crawler.csv', 'summary': 'test'},
        {'file_path': '/opt/course/COMP1405/Lecture/lec1.csv', 'summary': 'test'},
    ]
    t1 = GroupByFile()
    grouped_files = t1.process(input_data)
    print(grouped_files)
    assert len(grouped_files) != 0


def test_group_by_folder():
    input_data = [
        {'file_path': '/opt/course-materials/COMP2406/Lecture/lec1.csv', 'summary': 'test'},
        {'file_path': '/opt/course-materials/COMP2406/Lecture/lec2.csv', 'summary': 'test'},
        {'file_path': '/opt/course-materials/COMP2406/Lecture/lec2.csv', 'summary': 'test'},
        {'file_path': '/opt/course-materials/COMP4601/Lecture/lec1.csv', 'summary': 'test'},
        {'file_path': '/opt/course-materials/COMP4601/Lecture/lec2-crawler.csv',
            'summary': 'test'},
        {'file_path': '/opt/course-materials/COMP1405/Lecture/lec1.csv', 'summary': 'test'},
    ]
    t1 = GroupByFolder()
    grouped_files = t1.process(input_data)
    print(grouped_files)
    assert len(grouped_files) != 0


def test_group_by_file_overflow():
    input_data = [
        {'file_path': 'lec1.csv', 'summary': 'test1'},
        {'file_path': 'lec1.csv', 'summary': 'test2'},
        {'file_path': 'lec1.csv', 'summary': 'test3'},

        {'file_path': 'lec2.csv', 'summary': 'test1'},
        {'file_path': 'lec2.csv', 'summary': 'test2'},
        {'file_path': 'lec2.csv', 'summary': 'test3'},
        {'file_path': 'lec2.csv', 'summary': 'test4'},
    ]
    expected_result = [
        [
            {'file_path': 'lec1.csv', 'summary': 'test1'},
            {'file_path': 'lec1.csv', 'summary': 'test2'},
        ],
        [
            {'file_path': 'lec1.csv', 'summary': 'test3'},
        ],
        [
            {'file_path': 'lec2.csv', 'summary': 'test1'},
            {'file_path': 'lec2.csv', 'summary': 'test2'},
        ],
        [
            {'file_path': 'lec2.csv', 'summary': 'test3'},
            {'file_path': 'lec2.csv', 'summary': 'test4'},
        ],
    ]
    t1 = GroupByFile()
    t2 = SplitSummaries(max_tokens=2)
    # add a new "Overflow()" task that takes these buckets and further subdivides
    # ideally reuse logic from split transcript
    grouped_files = t1.process(input_data)
    overflow_files = t2.process(grouped_files)
    assert overflow_files == expected_result


def test_combine_kg_sm():
    input_data = [[
        {
            "file_path": "comp2406/t1",
            "nodes": [
                {"id": "node1"},
                {"id": "node2"},
                {"id": "node3"},
            ],
            "edges": [
                {"source": "node1", "target": "node3"},
                {"source": "node1", "target": "node2"},
            ]
        },
        {
            "file_path": "comp2406/t2",
            "nodes": [
                {"id": "Node1"},
                {"id": "node4"},
                {"id": "node5"},
            ],
            "edges": [
                {"source": "Node1", "target": "node4"},
                {"source": "node4", "target": "node5"},
            ]
        }
    ]]
    expected_output = [{
        "nodes": [
            {
                "id": "node1",
                "sources": ["comp2406/t1", "comp2406/t2"],
            },
            {
                "id": "node2",
                "sources": ["comp2406/t1"],
            },
            {
                "id": "node3",
                "sources": ["comp2406/t1"],
            },
            {
                "id": "node4",
                "sources": ["comp2406/t2"],
            },
            {
                "id": "node5",
                "sources": ["comp2406/t2"],
            },
        ],
        "edges": [
            {"source": "node1", "target": "node3"},
            {"source": "node1", "target": "node2"},
            {"source": "node1", "target": "node4"},
            {"source": "node4", "target": "node5"},
        ],
    }]

    t = CombineKnowledgeGraphs()
    result = t.process(input_data)

    print(result)

    assert result == expected_output


def test_save_to_db():
    input_data = [{
        "file_path": "lectures/captions/comp2406",
        "nodes": [
            {
                "id": "node1",
                "sources": ["comp2406/t1", "comp2406/t2"],
            },
            {
                "id": "node2",
                "sources": ["comp2406/t1"],
            },
            {
                "id": "node3",
                "sources": ["comp2406/t1"],
            },
            {
                "id": "node4",
                "sources": ["comp2406/t2"],
            },
            {
                "id": "node5",
                "sources": ["comp2406/t2"],
            },
        ],
        "edges": [
            {"source": "node1", "target": "node3"},
            {"source": "node1", "target": "node2"},
            {"source": "node1", "target": "node4"},
            {"source": "node4", "target": "node5"},
        ],
    }]
    t = SaveToDatabase(
        mongo_host="localhost",
        folder_mask="lectures/captions",
        db_name="test-kg",
    )
    result = t.process(input_data)
    assert len(result) != 0


def test_get_from_db():
    t = SaveToDatabase(
        mongo_host="localhost",
        folder_mask="lectures/captions",
        # db_name="test-kg",
    )
    collection = t.collection

    # Get list of project names
    projects = collection.distinct("project_name")
    print(f'projects={projects}')

    # Get kg for specifc project name
    project_comp2406 = collection.find_one(
        {"project_name": "COMP1405-F19 2024-04-04 01:33:45.771794"})
    print(f'project_comp2406={project_comp2406}')


def test_similarity():
    node1 = "cold_start_problem"
    # node2 = "restful api"
    node2 = "cold_start"
    node3 = "HTTP endpoints"

    import numpy as np
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer(
        'sentence-transformers/all-MiniLM-L6-v2')

    embeddings = embedding_model.encode([node1, node2, node3])

    similarity_1 = 1 / (1 + np.linalg.norm(embeddings[0] - embeddings[1]))
    print(similarity_1)

    similarity_2 = 1 / (1 + np.linalg.norm(embeddings[0] - embeddings[2]))
    print(similarity_2)

    assert 1 == 2


def test_stemming():
    from nltk.stem import PorterStemmer

    stemmer = PorterStemmer()
    # texts = ["list", "lists", "Lists", "arrays"]
    texts = ["cold-start", "cold_start", "cold-start-problem", "cold-problem"]

    texts = [text.replace('-', ' ') for text in texts]
    texts = [text.replace('_', ' ') for text in texts]
    stemmed_texts = [stemmer.stem(text) for text in texts]
    print(stemmed_texts)
    assert 1 == 2


def test_experiment():
    print("create experiments")
    tasks = []
    FOLDER_PATH = "/opt/course-materials/COMP4601-F23/Lecture Captions"
    configs = []
    pre_process_labels = ["none", "summarize"]
    post_process_labels = ["none", "fix"]
    for model in ["gemma:2b", "gemma:7b"]:
        pre_process_configs = [
            [t2k.GroupByFile()],
            [
                t2k.SplitTranscripts(max_tokens=1000),
                t2k.SummarizeTranscripts(model=model),
                t2k.GroupByFile(),
                t2k.SplitSummaries(max_tokens=700),
            ],
        ]
        post_process_configs = [
            [],
            [t2k.FixKnowledgeGraphs(model=model)]
        ]

        for i, pre_process in enumerate(pre_process_configs):
            for j, post_process in enumerate(post_process_configs):
                configs.append({
                    "model": model,
                    "pre_process": pre_process_labels[i],
                    "post_process": post_process_labels[j],
                })
                exp_tasks = [
                    t2k.LoadFolder(folder_path=FOLDER_PATH),
                    t2k.ExtractTranscripts(),
                ]
                exp_tasks.extend(pre_process)
                exp_tasks.append(t2k.CreateKnowledgeGraphs(model=model))
                exp_tasks.extend(post_process)
                exp_tasks.extend([
                    t2k.GroupByFolder(),
                    t2k.CombineKnowledgeGraphs(),
                ])
                tasks.extend(exp_tasks)

    # for task in tasks:
    #     print(type(task).__name__)
    print(configs)


def test_fuzzy():
    from fuzzywuzzy import fuzz

    def add_text(text):
        for other_text in texts:
            sim = fuzz.ratio(text.lower(), other_text.lower())
            if sim >= 80:
                grouped_texts.add(other_text)
                return
        
        grouped_texts.add(text)

    grouped_texts = set()
    texts = ["Restful Design", "Restful API design", "RESTApi", "RESTApiNamingConventions"]
    for text in texts:
        add_text(text)
    
    print(grouped_texts)
