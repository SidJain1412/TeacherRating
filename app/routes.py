from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask import render_template, redirect, flash, make_response, jsonify, url_for, request
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Teacher
from werkzeug.urls import url_parse
from datetime import datetime


auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if(username == "sid"):
        return 'admin'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}, 403))


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered!")
        return redirect(url_for('login'))
    # Title is going to base.html through register.html
    return render_template('register.html', title="Register", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out Successfully.")
    return redirect(url_for('login'))
