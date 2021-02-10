import os
import requests
import json
import uuid
from flask import Flask, request, render_template, jsonify, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, City, Service, User_Service, Type, User_Type, Job, User_Job, Comment, Message
from forms import RegistrationForm, WorkerForm, LoginForm, CommentForm
from validation import Validate
from mail import Email


app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///bluecollar'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# # File upload Settings
app.config['UPLOAD_PATH'] = 'static/images/profiles/'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

connect_db(app)

##############################################################################


def login_user(user):
    """Create user sessions"""

    session['uid'] = user.id
    session['email'] = user.email
    session['name'] = user.first_name


def logout_user():
    """Delete all sessions"""
    del session['uid']
    del session['email']
    del session['name']


def Validate_Image(filename):
    """Validate image extension"""
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        return False
    return True


##############################################################################


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

    login_form = LoginForm()
    return render_template("index.html", carpenters=carpenters, painters=painters, plumbers=plumbers, electricians=electricians, login_form=login_form)

###### GET ROUTES ###########################################


@ app.route("/worker/<int:id>")
def worker_details(id):
    """Handles worker details"""

    user = User.query.get_or_404(id)
    login_form = LoginForm()
    comment_form = CommentForm()
    # comment_id = [f.comment_id for f in comments if f.user_to == id]
    comments = Comment.query.filter(Comment.user_to_id == id).order_by(
        Comment.timestamp.desc()).all()
    ave = 0
    rate = [c.rating for c in comments]
    if rate:
        ave = sum(rate) / len(rate)
    return render_template("/users/worker.html", user=user, comments=comments, ave=round(ave), login_form=login_form, comment_form=comment_form)

###### API REQUESTS ROUTES ###########################################


@ app.route("/email/<email>", methods=["POST"])
def check_email_if_existing(email):
    """Handles return of services list"""
    data = [e.serialized_email()
            for e in User.query.filter(User.email == email).all()]
    return jsonify(data)


###### POST ROUTES ###########################################

@app.route("/comment/<int:id>", methods=["POST"])
def add_comments(id):
    """Handles saving of comments and rating"""
    form = CommentForm()
    rating = request.form['rating']
    if form.validate_on_submit():
        comment = Comment(
            title=form.title.data,
            comment=form.comment.data,
            rating=rating,
            user_from_id=session['uid'],
            user_to_id=id
        )
        db.session.add(comment)
        db.session.commit()
    return redirect(f"/worker/{id}")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles User Login"""

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.login(login_form.email.data, login_form.password.data)
        if user:
            login_user(user)
            return redirect(request.referrer)
    return render_template("/users/login.html", login_form=login_form)


@app.route("/logout")
def logout():
    """Handles User Logout"""
    logout_user()
    return redirect(request.referrer)


@ app.route("/registration/<user_type>", methods=['GET', 'POST'])
def register(user_type):
    """Handles User Registration"""
    cities = City.query.all()
    if user_type == 'user':
        form = RegistrationForm(cities=cities)
        ut = 1
    elif user_type == 'worker':
        form = WorkerForm(cities=cities)
        ut = 2
    else:
        return redirect("/")

    if form.validate_on_submit():

        # Create profile image file name
        filename = ""
        if form.profile.data:
            profile = form.profile.data
            file_ext = os.path.splitext(profile.filename)[1]
            filename = str(uuid.uuid4().hex) + file_ext

            # Validate Profile Picture
            if not Validate_Image(filename):
                form.profile.errors.append(
                    "Invalid file extension ('.jpg', '.png', '.gif'")
                return render_template("/users/registration.html", form=form, user_type=user_type)

        # Instantiate user class
        user = Validate(form, ut, filename)

        # Verify password format
        if not user.valid_password():
            form.password.errors.append(
                "Password must be at least 8 characters with numbers, special characters, lowercase and uppercase!")
            return render_template("/users/registration.html", form=form, user_type=user_type)

        # Verify User Email
        if not user.valid_email():
            form.email.errors.append(
                "Please enter a valid email address!")
            return render_template("/users/registration.html", form=form, user_type=user_type)

        # Create user session
        if user_type == "worker":
            facebook = form.facebook.data
            mobile = form.mobile.data
        else:
            facebook = ""
            mobile = ""

        sess = user.register_user(facebook, mobile)
        user.Add_User_Type(sess.id)

        if user_type == "worker":
            user.Add_Services(sess.id, form.carpenter.data, form.painter.data,
                              form.plumber.data, form.electrician.data)

        # Upload profile picture
        if filename:
            profile.save(os.path.join("static/images/profiles/") + filename)

        # Create user session
        login_user(sess)

        # Send email verification to user
        # sendMail = Email(session['email'])
        # sendMail.VerifyMail()
        return redirect("/")

    return render_template("/users/registration.html", form=form, user_type=user_type)


@ app.route("/user/<int:id>/edit", methods=["GET", "POST"])
def edit_user(id):
    """Handles editing of user"""
    user = User.query.get_or_404(id)
    return render_template("edit_profile.html", user=user)
