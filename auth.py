from flask import Blueprint
from flask_app import db

auth = Blueprint('auth', __name__)

@auth.route('/login3')
def login():
    return 'Login'

@auth.route('/signup3')
def signup():
    return 'Signup'

@auth.route('/logout3')
def logout():
    return 'Logout'