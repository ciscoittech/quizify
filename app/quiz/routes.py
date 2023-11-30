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
    exam_data = get_exam_with_questions(exam_id)
    if not exam_data:
        flash("Exam not found!", "danger")
        return redirect(url_for('quiz.examlist'))

    exam = exam_data
    questions = []
    for subsection in exam.get('subsections', []):
        questions.extend(subsection.get('questions', []))

    if 'current_question_index' not in session:
        session['current_question_index'] = 0

    current_question_index = session['current_question_index']
    current_question = questions[current_question_index]

    form = QuestionForm()
    if form.validate_on_submit():
        # Logic to handle user response - assuming we're storing answers in session
        user_answers = session.get('user_answers', {})
        user_answers[current_question_index] = form.choices.data
        session['user_answers'] = user_answers

        # Navigation logic
        if form.submit_next.data and current_question_index < len(questions) - 1:
            session['current_question_index'] += 1
        elif form.submit_back.data and current_question_index > 0:
            session['current_question_index'] -= 1
        elif form.flag_question.data:
            # Add flagging logic if necessary
            # Example: Mark the current question as flagged
            flagged_questions = session.get('flagged_questions', set())
            flagged_questions.add(current_question_index)
            session['flagged_questions'] = flagged_questions
        elif form.submit_end.data:
            # Process exam submission
            # Example: Clear the session and redirect to a results page
            session.pop('current_question_index', None)
            session.pop('user_answers', None)
            session.pop('flagged_questions', None)
            return redirect(url_for('quiz.exam_results', exam_id=exam_id))

        return redirect(url_for('quiz.start_exam', exam_id=exam_id))

    current_question_index = session['current_question_index']
    current_question = questions[current_question_index]
    form.choices.choices = [(option['text'], option['text']) for option in current_question['options']]

    return render_template('home/start_exam.html', exam=exam, question=current_question, form=form, current_question_index=current_question_index, questions=questions)








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