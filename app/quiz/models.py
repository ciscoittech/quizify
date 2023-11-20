import mongoengine as me
from mongoengine import Document, StringField, ReferenceField, ListField, EmbeddedDocumentField, FloatField, IntField, \
    DateTimeField


# Option Embedded Document
class Option(me.EmbeddedDocument):
    """
    Represents an option for a quiz question.
    Each option contains the answer text, a flag indicating if it's correct, and an optional explanation.
    """
    text = me.StringField(required=True)
    is_correct = me.BooleanField(default=False)
    explanation = me.StringField()


# Question Embedded Document
class Question(me.EmbeddedDocument):
    """
    Represents a single question in a quiz.
    Each question has a text, a related subsection, a set of options, a difficulty level, and an optional explanation.
    """
    text = me.StringField(required=True)
    subsection = me.ReferenceField('Subsection')  # Reference to a Subsection object
    options = me.ListField(me.EmbeddedDocumentField(Option))
    difficulty = me.StringField(choices=('Easy', 'Medium', 'Hard'))
    explanation = me.StringField()


# Subsection Document
class Subsection(me.Document):
    """
    Represents a subsection in an exam.
    Each subsection belongs to one exam and can contain multiple questions.
    """
    name = me.StringField(required=True)
    description = me.StringField()
    exam = me.ReferenceField('Exam')  # Reference to the Exam this subsection belongs to


# Exam Document
class Exam(me.Document):
    """
    Represents an entire exam or quiz.
    Each exam has a name, a list of subsections, a list of questions, and an active status flag.
    """
    name = me.StringField(required=True, unique=True)
    level = me.StringField(choices=['Beginner', 'Intermediate', 'Advanced'])
    price = me.FloatField(default=0.0)
    description = me.StringField()
    description_short = me.StringField()
    description_long = me.StringField()
    possible_jobs = me.StringField()
    issuing_organization = me.StringField()
    subsections = me.ListField(me.ReferenceField('Subsection'))  # List of subsections in the exam
    questions = me.ListField(me.EmbeddedDocumentField(Question))  # Questions included in the exam
    is_active = me.BooleanField(default=True)

    # Optional pre-delete hook
    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        # Handle cleanup of related data if necessary
        pass


# Optionally, connect signals for pre_delete actions
# me.signals.pre_delete.connect(Exam.pre_delete, sender=Exam)


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
