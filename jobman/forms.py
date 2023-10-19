from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from models import User

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
    
    def validate_username(self, extra_validators=None):
        return super().validate_on_submit(extra_validators)
    

class JobForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    level = StringField('Level', validators=[InputRequired()])
    submit = SubmitField('Post')

class ApplyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    contact = StringField('Mobile Number', validators=[Length(min=10, max=15, message="Enter a valid mobile number")])
    email = StringField('email', validators = [InputRequired(), Email() ])
    content = StringField('Cover Letter', validators=[InputRequired()])
    experience = IntegerField('Professional Experience in years', validators=[InputRequired()])
    degree = SelectField('Degree',
                        default='Bachelor',    
                        choices=[('School', 'School'),
                                ('HighSchool', 'HighSchool'),
                                ('Bachelor', 'Bachelor'),
                                ('Master', 'Master'),
                                ('PHD', 'PHD')],)
    # resume = FileField('Cover Letter', validators=[ FileAllowed(['jpg', 'png', 'bmp'])])
    # cv = FileField('Update Resume', validators=[FileAllowed(['jpg', 'png', 'bmp'])])
    submit = SubmitField('Apply')

class Apply(FlaskForm):
                status=SelectField('',
                        default='hold',    
                        choices=[('approve', 'approve'),
                                ('reject', 'reject'),
                                ('hold', 'hold')])
                submit = SubmitField('Update')