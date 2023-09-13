from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '998251e474ef6a9ae2b6b0804e7d4eb0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app )
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)


@loginmanager.user_loader
def load_user(user_id):
      return User.query.get(int(user_id))

class User(db.Model, UserMixin):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(20), unique=True, nullable=False)
      email = db.Column(db.String(120), unique=True, nullable=False)
      image_file = db.Column(db.String(20), default='default.img', nullable=False)
      password = db.Column(db.String(60), nullable=False)
      posts = db.relationship('Post', backref='author', lazy=True)

      def __repr__(self):
            return f"User ('{self.username}', '{self.email}', '{self.image_file}')"
      
class Post(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100), nullable=False)
      location = db.Column(db.String(100), nullable=False)
      content = db.Column(db.Text, nullable=False)
      level = db.Column(db.String(100), nullable=False)
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
      
      def __repr__(self):
           return f"Post('{self.title}')"      


posts = [
    {
        'location': 'Calicut',
        'title': 'Software Developer',
        'content': 'First ',
        'level': 'Fresher'
    },
    {
        'location': 'Bangalore',
        'title': 'Content Writer',
        'content': 'Second post content',
        'level': '1 year experience'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
        form = RegistrationForm()
        if form.validate_on_submit():
              hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
              user = User(username=form.username.data, email=form.email.data, password=hashed_password)
              db.session.add(user)
              db.session.commit()
              flash(f'Account created for {form.username.data}!', 'success')
              return redirect(url_for('login'))
        return render_template('signup.html',form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit():
              user = User.query.filter_by(email=form.email.data).first()
              if user and bycrypt.check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('home'))
              else:
                    flash('Login unsuccessfull. Please enter correct credentials')
        return render_template('login.html', form = form)

@app.route("/logout")
def logout():
      logout_user()
      return redirect(url_for('home'))      

@app.route("/account")
def account():
        return render_template('account.html', form = form)




if __name__ == '__main__':
    app.run(debug=True)