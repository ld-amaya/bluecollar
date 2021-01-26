import os
from flask import Flask, request, render_template, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, City, Barangay, Address, Type, User_Type, Job, User_Job, Comment, User_Comment, Rating, Message, User_Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///bluecollar'))

connect_db(app)
