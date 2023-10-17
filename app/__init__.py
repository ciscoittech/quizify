from flask import Flask, session
from flask_login import LoginManager
import mongoengine as me
import certifi
from config import Config
import os

# Move this to a separate function
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Blueprints registration
    from app.auth.routes import auth
    from app.admin.routes import admin
    from app.quiz.routes import quiz
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(quiz)

    # Database connection
    DB_URI = os.environ.get('DB_URI')
    me.connect(host=DB_URI, tlsCAFile=certifi.where())

    # Flask-login configuration
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.admin.models import User
        try:
            return User.objects.get(id=user_id)
        except me.DoesNotExist:
            return None

    return app

app = create_app()