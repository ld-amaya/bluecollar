import os
from flask import Flask, request, render_template, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, City, Barangay, Service, User_Service, Type, User_Type, Job, User_Job, Comment, Rating, Message
from forms import RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///bluecollar'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route("/")
def homepage():
    """Return home page"""
    barangays = Barangay.query.filter_by(city='Alcoy').all()
    return render_template("index.html", barangays=barangays)


@app.route("/registration")
def register():
    """Handles User Registration"""
    cities = City.query.all()
    forms = RegistrationForm(cities=cities)
    return render_template("registration.html", forms=forms)
