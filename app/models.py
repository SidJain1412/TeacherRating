from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    dept = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    dept = db.Column(db.String(64), index=True)
    overall_score = db.Column(db.Float, default=0.0)
    dedication_score = db.Column(db.Float, default=0.0)
    leniency_score = db.Column(db.Float, default=0.0)
    marks_score = db.Column(db.Float, default=0.0)
    teaching_score = db.Column(db.Float, default=0.0)
    friendliness_score = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return '<Teacher {}>'.format(self.name)
