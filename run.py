#------------http://flask.pocoo.org/docs/0.12/quickstart/
import os
from app import create_app
from flask import Flask, render_template, flash, redirect, url_for, request, logging

config_name = 'development'
path = os.path.join(os.path.abspath(os.curdir), 'instance')
myapp = create_app(config_name, path)

@myapp.route('/')
def index():
   #return 'Hello, World!'
   #return render_template('??/modules/home/home.html')
   return '''
<html>
    <head>
      <link rel="stylesheet" href="static/styles/style.css">
    </head>
    <header id="showcase" class='grid'>
     <div class="bg-image">
         <div class="content-wrap">
           <h1> To Get Out you must first...</h1>
           <br>
           <br>
           <a href="#section-b" class="btn">Get In</a>
         </div>
     </div>
     <div class="lang-sel">
       <a href="#"><img src="static/img/lang-icon.png" alt="GB"><strong>Change your language:</strong>English</a>
       <ul>
         <li><a href="#">English</a></li>
         <li><a href="#">Russian</a></li>
         <li><a href="#">French</a></li>
       </ul>
     </div>
     <div class="head-soc-icons" style="float:right; display:block; posttion:absolute;">
       <span>Follow us:</span>
       <div class="soc-icons">
         <a href="https://www.facebook.com/" class="fb soc_icon-facebook" title="Facebook"></a>
         <a href="1" class="gp soc_icon-googleplus" title="Google +"></a>
         <a href="http://twitter.com" class="fab fa-twitter" title="Twitter"></a>
         <a href="http://vimeo.com" class="vi soc_icon-vimeo" title="Vimeo"></a>
         <a href="http://pinterest.com" class="pt soc_icon-pinterest" title="Pinterest"></a>
         <a href="1" class="rss soc_icon-rss" title="RSS"></a>
       </div>
     </div>
    </header>
    <body>
        
    </body>
</html>'''

@myapp.route('/about')
def about():
   return render_template('about.html')

# Need 2 functions do_the_login() et show_the_login_form()

# @myapp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

if __name__ == '__main__':
    myapp.run()
