import os
import re
from models import db, User
from decouple import config
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
valid_data = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*^#?&])[A-Za-z\d@$!#^%*?&]{6,20}$'


class Password():

    def __init__(self, password):
        """Instantiate Password Class"""

        self.password = password

    def valid_password(self):
        """Handles password validation if it meets criteria"""

        # Compile Regex
        valid = re.compile(valid_data)
        # Search password for invalid input
        is_valid = re.search(valid, self.password)
        if is_valid:
            return True
        return False

    def save_password(self, user, new_pass):
        hashed = bcrypt.generate_password_hash(new_pass)
        # turn byte string to normal (unicode utf8) string
        user.password = hashed.decode("utf8")
        db.session.add(user)
        db.session.commit()
