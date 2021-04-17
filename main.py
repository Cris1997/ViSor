from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from flask_mail import Mail, Message
from flask import Blueprint
from flask_app import db

main = Blueprint('main', __name__)



@main.route('/profile')
def profile():
    return 'Profile'