from models import db, User
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, SelectField, IntegerField, FileField, SubmitField, BooleanField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


class LoginForm(FlaskForm):
    """Defines login form"""
    email = StringField('Email', validators=[
        InputRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=8, max=100)])


class CommentForm(FlaskForm):
    """Defines Comment Form"""
    title = StringField('Title', validators=[InputRequired()])
    comment = TextAreaField('Details', validators=[InputRequired()])


class RegistrationForm(FlaskForm):
    """Defines form to be used in registration"""

    profile = FileField('Upload Profile Picture')
    first_name = StringField('First Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[
        InputRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=8, max=100)])
    city = SelectField(u'Select City (Cebu Province Only)',
                       choices=[],
                       coerce=int)

    def __init__(self, cities=None):
        super().__init__()
        if cities:
            self.city.choices = [(c.id, c.name) for c in cities]


class WorkerForm(FlaskForm):
    """Defines the workerform for worker registration"""

    profile = FileField('Profile Picture')
    first_name = StringField('First Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[
        InputRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=8, max=100)])
    facebook = StringField('Facebook Link')
    mobile = IntegerField('Mobile Number')
    city = SelectField(u'Select City (Cebu Province Only)',
                       choices=[],
                       coerce=int)
    carpenter = BooleanField('Carpenter')
    painter = BooleanField('Painter')
    electrician = BooleanField('Electrician')
    plumber = BooleanField('Plumber')

    def __init__(self, cities=None):
        super().__init__()
        if cities:
            self.city.choices = [(c.id, c.name) for c in cities]
