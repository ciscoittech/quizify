import mongoengine as me
from models import Exam, Subsection, Question, Option  # Ensure you import your models
import json

# Connect to MongoDB
me.connect('quizifyprov1', host='localhost', port=27017)

# Function to create an Option from a data dictionary
def create_option(data):
    return Option(
        text=data['text'],
        is_correct=data.get('is_correct', False),
        explanation=data.get('explanation', '')
    )

# Function to create a Question from a data dictionary
def create_question(data):
    return Question(
        text=data['text'],
        options=[create_option(opt) for opt in data['options']],
        difficulty=data.get('difficulty', 'Medium'),
        explanation=data.get('explanation', '')
    )

# Function to import data for a single exam
def import_data(exam_data):
    # Create subsections with embedded questions
    exam_subsections = []
    for sub_data in exam_data.get("subsections", []):
        subsection_questions = [create_question(q) for q in sub_data.get("questions", [])]
        exam_subsections.append(Subsection(
            name=sub_data['name'],
            description=sub_data.get('description', ''),
            questions=subsection_questions
        ))

    # Create the exam with embedded subsections
    exam = Exam(
        name=exam_data["name"],
        level=exam_data.get("level", "Intermediate"),
        price=exam_data.get("price", 0.0),
        description=exam_data.get("description", ""),
        description_short=exam_data.get("description_short", ""),
        description_long=exam_data.get("description_long", ""),
        possible_jobs=exam_data.get("possible_jobs", ""),
        issuing_organization=exam_data.get("issuing_organization", ""),
        is_active=exam_data.get("is_active", True),
        subsections=exam_subsections
    ).save()

# Read data from JSON file
with open('seasy.json', 'r') as file:
    exam_data = json.load(file)

# Import the data
import_data(exam_data)
print("Data imported successfully!")