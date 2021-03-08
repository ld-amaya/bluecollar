"""User view test"""

import os
import io
import boto3
from unittest import TestCase
from app import app, CURRENT_USER_KEY
from flask import g
from models import db, User, Service, User_Service, Comment, Message, Type, Job, City, User_Type
from flask_bcrypt import Bcrypt
from datetime import datetime
from decouple import config


bcrypt = Bcrypt()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///bluecollar-tests'))
app.config['SQLALCHEMY_ECHO'] = False
# Disable wtf csrf token validation
app.config['WTF_CSRF_ENABLED'] = False

BUCKET = config('AWS_BUCKET')
BUCKET_URL = config('AWS_OBJECT_URL')
ACCESS_KEY = config('AWS_ACCESS_KEY')
SECRET_KEY = config('AWS_API_SECRET')

S3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

db.drop_all()
db.create_all()


class UserViewTest(TestCase):
    """Test for user view"""

    def setUp(self):
        """Create seed data"""
        # Image File
        self.Image = os.path.join('logo.png')

        # Delete all possible querys
        User.query.delete()
        Message.query.delete()
        Comment.query.delete()
        Service.query.delete()
        Type.query.delete()
        User_Type.query.delete()
        Job.query.delete()
        City.query.delete()
        User_Service.query.delete()

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
        self.bluecollar = bluecollar

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
        self.carpenter = service1
        self.painter = service2
        self.plumber = service3
        self.electrician = service4

        # add city
        city = City(
            name="Cebu City"
        )

        db.session.add(city)
        db.session.commit()
        self.city = city

        # encrypt password
        hashed = bcrypt.generate_password_hash("@BcD3Fgh1")
        hashed_utf8 = hashed.decode("utf8")
        user1 = User(
            profile="default-icon.png",
            first_name="Jose",
            last_name="Marie",
            email="jm@user.com",
            password=hashed_utf8,
            facebook="https://facebook.com",
            mobile="09171234567",
            city_id=self.city.id,
            rating=2,
            title="Best Carpenter",
            description="I am betting to be the best carpenter",
            confirmed=True,
            confirmed_on=datetime.utcnow())
        user2 = User(
            profile="default-icon.png",
            first_name="General",
            last_name="Matias",
            email="gen@user.com",
            password=hashed_utf8,
            facebook="https://facebook.com/general",
            mobile="09171234567",
            city_id=self.city.id,
            rating=3,
            title="Best Electrician",
            description="Electrecute me and you will see",
            confirmed=True,
            confirmed_on=datetime.utcnow()
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.user1 = user1
        self.user2 = user2

        # Add user type
        user_type = User_Type(
            user_id=self.user1.id,
            type_id=self.bluecollar.id
        )
        db.session.add(user_type)
        db.session.commit()

        # Assign User_Service
        us = User_Service(
            user_id=self.user1.id,
            service_id=self.carpenter.id
        )
        db.session.add(us)
        db.session.commit()

        # Add messages
        message1 = Message(
            message="Are you available on Thursday?",
            message_from=self.user1.id,
            message_to=self.user2.id
        )
        message2 = Message(
            message="Yes I will be, what do you need?",
            message_from=self.user2.id,
            message_to=self.user1.id
        )

        db.session.add(message1)
        db.session.add(message2)
        db.session.commit()

    def tearDown(self):
        response = super().tearDown()
        db.session.rollback()
        return response

    ############ Login and Registration Tests ##############################

    def test_login(self):
        """Test user login"""

        with app.test_client() as client:
            params = {'email': self.user1.email,
                      'password': '@BcD3Fgh1'}
            response = client.post('/login', data=params,
                                   follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<span id="session">Jose</span>', html)
            self.assertEqual(g.user.id, self.user1.id)

    def test_client_registration(self):
        """Test client/user registration"""

        with app.test_client() as client:
            params = {'first_name': 'Lou',
                      'last_name': 'Amaya',
                      'email': 'louamaya@me.com',
                      'password': '@BcD3Fgh1',
                      'city': self.city.id}
            response = client.post('/registration/client',
                                   data=params, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<span id="session">Lou</span>', html)
            self.assertEqual(g.user.email, 'louamaya@me.com')

    def test_bluecollar_registration(self):
        """Test bluecollar registration"""

        with app.test_client() as client:
            params = {'first_name': 'Ding',
                      'last_name': 'Dong',
                      'email': 'dingdong@gmail.com',
                      'password': '@BcD3Fgh1',
                      'facebook': 'https://facebook.com/dingdong',
                      'mobile': '09177654321',
                      'city': self.city.id,
                      'title': 'I am a painter not a plumber',
                      'description': 'Painting is my passion, plumber is my game',
                      'painter': 'y',
                      'plumber': 'y'}
            response = client.post('/registration/bluecollar',
                                   data=params, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(g.user.email, 'dingdong@gmail.com')
            self.assertEqual(g.user.service[0].name, "Painter")
            self.assertEqual(g.user.service[1].name, "Plumber")

    ############ Get Request Tests ##############################

    def test_index_page(self):
        """Test index page display"""

        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h2>Top Carpenters</h2>", html)

    ############ worker.html Route Requests Tests ##############################

    def test_display_worker_page(self):
        """Test worker get request route"""

        with app.test_client() as client:
            response = client.get(f"/worker/{self.user1.id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h2>Best Carpenter</h2>", html)

    def test_send_message_authenticated(self):
        """Test sending message for authenticated user"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session[CURRENT_USER_KEY] = self.user1.id
                g.user = self.user1

            response = client.post(
                f"/message/add/{self.user1.id}", data={
                    'message': 'Test message'
                }, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(g.user.messages[1].message, "Test message")

    def test_send_message_unauthenticated(self):
        """Test sending message for unauthenticated user should be redirected to home page"""
        with app.test_client() as client:
            response = client.post(
                f"/message/add/{self.user2.id}", data={
                    'message': 'Test message'
                }, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h2>Top Carpenters</h2>", html)

    def test_add_comment_authenticated(self):
        """Test add comment to bluecollar worker for authenticated user"""

        with app.test_client() as client:

            with client.session_transaction() as session:
                session[CURRENT_USER_KEY] = self.user1.id
                g.user = self.user1

            data = {
                'title': 'Great Job',
                'comment': 'Until next time',
                'rating': 3
            }

            response = client.post(
                f'/comment/{self.user1.id}', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<div id="user_comments">Until next time</div>', html)

    def test_add_comment_unauthenticated(self):
        """Test add comment to bluecollar worker for unauthenticated user should redirect to home"""

        with app.test_client() as client:
            data = {
                'title': 'Great Job',
                'comment': 'Until next time',
                'rating': 3
            }

            response = client.post(
                f'/comment/{self.user1.id}', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h2>Top Carpenters</h2>", html)

    ############ message.html Route Requests Tests ##############################

    def test_message_unauthenticated(self):
        """Test viewing messages page with unauthenticated shoule be redirected to home page"""

        with app.test_client() as client:
            response = client.get("/messages", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Top Carpenter", html)

    def test_messages_authenticated(self):
        """Test viewing messages page with Authenticated user"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session[CURRENT_USER_KEY] = self.user1.id
                g.user = self.user1

            response = client.get("/messages", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("General", html)

    ############ profile.html Route Requests Tests ##############################

    def test_worker_profile_unauthenticate(self):
        """Test profile GET Request unauthenticated"""

        with app.test_client() as client:

            response = client.get(
                "/profile/edit", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Top Carpenter", html)

    def test_worker_profile_authenticated(self):
        """Test profile GET Request authenticated"""

        with app.test_client() as client:

            with client.session_transaction() as session:
                session[CURRENT_USER_KEY] = self.user1.id
                g.user = self.user1

            response = client.get(
                "/profile/edit", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<input class="form-control" id="first_name" name="first_name" required type="text" value="Jose">', html)

    def test_worker_edit_profile_authenticated(self):
        """Test edit profile post request authenticated"""

        with app.test_client() as client:

            with client.session_transaction() as session:
                session[CURRENT_USER_KEY] = self.user1.id
                g.user = self.user1
                cid = self.city.id

            data = {
                'first_name': 'Mang Jose',
                'last_name': 'Marie',
                'email': 'jm@user.com',
                'facebook': 'https://facebook.com',
                'mobile': '09171234567',
                'cities': cid,
                'title': 'Best Carpenter',
                'description': 'I am the best carpenter'
            }

            response = client.post(
                "/profile/edit", data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<input class="form-control" id="first_name" name="first_name" required type="text" value="Mang Jose">', html)
            self.assertIn('Profile successfully updated', html)

    ############ image.html Route Requests Tests ##############################

    def test_image_upload_unauthenticated(self):
        """Test viewing image upload page with unauthenticated shoule be redirected to home page"""

        with app.test_client() as client:
            response = client.get("/image/upload", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Top Carpenter", html)

    def test_image_upload_authenticated(self):
        """Test image upload with authenticated user"""

        with app.test_client() as client:

            data = {
                'profile_pix': (io.BytesIO(b"abcdef"), self.Image)
            }
            with client.session_transaction() as session:
                session[CURRENT_USER_KEY] = self.user1.id
                g.user = self.user1

            response = client.post(
                "/image/upload", data=data, follow_redirects=True, content_type='multipart/form-data')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Profile successfully changed", html)

            # Remove image from local file and from S3
            filename = g.user.profile.split('/')
            os.remove('static/images/profiles/' + filename[3])
            S3.delete_object(Bucket=BUCKET, Key=filename[3])

    def test_non_image_upload_authenticated(self):
        """Test non-image upload for authenticated user"""

        with app.test_client() as client:
            data = {
                'profile_pix': (io.BytesIO(b"abcdef"), "/static/images/fb_logo.svg")
            }

            with client.session_transaction() as session:
                session[CURRENT_USER_KEY] = self.user1.id
                g.user = self.user1

            response = client.post(
                "/image/upload", data=data, follow_redirects=True, content_type='multipart/form-data')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Images Only!", html)
