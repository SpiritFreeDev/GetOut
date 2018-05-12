import os
from flask import Flask, render_template, flash, abort, Blueprint
from base64 import b64encode
from os import urandom
import jinja2
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_migrate import Migrate

from config import app_config

db = SQLAlchemy()

def create_app(config_name, path):
    if os.getenv('FLASK_CONFIG') == "production":
        random_bytes = urandom(64)
        app = Flask(__name__.split('.')[0])
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            #SECRET_KEY = b64encode(random_bytes).decode('utf-8')
            #SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
        )
    else:
        app = Flask(__name__.split('.')[0], instance_path=path, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.cfg')

    # Define search paths for the html templates
    # ! need to watch the html file names as identical names in different module may give unexpected results
    # Don't call all your module entry page home.html... as the first one found will be used
    my_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader(['app/modules',
                                     'app/modules/home',
                                     'app/modules/admin',
                                     'app/modules/user']),
        ])
    app.jinja_loader = my_loader

    # --- Database
    db.init_app(app)
    migrate = Migrate(app, db)

    from app.modules import models

    # Home routes
    from .modules.home.views.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # Admin routes
    from .modules.admin.views.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Users routes
    from .modules.user.views.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    # from .views.dbusers import dbusers as dbusers_blueprint
    # app.register_blueprint(dbusers_blueprint)

    # Error routes -- This part does not work anymore need to debug...
    # from .views.errors import errs as errs_blueprint
    # app.register_blueprint(errs_blueprint)

    # @app.route('/test1')
    # def test1():
    #     #test = os.path.join(os.path.abspath(os.curdir), 'apppack\instance')
    #     #test = os.getenv('FLASK_CONFIG')
    #     #return render_template('test.html', test=test)
    #     test = 'db'
    #
    #     return 'Hello ' + test

    # Test for internal server error
    @app.route('/test_server')
    def foo():
        abort(500)

    return app
