from models import db, User
from wtforms.validators import InputRequired, Email, Length, Optional
from wtforms import StringField, PasswordField, SelectField, IntegerField, FileField, BooleanField, TextAreaField, MultipleFileField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


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


class MessageForm(FlaskForm):
    """Defines Message Form"""
    message = TextAreaField("Your Message", validators=[InputRequired()])


class PasswordForm(FlaskForm):
    """Defines the Password Form"""
    password = PasswordField('Existing Password', validators=[
        InputRequired(), Length(min=8, max=100)])
    new_password = PasswordField('New Password', validators=[
        InputRequired(), Length(min=8, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), Length(min=8, max=100)])


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

    profile = FileField('Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'], "Images Only!")])
    first_name = StringField('First Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[
        InputRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=8, max=100)])
    facebook = StringField('Facebook Link')
    mobile = IntegerField('Mobile Number', validators=[Optional()])
    city = SelectField(u'Select City (Cebu Province Only)',
                       choices=[],
                       coerce=int)

    title = StringField('Portfolio Title')
    description = TextAreaField('Description')
    carpenter = BooleanField('Carpenter')
    painter = BooleanField('Painter')
    electrician = BooleanField('Electrician')
    plumber = BooleanField('Plumber')

    def __init__(self, cities=None):
        super().__init__()
        if cities:
            self.city.choices = [(c.id, c.name) for c in cities]


class UserProfileForm(FlaskForm):
    """Defines the profile form"""

    first_name = StringField('First Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[
        InputRequired(), Email(), Length(min=1, max=50)])


class WorkerProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[
        InputRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[
        InputRequired(), Email(), Length(min=1, max=50)])
    facebook = StringField('Facebook Link')
    mobile = IntegerField('Mobile Number', validators=[Optional()])
    title = StringField('Portfolio Title')
    description = TextAreaField('Description')


class JobForm(FlaskForm):
    """Defines the job type forms"""

    carpenter = BooleanField('Carpenter')
    painter = BooleanField('Painter')
    electrician = BooleanField('Electrician')
    plumber = BooleanField('Plumber')


class CityForm(FlaskForm):
    """Defines the city forms"""
    city = SelectField(u'Select City (Cebu Province Only)',
                       choices=[],
                       coerce=int)

    def __init__(self, cities=None):
        super().__init__()
        if cities:
            self.city.choices = [(c.id, c.name) for c in cities]


class ImageForm(FlaskForm):
    """Defines the profile image form"""
    profile_pix = FileField('Upload Picture',
                            validators=[InputRequired(),
                                        FileAllowed(['jpg', 'png'], "Images Only!")])


class AlbumForm(FlaskForm):
    """Defines the profile image form"""
    album_pix = MultipleFileField('Upload Picture',
                                  validators=[InputRequired(),
                                              FileAllowed(['jpg', 'png'], "Images Only!")])
