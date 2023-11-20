from datetime import datetime
from flask import abort, flash, render_template, request, redirect, url_for, session
from flask_login import current_user
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
