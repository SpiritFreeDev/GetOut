from wtforms import StringField, TextAreaField, PasswordField, IntegerField, validators, ValidationError, BooleanField, DateTimeField, DateField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm
from app.modules.models import User, Category
from flask import flash
from wtforms.validators import DataRequired, Email, EqualTo

#User form ---------------------------------------------------------------------------------------------
def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username is already in use.')
        flash('Username already exist', 'red darken-2')

def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email is already in use.')
        flash('Email already in use', 'red darken-2')

class UserForm(FlaskForm):
    first_name     = StringField('First Name', validators=[validators.length(min = 1, max = 50), validators.input_required()])
    last_name      = StringField('Last Name', validators=[validators.length(min = 1, max = 50), validators.input_required()])
    username       = StringField('User Name', validators=[validators.length(min = 4, max = 25), validators.input_required(), validate_username])
    email          = StringField('Email', validators=[validators.length(min = 6, max = 50), validators.input_required(), validators.Email(), validate_email])
    password_hash  = PasswordField('Temporary Password', validators=[validators.input_required()])
    is_sysadmin    = BooleanField('System Admin?')

class CatForm(FlaskForm):
    # TODO find a way to make subcat_description mandatory if subcat_name not empty
    cat_name        = StringField('Category', validators=[validators.length(min = 1, max = 50), validators.input_required()])
    cat_description = TextAreaField('Description', validators=[validators.length(min = 1, max = 200), validators.input_required()])
    subcat_name     = StringField('Sub-Category', validators=[validators.Optional(), validators.length(min = 1, max = 50)])
    subcat_description = TextAreaField('Details', validators=[validators.Optional(), validators.length(min = 1, max = 200), validators.input_required()])
