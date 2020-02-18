from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, TextAreaField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField, TextField
from wtforms import Form, BooleanField, validators
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, Email
from wtforms.fields.html5 import EmailField
from wtf_tinymce.forms.fields import TinyMceField
from .models import Blog

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

class ForgotUsername(FlaskForm):
    pass

class ForgotPassword(FlaskForm):
    pass

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(),InputRequired(), EqualTo('confirm', message='Passwords must match')])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Register')

class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

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
