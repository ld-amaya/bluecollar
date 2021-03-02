from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
profile_pix = "default-icon.png"


class Service(db.Model):
    """Create service types"""

    __tablename__ = "services"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(50),
                     nullable=False)

    user = db.relationship('User',
                           secondary='userservices',
                           backref='service')


class User_Service(db.Model):
    """Create user service relationship"""

    __tablename__ = "userservices"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='cascade'))
    service_id = db.Column(db.Integer,
                           db.ForeignKey('services.id', ondelete='cascade'))


class Type(db.Model):
    """Create User Type Table"""

    __tablename__ = "types"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(20),
                     nullable=False)

    user = db.relationship("User",
                           secondary="user_types",
                           backref="type")


class User_Type(db.Model):
    """Create user type relationship"""

    __tablename__ = "user_types"

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete='cascade'),
                        primary_key=True)
    type_id = db.Column(db.Integer,
                        db.ForeignKey("types.id", ondelete='cascade'),
                        primary_key=True)


class Job(db.Model):
    """Create job model"""

    __tablename__ = "jobs"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    job = db.Column(db.String(50),
                    nullable=False)
    description = db.Column(db.Text,
                            nullable=True)
    user = db.relationship("User",
                           secondary="userjobs",
                           backref="job")


class User_Job(db.Model):
    """Create user job relationship"""

    __tablename__ = "userjobs"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))
    job_id = db.Column(db.Integer,
                       db.ForeignKey("jobs.id"))


class Comment(db.Model):
    """Create a comment model"""

    __tablename__ = "comments"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text)
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer, default=0)
    user_from_id = db.Column(db.Integer,
                             db.ForeignKey("users.id", ondelete="cascade"),
                             nullable=False)
    user_to_id = db.Column(db.Integer,
                           db.ForeignKey("users.id", ondelete="cascade"),
                           nullable=False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    user = db.relationship("User",
                           foreign_keys=[user_from_id],
                           backref="comments")


class Message (db.Model):
    """Create the message model"""

    __tablename__ = "messages"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    message = db.Column(db.Text,
                        nullable=False)
    message_from = db.Column(db.Integer,
                             db.ForeignKey("users.id", ondelete="cascade"),
                             nullable=False)
    message_to = db.Column(db.Integer,
                           db.ForeignKey("users.id", ondelete="cascade"),
                           nullable=False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    is_read = db.Column(
        db.Boolean,
        default=False
    )
    user_from = db.relationship(
        "User", foreign_keys=[message_from], backref="messages")
    user_to = db.relationship("User", foreign_keys=[message_to])

    def serialized_messages(self, uid):
        """Return serialized messages"""
        if uid == self.message_from:
            uid = self.message_to
            sender = self.user_to.first_name
        else:
            uid = self.message_from
            sender = self.user_from.first_name
        return {
            'id': self.id,
            'uid': uid,
            'message': self.message,
            'sender': sender,
            'from': self.user_from.first_name,
            'to': self.user_to.first_name,
            'timestamp': self.timestamp
        }

    def serialized_sender(self):
        """Return serialized senders"""
        sender = self.user_from.first_name + " " + self.user_from.last_name
        return{
            'id': self.id,
            'sender_id': self.message_from,
            'sender': sender,
            'profile': self.user_from.profile
        }


class User(db.Model):
    """Create user model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.Text,
                         nullable=False)
    facebook = db.Column(db.Text)
    mobile = db.Column(db.String(50))
    apartment_number = db.Column(db.String(15))
    building = db.Column(db.String(50))
    street = db.Column(db.String(50))
    city_id = db.Column(db.Integer,
                        db.ForeignKey('cities.id', ondelete='cascade'))
    profile = db.Column(db.Text, default=profile_pix)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    rating = db.Column(db.Integer, default=0)
    comment_from = db.relationship("User",
                                   secondary="comments",
                                   primaryjoin=(Comment.user_to_id == id),
                                   secondaryjoin=(Comment.user_from_id == id))

    comment_to = db.relationship("User",
                                 secondary="comments",
                                 primaryjoin=(Comment.user_from_id == id),
                                 secondaryjoin=(Comment.user_to_id == id))

    def serialized_email(self):
        """Return serialized email"""
        return{
            "email": self.email
        }

    @ classmethod
    def login(cls, email, password):
        """Authenticates user"""

        user = User.query.filter_by(email=email).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class City(db.Model):
    """Create city  model"""

    __tablename__ = "cities"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(100))

    user = db.relationship("User", backref="city")

    def serialized_city(self):
        """Return serialized City"""
        return {
            'id': self.id,
            'city': self.name
        }


class Album(db.Model):
    """Create the image model"""

    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(200),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete="cascade"),
                        nullable=False)

    user = db.relationship("User",
                           backref="albums")


def connect_db(app):
    """Connect database to flask app"""

    db.app = app
    db.init_app(app)
