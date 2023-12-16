from bson import ObjectId
from pymongo import MongoClient


def get_exam_with_questions(exam_id):
    client = MongoClient('localhost', 27017)
    db = client.quizifyprov1  # Corrected database connection

    if not ObjectId.is_valid(exam_id):
        return None

    # pipeline = [
    #     {"$match": {"_id": ObjectId(exam_id)}},
    #     {"$unwind": "$subsections"},
    #     # Further stages as needed
    # ]

    # result = list(db.exams.aggregate(pipeline))
    # return result[0] if result else None

    exam = db.exam.find_one({"_id": ObjectId(exam_id)})
    return exam
