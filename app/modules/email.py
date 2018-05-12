from flask_mail import Message
from flask import render_template
# import app

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user, time=600):
    token = user.get_reset_password_token(time)
    recipients=[user.email]
    sender=app.config['ADMINS'][0]
    send_email('Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_pwd_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_pwd_email.html',
                                         user=user, token=token))
    return recipients

def send_verify_email_address(user, time=600):
    #TODO: change function name so it worke in case of email or chng pwd
    token = user.get_reset_password_token(time)
    recipients=[user.email]
    sender=app.config['ADMINS'][0]
    send_email('Please verify your email address',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/verify_emailaddress_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/verify_emailaddress_email.html',
                                         user=user, token=token))
