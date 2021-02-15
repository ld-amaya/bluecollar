import re
import requests
from models import db, User, User_Type, Type, User_Service
from decouple import config
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
ACCESS_KEY = config('KEY')
API_URL = 'http://apilayer.net/api/check'
valid_data = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"


class Validate():

    def __init__(self, form,  user_type, filename):
        """Instantiate user class"""

        self.first_name = form.first_name.data
        self.last_name = form.last_name.data
        self.email = form.email.data
        self.password = form.password.data
        self.city_id = form.city.data
        self.user_type = user_type
        self.profile = filename

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
        print(data)
        if data['mx_found']:
            return True
        return False

    def register_user(self, facebook, mobile):
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
        )
        db.session.add(user)
        db.session.commit()

        # Add Service Type
        if self.user_type == 'worker':
            user_type = User_Type(
                user_id=user.id,
                type_id=2
            )
            db.session.add(user_type)
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

    def Add_Services(self, user_id, carpenter, painter, plumber, electrician):
        """Add services to user"""
        if carpenter:
            carpenter = User_Service(
                user_id=user_id,
                service_id=1
            )
            db.session.add(carpenter)

        if painter:
            painter = User_Service(
                user_id=user_id,
                service_id=2
            )
            db.session.add(painter)

        if plumber:
            plumber = User_Service(
                user_id=user_id,
                service_id=3
            )
            db.session.add(plumber)

        if electrician:
            electrician = User_Service(
                user_id=user_id,
                service_id=4
            )
            db.session.add(electrician)

        db.session.commit()
