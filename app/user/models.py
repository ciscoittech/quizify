from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import mongoengine as me
from datetime import datetime
from app.quiz import models as quiz_models


class User(UserMixin, me.Document):
    email = me.StringField(required=True, unique=True)
    username = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    first_name = me.StringField()
    last_name = me.StringField()
    # Add a reference to exams taken by the user
    exams_taken = me.ListField(me.ReferenceField('ExamResult'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserExam(me.Document):
    user = me.ReferenceField(User, required=True, reverse_delete_rule=me.CASCADE)
    exam = me.ReferenceField(quiz_models.Exam, required=True)
    timestamp = me.DateTimeField(default=datetime.utcnow)  # to track when the user started the exam
    attempt_id = me.SequenceField()
    certification = me.ReferenceField(quiz_models.Exam)

    def has_ended(self):
        # Count the number of results associated with this UserExam instance
        results_count = Result.objects(user_exam=self).count()

        # Count the number of questions in the exam
        questions_count = len(quiz_models.Question.objects(exam=self.exam))

        # Return True if results count is equal to or greater than the questions count, else return False
        return results_count >= questions_count

    def formatted_timestamp(self):
        return self.timestamp.strftime('%B %d, %Y %H:%M')


class Result(me.Document):
    user_exam = me.ReferenceField(UserExam, required=True, reverse_delete_rule=me.CASCADE)
    question = me.ReferenceField(quiz_models.Question, required=True)
    selected_answer = me.StringField(required=True)
    time_taken = me.StringField(required=True)  # Placeholder, adjust based on your needs
    is_correct = me.BooleanField(required=True)
    timestamp = me.DateTimeField(default=datetime.utcnow)  # to track when the user answered the question
    submitted_at = me.DateTimeField()  # to track when the user submitted the answer
