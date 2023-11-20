import mongoengine as me

# Option Embedded Document
class Option(me.EmbeddedDocument):
    text = me.StringField(required=True)
    is_correct = me.BooleanField(default=False)
    explanation = me.StringField()

# Question Embedded Document
class Question(me.EmbeddedDocument):
    text = me.StringField(required=True)
    options = me.ListField(me.EmbeddedDocumentField(Option))
    difficulty = me.StringField(choices=('Easy', 'Medium', 'Hard'))
    explanation = me.StringField()

# Subsection Embedded Document
class Subsection(me.EmbeddedDocument):
    name = me.StringField(required=True)
    description = me.StringField()
    questions = me.ListField(me.EmbeddedDocumentField(Question))

# Exam Document
class Exam(me.Document):
    name = me.StringField(required=True, unique=True)
    level = me.StringField(choices=['Beginner', 'Intermediate', 'Advanced'])
    price = me.FloatField(default=0.0)
    description = me.StringField()
    description_short = me.StringField()
    description_long = me.StringField()
    possible_jobs = me.StringField()
    issuing_organization = me.StringField()
    is_active = me.BooleanField(default=True)
    subsections = me.ListField(me.EmbeddedDocumentField(Subsection))

# Optionally, connect signals for pre_delete actions
# me.signals.pre_delete.connect(Exam.pre_delete, sender=Exam)


class LeaderboardEntry(me.Document):
    user = me.ReferenceField('User', required=True)  # Link to the User document
    total_scores = me.FloatField(default=0.0)  # Cumulative scores from all exams
    exams_attempted = me.IntField(default=0)  # Number of exams the user has taken
    exams_passed = me.IntField(default=0)  # Number of exams the user has passed
    average_score = me.FloatField(default=0.0)  # Average score from all exams
    last_updated = me.DateTimeField(auto_now=True)  # Timestamp of the last update to this leaderboard entry
    rank = me.IntField()  # The user's current rank; this will need to be updated whenever leaderboard changes

    meta = {
        'indexes': [
            '-total_scores',  # descending index on total_scores for faster leaderboard retrieval
            '-exams_passed',
            '-average_score'
        ]
    }
