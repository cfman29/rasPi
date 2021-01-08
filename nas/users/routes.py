from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from nas import db, bcrypt
from nas.models import User
from nas.users.forms import RegisterForm, LoginForm, UpdateAccount, reset_password_request, reset_password
from nas.users.utility import save_image, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else: flash('Login unsuccessful, please check email and password are correct', 'danger')
    else:
        if form.password.data:
            if not len(form.password.data) >= 6 : flash("Password must be at least 6 characters", "warning")
    return render_template('users/login.html', form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = reset_password_request()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to you with instructions on how to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None: 
        flash('Token is expired or invalid', 'warning')
        return redirect(url_for('users.reset_password'))
    form = reset_password()
    if form.validate_on_submit(): 
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash('Logout success', 'success')
    return redirect(url_for('index'))


@users.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.image.data: 
            image_file = save_image(form.image.data)
            current_user.user_image = image_file
            print(form.image.data)
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('users.dashboard'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_img/' + current_user.user_image)
    return render_template('users/dashboard.html', image_file=image_file, form=form)

@users.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated == False or current_user.admin == False:  return redirect(url_for('index'))
    return render_template('users/admin.html', form=form)

    