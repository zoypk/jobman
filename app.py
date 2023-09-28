from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import os
from datetime import date
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = '998251e474ef6a9ae2b6b0804e7d4eb0'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance/site.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app )
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'users.login'

class RegistrationForm(FlaskForm):
    usertype = SelectField('Select Usertype',choices=[('Job Seeker', 'Job Seeker'),('Company', 'Company')],validators=[InputRequired()])
    username = StringField('Username',validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirmPassword = PasswordField('Confirm Password',validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')


class LoginForm(FlaskForm):
    usertype = SelectField('Select Usertype',choices=[('Job Seeker', 'Job Seeker'),('Company', 'Company')],
                           validators=[InputRequired()])
    email = StringField('email', validators = [InputRequired(), Email() ])
    password =  PasswordField('Password', validators = [InputRequired(),  ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    

class JobForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    level = StringField('Level', validators=[InputRequired()])
    submit = SubmitField('Post')

class Apply(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    contact = IntegerField('Content', validators=[InputRequired()])
    email = StringField('email', validators = [InputRequired(), Email() ])
    content = StringField('Cover Letter', validators=[InputRequired()])
    experience = IntegerField('Professional Experience in years', validators=[InputRequired()])
    resume = FileField('Cover Letter', validators=[ FileAllowed(['jpg', 'png', 'bmp'])])
    submit = SubmitField('Apply')

@login_manager.user_loader
def load_user(user_id):
      return User.query.get(int(user_id))


class User(db.Model, UserMixin):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(20), unique=True, nullable=False)
      usertype = db.Column(db.String(20), nullable=False)
      email = db.Column(db.String(120), unique=True, nullable=False)
      password = db.Column(db.String(60), nullable=False)
      jobs = db.relationship('Jobs', backref='job_applier', lazy=True)
      applications = db.relationship('Application', backref='application_submiter', lazy=True)

      def __repr__(self):
            return f"User ('{self.id}', '{self.username}', '{self.usertype}', '{self.email}')"
      
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=date.today())
    degree = db.Column(db.String(20), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    cv = db.Column(db.String(20), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
class Jobs(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100), nullable=False)
      location = db.Column(db.String(100), nullable=False)
      content = db.Column(db.Text, nullable=False)
      level = db.Column(db.String(100), nullable=False)
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
      applications = db.relationship('Application', backref='application_jober', lazy=True)
      
      def __repr__(self):
           return f"Post('{self.title}')"      


# posts = [
#     {
#         'location': 'Calicut',
#         'title': 'Software Developer',
#         'content': 'First ',
#         'level': 'Fresher'
#     },
#     {
#         'location': 'Bangalore',
#         'title': 'Content Writer',
#         'content': 'Second post content',
#         'level': '1 year experience'
#     }
# ]

@app.route("/posted_jobs")
@login_required
def posted_jobs():
    jobs = Jobs.query.filter_by(job_applier=current_user)
    print(jobs)
    return render_template('show_jobs.html', jobs=jobs)

@app.route("/")
@app.route("/show_jobs")
def show_jobs():
    jobs = Jobs.query.all()
    print(jobs)
    return render_template('show_jobs.html', jobs=jobs)

# def save_picture(form_picture):
#     f_name, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = f_name + f_ext
#     picture_path = os.path.join(app.root_path, 'static', picture_fn)
#     form_picture.save(picture_path)
#     return picture_fn


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/signup", methods=['GET', 'POST'])
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

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))

    if form.validate_on_submit():
        print('password clear')
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if form.usertype.data == 'Company':
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posted_jobs'))
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

@app.route("/logout")
@login_required
def logout():
      logout_user()
      return redirect(url_for('login'))      

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def post_jobs():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(title=form.title.data,
                   content=form.content.data,
                   location=form.location.data,
                   level=form.level.data,
                   job_applier=current_user)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('posted_jobs'))
    return render_template('create_post.html', form=form)

@app.route("/post/<int:post_id>")
def post(post_id): 
    post = Jobs.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Jobs.query.get_or_404(post_id)
    form = JobForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.location = form.location.data
        post.level = form.level.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.location.data = post.location
        form.level.data = post.level

    return render_template('create_post.html', post=post, form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Jobs.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/post/<int:job_id>/apply", methods=['GET', 'POST'])
def apply_post(job_id):
    # post = Post.query.get_or_404(post_id)
    form = Apply()
    job = Jobs.query.filter_by(id=job_id).first()
    if form.validate_on_submit():
        application = Application(experience=form.experience.data,
                              cover_letter=form.content.data,
                              application_submiter=current_user,
                              application_jober=job,
                            #   resume=form.resume.data.filename
                            )
        print(form.resume.data)
        # picture_file = save_picture(form.resume.data)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('show_jobs'))
    return render_template('apply.html', form=form, legend='Apply Now')




if __name__ == '__main__':
    app.run(debug=True)