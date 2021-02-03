"""Seed database with sample data from CSV Files."""
from csv import DictReader

from app import app
from models import db, connect_db, User, City, Barangay, Service, User_Service, Type, User_Type, Job, User_Job, Comment, Rating, Message

# Create user services
service1 = Service(
    name='Carpenter'
)
service2 = Service(
    name='Painter'
)
service3 = Service(
    name='Plumber'
)
service4 = Service(
    name='Electrician'
)
db.session.add(service1)
db.session.add(service2)
db.session.add(service3)
db.session.add(service4)
db.session.commit()

# Create Types of User
client = Type(
    name='client'
)
bluecollar = Type(
    name='bluecollar'
)
admin = Type(
    name='admin'
)

db.session.add(client)
db.session.add(bluecollar)
db.session.add(admin)
db.session.commit()


with open('generator/city.csv') as city:
    db.session.bulk_insert_mappings(City, DictReader(city))

with open('generator/bar.csv') as city:
    db.session.bulk_insert_mappings(Barangay, DictReader(city))

with open('generator/users.csv') as user:
    db.session.bulk_insert_mappings(User, DictReader(user))

db.session.commit()

with open('generator/user_type.csv') as type:
    db.session.bulk_insert_mappings(User_Type, DictReader(type))

with open('generator/user_service.csv') as service:
    db.session.bulk_insert_mappings(User_Service, DictReader(service))

db.session.commit()


job1 = Job(
    job="House Painting",
    description="Pain entire house with 1st, 2nd and final coating"
)

job2 = Job(
    job="Create Door",
    description="Create a door for  the kitchen"
)

db.session.add(job1)
db.session.add(job2)
db.session.commit()

userjob1 = User_Job(
    user_id=1,
    job_id=1
)

userjob2 = User_Job(
    user_id=2,
    job_id=2
)

db.session.add(userjob1)
db.session.add(userjob2)
db.session.commit()


comment1 = Comment(
    comment="Amazing job!!!",
    user_from=1,
    user_to=2
)

comment2 = Comment(
    comment="Door was sturdy and nicely done!",
    user_from=1,
    user_to=3
)

db.session.add(comment1)
db.session.add(comment2)
db.session.commit()

rating1 = Rating(
    rating=4,
    user_from=1,
    user_to=4
)

rating2 = Rating(
    rating=5,
    user_from=1,
    user_to=5
)

db.session.add(rating1)
db.session.add(rating2)
db.session.commit()

message1 = Message(
    message="Are you available on Thursday?",
    message_from=1,
    message_to=6
)

message2 = Message(
    message="Yes I will be, what do you need?",
    message_from=6,
    message_to=1
)

db.session.add(message1)
db.session.add(message2)
db.session.commit()
