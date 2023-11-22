from bson import ObjectId
from pymongo import MongoClient

def get_exam_with_questions(exam_id):
    client = MongoClient('localhost', 27017)
    db = client.your_database_name  # Replace with your actual database name

    # Ensure exam_id is a valid ObjectId
    if not ObjectId.is_valid(exam_id):
        return None  # or raise an exception

    pipeline = [
        {"$match": {"_id": ObjectId(exam_id)}},
        {"$unwind": "$subsections"},
        # Further stages as needed
    ]

    result = db.exams.aggregate(pipeline)  # Corrected to db.exams
    return list(result)

