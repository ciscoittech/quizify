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


from flask import request, session, flash, redirect, url_for, render_template
from .forms import QuestionForm  # Make sure to import your QuestionForm

from flask import request, session, flash, redirect, url_for, render_template
from .forms import QuestionForm  # Make sure to import your QuestionForm

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

    # Initialize or update current question index
    if 'current_question_index' not in session:
        session['current_question_index'] = 0
    current_question_index = session['current_question_index']
    current_question = questions[current_question_index]

    form = QuestionForm()
    if form.validate_on_submit():
        action = request.form.get('submit_action')

        if action == 'Submit & Next' and current_question_index < len(questions) - 1:
            session['current_question_index'] += 1
        elif action == 'Back' and current_question_index > 0:
            session['current_question_index'] -= 1
        elif action == 'End Exam':
            # Logic to handle exam submission
            # ...

        # Redirect to refresh the page and show the next/previous question
    return redirect(url_for('quiz.start_exam', exam_id=exam_id))

    # Re-fetch the current question in case index was updated
    current_question_index = session['current_question_index']
    current_question = questions[current_question_index]
    
    # Populate form choices based on current question
    # This depends on how your QuestionForm is set up
    # form.choices.choices = [(option.text, option.text) for option in current_question.options]

    return render_template('home/start_exam.html', exam=exam, question=current_question, form=form)





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
