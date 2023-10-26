from datetime import datetime
import mongoengine as me
from mongoengine import Document, StringField, BinaryField, BooleanField, DateTimeField, EmbeddedDocument, FloatField, ReferenceField, ObjectIdField, ListField, EmbeddedDocumentField, IntField
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
    description = StringField()
    questions = ListField(EmbeddedDocumentField(Question))
    is_active = BooleanField(default=True)
    description_short = StringField()
    description_long = StringField()
    possible_jobs = StringField()
    issueing_organization = StringField()
      # Exam status: active or archived

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        from quiz.models import UserResponse  # Import related models
        UserResponse.objects(exam=document).delete()

signals.pre_delete.connect(Exam.pre_delete, sender=Exam)



class LeaderboardEntry(Document):
    user = ReferenceField('User', required=True)  # Link to the User document
    total_scores = FloatField(default=0.0)  # Cumulative scores from all exams
    exams_attempted = IntField(default=0)  # Number of exams the user has taken
    exams_passed = IntField(default=0)  # Number of exams the user has passed
    average_score = FloatField(default=0.0)  # Average score from all exams
    last_updated = DateTimeField(auto_now=True)  # Timestamp of the last update to this leaderboard entry
    rank = IntField()  # The user's current rank; this will need to be updated whenever leaderboard changes

    meta = {
        'indexes': [
            '-total_scores',  # descending index on total_scores for faster leaderboard retrieval
            '-exams_passed',
            '-average_score'
        ]
    }
