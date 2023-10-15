from flask import render_template, redirect, request, session, url_for, flash
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app.auth.forms import RegistrationForm
from app.auth import auth
from app.admin.models import User
from app.auth.forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        session['user_id'] = str(user.id)  # Storing user_id in session
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.profile')
        return redirect(next_page)

    return render_template('accounts/login.html', title='Sign In', form=form)


@auth.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    return render_template('accounts/register.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('home/index.html')
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user_by_username = User.objects(username=form.username.data).first()
        if existing_user_by_username:
            flash('That username is already taken. Please choose a different one.', 'danger')
            return render_template('accounts/register.html', title='Register', form=form)

        # Check if email already exists
        existing_user_by_email = User.objects(email=form.email.data).first()
        if existing_user_by_email:
            flash('That email is already registered. Please log in or use a different email.', 'danger')
            return render_template('accounts/register.html', title='Register', form=form)

        # If both checks pass, create the user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        flash('Registration successful!', 'success')
        return redirect(url_for('admin.profile'))
    return render_template('accounts/register.html', title='Register', form=form)

@auth.route('/logout')
@auth.route('/start_exam/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))



