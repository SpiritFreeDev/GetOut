# TODO audit trail, confirm email, forgot email
import os
from flask import Flask, Blueprint, render_template, flash, redirect, url_for, request, session, make_response, jsonify

from passlib.hash import sha256_crypt

import app.modules.view_utils as vu
from ..forms import UserForm, CatForm

admin = Blueprint('admin', __name__)

from app import db
from app.modules.models import User, Category
# from app.modules.email import send_password_reset_email, send_verify_email_address

@admin.route('/home')
@vu.is_logged_in
@vu.is_siteadmin
def admin_home():
    ''' Define /admin/home
        Note: cannot do def admin as it would overwrite the blueprint admin definition above...
              thus why I use admin_home
    '''
    # to avoid using the cached version of the page when user logout and press the back button
    resp = make_response(render_template('templates/admin_home.html', title="Admin Home"))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

# Admin User Dashboard
@admin.route('/user_dash')
@vu.is_logged_in
@vu.is_siteadmin
def user_dash():
    ''' Define /admin/user_dash
        Area where admins manually add, edit, delete, lock user accounts

        TO DO: and view statistics: Weekly, monthly new users and graph, how many stay, leave, idle
               percent that create activities, percent posting on blog, and more
    '''
    users = User.query.order_by(User.username).all()
    # col = users.column_descriptions
    # column_names = [c["name"] for c in color]
    col_names = User.__table__.columns.keys()
    if users is not None:
      resp = make_response(render_template('templates/user_dash.html', users = users, count=len(users), col_names = col_names, title="User Dashboard"))
      resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
      return resp
    else:
      msg = "No user found"
      return render_template('templates/user_dash.html', msg=msg, count=0)

# Single user route -------------------------------------------------------------------------------------
@admin.route('/user/<int:id>/')
@vu.is_logged_in
@vu.is_siteadmin
def user(id):
    ''' Define /admin/user/xx
        Template: user.html
        Display information about Users

        TODO: add Profile info
    '''
    user = User.query.get_or_404(id)
    resp = make_response(render_template('templates/user.html', user = user, title="User Profile"))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

# Add User ----------------------------------------------------------------------------------------------
@admin.route('/add_user', methods=['GET','POST'])
@vu.is_logged_in
@vu.is_siteadmin
def add_user():
    ''' Define /admin/add_user
        Template: user_mod.html
        When a user is added manually, the system force to give a temporary pwd
    '''
    # return '<h1> Hello </h1>'
    add_user = True
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password_hash=sha256_crypt.encrypt(str(form.password_hash.data)),
                    is_sysadmin=bool(form.is_sysadmin.data),
                    temporary_pwd = True)

        try:
            # add user to the database
            db.session.add(user)
            # Before commit to DB we need to add step to verufy email
            # We could also ask user to review info before storing in db
            db.session.commit()
            flash('User added succesfully to the db', 'green lighten-4')
            #return redirect(url_for('dbusers.user_dash'))
            #return render_template('dbusers/test.html', user=user)
        except:
            # in case username or email already exists
            flash('Error: username or email already exists.','orange lighten-4')
            #return render_template('dbusers/add_user.html', form = form)
        return redirect(url_for('admin.user_dash'))
    return render_template('templates/user_mod.html', form = form, add_user = add_user, title="Add User")

# Edit user ----------------------------------------------------------------------------------------
@admin.route('/edit_user/<int:id>/', methods=['GET','POST'])
@vu.is_logged_in
@vu.is_siteadmin
def edit_user(id):
    '''Define /admin/edit_user
       Template: user_mod.html
    When a user is edited, the system force to change password and give a temporary one

    TODO add a comment field for the admin: why the update, should have a ticket number to perform changes
         add a lock all accounts

         Collect all changes to users in an audit database
    '''
    user = User.query.get_or_404(id)

    # Cannot edit your own sysadmin acount
    if session['userid'] == user.user_id:
       flash('You cannot edit your own account', 'orange lighten-4')
       return redirect(url_for('admin.user_dash'))
    else:
        # Populate user form fields coming from db (fast way)
        # However I get issues with WTF form validation as if it did not recognize the cell content
        #form = f.UserForm(obj=user)
        # The long way...
        form = UserForm(request.form)
        # Populate user form fields coming from db
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.username.data = user.username
        form.email.data = user.email
        #form.password_hash.data = user.password_hash
        form.is_sysadmin.data = user.is_sysadmin

        # Admin now has a form with pre filled info he can edit
        # Commit changes to the DB on submit
        if request.method == 'POST': # TODO not sure why validate does not work... and form.validate():
            # Populate user form fields coming from db
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.username  = request.form['username']
            user.email  = request.form['email']
            user.password_hash = sha256_crypt.encrypt(str(request.form['password_hash']))
            user.temporary_pwd = True
            if request.form.get('is_sysadmin') == 'y':
                user.is_sysadmin  = True
            else:
                user.is_sysadmin  = False

            # TODO add a check for no change
            db.session.commit()
            flash('User Updated', 'light-blue lighten-4')
            return redirect(url_for('admin.user_dash'))
        return render_template('templates/user_mod.html', form = form, user = user)

# Lock user --------------------------------------------------------------------------------------
@admin.route('/lock_user_toggle/<int:id>/', methods=['POST'])
@vu.is_logged_in
@vu.is_siteadmin
def lock_user_toggle(id):
    '''Define /admin/lock_user_toggle
       Template: None for now but later we should probably add an entry form for comments
    When a user is locked, the icon turns red, it's green by default

    TODO add a comment field for the admin: why the lock, should have a ticket number to perform changes
         add a lock all accounts

         Collect all changes to users in an audit database
    '''
    user = User.query.get_or_404(id)
    # Cannot lock your own sysadmin acount
    if session['userid'] == user.user_id:
       flash('You cannot lock your own account', 'orange lighten-4')
       return redirect(url_for('admin.user_dash'))
    else:
        # Account is locked - Unlock it
        if user.is_locked:
            user.is_locked = False
            db.session.commit()
            flash('User account ('+ user.username +') has been unlocked', 'light-blue lighten-4')
            return redirect(url_for('admin.user_dash'))
        # Account needs to be locked
        else:
            user.is_locked = True
            db.session.commit()
            flash('User account ('+ user.username +') has been locked', 'light-blue lighten-4')
            return redirect(url_for('admin.user_dash'))

# Delete user --------------------------------------------------------------------------------------
@admin.route('/delete_user/<int:id>/', methods=['POST'])
@vu.is_logged_in
@vu.is_siteadmin
def delete_user(id):
    user = User.query.get_or_404(id)
    # Cannot delete your own sysadmin acount
    if session['userid'] == user.user_id:
       flash('You cannot delete your own account', 'orange lighten-4')
       return redirect(url_for('admin.user_dash'))
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User Deleted', 'light-blue lighten-4')
        return redirect(url_for('admin.user_dash'))

# Admin API Users
@admin.route('/api/users')
@vu.is_logged_in
@vu.is_siteadmin
def users():
    ''' Define /admin/api/users restful API
        Area to get all user data

        TODO: API requires login ad admin account but no way to login to access the route
        Need to provide a generic way to secure and access this route (see google api)
        Since this is not going to be public we could add this as an admin task to register application that can access our data

        Can use Flask marshmallow to avoid having to update this if model change
    '''
    users = User.query.all()
    output = []
    for user in users:
        output.append({'user_id': user.user_id, 'first_name':user.first_name, 'last_name':user.last_name, 'username':user.username, 'email':user.email, 'register_date':user.register_date, 'is_sysadmin':user.is_sysadmin, 'email_confirmed': user.email_confirmed, 'temporary_pwd': user.temporary_pwd, 'is_locked': user.is_locked, 'last_urs_update': user.last_urs_update })
    return jsonify({'result': output})

#-----------------------------------------------------------------------------------------------------
# Category Dashboard ---------------------------------------------------------------------------------
@admin.route('/cat_dash')
@vu.is_logged_in
@vu.is_siteadmin
def cat_dash():
    ''' Define /admin/cat_dash
        Area to manually add, edit, delete, categories
    '''
    cats = Category.query.order_by(Category.cat_name).all()
    col_names = Category.__table__.columns.keys()
    if cats is not None:
      resp = make_response(render_template('templates/cat_dash.html', cats = cats, count=len(cats), col_names = col_names, title="Category Dashboard"))
      resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
      return resp
    else:
      msg = "No categories found"
      return render_template('templates/cat_dash.html', msg=msg, count=0)

# Add Category -------------------------------------------------------------------------------------
@admin.route('/add_cat', methods=['GET','POST'])
@vu.is_logged_in
@vu.is_siteadmin
def add_cat():
    ''' Define /admin/add_cat
        Template: cat_mod.html
    '''
    add_cat = True
    form = CatForm(request.form)
    if request.method == 'POST' and form.validate():
        cat = Category(cat_name=form.cat_name.data,
                    subcat_name=form.subcat_name.data,
                    cat_description=form.cat_description.data,
                    subcat_description=form.subcat_description.data
                    )
        try:
            # add category to the database
            db.session.add(cat)
            db.session.commit()
            flash('Category added succesfully to the db', 'light-blue lighten-4')
        except:
            # in case something goes wrong
            flash('Something went wrong.','orange lighten-4')
        return redirect(url_for('admin.cat_dash'))
    return render_template('templates/cat_mod.html', form = form, add_cat = add_cat, title="Add Category")

# Delete a category --------------------------------------------------------------------------------------
@admin.route('/delete_cat/<int:id>/', methods=['POST'])
@vu.is_logged_in
@vu.is_siteadmin
def delete_cat(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category Deleted', 'light-blue lighten-4')
    return redirect(url_for('admin.cat_dash'))

# Lock category --------------------------------------------------------------------------------------
@admin.route('/lock_cat_toggle/<int:id>/', methods=['POST'])
@vu.is_logged_in
@vu.is_siteadmin
def lock_cat_toggle(id):
    '''Define /admin/lock_cat_toggle
       Template: None for now but later we should probably add an entry form for comments
    When a cat is locked, the icon turns red, it's green by default

    TODO add a comment field for the admin: why the lock, should have a ticket number to perform changes
         add a lock all accounts

         Collect all changes to cats in an audit database
    '''
    cat = Category.query.get_or_404(id)
    # Category is locked - Unlock it
    if cat.is_locked:
        cat.is_locked = False
        db.session.commit()
        flash('Category ('+ cat.cat_name +') has been unlocked', 'light-blue lighten-4')
        return redirect(url_for('admin.cat_dash'))
    # Category needs to be locked
    else:
        cat.is_locked = True
        db.session.commit()
        flash('Category ('+ cat.cat_name +') has been locked', 'light-blue lighten-4')
        return redirect(url_for('admin.cat_dash'))

# Edit Category ------------------------------------------------------------------------------------
@admin.route('/edit_cat/<int:id>/', methods=['GET','POST'])
@vu.is_logged_in
@vu.is_siteadmin
def edit_cat(id):
    '''Define /admin/edit_cat
       Template: cat_mod.html

    TODO add a comment field for the admin: why the update, should have a ticket number to perform changes
         add a lock all cats

         Collect all changes to cats in an audit database
    '''
    cat = Category.query.get_or_404(id)

    form = CatForm(request.form)
    # Populate cat form fields coming from db
    form.cat_name.data = cat.cat_name
    form.cat_description.data = cat.cat_description
    form.subcat_name.data = cat.subcat_name
    form.subcat_description.data = cat.subcat_description

    # Admin now has a form with pre filled info he can edit
    # Commit changes to the DB on submit
    if request.method == 'POST': # TODO not sure why validate does not work... and form.validate():
        # Populate cat form fields coming from db
        cat.cat_name = request.form['cat_name']
        cat.cat_description = request.form['cat_description']
        cat.subcat_name  = request.form['subcat_name']
        cat.subcat_description  = request.form['subcat_description']

        # TODO add a check for no change
        db.session.commit()
        flash('Category Updated', 'light-blue lighten-4')
        return redirect(url_for('admin.cat_dash'))
    return render_template('templates/cat_mod.html', form = form, cat = cat)
