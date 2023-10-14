from datetime import datetime
import random
from app.quiz.models import Subsection
from app.user.models import User, Result, UserExam
from bson import ObjectId
from flask import session


def reset_exam_session():
    """Resets or removes session variables related to the exam."""
    session.pop('selected_questions', None)
    session.pop('current_question_number', None)


def end_exam(user_exam):
    """Handles the end of the exam logic."""
    correct_answers = Result.objects(user_exam=user_exam, is_correct=True).count()
    total_questions = len(session['selected_questions'])
    score = (correct_answers / total_questions) * 100
    user_exam.score = score
    user_exam.finished_at = datetime.utcnow()
    user_exam.save()


def get_or_create_user_exam(user, exam):
    user_exam = UserExam.objects(user=user, exam=exam).first()
    if not user_exam:
        user_exam = UserExam(user=user, exam=exam)
        user_exam.save()
    return user_exam


def get_selected_questions(exam):
    if 'selected_questions' not in session:
        all_questions = [question.id for subsection in Subsection.objects(exam=exam) for question in
                         subsection.questions]
        session['selected_questions'] = random.sample([str(q_id) for q_id in all_questions], 3)
    return session['selected_questions']


def create_result(user_exam, current_question, selected_answer, is_correct):
    submitted_at = datetime.utcnow()
    result = Result(
        user_exam=user_exam,
        question=current_question,
        selected_answer=selected_answer,
        time_taken='unknown',  # Convert time_taken to string to match the field type
        is_correct=is_correct,
        submitted_at=submitted_at
    )
    result.save()
    return result
