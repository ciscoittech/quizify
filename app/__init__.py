from flask import Flask, session
from flask_login import LoginManager
import mongoengine as me 
import certifi
from app.auth.routes import auth
from app.admin.routes import admin  # Adjust this line
from app.quiz.routes import quiz
from config import Config
import os

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(admin)  # Adjusted to the correct blueprint
app.register_blueprint(quiz)
app.config.from_object(Config)

# Connect to the MongoDB database using mongoengine


DB_URI = os.environ.get('DB_URI')
me.connect(host=DB_URI, tlsCAFile=certifi.where())
# connect('demoquiz', host='localhost', port=27017)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  #


@login_manager.user_loader
def load_user(user_id):
    from app.admin.models import User  # Import the User model here to avoid circular imports
    try:
        return User.objects.get(id=user_id)
    except me.DoesNotExist:
        return None
