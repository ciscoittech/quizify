from datetime import datetime
from flask import abort, render_template, request, redirect, url_for, session
from app.quiz.models import Exam, Subsection, Question
from app.quiz.forms import QuestionForm
from app.admin.models import User, Result, UserExam
from bson import ObjectId
import random
from app.quiz import quiz
from app.quiz.handlers import reset_exam_session, end_exam, get_or_create_user_exam, get_selected_questions, \
    create_result


@quiz.route('/exam')
def exam():
    # Fetching all vendors and exams for display
    # vendors = Vendor.objects.all()
    exams = Exam.objects.all()
    return render_template('home/exam1.html', exams=exams)


@quiz.route('/start_exam/<exam_id>', methods=['GET', 'POST'])
def start_exam(exam_id):
    try:
        # Get the user and exam based on their IDs from the database
        user = User.objects.get(id=session['user_id'])
        exam = Exam.objects.get(id=exam_id)
    except Exception as e:
        # If there's an exception (e.g., user or exam not found), trigger an error with a description
        abort(500, description=str(e))

    # Check if there is an existing attempt for the user on this exam
    existing_attempt = UserExam.objects(user=session['user_id'], exam=exam_id).order_by('-timestamp').first()
    new_attempt_id = existing_attempt.attempt_id + 1 if existing_attempt else 1

    # Create a new UserExam instance to track the current attempt
    user_exam = UserExam(user=user, exam=exam, attempt_id=new_attempt_id)
    user_exam.save()

    # If the exam has already ended, reset the exam session
    if user_exam.has_ended:
        reset_exam_session()

    # Get a list of selected questions for the exam
    selected_questions = get_selected_questions(exam)

    # Initialize the current question number in the session if not already set
    if 'current_question_number' not in session:
        session['current_question_number'] = 1

    # If the current question number exceeds the number of selected questions, reset the exam session and redirect to results
    if session['current_question_number'] > len(selected_questions):
        reset_exam_session()
        return redirect(url_for('quiz.exam_results', exam_id=exam_id))

    # Get the ID of the current question and fetch the question from the database
    current_question_id = ObjectId(selected_questions[session['current_question_number'] - 1])
    current_question = Question.objects.get(id=current_question_id)

    # Create a form for answering the question
    form = QuestionForm()
    form.choices.choices = [(key, value) for key, value in current_question.choices.items()]

    # Handle form submission
    if form.validate_on_submit():
        if form.submit_back.data:
            # If the back button is pressed, decrease the question number unless it's the first question
            if session['current_question_number'] > 1:
                session['current_question_number'] -= 1
            return redirect(url_for('quiz.start_exam', exam_id=exam_id))

        # Process the selected answer
        selected_answer = form.choices.data
        is_correct = selected_answer == current_question.correct_answer
        create_result(user_exam, current_question, selected_answer, is_correct)

        if form.submit_next.data:
            # If the "Next" button is pressed, move to the next question and record the start time
            session['current_question_number'] += 1
            session['question_start_time'] = datetime.utcnow()
            return redirect(url_for('quiz.start_exam', exam_id=exam_id))
        elif form.submit_end.data:
            # If the "End" button is pressed, end the exam and reset the session
            end_exam(user_exam)
            reset_exam_session()
            return redirect(url_for('quiz.exam_results', exam_id=exam_id))

    # Render the template for answering the question
    return render_template('home/start_exam.html', exam=exam, current_question=current_question, form=form)


@quiz.route('/exam_results/<exam_id>')
def exam_results(exam_id):
    # Fetch all UserExams for the current user and specific exam_id
    user_exams = UserExam.objects(user=session['user_id'], exam=exam_id).order_by('-timestamp')

    # A list to hold all attempts and their statistics
    all_attempts = []

    # Define the passing percentage
    passing_percentage = 70

    for user_exam in user_exams:
        results = Result.objects(user_exam=user_exam)
        total_questions = len(results)
        correct_answers = sum(1 for result in results if result.is_correct)
        incorrect_answers = total_questions - correct_answers
        formatted_time = user_exam.timestamp.strftime('%B %d, %Y %H:%M')

        # Check if total_questions is zero
        if total_questions != 0:
            user_percentage = (correct_answers / total_questions) * 100
        else:
            user_percentage = 0

        certification = user_exam.exam.name  # Fetching the exam name as 'certification'

        attempt = {
            "timestamp": formatted_time,
            "correct": correct_answers,
            "incorrect": incorrect_answers,
            "percentage": user_percentage,
            "certification": certification
        }
        all_attempts.append(attempt)

    return render_template('home/exam_results.html', attempts=all_attempts, passing_percentage=passing_percentage)


@quiz.route('/question_details/<question_id>')
def question_details(question_id):
    try:
        # Fetch the question based on the provided ID
        question = Question.objects.get(id=question_id)
    except Exception as e:
        # If there's an exception (e.g., question not found), trigger an error with a description
        abort(404, description=str(e))

    # Render the template and pass the question details
    return render_template('home/question_details.html', question=question)
