import os
from flask import Flask, request, render_template, jsonify, flash, session, redirect, g, Markup
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, City, Service, User_Service, Comment, Message, Album, Type
from forms import RegistrationForm, WorkerForm, LoginForm, CommentForm, MessageForm, PasswordForm, UserProfileForm, WorkerProfileForm, JobForm, ImageForm, AlbumForm, TokenForm
from itsdangerous import URLSafeTimedSerializer
from registration import Registration
from user import UserProfile
from password import Password
from service import ServiceType
from album import MyAlbum
from comment import UserComment
from datetime import datetime
from decouple import config
from mail import Mail


CURRENT_USER_KEY = "current_user"
BUCKET_URL = config('AWS_OBJECT_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECURITY_PASSWORD_SALT'] = config('SECRET_SALT')

toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# # File upload Settings
app.config['UPLOAD_PROFILE_PATH'] = 'static/images/profiles/'
app.config['UPLOAD_ALBUM_PATH'] = 'static/images/uploads/'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']


connect_db(app)

##############################################################################


@app.before_request
def global_user():
    """Create global user and global services"""
    g.services = Service.query.all()
    if CURRENT_USER_KEY in session:
        g.user = User.query.get(session[CURRENT_USER_KEY])
    else:
        g.user = None


def login_user(user):
    """Create user sessions"""

    session[CURRENT_USER_KEY] = user.id


def logout_user():
    """Delete all sessions"""
    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]


def Validate_Image(filename):
    """Validate image extension"""
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        return False
    return True

#################### LOGIN AND LOGOUT ###########################################


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Handles User Login"""

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.login(login_form.email.data,
                          login_form.password.data)
        if user:
            if user.confirmed:
                login_user(user)
                return redirect("/")
            else:
                flash(Markup(
                    "Please confirm your email address. <a href='/email/token' id='resend_token'> Resend Token </a>"))
        else:
            flash("Invalid credentials, please try again!")
    return render_template("/users/login.html", login_form=login_form)


@ app.route("/logout")
def logout():
    """Handles User Logout"""
    if not g.user:
        return redirect("/")
    logout_user()
    return redirect(request.referrer)


#################### GET ROUTES ###########################################


@app.route("/")
def homepage():
    """Return home page"""

    # Display the workers only
    user_service = User_Service.query.all()
    carpenter_id = [f.user_id for f in user_service if f.service_id == 1]
    painter_id = [f.user_id for f in user_service if f.service_id == 2]
    plumber_id = [f.user_id for f in user_service if f.service_id == 3]
    electrician_id = [f.user_id for f in user_service if f.service_id == 4]

    carpenters = User.query.filter(User.id.in_(carpenter_id)).order_by(
        User.rating.desc()).limit(4).all()
    painters = User.query.filter(User.id.in_(painter_id)).order_by(
        User.rating.desc()).limit(4).all()
    plumbers = User.query.filter(User.id.in_(plumber_id)).order_by(
        User.rating.desc()).limit(4).all()
    electricians = User.query.filter(
        User.id.in_(electrician_id)).order_by(
        User.rating.desc()).limit(4).all()

    login_form = LoginForm()
    return render_template("index.html", carpenters=carpenters, painters=painters, plumbers=plumbers, electricians=electricians, login_form=login_form)


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
    return render_template("/users/worker.html",
                           user=user,
                           comments=comments,
                           login_form=login_form,
                           comment_form=comment_form,
                           message_form=message_form)


@app.route("/messages")
def display_message():
    """Handles display of all messages"""

    # Redirect user to homepage if not logged in
    if not g.user:
        return redirect("/")

    # Get the unique id of from and to
    chatmates = (Message.query
                 .filter((Message.message_from == g.user.id) | (Message.message_to == g.user.id))
                 .all()
                 )

    # Things to consider
    # 1. Limit messages
    # 2. Create a chatmate table for easier query

    # Get the chatids
    chatids = []
    for c in chatmates:
        if not c.message_from == g.user.id and c.message_from not in chatids:
            chatids.append(c.message_from)
        elif not c.message_to == g.user.id and c.message_to not in chatids:
            chatids.append(c.message_to)
    chatmates = User.query.filter(User.id.in_(chatids)).all()
    return render_template("/users/messages.html", chatmates=chatmates)


@app.route("/view/<service_name>/<int:sid>")
def view_services(service_name, sid):
    """Handles view all bluecollar for a service"""

    user_service = User_Service.query.all()
    service_id = [f.user_id for f in user_service if f.service_id == sid]
    services = User.query.filter(User.id.in_(service_id)).all()

    return render_template("/users/services.html", services=services, service_name=service_name)

#################### POST ROUTES ###########################################


@ app.route("/message/add/<int:id>", methods=["POST"])
def send_message(id):
    """Handles adding message"""

    # Redirect user to homepage if not logged in
    if not g.user:
        return redirect("/")

    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            message=form.message.data,
            message_from=g.user.id,
            message_to=id,
            timestamp=datetime.utcnow()
        )
        db.session.add(message)
        db.session.commit()
    return redirect(f"/worker/{id}")


@ app.route("/comment/<int:id>", methods=["POST"])
def add_comments(id):
    """Handles saving of comments and rating"""

    if not g.user:
        return redirect("/")

    form = CommentForm()
    rating = request.form['rating']
    if form.validate_on_submit():
        uc = UserComment(form, rating, id)
        if uc.add_comment():
            if uc.add_rating():
                flash("Comment and Rating successfully added, Thank you!")
    return redirect(f"/worker/{id}")


@app.route("/confirm/email/<token>", methods=["GET", "POST"])
def confirm_email(token):
    expiration = 3600
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        user = User.query.filter_by(email=email).first_or_404()

        if user.confirmed:
            flash("Email already confirmed!", "success")
        else:
            user.confirmed = True
            user.confirmed_on = datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            flash("Thank you for confirming your account", "success")
        return redirect("/")
    except:
        flash("We cannot validate your email, enter your email address to resend token.")
        return redirect("/email/token")


@app.route("/email/token", methods=["GET", "POST"])
def email_token():
    """Handles resending of email confirmation"""
    # Send email verification to user
    form = TokenForm()
    if form.validate_on_submit():
        # check if mail is registered
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            mail = Mail(form.email.data, form.first_name.data)
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            token = serializer.dumps(
                form.email.data, salt=app.config['SECURITY_PASSWORD_SALT'])
            result = mail.send_confirmation_email(token)
            if result == 200:
                flash("Please confirm you email to activate account!", "success")
            return redirect("/")
        else:
            flash(
                "Email is not registered in our file, please try another email or register to continue!")
    return render_template("/users/token.html", form=form)


#################### GET, POST ROUTES ###########################################


@ app.route("/registration/<user_type>", methods=['GET', 'POST'])
def register(user_type):
    """Handles User Registration"""

    cities = City.query.all()

    if user_type == 'client':
        form = RegistrationForm(cities=cities)
    elif user_type == 'bluecollar':
        form = WorkerForm(cities=cities)
    else:
        return redirect("/")

    if form.validate_on_submit():
        # Create profile image file name
        filename = BUCKET_URL + "default-icon.png"
        if form.profile.data:
            img = MyAlbum(app.config['UPLOAD_PROFILE_PATH'],
                          app.config['UPLOAD_EXTENSIONS'])
            images = form.profile_pix.data
            filename = img.validate_profile(images)

        # Instantiate password class
        password = Password(form.password.data)

        # Verify password format
        if not password.valid_password():
            form.password.errors.append(
                "Password must be at least 8 characters with numbers, special characters, lowercase and uppercase!")
            return render_template("/users/registration.html", form=form, user_type=user_type)

        # Get user type
        uid = Type.query.filter(Type.name == user_type).first()
        ut = uid.id
        # Verify User Email
        user = Registration(form, ut, filename)
        # if not user.valid_email():
        #     form.email.errors.append("Please enter a valid email address!")
        #     return render_template("/users/registration.html", form=form, user_type=user_type)

        # Create user session
        if user_type == 'bluecollar':
            sess = user.register_user(form.facebook.data, form.mobile.data,
                                      form.title.data, form.description.data)
            service = ServiceType(form)
            service.Add_Services(sess.id)
        else:
            sess = user.register_user()

        # Create user session
        login_user(sess)

        # Add user type
        user.Add_User_Type(sess.id)

        # Send email verification to user
        mail = Mail(sess.email, sess.first_name)
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(
            sess.email, salt=app.config['SECURITY_PASSWORD_SALT'])
        result = mail.send_confirmation_email(token)
        if result == 200:
            flash("Please confirm you email to activate account!", "success")

        return redirect("/")

    return render_template("/users/registration.html", form=form, user_type=user_type)


@ app.route("/profile/edit", methods=["GET", "POST"])
def edit_user():
    """Handles editing of user profile"""

    if not g.user:
        return redirect("/")

    if g.user.type[0].name == "bluecollar":
        form = WorkerProfileForm(obj=g.user)
    else:
        form = UserProfileForm(obj=g.user)

    job = JobForm()
    if form.validate_on_submit():
        city = request.form['cities']
        user = UserProfile(form, city)

        if not g.user.type[0].name == "bluecollar":
            user.update()
        else:
            user.update(form.facebook.data, form.mobile.data,
                        form.title.data, form.description.data)

            services = User_Service.query.filter(
                User_Service.user_id == g.user.id).all()
            # Instantiate ServiceType class and add bluecollar services
            service = ServiceType(job)
            service.Add_Services(g.user.id, services)
        flash("Profile successfully updated", "success")
        # redirect to self to avoid form resubmission
        return redirect("/profile/edit")
    return render_template("/users/profile.html", form=form, job=job)


@app.route("/password/edit", methods=["GET", "POST"])
def password_edit():
    """Handles changing of password"""

    if not g.user:
        return redirect("/")
    form = PasswordForm()
    if form.validate_on_submit():

        # check if new and confirmed passwords are matched
        new_pass = form.new_password.data
        con_pass = form.confirm_password.data
        if new_pass != con_pass:
            form.new_password.errors.append("Password does not match!")
            return render_template("/users/password.html", form=form)

        # instantiate password class and verify password validity
        password = Password(new_pass)
        if not password.valid_password():
            form.confirm_password.errors.append(
                "Password must be at least 8 characters")
            form.confirm_password.errors.append(
                "Password must contain numbers")
            form.confirm_password.errors.append(
                "Passowrd must contain special characters @$!%*^#?&")
            form.confirm_password.errors.append(
                "Password must contain lowercase and uppercase")
            return render_template("/users/password.html", form=form)

        # Verify login
        is_valid = User.login(g.user.email, form.password.data)
        if is_valid:
            user = User.query.get_or_404(g.user.id)
            password.save_password(user, form.new_password.data)
            flash("Password successfully changed", "success")
            # redirect to self to avoid form resubmission
            return redirect("/password/edit")
    return render_template("/users/password.html", form=form)


@app.route("/image/upload", methods=["GET", "POST"])
def image_upload():
    """Handles uploading of images"""

    if not g.user:
        return redirect("/")

    form = ImageForm()
    album_form = AlbumForm()
    if form.validate_on_submit():
        img = MyAlbum(app.config['UPLOAD_PROFILE_PATH'],
                      app.config['UPLOAD_EXTENSIONS'])
        images = form.profile_pix.data
        filename = img.validate_profile(images)
        if filename:
            g.user.profile = filename
            db.session.add(g.user)
            db.session.commit()
            flash("Profile successfully changed", "success")
            # redirect to self to avoid form resubmission
            return redirect("/image/upload")
        else:
            form.profile_pix.errors.append(
                "An error occured while uploading profile pictureß, please try again!")
    return render_template("/users/image.html", form=form, album_form=album_form)


@app.route("/album/upload", methods=["GET", "POST"])
def album_upload():
    """Handles uploading of album"""

    if not g.user:
        return redirect("/")

    album_form = AlbumForm()
    form = ImageForm()

    if album_form.validate_on_submit():
        img = MyAlbum(app.config['UPLOAD_ALBUM_PATH'],
                      app.config['UPLOAD_EXTENSIONS'])
        images = album_form.album_pix.data
        if img.validate_album(images):
            flash("Album successfully changed", "success")
            # redirect to self to avoid form resubmission
            return redirect("/image/upload")
        else:
            album_form.album_pix.errors.append(
                "An error occured while uploading profile pictures, please try again!")
    return render_template("/users/image.html", form=form, album_form=album_form)


@app.route("/image/delete/<int:image_id>", methods=["POST"])
def delete_image(image_id):
    """Handles deleting of image from the album"""
    image = Album.query.get_or_404(image_id)
    filename = image.filename
    db.session.delete(image)
    db.session.commit()

    # Remove image from local File
    if not MyAlbum.delete_image(filename):
        print("No image found!")
    return redirect("/album/upload")

###### API REQUESTS ROUTES ###########################################


@ app.route("/messages/retrieve/<int:id>")
def retrieve_messages(id):
    """Handles retrieval of message from for user"""
    if not g.user:
        return redirect("/")
    all_messages = (Message.query
                    .filter(((Message.message_from == g.user.id) & (Message.message_to == id)) |
                            ((Message.message_from == id) & (Message.message_to == g.user.id)))
                    .order_by(Message.timestamp.desc())
                    .all())
    for m in all_messages:
        if not m.message_from == g.user.id:
            m.is_read = True
            db.session.add(m)
            db.session.commit()
    messages = [m.serialized_messages(g.user.id) for m in all_messages]

    return jsonify(messages)


@ app.route("/checkunread/<int:id>")
def check_unread_messages(id):
    """Check for unread messages"""

    if not g.user:
        return redirect("/")
    all_messages = (Message.query
                    .filter(((Message.message_from == g.user.id) & (Message.message_to == id)) |
                            ((Message.message_from == id) & (Message.message_to == g.user.id)))
                    .order_by(Message.timestamp.desc())
                    .all())
    read = True
    for m in all_messages:
        if not m.is_read and not m.message_from == g.user.id:
            read = False
    return ({'read': read})


@ app.route("/cities")
def return_cities():
    """Handles City List API Request"""

    cities = [c.serialized_city() for c in City.query.all()]
    user = User.query.get_or_404(g.user.id)
    services = [s.name for s in user.service]
    return jsonify(user={'id': user.city.id, 'city': user.city.name}, cities=cities, services=services)


@ app.route("/email/<email>")
def check_email_if_existing(email):
    """Handles return of services list"""

    data = [e.serialized_email()
            for e in User.query.filter(User.email == email).all()]
    return jsonify(data)


@ app.route("/messages/send", methods=["POST"])
def send_new_message():
    """Handles sending of new messages via axios"""

    if not g.user:
        return ({'status': False})
    data = request.json
    new_message = Message(
        message=data['text'],
        message_from=g.user.id,
        message_to=data['id'],
        timestamp=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()

    # return new data
    all_messages = (Message.query
                    .filter(((Message.message_from == g.user.id) & (Message.message_to == data['id'])) |
                            ((Message.message_from == data['id']) & (Message.message_to == g.user.id)))
                    .order_by(Message.timestamp.desc())
                    .all())
    messages = [m.serialized_messages(g.user.id) for m in all_messages]
    return jsonify(messages)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
