from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, TextAreaField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField, TextField
from wtforms import Form, BooleanField, validators
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, Email, ValidationError
from wtforms.fields.html5 import EmailField
from wtf_tinymce.forms.fields import TinyMceField
from .models import Blog, User

class NewPost(FlaskForm):
    blog_title = StringField('Title', validators=[DataRequired(message="All texts must have a title")])
    blog_slug = StringField('Slug', validators=[DataRequired()])
    blog_author = StringField('By', validators=[DataRequired()])
    blog_content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('submit', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')

class RequestResetForm(FlaskForm):
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("No account registered with that email. ")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(),InputRequired(), EqualTo('password', message='Passwords must match')])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken. Please try another")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("There is an account associated with this email address already.")

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(),InputRequired(), EqualTo('password_hash', message='Passwords must match')])

    submit = SubmitField('Reset Password')

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        DataRequired()])
    body = TextField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
