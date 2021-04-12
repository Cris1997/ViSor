from flask import Blueprint
from flask_app import db

main = Blueprint('main', __name__)

@main.route('/ytuque')
def index():
    return 'Index'

@main.route('/profile')
def profile():
    return 'Profile'