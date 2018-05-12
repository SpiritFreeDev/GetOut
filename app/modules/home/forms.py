from wtforms import StringField, TextAreaField, PasswordField, IntegerField, validators, ValidationError, BooleanField, DateTimeField, DateField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm
from app.modules.models import User, Category
from flask import flash
from wtforms.validators import DataRequired, Email, EqualTo

#Registration form ------------------------------------------------------------------------------------------------------
def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username is already in use.')
        flash('Username already exist', 'red darken-2')

def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email is already in use.')
        flash('Email already in use', 'red darken-2')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[validators.length(min = 1, max = 50), validators.input_required()])
    last_name = StringField('Last Name', validators=[validators.length(min = 1, max = 50), validators.input_required()])
    username  = StringField('User Name', validators=[validators.length(min = 4, max = 25), validators.input_required(), validate_username])
    email  = StringField('Email', validators=[validators.length(min = 6, max = 50), validators.input_required(), validators.Email(), validate_email])
    password  = PasswordField('Password', validators=[
        validators.EqualTo('confirm', message = "Passwords do not match"),
        validators.DataRequired()
    ])
    confirm  = PasswordField('Confirm Password')
#Login form -------------------------------------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    username  = StringField('User Name', validators=[validators.length(min = 4, max = 25), validators.input_required(), validate_username], render_kw={'autofocus': True})
    password  = PasswordField('Password', validators=[validators.DataRequired()])
#Reset Password form ----------------------------------------------------------------------------------------------------
class ResetPasswordForm(FlaskForm):
    password  = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # submit = SubmitField('Request Password Reset')
