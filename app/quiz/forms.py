from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    choices = RadioField('Choose an answer', choices=[], validators=[DataRequired()])
    submit_next = SubmitField('Submit & Next')
    submit_end = SubmitField('End Exam')
    submit_back = SubmitField('Back')  # Add this line for the Back button
    flag_question = SubmitField('Flag Question')  # And this line for the Flag button
