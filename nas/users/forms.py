from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from nas.models import User

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=40)])
    email = StringField('E mail', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=40)])
    confirmpassword = PasswordField('Confirm password', validators=[DataRequired(), Length(min=6, max=40), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: raise ValueError('Email already in use')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    submit = SubmitField('Login')

class UpdateAccount(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=40)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image = FileField('Update profile image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user: raise ValueError('Email already in use')

class reset_password_request(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValueError('There is no account linked to the email provided')

class reset_password(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=40)])
    confirmpassword = PasswordField('Confirm password', validators=[DataRequired(), Length(min=6, max=40), EqualTo('password')])
    submit = SubmitField('Reset password')