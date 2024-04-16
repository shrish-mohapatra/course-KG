from pymongo import MongoClient

db_client = MongoClient(
    host="mongodb",
    port=27017,
    username="root",
    password="pw",
)

db = db_client["course-kg"]
collection = db["kg-7b"]