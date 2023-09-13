from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min=2, max=20)])
    email = StringField('email', validators = [InputRequired(), Email() ])
    password =  PasswordField('Password', validators = [InputRequired(),  ])
    confirmPassword = PasswordField('Password', validators = [InputRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email() ])
    password =  PasswordField('Password', validators = [InputRequired(),  ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
