from datetime import datetime
from flask import abort, flash, render_template, request, redirect, url_for, session
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

