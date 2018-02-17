from flask import Flask, render_template, flash, abort, Blueprint
#from flask_sqlalchemy import SQLAlchemy, inspect
#from flask_migrate import Migrate

from config import app_config

#db = SQLAlchemy()

def create_app(config_name, path):
    app = Flask(__name__.split('.')[0], instance_path=path, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.cfg')

    # --- Database
    #db.init_app(app)
    #migrate = Migrate(app, db)

    # from . import models

    # Home routes
    # from .views.home import home as home_blueprint
    # app.register_blueprint(home_blueprint)

    # Admin routes
    # from .views.admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')
    #
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
