from bson import ObjectId
from pymongo import MongoClient

def get_exam_with_questions(exam_id):
    client = MongoClient('localhost', 27017)
    db = 'quizifyprov1'  # Replace with your actual database name

    if not ObjectId.is_valid(exam_id):
        return None  # Handle invalid ObjectId

    pipeline = [
        {"$match": {"_id": ObjectId(exam_id)}},
        {"$unwind": "$subsections"},
        # Further stages as needed
    ]

    result = db.exams.aggregate(pipeline)
    return list(result)