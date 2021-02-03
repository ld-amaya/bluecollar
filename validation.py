import re
import requests
from models import db, User, Register, User_Type, Type
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

API_URL = 'http://apilayer.net/api/check'
ACCESS_KEY = '9803bd89e3c361b6684085127106fbaf'
valid_data = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"


class Validate():

    def __init__(self, form):
        """Instantiate user class"""

        self.first_name = form.first_name.data
        self.last_name = form.last_name.data
        self.email = form.email.data
        self.password = form.password.data
        self.city = form.city.data

    def valid_password(self):
        """Handles password validation if it meets criteria"""

        # Compile Regex
        valid = re.compile(valid_data)
        # Search password for invalid input
        is_valid = re.search(valid, self.password)
        if is_valid:
            return True
        return False

    def valid_email(self):
        """Handles email verification using MailBoxLayer API"""
        api_data = requests.get(
            f"{API_URL}?access_key={ACCESS_KEY}&email={self.email}")
        data = api_data.json()
        if data['mx_found']:
            return True
        return False

    def register_user(self):
        """Handles user registration"""

        hashed = bcrypt.generate_password_hash(self.password)
        # turn byte string to normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = User(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=hashed_utf8,
            city_id=self.city)
        db.session.add(user)
        db.session.commit()

        return user

    def Add_User_Type(self, user_id):

        user_type = User_Type(
            user_id=user_id,
            type_id=1
        )
        db.session.add(user_type)
        db.session.commit()
