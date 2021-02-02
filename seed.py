"""Seed database with sample data from CSV Files."""
from csv import DictReader

from app import app
from models import db, connect_db, User, City, Barangay, Service, User_Service, Type, User_Type, Job, User_Job, Comment, Rating, Message

with open('generator/city.csv') as city:
    db.session.bulk_insert_mappings(City, DictReader(city))

with open('generator/bar.csv') as city:
    db.session.bulk_insert_mappings(Barangay, DictReader(city))

db.session.commit()

user1 = User(
    first_name='Lou',
    last_name='Amaya',
    email='louamayame.com',
    password='1234',
    facebook='facebooklink',
    mobile='123456789',
    apartment_number='room 1',
    building='bldg 2',
    street='street 3',
    city_id=1,
    barangay_id=1
)

user2 = User(
    first_name='Rey',
    last_name='Amaya',
    email='reyamaya@me.com',
    password='5432',
    facebook='reyfacebooklink',
    mobile='98765432',
    apartment_number='room 2',
    building='bldg 3',
    street='street 4',
    city_id=1,
    barangay_id=1
)

db.session.add(user1)
db.session.add(user2)
db.session.commit()

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

# Associate user with service
userservice1 = User_Service(
    user_id=1,
    service_id=1
)
userservice2 = User_Service(
    user_id=2,
    service_id=2
)
userservice3 = User_Service(
    user_id=1,
    service_id=3
)
db.session.add(userservice1)
db.session.add(userservice2)
db.session.add(userservice3)
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

# Create User Type relationship
usertype1 = User_Type(
    user_id=1,
    type_id=1
)
usertype2 = User_Type(
    user_id=2,
    type_id=2
)
db.session.add(usertype1)
db.session.add(usertype2)
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
    user_from=2,
    user_to=1
)

db.session.add(comment1)
db.session.add(comment2)
db.session.commit()

rating1 = Rating(
    rating=4,
    user_from=2,
    user_to=1
)

rating2 = Rating(
    rating=5,
    user_from=1,
    user_to=2
)

db.session.add(rating1)
db.session.add(rating2)
db.session.commit()

message1 = Message(
    message="Are you available on Thursday?",
    message_from=1,
    message_to=2
)

message2 = Message(
    message="Yes I will be, what do you need?",
    message_from=2,
    message_to=1
)

db.session.add(message1)
db.session.add(message2)
db.session.commit()
