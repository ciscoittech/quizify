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
def create_question(data, subsections):
    # Find the corresponding subsection object
    subsection = next((sub for sub in subsections if sub.name == data['subsection']), None)

    return Question(
        text=data['text'],
        subsection=subsection,
        options=[create_option(opt) for opt in data['options']],
        difficulty=data.get('difficulty', 'Medium'),
        explanation=data.get('explanation', '')
    )


# Function to import data
def import_data(data):
    for exam_data in data:
        # Create exam with embedded subsections
        exam_subsections = [Subsection(name=sub['name'], description=sub.get('description', '')) for sub in
                            exam_data.get("Subsections", [])]

        exam = Exam(
            name=exam_data["name"],
            level=exam_data.get("level", "Intermediate"),
            price=exam_data.get("price", 0.0),
            # ... other exam fields ...
            subsections=exam_subsections,
            questions=[create_question(q, exam_subsections) for q in exam_data.get("Questions", [])]
        ).save()


# Read data from JSON file
with open('your_data_file.json', 'r') as file:
    data = json.load(file)

# Import the data
import_data(data)
