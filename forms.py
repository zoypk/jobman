from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min=2, max=20)])
    email = StringField('email', validators = [InputRequired(), Email() ])
    password =  PasswordField('Password', validators = [InputRequired(),  ])
    confirmPassword = PasswordField('Password', validators = [InputRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() 
        if user:
            raise ValidationError('Username not available')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first() 
        if email:
            raise ValidationError('email not available')

class LoginForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email() ])
    password =  PasswordField('Password', validators = [InputRequired(),  ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
