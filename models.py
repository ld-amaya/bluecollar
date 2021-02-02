from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
                           backref='services')


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
                           backref="type",
                           cascade="all")


class User_Type(db.Model):
    """Create user type relationship"""

    __tablename__ = "user_types"

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True)
    type_id = db.Column(db.Integer,
                        db.ForeignKey("types.id"),
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
    users = db.relationship("User",
                            secondary="userjobs",
                            backref="jobs")


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
    comment = db.Column(db.Text,
                        nullable=False)
    user_from = db.Column(db.Integer,
                          db.ForeignKey("users.id", ondelete="cascade"),
                          nullable=False)
    user_to = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete="cascade"),
                        nullable=False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )


class Rating(db.Model):
    """Create a rating model"""

    __tablename__ = "ratings"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    rating = db.Column(db.Integer,
                       nullable=False)
    user_from = db.Column(db.Integer,
                          db.ForeignKey("users.id", ondelete="cascade"),
                          nullable=False)
    user_to = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete="cascade"),
                        nullable=False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )


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


class Register(db.Model):
    """Create registration model for easy registration"""

    __tablename__ = "registers"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    email = db.Column(db.String(100),
                      nullable=False)
    password = db.Column(db.String(100),
                         nullable=False)

    city_id = db.Column(db.Integer, db.ForeignKey(
        'cities.id', ondelete='cascade'))


class User (db.Model):
    """Create user model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    email = db.Column(db.String(100),
                      nullable=False)
    password = db.Column(db.Text,
                         nullable=False)
    facebook = db.Column(db.Text)
    mobile = db.Column(db.Integer,
                       nullable=False)
    apartment_number = db.Column(db.String(15))
    building = db.Column(db.String(50))
    street = db.Column(db.String(50))
    city_id = db.Column(db.Integer,
                        db.ForeignKey('cities.id', ondelete='cascade'))
    barangay_id = db.Column(db.Integer,
                            db.ForeignKey('barangays.id', ondelete='cascade'))

    comment = db.relationship("Comment",
                              secondary="comments",
                              primaryjoin=(Comment.user_from == id),
                              secondaryjoin=(Comment.user_to == id),
                              backref="user")

    rating = db.relationship("Rating",
                             secondary="ratings",
                             primaryjoin=(Rating.user_from == id),
                             secondaryjoin=(Rating.user_to == id),
                             backref="user")

    message = db.relationship("Message",
                              secondary="messages",
                              primaryjoin=(Message.message_from == id),
                              secondaryjoin=(Message.message_to == id),
                              backref="use")


class City(db.Model):
    """Create city  model"""

    __tablename__ = "cities"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(100))

    user = db.relationship("User", backref="city")
    client = db.relationship("Register", backref="city")


class Barangay(db.Model):
    """Create barangay model"""

    __tablename__ = "barangays"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    city = db.Column(db.String(100))
    barangay = db.Column(db.String(100))

    user = db.relationship("User", backref="barangay")


def connect_db(app):
    """Connect database to flask app"""

    db.app = app
    db.init_app(app)
