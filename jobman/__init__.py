from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4
# from jobman.models import User
from flask_login import LoginManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
bootstrap = Bootstrap4()

# login_manager.login_view = 'users.login'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)



    from jobman.user.routes import users
    from jobman.post.routes import posts
    app.register_blueprint(users)
    app.register_blueprint(posts)



    app.config['SECRET_KEY'] = '998251e474ef6a9ae2b6b0804e7d4eb0'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance/site.db")}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    migrate = Migrate(app, db)
    login_manager.init_app(app)



    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    


    return app














# models


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
#

# def save_picture(form_picture):
#     f_name, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = f_name + f_ext
#     picture_path = os.path.join(app.root_path, 'static', picture_fn)
#     form_picture.save(picture_path)
#     return picture_fn