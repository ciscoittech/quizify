from datetime import datetime
import mongoengine as me
from mongoengine import Document, StringField, BinaryField, BooleanField, DateTimeField, EmbeddedDocument, FloatField, ReferenceField, ObjectIdField, ListField, EmbeddedDocumentField
from mongoengine import signals


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
    questions = ListField(EmbeddedDocumentField(Question))
    is_active = BooleanField(default=True)  # Exam status: active or archived

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        from quiz.models import UserResponse  # Import related models
        UserResponse.objects(exam=document).delete()

signals.pre_delete.connect(Exam.pre_delete, sender=Exam)

