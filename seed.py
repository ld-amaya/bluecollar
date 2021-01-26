from app import app
from models import db, connect_db, User, City, Barangay, Address, Type, User_Type, Job, User_Job, Comment, User_Comment, Rating, Message, User_Message

user1 = User(
    first_name='Lou',
    last_name='Amaya',
    email='louamayame.com',
    password='1234',
    facebook='facebooklink',
    mobile='123456789',
    apartment_number='room 1',
    building='bldg 2',
    street='street 3'
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
    street='street 4'
)

db.session.add(user1)
db.session.add(user2)
db.session.commit()

city = City(
    name="Cebu",
    user_id='1'
)

db.session.add(city)
db.session.commit()

barangay = Barangay(
    name="Talamban"
)

db.session.add(barangay)
db.session.commit()

address = Address(
    city_id=1,
    barangay_id=1
)

db.session.add(address)
db.session.commit()
