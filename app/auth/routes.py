import secrets, requests
from urllib.parse import urlencode
from flask import abort, current_app, render_template, redirect, request, session, url_for, flash
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app.auth.forms import RegistrationForm
from app.auth import bp
from app.admin.models import User
from app.auth.forms import LoginForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        session['user_id'] = str(user.id)  # Storing user_id in session

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.profile')
        return redirect(next_page)

    return render_template('accounts/loginoauth.html', title='Sign In', form=form)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    return render_template('accounts/register.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
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


@bp.route('/logout')
@bp.route('/start_exam/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))



@bp.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('admin.profile'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('auth.oauth2_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)



@bp.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('auth.oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    # find or create the user in the database
    user = User.objects(email=email).first()
    if user is None:
        user = User(email=email, username=email.split('@')[0])
        user.save()  # MongoEngine's save method

    # log the user in
    login_user(user)
    return redirect(url_for('admin.profile'))