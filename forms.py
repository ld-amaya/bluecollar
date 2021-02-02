from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length
from models import db, User, Register


class RegistrationForm(FlaskForm):
    """Defines form to be used in registration"""

    first_name = StringField('First Name',
                             validators=[InputRequired(),
                                         Length(min=1, max=50)])
    last_name = StringField('Last Name',
                            validators=[InputRequired(),
                                        Length(min=1, max=50)])
    email = StringField('Email',
                        validators=[InputRequired(),
                                    Email(),
                                    Length(min=1, max=50)])
    password = PasswordField('Password',
                             validators=[InputRequired(),
                                         Length(min=8, max=100)])
    city = SelectField(u'Select City (Cebu Province Only)',
                       choices=[],
                       coerce=int)

    def __init__(self, cities=None):
        super().__init__()
        if cities:
            self.city.choices = [(c.id, c.name) for c in cities]
