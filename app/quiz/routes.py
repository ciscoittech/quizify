from datetime import datetime
from flask import abort, flash, render_template, request, redirect, url_for, session
from flask_login import current_user
from app.quiz.handlers import get_exam_with_questions
from app.quiz.models import Exam, Question
from app.quiz.forms import CertificationForm, ExamForm, QuestionForm
from app.admin.models import User
from bson import ObjectId
import random
from app.quiz import bp


@bp.route('/exam')
def examlist():
    exams = Exam.objects.all()
    print(exams)  # Fetch all exams from the database
    return render_template('home/ecommerce-products-list.html', exams=exams)


@bp.route('/enroll_exam/<exam_id>')
def enroll_exam(exam_id):
    exam = Exam.objects(id=exam_id).first()
    if not exam:
        flash('Exam not found!', 'danger')
        return redirect(url_for('quiz.examlist'))

    if exam not in current_user.enrolled_exams:
        current_user.enrolled_exams.append(exam)
        current_user.save()
        flash('Enrolled in exam successfully!', 'success')
    else:
        flash('You are already enrolled in this exam.', 'info')

    return redirect(url_for('quiz.examlist'))


@bp.route('/disenroll_exam/<exam_id>')
def disenroll_exam(exam_id):
    exam = Exam.objects(id=exam_id).first()
    if not exam:
        flash('Exam not found!', 'danger')
        return redirect(url_for('quiz.examlist'))

    if exam in current_user.enrolled_exams:
        current_user.enrolled_exams.remove(exam)
        current_user.save()
        flash('Disenrolled from the exam successfully!', 'success')
    else:
        flash('You are not enrolled in this exam.', 'info')

    return redirect(url_for('quiz.examlist'))


@bp.route('/launch_exam/<exam_id>')
def launch_exam(exam_id):
    # Logic to handle exam launch
    # This could involve redirecting to an exam page, loading exam questions, etc.
    return render_template('quiz/exam_page.html', exam_id=exam_id)


@bp.route('/start_exam/<exam_id>', methods=['GET', 'POST'])
def start_exam(exam_id):
    # Retrieve exam data (this function should be defined elsewhere in your code)
    exam_data = get_exam_with_questions(exam_id)

    # If exam data is not found, redirect to the exam list with an error message
    if not exam_data:
        flash("Exam not found!", "danger")
        return redirect(url_for('quiz.examlist'))

    # Initialize or retrieve the current question index from the session
    if 'current_question_index' not in session:
        session['current_question_index'] = 0

    # Create an instance of your question form
    form = QuestionForm()

    # Process the form submission
    if form.validate_on_submit():
        current_question_index = session.get('current_question_index', 0)
        navigation_direction = request.form.get('navigation_direction')

        # Increment or decrement the question index based on the navigation direction
        if navigation_direction == 'next' and current_question_index < len(exam_data['questions']) - 1:
            session['current_question_index'] += 1
        elif navigation_direction == 'back' and current_question_index > 0:
            session['current_question_index'] -= 1

        session.modified = True  # Mark the session as modified
        return redirect(url_for('quiz.start_exam', exam_id=exam_id))

    # Get the current question
    current_question_index = session.get('current_question_index', 0)
    current_question = exam_data['questions'][current_question_index] if exam_data['questions'] else None

    # Populate form choices (if the current question exists)
    if current_question:
        form.choices.choices = [(option['text'], option['text']) for option in current_question['options']]

    return render_template('home/start_exam.html', exam=exam_data, question=current_question, form=form, current_question_index=current_question_index)





# @bp.route('/start_exam/<exam_id>', methods=['GET', 'POST'])
# def start_exam(exam_id):
#     exam_data = get_exam_with_questions(exam_id)
#     if not exam_data:
#         flash("Exam not found!", "danger")
#         return redirect(url_for('quiz.examlist'))
#
#     exam = exam_data
#     questions = []
#     for subsection in exam.get('subsections', []):
#         questions.extend(subsection.get('questions', []))
#
#     print("Total Questions:", len(questions))  # Debug: Check total number of questions
#
#     if 'current_question_index' not in session:
#         session['current_question_index'] = 0
#
#     current_question_index = session['current_question_index']
#     print("Current question index at start:", current_question_index)  # Debug: Check initial index
#
#     current_question = questions[current_question_index]
#
#     form = QuestionForm()
#     if form.validate_on_submit():
#         print("Form submitted.")  # Debug: Check if form is submitted
#
#         # Handle user response
#         user_answers = session.get('user_answers', {})
#         user_answers[current_question_index] = form.choices.data
#         session['user_answers'] = user_answers
#         session.modified = True  # Ensure session is marked as modified
#
#         # Navigation logic
#         if form.submit_next.data and current_question_index < len(questions) - 1:
#             session['current_question_index'] += 1
#             print("Next button pressed. Index updated to:", session['current_question_index'])  # Debug
#         elif form.submit_back.data and current_question_index > 0:
#             session['current_question_index'] -= 1
#             print("Back button pressed. Index updated to:", session['current_question_index'])  # Debug
#         elif form.flag_question.data:
#             flagged_questions = session.get('flagged_questions', set())
#             flagged_questions.add(current_question_index)
#             session['flagged_questions'] = flagged_questions
#             session.modified = True
#             print("Question flagged. Flagged questions:", session['flagged_questions'])  # Debug
#         elif form.submit_end.data:
#             print("End exam button pressed.")  # Debug
#             session.pop('current_question_index', None)
#             session.pop('user_answers', None)
#             session.pop('flagged_questions', None)
#             session.modified = True
#             return redirect(url_for('quiz.exam_results', exam_id=exam_id))
#
#         return redirect(url_for('quiz.start_exam', exam_id=exam_id))
#
#     current_question_index = session['current_question_index']
#     current_question = questions[current_question_index]
#     form.choices.choices = [(option['text'], option['text']) for option in current_question['options']]
#
#     return render_template('home/start_exam.html', exam=exam, question=current_question, form=form,
#                            current_question_index=current_question_index, questions=questions)


@bp.route('/submit_exam/<exam_id>', methods=['POST'])
def submit_exam(exam_id):
    # Retrieve submitted answers from the form
    # This is a dummy example; you'll need to adjust it based on your form structure
    answers = request.form

    # Process the answers
    # Here, you would typically check the answers against the correct ones
    # and calculate the user's score, record the results, etc.

    # Redirect to a results page or another appropriate page
    # For now, redirecting back to the exam list
    flash('Exam submitted successfully!', 'success')
    return redirect(url_for('quiz.examlist'))


@bp.route('/submit_answer/<exam_id>/<int:question_index>', methods=['POST'])
def submit_answer(exam_id, question_index):
    pass
