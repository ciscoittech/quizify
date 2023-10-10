# app/error/handlers.py

from flask import render_template
from app.error import error

@error.app_errorhandler(Exception)
def handle_generic_error(error):
    return render_template('error/generic_error.html', error=error), 500
