from app import app, db
from app.forms import LoginForm, RegistrationForm, AddTeacherForm, RateTeacherForm
from flask import render_template, redirect, flash, make_response, jsonify, url_for, request
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Teacher, Rating
from werkzeug.urls import url_parse
from datetime import datetime
from .views import update_score


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
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/add_teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    form = AddTeacherForm()

    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(
            first_name=form.first_name.data, last_name=form.last_name.data, dept=form.dept.data).first()
        if teacher is not None:
            flash('Teacher already exists')
            return redirect(url_for('add_teacher'))
        teacher = Teacher(first_name=form.first_name.data,
                          last_name=form.last_name.data, dept=form.dept.data, created_by=current_user.id)
        db.session.add(teacher)
        db.session.commit()
        flash("Successfully Added New Teacher!")
        return redirect(url_for('add_teacher'))
    return render_template('add_teacher.html', title='Add Teacher', form=form)


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


@app.route('/view_teachers')
@login_required
def view_teachers():
    teachers = Teacher.query.order_by(Teacher.created_at.desc()).all()
    if(len(teachers)):
        return render_template('view_teachers.html', title="Teachers", teachers=teachers)
    flash('No teachers added. Please add some.')
    return redirect(url_for('add_teacher'))


@app.route('/rate_teacher/<teacherId>', methods=['GET', 'POST'])
@login_required
def rate_teacher(teacherId):
    form = RateTeacherForm()
    if form.validate_on_submit():
        dedication_score = form.dedication_score.data
        leniency_score = form.leniency_score.data
        marks_score = form.marks_score.data
        teaching_score = form.teaching_score.data
        friendliness_score = form.friendliness_score.data
        rating = Rating(teacher_id=teacherId, user_id=current_user.id,
                        dedication_score=dedication_score,
                        leniency_score=leniency_score,
                        marks_score=marks_score,
                        teaching_score=teaching_score,
                        friendliness_score=friendliness_score)

        if(update_score(teacherId, dedication_score, leniency_score, marks_score, teaching_score, friendliness_score)):
            db.session.add(rating)
            db.session.commit()
            flash('Successfuly rated! Thank you for your contribution.')
            return redirect(url_for('view_teachers'))
        else:
            flash(
                'Unknown error. Sorry, please report the issue to the admin. Try again.')
            return redirect(url_for(rate_teacher, teacherId=teacherId))
    teacher = Teacher.query.filter_by(id=teacherId).first()
    return render_template('rate_teacher.html', title="Rate Teacher", teacher=teacher, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out Successfully.")
    return redirect(url_for('login'))
