from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mongoengine as me
from mongoengine import signals
from mongoengine import Document, StringField, BinaryField, BooleanField, DateTimeField, EmbeddedDocument, FloatField, ReferenceField, ObjectIdField, ListField, IntField, EmbeddedDocumentField
from datetime import datetime
from app.quiz import models as quiz_models


class User(me.Document, UserMixin):
    email = me.StringField(required=True, unique=True)
    username = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    first_name = me.StringField()
    last_name = me.StringField()
    created_at = me.DateTimeField(auto_now_add=True)
    last_modified = me.DateTimeField(auto_now=True)
    tier = me.StringField(choices=["Free", "Paid", "Premium"])
    exams_taken = me.ListField(me.ReferenceField('ExamResult'))
    enrolled_exams = me.ListField(me.ReferenceField('Exam'))  # List of enrolled exams


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        # Logic for handling user deletion, e.g., removing related responses
        pass


signals.pre_delete.connect(User.pre_delete, sender=User)


class Response(EmbeddedDocument):
    question_id = ObjectIdField()
    selected_option_id = ObjectIdField()


class UserResponse(Document):
    user = ReferenceField(User, required=True)
    exam = ReferenceField(quiz_models.Exam, required=True)
    date_taken = DateTimeField()
    responses = ListField(EmbeddedDocumentField(Response))
    scores = FloatField()  # Store scores for this exam attempt
    attempt_number = IntField()  # Number of times a user has taken this specific exam

class Transaction(Document):
    TRANSACTION_STATUS = ('Completed', 'Pending', 'Failed', 'Refunded')
    
    user = ReferenceField(User, required=True)
    exam = ReferenceField(quiz_models.Exam, required=True)
    amount = FloatField(required=True)
    timestamp = DateTimeField()
    stripe_charge_id = StringField()
    status = StringField(choices=TRANSACTION_STATUS)