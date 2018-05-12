# Check if user logged in
# Need funtools wrapsfrom functools import wraps
from flask import flash, redirect, url_for, session
from functools import wraps
from base64 import b64encode
from os import urandom

def is_logged_in(f):
    @wraps(f)
    def decfunc1(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Your Session Expired or you are Unauthorized to see this page', 'orange darken-2')
            return redirect(url_for('home.login'))
    return decfunc1

# def is_not_logged_in(f):
#     @wraps(f)
#     def decfunc5(*args, **kwargs):
#         if not 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('No need to reset your password you are already logged in', 'info')
#             return redirect(url_for('home.dashboard'))
#     return decfunc5

def is_siteadmin(f):
    @wraps(f)
    def decfunc2(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            # log user out
            session.clear()
            flash('Your Session Expired or you are Unauthorized to see this page', 'orange darken-2')
            return redirect(url_for('home.login'))
    return decfunc2
