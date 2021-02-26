import requests
from models import db, User, User_Type, Type, User_Service
from decouple import config
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
ACCESS_KEY = config('KEY')
API_URL = config('API_URL')


class Registration():

    def __init__(self, form,  ut, filename):
        """Instantiate user class"""

        self.first_name = form.first_name.data
        self.last_name = form.last_name.data
        self.email = form.email.data
        self.password = form.password.data
        self.city_id = form.city.data
        self.user_type = ut
        self.profile = filename

    def valid_email(self):
        """Handles email verification using MailBoxLayer API"""
        api_data = requests.get(
            f"{API_URL}?access_key={ACCESS_KEY}&email={self.email}")
        data = api_data.json()
        if data['mx_found']:
            return True
        return False

    def register_user(self, facebook="", mobile="", title="", description=""):
        """Handles user registration"""

        hashed = bcrypt.generate_password_hash(self.password)
        # turn byte string to normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = User(
            profile=self.profile,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=hashed_utf8,
            facebook=facebook,
            mobile=mobile,
            city_id=self.city_id,
            title=title,
            description=description
        )
        db.session.add(user)
        db.session.commit()

        return user

    def Add_User_Type(self, user_id):
        """Add user type"""
        user_type = User_Type(
            user_id=user_id,
            type_id=self.user_type
        )
        db.session.add(user_type)
        db.session.commit()
