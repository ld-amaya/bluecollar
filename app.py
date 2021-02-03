import os
import requests
import json
from flask import Flask, request, render_template, jsonify, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, City, Barangay, Service, User_Service, Type, User_Type, Job, User_Job, Comment, Rating, Message
from forms import RegistrationForm
from validation import Validate

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

    # Display the workers only
    user_service = User_Service.query.all()
    carpenter_id = [f.user_id for f in user_service if f.service_id == 1]
    painter_id = [f.user_id for f in user_service if f.service_id == 2]
    plumber_id = [f.user_id for f in user_service if f.service_id == 3]
    electrician_id = [f.user_id for f in user_service if f.service_id == 4]

    carpenters = User.query.filter(User.id.in_(carpenter_id)).limit(4).all()
    painters = User.query.filter(User.id.in_(painter_id)).limit(4).all()
    plumbers = User.query.filter(User.id.in_(plumber_id)).limit(4).all()
    electricians = User.query.filter(
        User.id.in_(electrician_id)).limit(4).all()

    return render_template("index.html", carpenters=carpenters, painters=painters, plumbers=plumbers, electricians=electricians)

###### GET ROUTES ###########################################


@app.route("/worker/<int:id>")
def worker_details(id):
    """Handles worker details"""

    user = User.query.get_or_404(id)
    return render_template("/users/worker.html", user=user)

###### POST ROUTES ###########################################


@app.route("/registration", methods=['GET', 'POST'])
def register():
    """Handles User Registration"""
    cities = City.query.all()
    form = RegistrationForm(cities=cities)

    if form.validate_on_submit():

        # Instantiate user class
        user = Validate(form)
        # Veify password format
        if not user.valid_password():
            form.password.errors.append(
                "Password must be at least 8 characters with numbers, special characters, lowercase and uppercase!")
            return render_template("registration.html", form=form)
        # Verify User Email
        if not user.valid_email():
            form.first_name.errors.append(
                "Please enter a valid email address!")
            return render_template("registration.html", form=form)
        sess = user.register_user()
        user.Add_User_Type(sess.id)
        session['email'] = sess.email
        session['name'] = sess.first_name
        return redirect("/")
    return render_template("registration.html", form=form)
