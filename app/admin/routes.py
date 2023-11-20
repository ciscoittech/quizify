from datetime import datetime
from datetime import timedelta
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.quiz.models import Exam
from app.admin import bp
from app.admin.forms import UpdateProfileForm, DeleteForm
from app.admin.models import User, UserResponse




@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Initialize the form
    # form = UpdateProfileForm()

    # # Fetch all exams for display
    # exams = Exam.objects.all()

    # # Fetch user's exam results for displaying progress and scores
    # user_exam_results = UserResponse.objects(user=current_user)

    # If there's a POST request to update the profile
    # if form.validate_on_submit():
    #     current_user.username = form.username.data
    #     current_user.email = form.email.data
    #     # Add code to handle profile picture upload if desired
    #     current_user.save()
    #     flash('Your profile has been updated!', 'success')
    #     return redirect(url_for('user.profile'))
    
    # For a GET request, populate the form with the current user's info
    # elif request.method == 'GET':
    #     form.username.data = current_user.username
    #     form.email.data = current_user.email

    return render_template(
        'home/profile.html', 
        title='Profile',
        # exams=exams,
        # user_exam_results=user_exam_results,
        # form=form  # Uncomment this when you decide to use the form
    )


# Define a route for editing the user profile
@bp.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')


@bp.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    form = DeleteForm()
    if form.validate_on_submit():
        user_instance = User.objects(id=user_id).first()
        if user_instance:
            user_instance.delete()
            flash('User successfully deleted!', 'success')
        else:
            flash('User not found!', 'danger')
    return redirect(url_for('admin.reports'))


@bp.route('/dashboard')
def reports():
    delete_form = DeleteForm()
    # Define the start of today
    start_of_today = datetime.combine(datetime.today().date(), datetime.min.time())

    # Define the start of tomorrow
    start_of_tomorrow = start_of_today + timedelta(days=1)

    # Get all users
    all_users = User.objects.all()

    # Get total number of users
    total_users = all_users.count()

    # Get users who signed up today
    today = 20
    users_today = 20

    return render_template('dashboard/dashboard.html', all_users=all_users, total_users=total_users,
                           users_today=users_today, delete_form=delete_form)



