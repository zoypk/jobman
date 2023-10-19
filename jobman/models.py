from flask_login import UserMixin
from datetime import date
from jobman import db

class User(db.Model, UserMixin):
    username = db.Column(db.String(20), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    usertype = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    jobs = db.relationship('Jobs', backref='job_applier', lazy=True)
    applications = db.relationship('Application', backref='application_submiter', lazy=True)

    def __repr__(self):
            return f"User ('{self.id}', '{self.username}', '{self.usertype}', '{self.email}')"
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(20), )
    experience = db.Column(db.Integer, )
    cover_letter = db.Column(db.Text, )
    id = db.Column(db.Integer, primary_key=True)
    # gender = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, default=date.today())
    degree = db.Column(db.String(20))
    # industry = db.Column(db.String(50), )
    # cv = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') )
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id') )
    status = db.Column(db.String(20))

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