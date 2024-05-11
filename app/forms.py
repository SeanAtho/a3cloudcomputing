import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class ComplexPassword:
    def __init__(self, message=None):
        if not message:
            message = 'Password must include at least one letter, one digit, and one special character.'
        self.message = message

    def __call__(self, form, field):
        if not re.search(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), ComplexPassword()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), ComplexPassword()])
    remember_me = BooleanField('Remember Me')  # Correct implementation as a BooleanField
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=256)])
    location = StringField('Location', validators=[Length(min=0, max=100)])  # Field for location
    birthdate = DateField('Birthdate', format='%Y-%m-%d')  # Field for birthdate using a date picker
    submit = SubmitField('Update Profile')
