from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


class User_Comment(db.Model):
    """Creates relationship between user and comment"""

    __tablename__ = "usercomments"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    comment_id = db.Column(db.Integer,
                           db.ForeignKey("comments.id"),
                           nullable=False)
    user_from = db.Column(db.Integer,
                          db.ForeignKey("users.id"),
                          nullable=False)
    user_to = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)


class Rating(db.Model):
    """Create a rating model"""

    __tablename__ = "ratings"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    rating = db.Column(db.Integer,
                       nullable=False)
    user_from = db.Column(db.Integer,
                          db.ForeignKey("users.id"),
                          nullable=False)
    user_to = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)


class Message (db.Model):
    """Create the message model"""

    __tablename__ = "messages"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    message = db.Column(db.Text,
                        nullable=False)


class User_Message(db.Model):
    """Create user messages relationship"""

    __tablename__ = "usermessages"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey("messages.id"),
                           nullable=False)
    message_from = db.Column(db.Integer,
                             db.ForeignKey("users.id"),
                             nullable=False)
    message_to = db.Column(db.Integer,
                           db.ForeignKey("users.id"),
                           nullable=False)


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
    address_id = db.Column(db.Integer,
                           db.ForeignKey("addresses.id"))

    city = db.relationship("City",
                           backref="users",
                           cascade="all")

    comment = db.relationship("User",
                              secondary="usercomments",
                              primaryjoin=(User_Comment.user_from == id),
                              secondaryjoin=(User_Comment.user_to == id))

    rating = db.relationship("User",
                             secondary="ratings",
                             primaryjoin=(Rating.user_from == id),
                             secondaryjoin=(Rating.user_to == id))

    message = db.relationship("User",
                              secondary="usermessages",
                              primaryjoin=(User_Message.message_from == id),
                              secondaryjoin=(User_Message.message_to == id))


class City(db.Model):
    """Create city  model"""

    __tablename__ = "cities"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))

    barangay = db.relationship("Barangay",
                               secondary="addresses",
                               backref="city",
                               cascade="all")


class Barangay(db.Model):
    """Create barangay model"""

    __tablename__ = "barangays"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False)


class Address(db.Model):
    """Create city and barangay relationship table"""

    __tablename__ = "addresses"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    city_id = db.Column(db.Integer,
                        db.ForeignKey("cities.id"))
    barangay_id = db.Column(db.Integer,
                            db.ForeignKey("barangays.id"))

    user = db.relationship("User",
                           backref="address",
                           cascade="all")


def connect_db(app):
    """Connect database to flask app"""

    db.app = app
    db.init_app(app)
