from datetime import datetime
import mongoengine as me


class Quiz(me.Document):
    question_number = me.IntField(required=True)
    question = me.StringField(required=True)
    options = me.DictField()
    correct_answer = me.StringField(required=True)


class Question(me.Document):
    content = me.StringField(required=True)
    choices = me.DictField()
    correct_answer = me.StringField(required=True, choices=["A", "B", "C", "D", "E"])
    explanation = me.StringField()


class Subsection(me.Document):
    title = me.StringField(required=True)
    description = me.StringField()
    exam = me.ReferenceField('Exam')  # Reference to the Exam document
    questions = me.ListField(me.ReferenceField(Question))


class Exam(me.Document):
    name = me.StringField(required=True, unique=True)
    description = me.StringField()
    subsections = me.ListField(me.ReferenceField(Subsection))


