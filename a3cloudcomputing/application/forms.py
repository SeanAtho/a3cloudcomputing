from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from application.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Fields:
        username (StringField): The desired username for the user.
        email (StringField): The email address of the user.
        password (PasswordField): The desired password for the user.
        confirm_password (PasswordField): Confirmation of the password.
        submit (SubmitField): The submit button to submit the form.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        Validate that the username is unique.

        Args:
            username (StringField): The username to validate.

        Raises:
            ValidationError: If the username is already taken.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """
        Validate that the email is unique.

        Args:
            email (StringField): The email to validate.

        Raises:
            ValidationError: If the email is already registered.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    """
    Form for user login.

    Fields:
        email (StringField): The email address of the user.
        password (PasswordField): The password of the user.
        remember (BooleanField): Option to remember the user.
        submit (SubmitField): The submit button to submit the form.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    """
    Form for creating a new post.

    Fields:
        title (StringField): The title of the post.
        content (TextAreaField): The content of the post.
        submit (SubmitField): The submit button to submit the form.
    """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdateAccountForm(FlaskForm):
    """
    Form for updating account information.

    Fields:
        username (StringField): The new username for the user.
        email (StringField): The new email address of the user.
        picture (FileField): The new profile picture of the user.
        submit (SubmitField): The submit button to submit the form.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """
        Validate that the new username is unique, if changed.

        Args:
            username (StringField): The new username to validate.

        Raises:
            ValidationError: If the new username is already taken.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """
        Validate that the new email is unique, if changed.

        Args:
            email (StringField): The new email to validate.

        Raises:
            ValidationError: If the new email is already registered.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')

class ResetPasswordForm(FlaskForm):
    """
    Form for resetting password.

    Fields:
        password (PasswordField): The new password for the user.
        confirm_password (PasswordField): Confirmation of the new password.
        submit (SubmitField): The submit button to submit the form.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
