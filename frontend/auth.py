'''
This is a Blueprint consisting of all routes related to user authentication , like signup, login , logout.
'''

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user,logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models_db import User
from . import db
from .forms import *


auth = Blueprint('auth', __name__)

# db.create_all(app=create_app())

@auth.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form = form)

@auth.route('/signup')
def signup():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form = form)

@auth.route('/login', methods = ['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('\n')
        flash('Please check your login details and try again.')

        return redirect(url_for('auth.login'))

    login_user(user)
    return render_template('pages/loginSuccess.home.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    print('User created')

    # return redirect(url_for('auth.login'))
    return redirect(url_for('auth.login'))

from . import login_manager


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('main.home'))
