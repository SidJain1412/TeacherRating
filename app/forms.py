# Using Flask WTF (WT Forms) to represent web forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Teacher


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    # Automatic resolving of email
    email = StringField('Email', validators=[DataRequired(), Email()])
    dept = SelectField('Department', choices=[(
        'CSE', 'CSE'), ('IT', 'IT'), ('Software', 'Software')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Check if both passwords are the same
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # validate_{field_name} makes a custom validator automatically used for that field
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('E-mail is already in use. Try again.')
        domain = email.data.split('@')[1]
        if(domain != 'srmuniv.edu.in'):
            raise ValidationError('Please enter an SRM email ID')


class AddTeacherForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dept = SelectField('Department', choices=[(
        'CSE', 'CSE'), ('IT', 'IT'), ('Software', 'Software')], validators=[DataRequired()])
    submit = SubmitField('Add Teacher')


class RateTeacherForm(FlaskForm):
    dedication_score = DecimalField('Dedication', validators=[DataRequired()])
