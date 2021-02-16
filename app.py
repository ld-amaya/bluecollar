import os
import requests
import json
import uuid
from flask import Flask, request, render_template, jsonify, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, City, Service, User_Service, Type, User_Type, Job, User_Job, Comment, Message
from forms import RegistrationForm, WorkerForm, LoginForm, CommentForm, MessageForm, PasswordForm, ProfileForm, JobForm, CityForm
from validation import Validate, Password, ServiceType
from mail import Email
from datetime import datetime

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
    session['type'] = user.type[0].name


def logout_user():
    """Delete all sessions"""
    del session['uid']
    del session['email']
    del session['name']
    del session['type']


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
    message_form = MessageForm()
    # comment_id = [f.comment_id for f in comments if f.user_to == id]
    comments = Comment.query.filter(Comment.user_to_id == id).order_by(
        Comment.timestamp.desc()).all()
    ave = 0
    rate = [c.rating for c in comments]
    if rate:
        ave = sum(rate) / len(rate)
    return render_template("/users/worker.html",
                           user=user,
                           comments=comments,
                           ave=round(ave),
                           login_form=login_form,
                           comment_form=comment_form,
                           message_form=message_form)


@app.route("/messages")
def display_message():
    """Handles display of all messages"""

    # Redirect user to homepage if not logged in
    if not 'uid' in session:
        return redirect("/")

    # Get the unique id of from and to
    chatmates = (Message.query
                 .filter((Message.message_from == session['uid']) | (Message.message_to == session['uid']))
                 .all()
                 )
    # Get the chatids
    chatids = []
    for c in chatmates:
        if not c.message_from == session['uid'] and c.message_from not in chatids:
            chatids.append(c.message_from)
        elif not c.message_to == session['uid'] and c.message_to not in chatids:
            chatids.append(c.message_to)
    chatmates = User.query.filter(User.id.in_(chatids)).all()
    return render_template("/users/messages.html", chatmates=chatmates)


@app.route("/profile")
def display_profile():
    """Handles profile page display"""
    return render_template("/users/profile.html")

###### POST ROUTES ###########################################


@ app.route("/message/add/<int:id>", methods=["POST"])
def send_message(id):
    """Handles adding message"""

    # Redirect user to homepage if not logged in
    if not 'uid' in session:
        return redirect("/")

    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            message=form.message.data,
            message_from=session['uid'],
            message_to=id,
            timestamp=datetime.utcnow()
        )
        db.session.add(message)
        db.session.commit()
    return redirect(f"/worker/{id}")


@ app.route("/comment/<int:id>", methods=["POST"])
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

        # Instantiate user and password class
        user = Validate(form, ut, filename)
        password = Password(form)
        # Verify password format
        if not password.valid_password():
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


@ app.route("/profile/edit", methods=["GET", "POST"])
def edit_user():
    """Handles editing of user"""
    cities = City.query.all()
    user = User.query.get_or_404(session['uid'])
    form = ProfileForm(obj=user)
    job = JobForm()
    if form.validate_on_submit():
        city = request.form['cities']
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.facebook = form.facebook.data
        user.mobile = form.mobile.data
        user.city_id = city
        db.session.add(user)
        db.session.commit()

        if session['type'] == "bluecollar":
            # Remove all existing user service
            services = User_Service.query.filter(
                User_Service.user_id == session['uid']).all()
            for s in services:
                db.session.delete(s)

            # add new services selected
            service = ServiceType(
                job.carpenter.data, job.painter.data, job.electrician.data, job.plumber.data)
            service.UserService(session['uid'])
        flash("Profile successfully updated", "success")
    return render_template("/users/profile.html", form=form, job=job)


@app.route("/password/edit", methods=["GET", "POST"])
def password_edit():
    """Handles changing of password"""
    form = PasswordForm()
    if form.validate_on_submit():

        # check if new and confirmed passwords are matched
        new_pass = form.new_password.data
        con_pass = form.confirm_password.data
        if new_pass != con_pass:
            form.new_password.errors.append("Password does not match!")
            return render_template("/users/password.html", form=form)

        # instantiate password class and verify password validity
        password = Password(form)
        if not password.valid_password():
            form.confirm_password.errors.append(
                "Password must be at least 8 characters")
            form.confirm_password.errors.append(
                "Password must contain numbers")
            form.confirm_password.errors.append(
                "Passowrd must contain special characters")
            form.confirm_password.errors.append(
                "Password must contain lowercase and uppercase")
            return render_template("/users/password.html", form=form)

        # Verify login
        is_valid = User.login(session['email'], form.password.data)
        if is_valid:
            user = User.query.get_or_404(session['uid'])
            password.save_password(user, form.new_password.data)
            flash("Password successfully changed", "success")
    return render_template("/users/password.html", form=form)


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Handles User Login"""

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.login(login_form.email.data, login_form.password.data)
        if user:
            login_user(user)
            # Check if user came from login.html then redirect to homepage
            if 'login' in request.referrer:
                return redirect("/")
            return redirect(request.referrer)
    return render_template("/users/login.html", login_form=login_form)


@ app.route("/logout")
def logout():
    """Handles User Logout"""
    logout_user()
    return redirect(request.referrer)


###### API REQUESTS ROUTES ###########################################


@ app.route("/email/<email>", methods=["POST"])
def check_email_if_existing(email):
    """Handles return of services list"""
    data = [e.serialized_email()
            for e in User.query.filter(User.email == email).all()]
    return jsonify(data)


@ app.route("/messages/retrieve/<int:id>", methods=["POST"])
def retrieve_messages(id):
    """Handles retrieval of message from for user"""

    all_messages = (Message.query
                    .filter(((Message.message_from == session['uid']) & (Message.message_to == id)) |
                            ((Message.message_from == id) & (Message.message_to == session['uid'])))
                    .order_by(Message.timestamp.desc())
                    .all())
    for m in all_messages:
        if not m.message_from == session['uid']:
            m.is_read = True
            db.session.add(m)
            db.session.commit()
    messages = [m.serialized_messages(session['uid']) for m in all_messages]

    return jsonify(messages)


@app.route("/messages/send", methods=["POST"])
def send_new_message():
    """Handles sending of new messages via axios"""

    data = request.json
    new_message = Message(
        message=data['text'],
        message_from=session['uid'],
        message_to=data['id'],
        timestamp=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()

    # return new data
    all_messages = (Message.query
                    .filter(((Message.message_from == session['uid']) & (Message.message_to == data['id'])) |
                            ((Message.message_from == data['id']) & (Message.message_to == session['uid'])))
                    .order_by(Message.timestamp.desc())
                    .all())
    messages = [m.serialized_messages(session['uid']) for m in all_messages]
    return jsonify(messages)


@app.route("/checkunread/<int:id>", methods=["POST"])
def check_unread_messages(id):
    """Check for unread messages"""
    all_messages = (Message.query
                    .filter(((Message.message_from == session['uid']) & (Message.message_to == id)) |
                            ((Message.message_from == id) & (Message.message_to == session['uid'])))
                    .order_by(Message.timestamp.desc())
                    .all())
    read = True
    for m in all_messages:
        if not m.is_read and not m.message_from == session['uid']:
            read = False
    return ({'read': read})


@app.route("/cities", methods=["POST"])
def return_cities():
    """Handles City List API Request"""
    cities = [c.serialized_city() for c in City.query.all()]
    user = User.query.get_or_404(session['uid'])
    services = [s.name for s in user.service]
    return jsonify(user={'id': user.city.id, 'city': user.city.name}, cities=cities, services=services)
