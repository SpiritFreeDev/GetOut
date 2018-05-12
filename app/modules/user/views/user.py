# TODO audit trail, confirm email, forgot email
import os
from flask import Flask, Blueprint, render_template, flash, redirect, url_for, request, session, make_response

#from passlib.hash import sha256_crypt

import app.modules.view_utils as vu
#import app.forms as f

user = Blueprint('user', __name__)

# from app import db
from app.modules.models import User, Category
# from app.modules.email import send_password_reset_email, send_verify_email_address

@user.route('/home')
@vu.is_logged_in
def user_home():
    ''' Define /user/home
        Note: cannot do def user as it would overwrite the blueprint user definition above...
              thus why I use user_home
    '''
    # to avoid using the cached version of the page when user logout and press the back button
    resp = make_response(render_template('templates/user_home.html', title="User Home"))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

# # User Dashboard
# @admin.route('/user_dash')
# #@vu.is_logged_in
# #@vu.is_sysadmin
# def user_dash():
#     ''' Define /admin/user_dash
#         Area to manually add, edit, delete, lock user accounts and view statistics
#     '''
#     users = User.query.order_by(User.username).all()
#     # col = users.column_descriptions
#     # column_names = [c["name"] for c in color]
#     col_names = User.__table__.columns.keys()
#     if users is not None:
#       resp = make_response(render_template('templates/user_dash.html', users = users, count=len(users), col_names = col_names, title="User Dashboard"))
#       resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
#       return resp
#     else:
#       msg = "No user found"
#       return render_template('templates/user_dash.html', msg=msg, count=0)

#---------------------------------------------------------------------------

# q = User.query.all()
#
# # this expression:
# mylist = q.column_descriptions
#
# # would return: mylist
# [
#     {
#         'name':'User',
#         'type':User,
#         'aliased':False,
#         'expr':User,
#         'entity': User
#     },
#     {
#         'name':'id',
#         'type':Integer(),
#         'aliased':False,
#         'expr':User.id,
#         'entity': User
#     },
#     {
#         'name':'user2',
#         'type':User,
#         'aliased':True,
#         'expr':user_alias,
#         'entity': user_alias
#     }
# ]
# column_names = [c["name"] for c in mylist]
#         return [dict(zip(column_names, row)) for row in result.all()]
#
# >>> [d['name'] for d in mylist]
#
# https://datatables.net/examples/styling/material.html

#---------------------------------------------------------------------------

# # Flask decorators (@is_logged_in) - http://flask.pocoo.org/snippets/98/
# @dbusers.route('/user_dash')
# @vu.is_logged_in
# @vu.is_sysadmin
# def user_dash():
#     users = Employee.query.order_by(Employee.first_name).all()
#     if users is not None:
#       resp = make_response(render_template('dbusers/user_dash.html', users = users, count=len(users), title="User Dashboard"))
#       resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
#       return resp
#     else:
#       msg = "No user found"
#       return render_template('dbusers/user_dash.html', msg=msg, count=0)
#
# # Add User
# @dbusers.route('/add_user', methods=['GET','POST'])
# @vu.is_logged_in
# @vu.is_sysadmin
# def add_user():
#     '''
#     When a user is added, the system force to give a temporary pwd
#     Department and role assignment is done here
#     '''
#     add_user = True
#     form = f.UserForm(request.form)
#     if request.method == 'POST': # and form.validate():  TODO Does not work because issue wwith Query Select Field
#         #department = form.department.data,
#         #role = form.role.data,
#         user = Employee(email=form.email.data,
#                     username=form.username.data,
#                     first_name=form.first_name.data,
#                     last_name=form.last_name.data,
#                     department_id=request.form['department'],
#                     role_id = request.form['role'],
#                     password_hash=sha256_crypt.encrypt(str(form.password_hash.data)),
#                     is_clinadmin=bool(form.is_clinadmin.data),
#                     is_sysadmin=bool(form.is_sysadmin.data),
#                     temporary_pwd = True)
#
#         try:
#             # add employee to the database
#             db.session.add(user)
#             # Before commit to DB we need to add step to verufy email
#             # We could also ask user to review info before storing in db
#             db.session.commit()
#             flash('User added succesfully to the db', 'success')
#             #return redirect(url_for('dbusers.user_dash'))
#             #return render_template('dbusers/test.html', user=user)
#         except:
#             # in case username or email already exists
#             flash('Error: username or email already exists.','danger')
#             #return render_template('dbusers/add_user.html', form = form)
#         return redirect(url_for('dbusers.user_dash'))
#     return render_template('dbusers/user_mod.html', form = form, add_user = add_user, title="Add User")
#
# # Edit user
# @dbusers.route('/edit_user/<int:id>/', methods=['GET','POST'])
# @vu.is_logged_in
# @vu.is_sysadmin
# def edit_user(id):
#     '''
#     When a user is edited, the system force to change password and give a temporary one
#     Department and role assignment is done here
#     '''
#     user = Employee.query.get_or_404(id)
#     # These query are here so we can display existing db department and role to edit in the form
#     qdept = Department.query.filter_by(dept_id=user.department_id).first()
#     qrole = Role.query.filter_by(role_id=user.role_id).first()
#     # Cannot edit your own sysadmin acount
#     if session['userid'] == user.user_id:
#        flash('You cannot edit your own account', 'danger')
#        return redirect(url_for('dbusers.user_dash'))
#     else:
#         # Populate user form fields coming from db (fast way)
#         # However I get issues with WTF form validation as if it did not recognize the cell content
#         #form = f.UserForm(obj=user)
#         # The long way...
#         form = f.UserForm(request.form)
#         # Populate user form fields coming from db
#         form.first_name.data = user.first_name
#         form.last_name.data = user.last_name
#         form.username.data = user.username
#         form.email.data = user.email
#         form.department.data = qdept
#         form.role.data = qrole
#         #form.password_hash.data = user.password_hash
#         form.is_sysadmin.data = user.is_sysadmin
#         form.is_clinadmin.data = user.is_clinadmin
#
#         # Admin now has a form with pre filled info he can edit
#         # Commit changes to the DB on submit
#         if request.method == 'POST':  #  TODO figure out why does not validate    and form.validate():
#             # Populate user form fields coming from db
#             user.first_name = request.form['first_name']
#             user.last_name = request.form['last_name']
#             user.username  = request.form['username']
#             user.email  = request.form['email']
#             user.department_id  = request.form['department']
#             user.role_id  = request.form['role']
#             user.password_hash = sha256_crypt.encrypt(str(request.form['password_hash']))
#             user.temporary_pwd = True
#             user.is_clinadmin  = bool(request.form.get('is_clinadmin'))
#             # if request.form.get('is_clinadmin') == 'y':
#             #     user.is_clinadmin  = True
#             # else:
#             #     user.is_clinadmin  = False
#             if request.form.get('is_sysadmin') == 'y':
#                 user.is_sysadmin  = True
#             else:
#                 user.is_sysadmin  = False
#
#             # TODO add a check for no change
#             db.session.commit()
#             flash('User Updated', 'success')
#             #return render_template('dbusers/test.html', test=user.first_name)
#             return redirect(url_for('dbusers.user_dash'))
#         #return render_template('dbusers/test.html', test=form.first_name.data)
#         #return render_template('dbusers/test.html', user=user.department_id)
#         return render_template('dbusers/user_mod.html', form = form, user = user)
#
# # Delete user
# @admin.route('/delete_user/<int:id>/', methods=['POST'])
# # @vu.is_logged_in
# # @vu.is_sysadmin
# def delete_user(id):
#     user = User.query.get_or_404(id)
#     # Cannot delete edit your own sysadmin acount
#     if session['userid'] == user.user_id:
#        flash('You cannot delete your own account', 'danger')
#        return redirect(url_for('admin.user_dash'))
#     else:
#         db.session.delete(user)
#         db.session.commit()
#         flash('User Deleted', 'success')
#         return redirect(url_for('admins.user_dash'))
#
# # Category Dashboard
# @admin.route('/cat_dash')
# #@vu.is_logged_in
# #@vu.is_sysadmin
# def cat_dash():
#     ''' Define /admin/user_dash
#         Area to manually add, edit, delete, lock user accounts and view statistics
#     '''
#     cats = Category.query.order_by(Category.cat_name).all()
#     # col = users.column_descriptions
#     # column_names = [c["name"] for c in color]
#     col_names = Category.__table__.columns.keys()
#     if cats is not None:
#       resp = make_response(render_template('templates/cat_dash.html', cats = cats, count=len(cats), col_names = col_names, title="Category Dashboard"))
#       resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
#       return resp
#     else:
#       msg = "No user found"
#       return render_template('templates/cat_dash.html', msg=msg, count=0)
