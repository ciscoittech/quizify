import mongoengine as me
import json
from mongoengine import Document, StringField, BinaryField, BooleanField, DateTimeField, EmbeddedDocument, FloatField, ReferenceField, ObjectIdField, ListField, EmbeddedDocumentField

# Connection to MongoDB
me.connect('quizifypro', host='localhost', port=27017)

# Define the models
class Option(me.EmbeddedDocument):
    text = StringField(required=True)
    is_correct = BooleanField(default=False)
    explanation = StringField()

class Question(EmbeddedDocument):
    text = StringField(required=True)
    subsection = StringField()
    options = ListField(EmbeddedDocumentField(Option))

class Exam(Document):
    name = StringField(required=True)
    price = FloatField(default=19.99)
    description = StringField()
    questions = ListField(EmbeddedDocumentField(Question))
    is_active = BooleanField(default=True)
    description_long = StringField()
    possible_jobs = StringField()

# Load data from securityplus.json
with open("securityplus.json", "r") as file:
    data = json.load(file)

exam_data = data['Exam']

# Create an instance of Exam model
exam = Exam(
    name=exam_data['name'],
    description=exam_data['description'],
    description_long=exam_data['description_long'],
    possible_jobs=', '.join(exam_data['possible_jobs'])
)

# Iterate through the questions and add them
for question_data in exam_data['questions']:
    question = Question(text=question_data['text'], subsection=exam_data['section'])
    for option_data in question_data['options']:
        option = Option(text=option_data['text'], is_correct=option_data.get('is_correct', False))
        question.options.append(option)
    exam.questions.append(question)

# Save to MongoDB
exam.save()
print("Data imported successfully!")
