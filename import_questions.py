import mongoengine as me
import os
import certifi
import json

# Define the models
class Option(me.EmbeddedDocument):
    text = me.StringField(required=True)
    is_correct = me.BooleanField(default=False)
    explanation = me.StringField()

class Question(me.EmbeddedDocument):
    text = me.StringField(required=True)
    subsection = me.StringField()
    options = me.ListField(me.EmbeddedDocumentField(Option))

class Exam(me.Document):
    name = me.StringField(required=True)
    price = me.FloatField(default=19.99)
    questions = me.ListField(me.EmbeddedDocumentField(Question))
    is_active = me.BooleanField(default=True)


# Load data from import_questions.json
with open("securityplus.json", "r") as file:
    data = json.load(file)

exam_data = data['Exam']

# Create an instance of Exam model
exam = Exam(name=exam_data['name'])

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
