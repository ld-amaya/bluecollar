from models import db
from flask import g


class UserProfile():

    def __init__(self, form, city):
        """Instantiate profile class"""

        self.first_name = form.first_name.data
        self.last_name = form.last_name.data
        self.email = form.email.data
        self.city_id = city

    def update(self, facebook="", mobile="", title="", description=""):
        """Update user profile"""

        g.user.first_name = self.first_name
        g.user.last_name = self.last_name
        g.user.email = self.email
        g.user.facebook = facebook
        g.user.mobile = mobile
        g.user.city_id = self.city_id
        g.user.title = title
        g.user.description = description
        db.session.add(g.user)
        db.session.commit()
