from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from nas import db, bcrypt
from nas.models import User
from nas.users.forms import RegisterForm, LoginForm, UpdateAccount, reset_password_request, reset_password
from nas.users.utility import send_reset_email

users = Blueprint('users', __name__)
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('primary.index'))
    form = RegisterForm()
    if form.validate_on_submit(): 
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('primary.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful', 'success')
            return redirect(url_for('primary.index'))
        else: flash('Login unsuccessful, please check email and password are correct', 'danger')
    else:
        if form.password.data:
            if not len(form.password.data) >= 6 : flash("Password must be at least 6 characters", "warning")
    return render_template('users/login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash('Logout success', 'success')
    return redirect(url_for('primary.index'))