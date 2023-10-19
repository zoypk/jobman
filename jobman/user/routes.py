from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from models import User
from forms import RegistrationForm, LoginForm
from jobman import db, bcrypt

users = Blueprint('users', __name__)

@users.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, usertype=form.usertype.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('show_jobs'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if form.usertype.data == 'Company':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('show_jobs'))
            elif form.usertype.data == 'Job Seeker': 
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('show_jobs'))
        else:
                flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
    else:
        flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))