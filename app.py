from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime 
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '998251e474ef6a9ae2b6b0804e7d4eb0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app )

from models import User, Post

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
              flash(f'Account created for {form.username.data}!', 'success')
              return redirect(url_for('login'))
        return render_template('signup.html',form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
        form = LoginForm()
            
        return render_template('login.html', form = form)








if __name__ == '__main__':
    app.run(debug=True)