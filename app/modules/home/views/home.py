# TODO audit trail, confirm email, forgot email
import os
from flask import Flask, Blueprint, render_template, flash, redirect, url_for, request, session, make_response
# http://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha256_crypt.html
from passlib.hash import sha256_crypt

import app.modules.view_utils as vu
# import app.modules.forms as f
from ..forms import RegisterForm, LoginForm

home = Blueprint('home', __name__)

from app import db
from app.modules.models import User
from app.modules.email import send_password_reset_email, send_verify_email_address

@home.route('/')
def index():
    """
    Site landing page - Can refer to this page in Flask as home.index
    """
    # to avoid using the cached version of the page when user logout and press the back button
    resp = make_response(render_template('templates/home.html', title="Welcome"))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

#Registration #----------------------------------------------------------------------------------------------------------------
@home.route('/register', methods=['GET','POST'])
def register():
    """
    Add an new user to the database through the registration form
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password_hash=sha256_crypt.encrypt(str(form.password.data)))
        # add employee to the database even if email not verified yet
        # verified email variable is automatically set to false
        db.session.add(user)
        # Before commit to DB we need to add step to verify email
        # We could also ask user to review info before storing in db
        db.session.commit()
        # TODO: Send email to verify address but commit the data anyway
        # we will prevent access based on wether the email was verified or not
        # ----------------------------
        # send_verify_email_address(user, 1800)
        flash('One last step: Check your email and follow the instructions', 'orange lighten-4')
        return redirect(url_for('home.login'))
    return render_template('templates/register.html', form = form, title='Register', navbar_active_r='active')

#Login route #---------------------------------------------------------------------------------------------------------------
@home.route('/login', methods=['GET','POST'])
def login():
    """
    Sign In Users
    """
    form = LoginForm(request.form)
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password_totest = request.form['password']
        # Retrieve user from db by username
        user = User.query.filter_by(username=username).first()

        if user is not None:
            # get user info
            dbid = user.user_id
            dbpassword = user.password_hash
            dbfname = user.first_name
            dblname = user.last_name
            dbemail = user.email
            dbsadmin = user.is_sysadmin
            dbverified = user.email_confirmed
            dblock = user.is_locked

            # Force users to verify email before granting access
            if not dbverified:
                return redirect(url_for('home.confirm_email'), user=user, title='Confirm Email')
            else:
                if dblock:
                    flash('Your account is locked, please contact our costumer service', 'red darken-1')
                    return redirect(url_for('home.login'), user=user, title='Locked account')
                else:
                    # Compare password and set session variables
                    if sha256_crypt.verify(password_totest, dbpassword):
                       # Allow automatic logout
                       session.permanent = True
                       session.modified = True
                       # Set session variables
                       session['logged_in'] = True
                       session['username'] = username
                       session['userid'] = dbid
                       session['name'] = dbfname + " " + dblname
                       if dbsadmin > 0:
                         session['admin'] = True

                       # flash('You are now logged in', 'green lighten-4')
                       if dbsadmin:
                         return redirect(url_for('admin.admin_home'))
                       else:
                         return redirect(url_for('user.user_home'))
                    else:
                       error = "Incorrect Username or Password"
                       flash('Incorrect Username or Password', 'red darken-1')
        else:
            #app.logger.info('No user')
            error = "Incorrect Username or Password"
            flash('Incorrect Username or Password', 'red darken-1')

    return render_template('templates/login.html', form = form, title='Login', navbar_active_l='active')

#logout
#----------------------------------------------------------------------------------------------------
@home.route('/logout')
@vu.is_logged_in
def logout():
    session.clear()
    # OR
    # for key in session.keys():
    #  session.pop(key)
    return redirect(url_for('home.index'))
#
# # Ask user to provide email and send an email with a link
# @home.route('/reset_password_request', methods=['GET', 'POST'])
# #@vu.is_not_logged_in
# def reset_password_request():
#     # no need to reset password if you are logged in
#     # Well I disagree with that... you may need to reset pwd if you believe your account has been hacked
#     if request.method == 'POST':
#         # Get form fields
#         email = request.form['email']
#         employee = Employee.query.filter_by(email=email).first()
#         if employee:
#             tkn = send_password_reset_email(employee, 1800)
#             session.clear()
#         #flash(tkn, 'info')
#         flash('Check your email for the instructions. You have 30 minutes to reset your password', 'red darken-2')
#         return redirect(url_for('home.login'))
#     return render_template('home/reset_pwd_req.html', title='Reset Password')
#
# # when the user click on the link in the email they received, they get a page where the password can be changed
# # TODO: Need to add rules, maybe force them to add old pwd too as another check...
# @home.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     # if session.logged_in:
#     #     return redirect(url_for('home'))
#     employee = Employee.verify_reset_password_token(token)
#     if not employee:
#         return redirect(url_for('home'))
#     form = f.ResetPasswordForm(request.form)
#     if request.method == 'POST':
#         #employee.set_password(request.form['password'])
#         employee.password_hash=sha256_crypt.encrypt(str(form.password.data))
#         db.session.commit()
#         flash('Your password has been reset.', 'green lighten-4')
#         # may need to clear session and logout users that are logged in when doing pwd reset_pwd
#         # TODO: Check...
#         return redirect(url_for('home.login'))
#     return render_template('home/reset_pwd.html', form=form, Title="Reset Pwd")
#
# @home.route('/verify_email/<token>', methods=['GET', 'POST'])
# def verify_email(token):
#     # if session.logged_in:
#     #     return redirect(url_for('home'))
#     employee = Employee.verify_reset_password_token(token)
#     if not employee:
#         return redirect(url_for('home'))
#         #employee.set_password(request.form['password'])
#     employee.email_confirmed=True
#     db.session.commit()
#     flash('Your email has been confirmed', 'green lighten-4')
#     return render_template('home/verified_email.html', Title="Verify Registration e-mail")
#
# @home.route('/confirm_email/<int:id>/', methods=['GET', 'POST'])
# #@vu.is_not_logged_in
# def confirm_email(id):
#     employee = Employee.query.filter_by(id).first()
#     return render_template('home/confirm_email.html', employee=employee, title='Confirm email')
#
# # Ask user to provide email and send an email with a link
# @home.route('/confirm_email_request/<email>/', methods=['POST'])
# #@vu.is_not_logged_in
# def confirm_email_request(email):
#     employee = Employee.query.filter_by(email=email).first()
#     if employee:
#         tkn = send_verify_email_address(employee, 1800)
#     #flash(tkn, 'info')
#     flash('Check your email for the instructions. You have 30 minutes to confirm your email', 'red darken-2')
#     return redirect(url_for('home.login'))
