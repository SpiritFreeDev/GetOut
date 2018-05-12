#------------http://flask.pocoo.org/docs/0.12/quickstart/
#
# For production in Python anywhere
# In the Code section of the Web tab on the dashboard,
# click on the link to the WSGI configuration file.
#   MAKE SURE YOU SET THE ENV VARIABLE
#   os.environ["FLASK_CONFIG"] = "production"
#   os.environ['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'
#   os.environ['SQLALCHEMY_DATABASE_URI'] = 'mysql://your-username:your-password@your-host-address/your-database-name'
#
# config_name = os.environ.get("FLASK_CONFIG")
# $env:FLASK_APP = "run.py"
#
import os
from app import create_app
from flask import Flask, render_template, flash, redirect, url_for, request, logging
from flask_mail import Mail, Message

# For dev set the FLASK_CONFIG env var
# os.environ["FLASK_CONFIG"] = "development"
config_name = os.environ.get("FLASK_CONFIG")
path = os.path.join(os.path.abspath(os.curdir), 'instance')
myapp = create_app(config_name, path)

# Cannot place this in __init__.py as home.py needs to load email.py
# that requires the app to be defined to work...
mail = Mail(myapp)

# @myapp.route('/')
# def index():
#    #return 'Hello, World!'
# #   return render_template(os.path.join(TEMPLATE_PATH,'/home.html'))
#    return '''
# <html>
#     <head>
#       <link rel="stylesheet" href="static/styles/style.css">
#     </head>
#     <header id="showcase" class='grid'>
#      <div class="bg-image">
#          <div class="content-wrap">
#            <h1> To Get Out you must first...</h1>
#            <br>
#            <br>
#            <a href="#section-b" class="btn">Get In</a>
#          </div>
#      </div>
#      <div class="lang-sel">
#        <a href="#"><img src="static/img/lang-icon.png" alt="GB"><strong>Change your language:</strong>English</a>
#        <ul>
#          <li><a href="#">English</a></li>
#          <li><a href="#">Russian</a></li>
#          <li><a href="#">French</a></li>
#        </ul>
#      </div>
#      <div class="head-soc-icons" style="float:right; display:block; posttion:absolute;">
#        <span>Follow us:</span>
#        <div class="soc-icons">
#          <a href="https://www.facebook.com/" class="fb soc_icon-facebook" title="Facebook"></a>
#          <a href="1" class="gp soc_icon-googleplus" title="Google +"></a>
#          <a href="http://twitter.com" class="fab fa-twitter" title="Twitter"></a>
#          <a href="http://vimeo.com" class="vi soc_icon-vimeo" title="Vimeo"></a>
#          <a href="http://pinterest.com" class="pt soc_icon-pinterest" title="Pinterest"></a>
#          <a href="1" class="rss soc_icon-rss" title="RSS"></a>
#        </div>
#      </div>
#     </header>
#     <body>
#
#     </body>
# </html>'''

if __name__ == '__main__':
    # myapp.run(host='0.0.0.0')
    myapp.run()
