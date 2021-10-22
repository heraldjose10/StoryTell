from flask_mail import Message
from blogApp import mail, app
from flask import render_template


def send_mail(recipients, sender, text_body, html_body):
    msg = Message(subject='StoryTell password reset mail',
                  recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    print(recipients)
    print(sender)
    mail.send(msg)
    


def send_pass_reset_mail(user):
    token = user.get_password_reset_token()
    send_mail(recipients=[user.email],
              sender=app.config['ADMINS'][0],
              text_body=render_template('email/password_reset_mail.txt', user=user, token=token),
              html_body=render_template('email/password_reset_mail.html', user=user, token=token))
