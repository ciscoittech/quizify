from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, RadioField, StringField, SubmitField, TextAreaField, ValidationError, \
    BooleanField
from wtforms.validators import DataRequired, Length, Optional


class QuestionForm(FlaskForm):
    choices = RadioField('Choose an answer', choices=[], validators=[DataRequired()])
    submit_next = SubmitField('Submit & Next')
    submit_end = SubmitField('End Exam')
    submit_back = SubmitField('Back')  # Add this line for the Back button
    flag_question = SubmitField('Flag Question')  # And this line for the Flag button


class CertificationForm(FlaskForm):
    title = StringField('Certification Title', validators=[DataRequired(), Length(min=2, max=100)])
    issuing_organization = StringField('Issuing Organization', validators=[DataRequired(), Length(min=2, max=100)])
    date_issued = DateField('Date Issued', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Add Certification')


class ExamForm(FlaskForm):
    name = StringField('Exam Name', validators=[DataRequired()])
    price = FloatField('Price', default=19.99, validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    description_short = TextAreaField('Short Description', validators=[Optional()])
    description_long = TextAreaField('Long Description', validators=[Optional()])
    possible_jobs = StringField('Possible Jobs', validators=[Optional()])
    issueing_organization = StringField('Issuing Organization', validators=[Optional()])
