from datetime import datetime
from flask import abort, render_template, request, redirect, url_for, session
from app.quiz.models import Exam, Subsection, Question
from app.quiz.forms import QuestionForm
from app.user.models import User, Result, UserExam
from bson import ObjectId
import random
from app.quiz import quiz
from app.quiz.handlers import reset_exam_session, end_exam, get_or_create_user_exam, get_selected_questions, create_result





@quiz.route('/exam')
def exam():
    # Fetching all vendors and exams for display
    # vendors = Vendor.objects.all()
    exams = Exam.objects.all()
    return render_template('home/exam1.html', exams=exams)




@quiz.route('/start_exam/<exam_id>', methods=['GET', 'POST'])
def start_exam(exam_id):
    try:
        user = User.objects.get(id=session['user_id'])
        exam = Exam.objects.get(id=exam_id)
    except Exception as e:
        abort(500, description=str(e))  # This will trigger your error handler

    existing_attempt = UserExam.objects(user=session['user_id'], exam=exam_id).order_by('-timestamp').first()
    new_attempt_id = existing_attempt.attempt_id + 1 if existing_attempt else 1
    user_exam = UserExam(user=user, exam=exam, attempt_id=new_attempt_id)
    user_exam.save()

    
    if user_exam.has_ended:
        reset_exam_session()

    selected_questions = get_selected_questions(exam)

    if 'current_question_number' not in session:
        session['current_question_number'] = 1

    if session['current_question_number'] > len(selected_questions):
        reset_exam_session()
        return redirect(url_for('quiz.exam_results', exam_id=exam_id))

    current_question_id = ObjectId(selected_questions[session['current_question_number'] - 1])
    current_question = Question.objects.get(id=current_question_id)

    form = QuestionForm()
    form.choices.choices = [(key, value) for key, value in current_question.choices.items()]

    if form.validate_on_submit():
        if form.submit_back.data:
            # If back button is pressed, decrease the question number unless it's the first question
            if session['current_question_number'] > 1:
                session['current_question_number'] -= 1
            return redirect(url_for('quiz.start_exam', exam_id=exam_id))

        selected_answer = form.choices.data
        is_correct = selected_answer == current_question.correct_answer
        create_result(user_exam, current_question, selected_answer, is_correct)

        if form.submit_next.data:
            session['current_question_number'] += 1
            # Record the time the next question is presented
            session['question_start_time'] = datetime.utcnow()
            return redirect(url_for('quiz.start_exam', exam_id=exam_id))
        elif form.submit_end.data:
            end_exam(user_exam)
            reset_exam_session()
            return redirect(url_for('quiz.exam_results', exam_id=exam_id))

    return render_template('home/start_exam.html', exam=exam, current_question=current_question, form=form)





@quiz.route('/exam_results/<exam_id>')
def exam_results(exam_id):
    # Fetch all UserExams for the current user and specific exam_id
    user_exams = UserExam.objects(user=session['user_id'], exam=exam_id).order_by('-timestamp')

    # A list to hold all attempts and their statistics
    all_attempts = []

    for user_exam in user_exams:
        results = Result.objects(user_exam=user_exam)
        total_questions = len(results)
        correct_answers = sum(1 for result in results if result.is_correct)
        incorrect_answers = total_questions - correct_answers
        certificate = user_exam.certification
        # percentage = (correct_answers / total_questions) * 100

        attempt = {
            "timestamp": user_exam.timestamp,
            "correct": correct_answers,
            "incorrect": incorrect_answers,
            # "percentage": percentage,
            "certificate": certificate
        }
        all_attempts.append(attempt)

    return render_template('home/exam_results.html', attempts=all_attempts)
