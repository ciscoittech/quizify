from datetime import datetime
from flask import abort, flash, render_template, request, redirect, url_for, session
from app.quiz.models import Exam, Question
from app.quiz.forms import CertificationForm, ExamForm, QuestionForm
from app.admin.models import User
from bson import ObjectId
import random
from app.quiz import bp



@bp.route('/examlist')
def examlist():
    exams = Exam.objects.all()  # Fetch all exams from the database
    return render_template('home/ecommerce-products-list.html', exams=exams)


from app.quiz.models import Exam  # Import the Exam model

# ...

@bp.route('/exams/add', methods=['GET', 'POST'])
# @login_required
# @admin_required  # This is a new decorator you might have to define to ensure only admins can access
def add_exam():
    form = ExamForm()  # Use an appropriate form for creating exams
    if form.validate_on_submit():
        exam = Exam(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            questions=[],  # You can customize this part based on how you handle questions
            is_active=form.is_active.data,
            description_short=form.description_short.data,
            description_long=form.description_long.data,
            possible_jobs=form.possible_jobs.data,
            issueing_organization=form.issueing_organization.data
        )
        exam.save()
        flash('Exam added successfully!', 'success')
        return redirect(url_for('exams'))  # Update the redirect URL to match your route
    return render_template('home/add_exam.html', title='Add Exam', form=form)  # Update the template name and title

@bp.route('/exams', methods=['GET'])
def exams():
    exams = Exam.objects.all()
    return render_template('exams.html', exams=exams)  # Update the template name

@bp.route('/exams/<exam_id>', methods=['GET'])
def exam_detail(exam_id):
    exam = Exam.objects.get(id=exam_id)
    return render_template('exam_detail.html', exam=exam)  # Update the template name

@bp.route('/exams/<exam_id>/edit', methods=['GET', 'POST'])
# @login_required
# @admin_required
def edit_exam(exam_id):
    exam = Exam.objects.get(id=exam_id)
    form = ExamForm(obj=exam)  # Use an appropriate form for editing exams
    if form.validate_on_submit():
        exam.name = form.name.data
        exam.price = form.price.data
        exam.description = form.description.data
        exam.is_active = form.is_active.data
        exam.description_short = form.description_short.data
        exam.description_long = form.description_long.data
        exam.possible_jobs = form.possible_jobs.data
        exam.issueing_organization = form.issueing_organization.data
        exam.save()
        flash('Exam updated successfully!', 'success')
        return redirect(url_for('exam_detail', exam_id=exam_id))  # Update the redirect URL
    return render_template('edit_exam.html', title='Edit Exam', form=form)  # Update the template name and title

@bp.route('/exams/<exam_id>/delete', methods=['POST'])
# @login_required
# @admin_required
def delete_exam(exam_id):
    exam = Exam.objects.get(id=exam_id)
    exam.delete()
    flash('Exam deleted!', 'success')
    return redirect(url_for('exams'))  # Update the redirect URL
