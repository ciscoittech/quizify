from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.quiz.models import Exam
from app.user import user
from app.user.forms import UpdateProfileForm, DeleteForm



# Define a route for the user profile
@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    exams = Exam.objects.all()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Add code to handle profile picture upload
        current_user.save()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('home/profile.html', title='Profile', form=form, exams=exams)

# Define a route for editing the user profile
@user.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')


@user.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    form = DeleteForm()
    if form.validate_on_submit():
        user_instance = user.objects(id=user_id).first()
        if user_instance:
            user_instance.delete()
            flash('User successfully deleted!', 'success')
        else:
            flash('User not found!', 'danger')
    return redirect(url_for('main.dashboard'))