from flask import Flask, session
from flask_login import LoginManager
import mongoengine as me
from app.auth.routes import auth
from app.user.routes import user  # Adjust this line
from app.quiz.routes import quiz
from config import Config

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(user)  # Adjusted to the correct blueprint
app.register_blueprint(quiz)
app.config.from_object(Config)

# Connect to the MongoDB database using mongoengine
me.connect('demoquiz', host='localhost', port=27017)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'  #

@login_manager.user_loader
def load_user(user_id):
    from app.user.models import User  # Import the User model here to avoid circular imports
    try:
        return User.objects.get(id=user_id)
    except me.DoesNotExist:
        return None